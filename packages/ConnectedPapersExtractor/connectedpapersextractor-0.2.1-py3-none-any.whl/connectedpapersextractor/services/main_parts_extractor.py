from __future__ import annotations

from injector import inject

from ..article import Documents


@inject
class MainPartsExtractorService:
    def __init__(self):
        pass

    def extract(self, docs: Documents) -> Documents:
        return docs
