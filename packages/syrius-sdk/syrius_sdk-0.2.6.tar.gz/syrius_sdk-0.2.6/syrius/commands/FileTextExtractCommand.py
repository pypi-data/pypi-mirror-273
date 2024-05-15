from typing import Literal, ClassVar

from syrius.commands.abstract import Command, AbstractCommand


class FileTextExtractCommand(Command):
    """ """
    id: int = 5
    file_type: Literal["local", "s3"]
    filepath: str | AbstractCommand
    remove_breaks: bool | AbstractCommand
    remove_multi_whitespaces: bool | AbstractCommand
