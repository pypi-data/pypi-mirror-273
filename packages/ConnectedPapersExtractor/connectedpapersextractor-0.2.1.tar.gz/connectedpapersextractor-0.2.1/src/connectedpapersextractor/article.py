from __future__ import annotations

import os
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Optional

from langchain_core.documents import Document
from PyPDF2 import PageObject
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

Documents = list[Document]


@dataclass
class Article:
    file_path: Path
    download_link: Optional[str] = None
    title: Optional[str] = None
    year: Optional[int] = None
    citations: Optional[int] = None
    _n_pages: Optional[int] = field(init=False, default=None)
    _n_words: Optional[int] = field(init=False, default=None)
    text_summary: Optional[str] = field(init=False, default=None)

    def is_valid(self) -> bool:
        if not self.file_path.exists():
            return False
        try:
            io = self.file_path
            PdfReader(io)
        except PdfReadError:
            os.remove(str(self.file_path.absolute()))
            return False
        return True

    @property
    def n_pages(self) -> int:
        self._count_pages_and_words()
        if self._n_pages is None:
            raise ValueError
        return self._n_pages

    @property
    def n_words(self) -> int:
        self._count_pages_and_words()
        if self._n_words is None:
            raise ValueError
        return self._n_words

    def _count_pages_and_words(self):
        io = self.file_path.open("rb")
        if self._n_words is None:
            try:
                reader = PdfReader(io)
                self._n_pages = len(reader.pages)
                self._n_words = _count_words(reader)
            finally:
                io.close()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Article):
            return False
        return self.file_path == other.file_path

    def __hash__(self) -> int:
        return self.file_path.__hash__()


Articles = list[Article]


def _count_words(reader: PdfReader) -> int:
    return sum(
        map(len, map(str.split, map(PageObject.extract_text, reader.pages)))
    )
