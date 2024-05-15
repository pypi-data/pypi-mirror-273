import pathlib
from typing import List

from telegraph import Telegraph
from tqdm import tqdm

from grabber.core.utils import (
    downloader,
    query_mapping,
    headers_mapping,
    get_tags,
    get_soup,
    telegraph_uploader,
)


def get_pages_from_pagination(url: str) -> List[str]:
    pagination_pages_query = "div.oceanwp-pagination.clr ul.page-numbers a.page-numbers"
    articles_from_pagination_query = "div.entries article.blog-entry a"
    next_page_url_base = f"{url}page/"
    source_urls = set()

    first_page = get_soup(url)
    articles = set(first_page.select(articles_from_pagination_query))
    pages = first_page.select(pagination_pages_query)

    if pages:
        pages_links = set()
        last_page = pages[-2]
        number_last_page = last_page.text
        for idx in range(2, int(number_last_page) + 1):
            pages_links.add(f"{next_page_url_base}{idx}")

        for link in pages_links:
            soup = get_soup(link)
            articles.update(set(soup.select(articles_from_pagination_query)))

    for a_tag in articles:
        if a_tag is not None and a_tag.attrs["href"] not in source_urls:
            source_urls.add(a_tag.attrs["href"])

    return source_urls


def get_sources_for_everia(
    sources: List[str],
    entity: str,
    telegraph_client: Telegraph,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    **kwargs,
) -> None:
    is_tag = kwargs.get("is_tag", False)
    query, src_attr = query_mapping[entity]
    headers = headers_mapping.get(entity, None)
    page_title = None
    title_folder_mapping = {}
    posts_sent_counter = 0
    titles = []

    if final_dest:
        final_dest = pathlib.Path(final_dest)
        if not final_dest.exists():
            final_dest.mkdir(parents=True, exist_ok=True)

    if is_tag:
        soup = get_soup(target_url=sources[0], headers=headers)
        page_title = soup.get_text(strip=True).split(" – EVERIA.CLUB")[0].strip().rstrip()
        sources = list(get_pages_from_pagination(sources[0]))

    tqdm_sources_iterable = tqdm(
        enumerate(sources),
        total=len(sources),
        desc="Retrieving URLs...",
    )

    for idx, source_url in tqdm_sources_iterable:
        image_tags, soup = get_tags(source_url, headers=headers, query=query)

        if page_title is None:
            page_title = soup.get_text(strip=True).split(" – EVERIA.CLUB")[0].strip().rstrip()
            titles.append(page_title)

        unique_img_urls = set()
        for idx, img_tag in enumerate(image_tags):
            img_src = img_tag.attrs[src_attr]
            img_name: str = img_src.split("/")[-1].split("?")[0]
            img_name = img_name.strip().rstrip()
            unique_img_urls.add((f"{idx + 1}-{img_name}", img_src))

        tqdm_sources_iterable.set_description(f"Finished retrieving images for {page_title}")

        if final_dest:
            folder_name = page_title
            title_dest = final_dest / folder_name
            if not title_dest.exists():
                title_dest.mkdir(parents=True, exist_ok=True)
            title_folder_mapping[page_title] = (unique_img_urls, title_dest)

        if save_to_telegraph:
            telegraph_uploader(
                unique_img_urls=unique_img_urls,
                page_title=page_title,
                posts_sent_counter=posts_sent_counter,
                telegraph_client=telegraph_client,
            )
            posts_sent_counter += 1

    if final_dest:
        downloader(
            titles=titles,
            title_folder_mapping=title_folder_mapping,
            headers=headers,
        )
