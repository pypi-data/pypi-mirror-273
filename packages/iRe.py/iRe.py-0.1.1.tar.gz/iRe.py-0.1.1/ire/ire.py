import os
from dataclasses import dataclass
from inspect import getfullargspec
from os import getcwd, makedirs, rename
from os.path import islink, join
from tempfile import TemporaryDirectory
from typing import Literal, Optional, Union, TypeVar, Callable

import pandas as pd
from IPython.display import display, HTML, Image
from utz import err

from ire.dvc import DvcConfig, is_dvc_repo, process_dvc_config
from ire.git import GitConfig, has_unpushed_commits, process_git_config
from ire.utils import md5_file, run


DEFAULT_ARTIFACTS_DIR = ".ire"
METADATA_KEY = 'iRe'

ParquetEngine = Optional[Literal['fastparquet', 'pyarrow', 'auto']]


@dataclass
class Config:
    git: GitConfig
    dvc: DvcConfig
    dir: str = DEFAULT_ARTIFACTS_DIR
    engine: ParquetEngine = None


# Default config values
config = Config(
    git='add',
    dvc='add' if is_dvc_repo() else False,
)


@dataclass
class Output:
    path: str
    md5: str


Fmt = Union[Literal['parquet'], Literal['plotly'], Literal['png']]
ShowPlot = Union[None, 'png', 'html']


T = TypeVar("T")
DEFAULT_EXTENSION_OVERRIDES = {
    'plotly': 'json',
}


def chdir(path):
    os.chdir(path)
    config.dir = join(path, DEFAULT_ARTIFACTS_DIR)


def write_obj(
        obj: T,
        write: Callable,
        fmt: Fmt,
        name: str = None,
        dir: str = DEFAULT_ARTIFACTS_DIR,
        extension: str = None,
        git: Optional[GitConfig] = None,
        dvc: Optional[DvcConfig] = None,
        verbose: bool = False,
        engine: ParquetEngine = None,
):
    if extension is None:
        extension = DEFAULT_EXTENSION_OVERRIDES.get(fmt, fmt)

    def pre_write(path: str):
        if dvc and islink(path):
            # If the file is a symlink, we need to unprotect it before writing
            run('dvc', 'unprotect', path, verbose=verbose)

    write_kwargs = {}
    spec = getfullargspec(write)
    if 'engine' in spec.args:
        if engine is None:
            engine = config.engine
        if engine:
            write_kwargs['engine'] = engine

    if name is None:
        with TemporaryDirectory(dir=getcwd()) as tmpdir:
            basename = f"tmp.{extension}"
            tmp_path = os.path.join(tmpdir, basename)
            write(obj, tmp_path, **write_kwargs)
            md5 = md5_file(tmp_path)
            path = os.path.join(dir, f"{md5}.{extension}")
            makedirs(dir, exist_ok=True)
            pre_write(path)
            rename(tmp_path, path)
    else:
        path = os.path.join(dir, f"{name}.{extension}")
        makedirs(dir, exist_ok=True)
        pre_write(path)
        write(obj, path, **write_kwargs)
    err(f"Saved {fmt} to {path}")
    path = process_dvc_config(dvc, path, verbose=verbose) or path
    process_git_config(git, path, verbose=verbose)
    metadata = { METADATA_KEY: { 'fmt': fmt, 'path': path, 'dvc': bool(dvc), } }
    return metadata


def write_parquet(df: pd.DataFrame, path: str, engine: ParquetEngine = None):
    if engine is None:
        engine = 'auto'
    elif engine not in ('fastparquet', 'pyarrow'):
        raise ValueError(f"Unrecognized Parquet engine: {engine}")
    df.to_parquet(path, engine=engine)


def write_image(img: Union[Image, bytes], path: str):
    with open(path, 'wb') as f:
        data = img.data if isinstance(img, Image) else img
        f.write(data)


def write_plotly(fig: 'Figure', path: str):
    fig_json = fig.to_json()
    with open(path, 'w') as f:
        f.write(fig_json)


def write_matplotlib(fig: 'plt.Figure', path: str):
    fig.savefig(path)


def maybe_handle_plotly(obj, kwargs, show: ShowPlot = None):
    try:
        from plotly.graph_objs import Figure
        if isinstance(obj, Figure):
            fig = obj
            metadata = write_obj(fig, write=write_plotly, fmt='plotly', **kwargs)
            if show == 'png':
                img_bytes = fig.to_image(format='png')
                display(Image(img_bytes), metadata=metadata)
            elif show == 'html':
                html = fig.to_html()
                display(HTML(html), metadata=metadata)
            else:
                display(fig, metadata=metadata)
            return True
    except ImportError:
        pass
    return False


def maybe_handle_matplotlib(obj, kwargs):
    try:
        import matplotlib.pyplot as plt
        if isinstance(obj, plt.Figure):
            fig = obj
            metadata = write_obj(fig, write=write_matplotlib, fmt='png', **kwargs)
            display(fig, metadata=metadata)
            plt.close()
            return True
    except ImportError:
        pass
    return False


def export(
        obj,
        name: str = None,
        dir: str = None,
        git: Optional[GitConfig] = None,
        dvc: Optional[DvcConfig] = None,
        verbose: bool = False,
        show: ShowPlot = None,
        engine: ParquetEngine = None,
):
    if git is None:
        git = config.git
    if dvc is None:
        dvc = config.dvc
    if dir is None:
        dir = config.dir
    if show:
        if show not in ['html', 'png']:
            raise ValueError(f"Unrecognized `show` param: {show}")

    kwargs = dict(dir=dir, name=name, git=git, dvc=dvc, verbose=verbose)
    if isinstance(obj, pd.DataFrame):
        df = obj
        metadata = write_obj(obj=obj, write=write_parquet, fmt='parquet', **kwargs)
        html = df._repr_html_()
        return display(HTML(html), metadata=metadata)
    elif isinstance(obj, Image):
        metadata = write_obj(obj=obj, write=write_image, fmt='png', **kwargs)
        return display(obj, metadata=metadata)
    elif isinstance(obj, bytes):
        img = Image(obj)
        metadata = write_obj(obj=img, write=write_image, fmt='png', **kwargs)
        return display(img, metadata=metadata)
    elif not maybe_handle_plotly(obj, kwargs, show=show) and not maybe_handle_matplotlib(obj, kwargs):
        raise ValueError(f"Unrecognized export type: {type(obj)}")


def _ire_df_repr_html_(df):
    return export(df)


def push(
        git: bool = True,
        dvc: Optional[bool] = None,
        # Err on the side of letting the user know about Git/DVC pushes
        verbose: bool = True,
):
    if git:
        if has_unpushed_commits():
            run('git', 'push', verbose=verbose)
        else:
            if verbose:
                err("Git appears up to date, skipped push")
    if dvc or (dvc is None and config.dvc is not False):
        run('dvc', 'push', verbose=verbose)
