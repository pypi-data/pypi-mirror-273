# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
"""
This is then main function for open any files in local or remote space
with the best python libraries and the best practice such as build-in
``io.open``, ``mmap.mmap``, etc.
"""
from __future__ import annotations

import abc
import csv
import io
import json
import marshal
import mmap
import os
import pickle
from contextlib import contextmanager
from pathlib import Path
from typing import (
    IO,
    Any,
    AnyStr,
    Callable,
    ClassVar,
    Literal,
    Optional,
    Protocol,
    Union,
    get_args,
)

# NOTE: import msgpack
import yaml

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from .__regex import SettingRegex
from .utils import search_env, search_env_replace

FileCompressType = Literal["gzip", "gz", "xz", "bz2"]

# NOTE:
#   add more compress type such as
#       - h5,hdf5(h5py)
#       - fits(astropy)
#       - rar(...)
DirCompressType = Literal["zip", "rar", "tar", "h5", "hdf5", "fits"]


class CompressProtocol(Protocol):
    def decompress(self, *args, **kwargs) -> AnyStr: ...

    def open(self, *args, **kwargs) -> IO: ...


class OpenFileAbc(abc.ABC):
    @abc.abstractmethod
    def read(self, *args, **kwargs): ...

    @abc.abstractmethod
    def write(self, *args, **kwargs): ...


class OpenFile(OpenFileAbc):
    """Open File Object"""

    def __init__(
        self,
        path: Union[str, Path],
        *,
        encoding: Optional[str] = None,
        compress: Optional[FileCompressType] = None,
    ):
        self.path: Path = Path(path) if isinstance(path, str) else path
        self.encoding: str = encoding or "utf-8"
        self.compress: Optional[FileCompressType] = compress

        # Action anything after set up attributes.
        self.after_set_attrs()

    def after_set_attrs(self) -> None: ...

    @property
    def compress_lib(self) -> CompressProtocol:
        """Return Compress package"""
        if not self.compress:
            return io
        elif self.compress in ("gzip", "gz"):
            import gzip

            return gzip
        elif self.compress in ("bz2",):
            import bz2

            return bz2
        elif self.compress in ("xz",):
            import lzma as xz

            return xz
        raise NotImplementedError(
            f"Compress {self.compress} does not implement yet"
        )

    @property
    def decompress(self) -> Callable:
        if self.compress and self.compress in get_args(FileCompressType):
            return self.compress_lib.decompress
        raise NotImplementedError(
            "Does not implement decompress method for None compress value."
        )

    def convert_mode(
        self,
        mode: Optional[str] = None,
        default: bool = True,
    ) -> dict[str, str]:
        if not mode:
            if default:
                return {"mode": "r"}
            raise ValueError("The mode value does not set.")
        byte_mode: bool = "b" in mode
        if self.compress is None:
            _mode: dict[str, str] = {"mode": mode}
            return _mode if byte_mode else {"encoding": self.encoding, **_mode}
        elif not byte_mode and self.compress in ("gzip", "gz", "xz", "bz2"):
            # NOTE:
            #   Add `t` in open file mode for force with text mode.
            return {"mode": f"{mode}t", "encoding": self.encoding}
        elif byte_mode and self.compress in ("gzip", "gz", "xz", "bz2"):
            return {"mode": mode}

    def open(self, *, mode: Optional[str] = None, **kwargs) -> IO:
        return self.compress_lib.open(
            self.path,
            **self.convert_mode(mode),
            **kwargs,
        )

    @contextmanager
    def mopen(self, *, mode: Optional[str] = None) -> IO:
        _mode: str = mode or "r"
        _f: IO = self.open(mode=mode)
        _access = mmap.ACCESS_READ if ("r" in _mode) else mmap.ACCESS_WRITE
        try:
            yield mmap.mmap(
                _f.fileno(),
                length=0,
                access=_access,
            )
        except ValueError:
            yield _f
        finally:
            _f.close()

    def read(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        raise NotImplementedError


class OpenDir:
    """Open File Object"""

    def __init__(
        self,
        path: Union[str, Path],
        *,
        compress: Optional[DirCompressType] = None,
    ):
        self.path = path
        self.compress = compress
        # Action anything after set up attributes.
        self.after_set_attrs()

    def after_set_attrs(self) -> None: ...

    def open(self, *, mode: str, **kwargs):
        if not self.compress:
            return ""
        elif self.compress in {"zip"}:
            import zipfile

            return zipfile.ZipFile(
                self.path,
                mode=mode,
                compression=zipfile.ZIP_DEFLATED,
                **kwargs,
            )
        elif self.compress in {"tar"}:
            import tarfile

            # TODO: Wrapped tar module with change some methods like,
            #   - add --> write
            return tarfile.open(
                self.path,
                mode=f"{mode}:gz",  # w:bz2
            )
        return NotImplementedError


class Env(OpenFile):
    """Env object which mapping search engine"""

    keep_newline: ClassVar[bool] = False
    default: ClassVar[str] = ""

    def read(self, *, update: bool = True) -> dict[str, str]:
        with self.open(mode="r") as _r:
            _r.seek(0)
            _result: dict = search_env(
                _r.read(),
                keep_newline=self.keep_newline,
                default=self.default,
            )
            if update:
                os.environ.update(**_result)
            return _result

    def write(self, data: dict[str, Any]) -> None:
        raise NotImplementedError


class Yaml(OpenFile):
    """Yaml File Object

    .. noted::
        - The boolean value in the yaml file
            - true: Y, true, Yes, ON
            - false: n, false, No, off
    """

    def read(self, safe: bool = True) -> dict[str, Any]:
        if safe:
            with self.open(mode="r") as _r:
                return yaml.load(_r.read(), SafeLoader)
        return NotImplementedError

    def write(self, data: dict[str, Any]) -> None:
        with self.open(mode="w") as _w:
            yaml.dump(data, _w, default_flow_style=False)


class YamlEnv(Yaml):
    """Yaml object which mapping search environment variable."""

    raise_if_not_default: ClassVar[bool] = False
    default: ClassVar[str] = "N/A"
    escape: ClassVar[str] = "ESC"

    @staticmethod
    def prepare(x: str) -> str:
        return x

    def read(self, safe: bool = True) -> dict[str, Any]:
        if safe:
            with self.open(mode="r") as _r:
                _env_replace: str = search_env_replace(
                    SettingRegex.RE_YAML_COMMENT.sub("", _r.read()),
                    raise_if_default_not_exists=self.raise_if_not_default,
                    default=self.default,
                    escape=self.escape,
                    caller=self.prepare,
                )
                if _result := yaml.load(_env_replace, SafeLoader):
                    return _result
                return {}
        return NotImplementedError

    def write(self, data: dict[str, Any]) -> None:
        raise NotImplementedError


class CSV(OpenFile):
    def read(self) -> list[str]:
        with self.open(mode="r") as _r:
            try:
                dialect = csv.Sniffer().sniff(_r.read(128))
                _r.seek(0)
                return list(csv.DictReader(_r, dialect=dialect))
            except csv.Error:
                return []

    def write(
        self,
        data: Union[list[Any], dict[Any, Any]],
        *,
        mode: Optional[str] = None,
        **kwargs,
    ) -> None:
        mode = mode or "w"
        assert mode in (
            "a",
            "w",
        ), "save mode must contain only value `a` nor `w`."
        with self.open(mode=mode, newline="") as _w:
            _has_data: bool = True
            if isinstance(data, dict):
                data: list = [data]
            elif not data:
                data: list = [{}]
                _has_data: bool = False
            if _has_data:
                writer = csv.DictWriter(
                    _w,
                    fieldnames=list(data[0].keys()),
                    lineterminator="\n",
                    **kwargs,
                )
                if mode == "w" or not self.has_header:
                    writer.writeheader()
                writer.writerows(data)

    @property
    def has_header(self) -> bool:
        with self.open(mode="r") as _r:
            try:
                return csv.Sniffer().has_header(_r.read(128))
            except csv.Error:
                return False


class CSVPipeDim(CSV):
    def after_set_attrs(self) -> None:
        csv.register_dialect(
            "pipe_delimiter", delimiter="|", quoting=csv.QUOTE_ALL
        )

    def read(self) -> list:
        with self.open(mode="r") as _r:
            try:
                return list(
                    csv.DictReader(_r, delimiter="|", quoting=csv.QUOTE_ALL)
                )
            except csv.Error:
                return []

    def write(
        self,
        data: Union[list[Any], dict[Any, Any]],
        *,
        mode: Optional[str] = None,
        **kwargs,
    ) -> None:
        mode = mode or "w"
        assert mode in {
            "a",
            "w",
        }, "save mode must contain only value `a` nor `w`."
        with self.open(mode=mode, newline="") as _w:
            _has_data: bool = True
            if isinstance(data, dict):
                data: list = [data]
            elif not data:
                data: list = [{}]
                _has_data: bool = False
            if _has_data:
                writer = csv.DictWriter(
                    _w,
                    fieldnames=list(data[0].keys()),
                    lineterminator="\n",
                    delimiter="|",
                    quoting=csv.QUOTE_ALL,
                    **kwargs,
                )
                if mode == "w" or not self.has_header:
                    writer.writeheader()
                writer.writerows(data)


class Json(OpenFile):
    def read(self) -> Union[dict[Any, Any], list[Any]]:
        with self.open(mode="r") as _r:
            try:
                return json.loads(_r.read())
            except json.decoder.JSONDecodeError:
                return {}

    def write(
        self,
        data,
        *,
        indent: int = 4,
    ) -> None:
        _w: IO
        with self.open(mode="w") as _w:
            if self.compress:
                _w.write(json.dumps(data))
            else:
                json.dump(data, _w, indent=indent)


class JsonEnv(Json):
    raise_if_not_default: bool = False
    default: str = "N/A"
    escape: str = "ESC"

    @staticmethod
    def prepare(x: str) -> str:
        return x

    def read(self) -> Union[dict[Any, Any], list[Any]]:
        with self.open(mode="r") as _r:
            return json.loads(
                search_env_replace(
                    _r.read(),
                    raise_if_default_not_exists=self.raise_if_not_default,
                    default=self.default,
                    escape=self.escape,
                    caller=self.prepare,
                )
            )

    def write(self, data, *, indent: int = 4) -> None:
        raise NotImplementedError


class Pickle(OpenFile):
    def read(self):
        with self.open(mode="rb") as _r:
            return pickle.loads(_r.read())

    def write(self, data):
        with self.open(mode="wb") as _w:
            pickle.dump(data, _w)


class Marshal(OpenFile):
    def read(self):
        with self.open(mode="rb") as _r:
            return marshal.loads(_r.read())

    def write(self, data):
        with self.open(mode="wb") as _w:
            marshal.dump(data, _w)


__all__ = (
    "OpenFile",
    "Env",
    "Json",
    "JsonEnv",
    "Yaml",
    "YamlEnv",
    "CSV",
    "CSVPipeDim",
    "Marshal",
    "Pickle",
)
