from __future__ import annotations

from operator import attrgetter

from injector import inject

from ..article import Articles


@inject
class SummariesCombineService:
    def __init__(self):
        pass

    def combine(self, articles_with_summaries: Articles) -> str:
        return "\n\n".join(
            map(": ".join,
                map(attrgetter("title", "text_summary"),
                    articles_with_summaries),
                )
            )


default_summaries_combine = SummariesCombineService()
