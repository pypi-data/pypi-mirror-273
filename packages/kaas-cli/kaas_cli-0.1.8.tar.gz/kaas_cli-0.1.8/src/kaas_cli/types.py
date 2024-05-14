from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import IO, Any, Optional

from click import ClickException, echo

File_Data = dict[str, tuple[Optional[str], Any, Optional[str]]]
Metadata = dict[str, Any]


class KaasCliException(ClickException):
    def show(self, file: IO[Any] | None = None) -> None:
        echo(f'{self.message}', file=file)


def github_url_repr(username):
    return f"https://github.com/{username}"


@dataclass
class User:
    url: str = field(init=False)
    email: str
    createdAt: str
    username: str

    def __post_init__(self):
        self.url = github_url_repr(self.username)


@dataclass
class Vault:
    id: str
    name: str
    createdAt: str
    user: User


@dataclass
class Key:
    key: str
    name: str
    createdAt: str
    expiresAt: Optional[str] = None
