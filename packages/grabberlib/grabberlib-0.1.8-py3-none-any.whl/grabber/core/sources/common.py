import pathlib
from typing import List

from telegraph import Telegraph
from tqdm import tqdm

from grabber.core.settings import get_media_root
from grabber.core.utils import (
    downloader,
    query_mapping,
    headers_mapping,
    get_tags,
    telegraph_uploader,
)


def get_sources_for_common(
    sources: List[str],
    entity: str,
    telegraph_client: Telegraph,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    **kwargs,
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
        final_dest_folder = get_media_root() / final_dest
        if not final_dest_folder.exists():
            final_dest_folder.mkdir(parents=True, exist_ok=True)
            final_dest = final_dest_folder

    for idx, source_url in tqdm_sources_iterable:
        folder_name = ""
        image_tags, soup = get_tags(
            source_url,
            headers=headers,
            query=query,
        )
        if not image_tags and entity == "asigirl":
            queries_and_atrrs = [
                ("a.gallery-item", "data-src"),
                ("a.swipebox", "href"),
                ("div.gallery-group a", "href"),
                ("div.gallery-container.justified-gallery a", "href"),
            ]
            for query, src_attr in queries_and_atrrs:
                image_tags, soup = get_tags(
                    source_url,
                    headers=headers,
                    query=query,
                )
                if image_tags:
                    break

        if page_title is None:
            page_title = soup.find('title').get_text(strip=True).rstrip()
            if "Free Download" in page_title:
                page_title = page_title.split("- Free Download")[0]
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
