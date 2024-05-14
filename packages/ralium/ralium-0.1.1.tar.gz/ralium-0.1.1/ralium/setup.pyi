from ralium._util import (
    FilePathStr,
    DirPathStr,
    Any
)

HTML_FILE_EXTENSIONS: list[str]

def _exe_str_error(name: str, var: Any) -> Exception: ...
def _add_data_arg(src: FilePathStr, dst: FilePathStr) -> str: ...

def collect_webfolder(webfolder: DirPathStr) -> dict[FilePathStr]: ...

def setup(
    pyfile: FilePathStr,
    name: str | None = None,
    icon: FilePathStr | None = None,
    onefile: bool = True,
    noconsole: bool = True,
    webfolder: DirPathStr | None = None,
    *pyi_args: tuple[Any]
) -> None: ...