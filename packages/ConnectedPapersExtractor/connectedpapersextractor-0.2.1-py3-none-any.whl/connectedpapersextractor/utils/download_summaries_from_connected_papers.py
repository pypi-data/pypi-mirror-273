from __future__ import annotations

from itertools import count
from pathlib import Path
from typing import Union

from enhanced_webdriver import EnhancedWebdriver
from undetected_chromedriver import ChromeOptions

from .. import Article
from .. import Articles
from ..utils.download_summaries import download_summaries


def _collect_article(driver: EnhancedWebdriver, dir_path: Path):
    link = driver.get_attribute(
        '//*[@id="desktop-app"]/div[2]/div[4]/div[3]/div/div[2]/div[5]/a[1]',
        "href",
    )
    if (
        driver.get_text_of_element(
            '//*[@id="desktop-app"]/div[2]/div[4]'
            '/div[3]/div/div[2]/div[5]/a[1]/span'
        ) != "PDF"
    ):
        return
    title = driver.get_text_of_element(
        '//*[@id="desktop-app"]/div[2]/div[4]/div[3]/div/div[2]/div[1]/div/a'
    )
    file_path = dir_path.joinpath(link.rpartition("/")[-1]).with_suffix(".pdf")
    return Article(
        file_path=file_path,
        download_link=link,
        year=int(
            driver.get_text_of_element(
                '//*[@id="desktop-app"]/div[2]/div[4]/div[1]/div/div[2]'
                '/div/div[2]/div[2]/div[2]/div[2]'
            )
        ),
        citations=int(
            driver.get_text_of_element(
                '//*[@id="desktop-app"]/div[2]/div[4]/'
                'div[3]/div/div[2]/div[4]/div[1]'
            ).split()[0]
        ),
        title=title,
    )


def _collect_articles(driver: EnhancedWebdriver, dir_path: Path) -> Articles:
    articles = list()
    for index in count(1):
        if not driver.click(
            '//*[@id="desktop-app"]/div[2]/div[4]/'
            f'div[1]/div/div[2]/div/div[2]/div[{index}]'
        ):
            break
        articles.append(_collect_article(driver, dir_path))
    return articles


def download_summaries_from_connected_papers(
    connected_papers_link: str,
    dir_path: Union[str, Path] = Path("/"),
) -> Articles:
    options = ChromeOptions()
    options.headless = True
    driver = EnhancedWebdriver.create(undetected=True, options=options)
    driver.get(connected_papers_link)
    summaries = _collect_articles(driver, Path(dir_path))
    driver.quit()
    download_summaries(summaries, Path(dir_path))
    return summaries
