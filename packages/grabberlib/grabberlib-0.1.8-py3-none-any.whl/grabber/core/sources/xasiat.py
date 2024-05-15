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


def get_for_xasiat(
    sources: List[str],
    entity: str,
    telegraph_client: Telegraph,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    **kwargs,
) -> None:
    send_to_telegram = kwargs.get("send_to_telegram", False)
    titles = set()
    tqdm_sources_iterable = tqdm(
        enumerate(sources),
        total=len(sources),
    )
    query, src_attr = query_mapping[entity]
    headers = headers_mapping.get(entity, None)
    folders = set()
    titles_and_folders = set()
    title_folder_mapping = {}

    if final_dest:
        final_dest_folder = get_media_root() / final_dest
        if not final_dest_folder.exists():
            final_dest_folder.mkdir(parents=True, exist_ok=True)
            final_dest = final_dest_folder

    for idx, source_url in tqdm_sources_iterable:
        folder_name = ""
        tqdm_sources_iterable.set_description(f"Retrieving URLs from {source_url}")
        tags, soup = get_tags(
            source_url,
            headers=headers,
            query=query,
        )

        title_tag = soup.select("title")[0]  # type: ignore
        folder_name = title_tag.get_text().strip().rstrip()
        title = folder_name
        titles.add(title)
        titles_and_folders.add((title, folder_name))

        if final_dest:
            new_folder = get_media_root() / final_dest / folder_name
        else:
            new_folder = get_media_root() / folder_name

        if not new_folder.exists():
            new_folder.mkdir(parents=True, exist_ok=True)

        folders.add(new_folder)
        unique_img_urls = set()

        for idx, img_tag in enumerate(tags or []):
            img_src = img_tag.attrs[src_attr]

            if "xasiat" in img_src:
                img_name: str = img_src.split("/")[-2]
                img_name = img_name.strip().rstrip()
                img_extension: str = img_name.split(".")[-1]
            else:
                img_name: str = img_src.split("/")[-1]
                img_name = img_name.strip().rstrip()
                img_extension: str = img_name.split(".")[-1]

            unique_img_urls.add(
                (title, f"{idx + 1}.{img_extension}", img_src),
            )

        title_folder_mapping[title] = (unique_img_urls, new_folder)

    downloader(title_folder_mapping, headers)
    telegraph_uploader(
        title_folder_mapping=title_folder_mapping,
        send_to_telegram=send_to_telegram,
        save_to_telegraph=save_to_telegraph,
        telegraph_client=telegraph_client,
    )
