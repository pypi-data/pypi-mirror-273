import warnings
from functools import lru_cache
from pathlib import Path
from typing import IO, Any, Dict, Optional, Union, cast

import fsspec
from tqdm import tqdm
from upath import UPath

from fastdev.fileio.handlers.base_handler import BaseFileHandler
from fastdev.fileio.handlers.json_handler import JSONHandler
from fastdev.fileio.handlers.yaml_handler import YAMLHandler

FILE_HANDLER_CLASSES = {
    "json": JSONHandler,
    "yaml": YAMLHandler,
    "yml": YAMLHandler,
}
FILE_HANDLERS: Dict[str, BaseFileHandler] = {}
warnings.filterwarnings("ignore", module="upath")


def ucopy(src_path: str, dst_path: str):
    src_upath, dst_upath = UPath(src_path), UPath(dst_path)
    src_fs, dst_fs = src_upath.fs, dst_upath.fs
    if src_fs.protocol == dst_fs.protocol:
        src_fs.copy(src_path, dst_path, recursive=True)
    else:
        if src_fs.isfile(src_path):
            if dst_fs.isdir(dst_path):
                dst_path = str(dst_upath / src_upath.name)
            with src_fs.open(src_path, "rb") as src_file:
                with dst_fs.open(dst_path, "wb") as dst_file:
                    dst_file.write(src_file.read())  # type: ignore
        else:
            src_mapper = fsspec.get_mapper(src_path)
            tgt_mapper = fsspec.get_mapper(dst_path)
            for key in tqdm(src_mapper):
                tgt_mapper[key] = src_mapper[key]


@lru_cache()
def get_file_handler(file_format: str) -> BaseFileHandler:
    if file_format not in FILE_HANDLERS:
        if file_format not in FILE_HANDLER_CLASSES:
            raise ValueError(f"Unsupported file format: {file_format}")
        else:
            FILE_HANDLERS[file_format] = FILE_HANDLER_CLASSES[file_format]()
    return FILE_HANDLERS[file_format]


def load(
    file: Union[str, Path, IO],
    file_format: Optional[str] = None,
    **kwargs,
) -> Any:
    """Load json/yaml/toml/pickle file from file."""
    # Parameters validation
    if isinstance(file, Path):
        file = str(file)
    if file_format is None:
        if isinstance(file, str):
            file_format = file.split(".")[-1]
        else:
            raise ValueError("file_format is required when file is not a string or path")

    # Get file handler
    file_handler = get_file_handler(file_format)

    # Load file
    if isinstance(file, str):
        mode = "rb" if file_handler.str_or_bytes == "bytes" else "r"
        with fsspec.open(file, mode) as f:
            obj = file_handler.load_from_fileobj(cast(IO, f), **kwargs)
    elif hasattr(file, "read"):
        obj = file_handler.load_from_fileobj(cast(IO, file), **kwargs)
    else:
        raise TypeError("File must be a filepath str or a file object")
    return obj


def dump(
    obj: Any,
    file: Union[str, Path, IO],
    file_format: Optional[str] = None,
    **kwargs,
):
    """Dump obj to json/yaml/toml/pickle file."""
    # Parameters validation
    if isinstance(file, Path):
        file = str(file)
    if file_format is None:
        if isinstance(file, str):
            file_format = file.split(".")[-1]
        else:
            raise ValueError("file_format is required when file is not a string or path")

    # Get file handler
    file_handler = get_file_handler(file_format)

    if isinstance(file, str):
        mode = "wb" if file_handler.str_or_bytes == "bytes" else "r"
        with fsspec.open(file, mode) as f:
            file_handler.dump_to_fileobj(obj, cast(IO, f), **kwargs)
    elif hasattr(file, "write"):
        file_handler.dump_to_fileobj(obj, cast(IO, file), **kwargs)
    else:
        raise TypeError("File must be a filepath str or a file object")
