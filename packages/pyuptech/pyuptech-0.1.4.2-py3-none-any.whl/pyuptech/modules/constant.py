from pathlib import Path
from typing import TypeAlias, Literal

LIB_FILE_PATH: str = (Path(__file__).parent.parent / "lib/libuptech.so").as_posix()
BinaryIO: TypeAlias = Literal[0, 1] | int
