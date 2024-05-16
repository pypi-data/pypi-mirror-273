import pathlib
from typing import List, Optional

from telegraph import Telegraph
from tqdm import tqdm

from grabber.core.utils import (
    downloader,
    query_mapping,
    headers_mapping,
    get_tags,
    telegraph_uploader,
)


def get_images_from_pagination(url: str, headers: Optional[dict] = None) -> List[str]:
    page_nav_query = "div.page-link-box li a.page-numbers"
    tags, _ = get_tags(url, headers=headers, query=page_nav_query)
    return [a.attrs["href"] for a in tags if tags]


def get_sources_for_4kup(
    sources: List[str],
    entity: str,
    telegraph_client: Optional[Telegraph] = None,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    is_tag: Optional[bool] = False,
    limit: Optional[int] = None,
) -> None:
    tqdm_sources_iterable = tqdm(
        enumerate(sources),
        total=len(sources),
        desc="Retrieving URLs...",
    )
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

    for idx, source_url in tqdm_sources_iterable:
        image_tags, soup = get_tags(
            source_url,
            headers=headers,
            query=query,
        )

        if page_title is None:
            page_title = soup.find("title").get_text(separator=" ", strip=True).split("- Beautiful")[0].rstrip()
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
                tqdm_iterable=tqdm_sources_iterable,
            )
            posts_sent_counter += 1
        page_title = None

    if final_dest:
        downloader(
            titles=titles,
            title_folder_mapping=title_folder_mapping,
            headers=headers,
        )

