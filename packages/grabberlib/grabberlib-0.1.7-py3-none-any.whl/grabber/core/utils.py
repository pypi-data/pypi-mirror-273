import asyncio
import multiprocessing
import pathlib
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from dataclasses import dataclass
from time import sleep
from typing import Any, Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup, Tag
from casefy.casefy import snakecase
from lxml import etree
from PIL import Image
from telegraph import Telegraph
from telegraph import exceptions
from tenacity import retry, wait_chain, wait_fixed
from tqdm import tqdm

from grabber.core.bot.core import send_message
from grabber.core.settings import AUTHOR_NAME, AUTHOR_URL, SHORT_NAME, get_media_root

DEFAULT_THREADS_NUMBER = multiprocessing.cpu_count()
PAGINATION_QUERY = "div.jeg_navigation.jeg_pagination"
PAGINATION_PAGES_COUNT_QUERY = f"{PAGINATION_QUERY} span.page_info"
PAGINATION_BASE_URL_QUERY = "div.jeg_navigation.jeg_pagination a.page_number"
POSTS_QUERY_XPATH = "/html/body/div[2]/div[5]/div/div[1]/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/article/div/div/a"


query_mapping = {
    "xiuren": ("div.content-inner img", "src"),
    "nudebird": ("div.thecontent a", "href"),
    "hotgirl": ("div.thecontent a", "href"),
    "nudecosplay": ("div.content-inner a img", "src"),
    "v2ph": ("div.photos-list.text-center img", "src"),  # Needs to handle pagination
    "cgcosplay": ("div.gallery-icon.portrait img", "src"),
    "mitaku": ("img.msacwl-img", "data-lazy"),
    "xasiat": ("div.images a", "href"),
    "telegraph": ("img", "src"),
    "4khd": (
        "div.is-layout-constrained.entry-content.wp-block-post-content img",
        "src",
    ),
    "yellow": (
        "div.elementor-widget-container a[href^='https://terabox.com']",
        "href",
    ),
    "everia": ("div.entry-content img", "src"),
    "bestgirlsexy": ("div.elementor-widget-container p img", "data-src"),
    "asigirl": ("a.asigirl-item", "href"),
    "cosplaytele": ("img.attachment-full.size-full", "src"),
}


@dataclass(kw_only=True)
class PaginationXPath:
    pagination_query: str
    pages_count_query: str
    pagination_base_url_query: str
    posts_query_xpath: str

    def __post_init__(self) -> None:
        self.pages_count_query = f"{self.pagination_query} {self.pages_count_query}"


query_pagination_mapping = {
    "xiuren": PaginationXPath(
        pagination_query="div.jeg_navigation.jeg_pagination",
        pages_count_query="span.page_info",
        pagination_base_url_query="div.jeg_navigation.jeg_pagination a.page_number",
        posts_query_xpath=(
            "/html/body/div[2]/div[5]/div/div[1]/div/div/div[2]/"
            "div/div/div[2]/div/div[1]/div/div/div/article/div/div/a"
        ),
    ),
    "yellow": PaginationXPath(
        pagination_query="div.jeg_navigation.jeg_pagination",
        pages_count_query="span.page_info",
        pagination_base_url_query="div.jeg_navigation.jeg_pagination a.page_number",
        posts_query_xpath=(
            "/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/"
            "div/div/div[2]/div/div[1]/div/div/div/article/div/div/a"
        ),
    ),
    "nudecosplay": PaginationXPath(
        pagination_query="div.jeg_navigation.jeg_pagination",
        pages_count_query="span.page_info",
        pagination_base_url_query="div.jeg_navigation.jeg_pagination a.page_number",
        posts_query_xpath="/html/body/div[2]/div[5]/div/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/article/div/a",
    ),
}
headers_mapping = {
    "nudebird": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "nudecosplay": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "v2ph": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "cgcosplay": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "mitaku": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "xasiat": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "4khd": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
}


@retry(
    wait=wait_chain(
        *[wait_fixed(3) for _ in range(5)]
        + [wait_fixed(7) for _ in range(4)]
        + [wait_fixed(9) for _ in range(3)]
        + [wait_fixed(15)],
    ),
    reraise=True,
)
def get_image_stream(
    url,
    headers: Optional[Dict[str, Any]] = None,
) -> requests.Response:
    """Wait 3s for 5 attempts
    7s for the next 4 attempts
    9s for the next 3 attempts
    then 15 for all attempts thereafter
    """
    if headers is not None:
        r = requests.get(url, headers=headers, stream=True)
    else:
        r = requests.get(url, stream=True)

    if r.status_code >= 300:
        raise Exception(f"Not able to retrieve {url}: {r.status_code}\n")

    return r


@retry(
    wait=wait_chain(
        *[wait_fixed(3) for _ in range(5)]
        + [wait_fixed(7) for _ in range(4)]
        + [wait_fixed(9) for _ in range(3)]
        + [wait_fixed(15)],
    ),
    reraise=True,
)
def get_tags(
    url,
    query: str,
    headers: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Tag], BeautifulSoup]:
    """Wait 3s for 5 attempts
    7s for the next 4 attempts
    9s for the next 3 attempts
    then 15 for all attempts thereafter
    """
    soup = get_soup(target_url=url, headers=headers)
    tags = soup.select(query)

    return tags, soup


def get_soup(
    target_url: str,
    headers: dict[str, str] | None = None,
) -> BeautifulSoup:
    response = requests.get(target_url, headers=headers)
    return BeautifulSoup(response.content, features="lxml")


def downloader(
    titles: List[str],
    title_folder_mapping: Dict[str, Tuple[Tuple[str, str], pathlib.Path]],
    headers: Optional[Dict[str, str]] = None,
) -> None:
    with ThreadPoolExecutor(max_workers=DEFAULT_THREADS_NUMBER) as executor:
        # Dictionary to hold Future objects
        futures_to_title = {}
        future_counter = 0
        for title in titles:
            images_set, folder_dest = title_folder_mapping[title]
            partial_download = partial(
                download_images,
                new_folder=folder_dest,
                headers=headers,
                title=title,
            )
            future = executor.submit(partial_download, images_set)
            futures_to_title[future] = title
            future_counter += 1

        # Handling futures as they complete
        for future in tqdm(
            as_completed(futures_to_title),
            total=future_counter,
            desc=f"Retrieving {future_counter} tasks of downloading images",
        ):
            print(future.result())  # Get the result from the future object


def download_images(
    images_set,
    new_folder: pathlib.Path,
    title: str,
    headers: Optional[Dict[str, str]] = None,
):
    """Download an image from a given URL and save it to the specified filename.

    Parameters
    ----------
    - image_url: The URL of the image to be downloaded.
    - filename: The filename to save the image to.

    """

    tqdm_iterable = tqdm(
        images_set,
        total=len(images_set),
        desc=f"Downloading images for {title}",
    )

    for img_name, image_url in tqdm_iterable:
        filename = new_folder / f"{img_name}"
        should_convert_images = filename.suffix == ".webp"
        resp = get_image_stream(image_url, headers=headers)

        with open(filename.as_posix(), "wb") as img_file:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, img_file)

    if should_convert_images:
        convert_from_webp_to_jpg(new_folder)
    return "Done"


def telegraph_uploader(
    unique_img_urls: Tuple[Tuple[str, str]],
    page_title: str,
    posts_sent_counter: Optional[int] = 0,
    telegraph_client: Optional[Telegraph] = None,
    tqdm_iterable: Optional[tqdm] = None,
) -> None:
    if telegraph_client is None:
        telegraph_client = get_new_telegraph_client()

    posts = []
    html_post = create_html_template(unique_img_urls)
    post_url = create_page(
        title=page_title, html_content=html_post, telegraph_client=telegraph_client
    )
    telegraph_post = f"{page_title} - {post_url}"
    posts.append(telegraph_post)

    if posts_sent_counter == 10:
        sleep(10)

    try:
        asyncio.run(
            send_message(
                post_text=telegraph_post,
                retry=True,
                posts_counter=posts_sent_counter,
                tqdm_iterable=tqdm_iterable,
            )
        )
    except Exception:
        sleep(20)
        asyncio.run(
            send_message(
                post_text=telegraph_post,
                retry=True,
                posts_counter=posts_sent_counter,
                tqdm_iterable=tqdm_iterable,
            )
        )

        albums_dir = pathlib.Path.home() / ".albums_data"
        albums_dir.mkdir(parents=True, exist_ok=True)
        albums_file = albums_dir / "pages.txt"

        with albums_file.open("w") as f:
            f.write("\n".join(posts))

        albums_links = albums_file.read_text().split("\n")

        print_albums_message(albums_links)


def sort_file(file: pathlib.Path) -> str:
    filename = file.name.split(".")[0]
    filename = filename.zfill(2)
    return filename


def convert_from_webp_to_jpg(folder: pathlib.Path) -> None:
    files = list(folder.iterdir())
    tqdm_iterable = tqdm(
        files,
        total=len(files),
        desc="Converting images from WebP to JPEG",
        leave=False,
    )

    for file in tqdm_iterable:
        if file.suffix == ".webp":
            image = Image.open(file).convert("RGB")
            new_file = file.with_suffix(".jpg")
            image.save(new_file, "JPEG")
            file.unlink()


def get_new_telegraph_client() -> Telegraph:
    telegraph_factory = Telegraph()
    resp = telegraph_factory.create_account(
        short_name=SHORT_NAME,
        author_name=AUTHOR_NAME,
        author_url=AUTHOR_URL,
        replace_token=True,
    )
    access_token = resp["access_token"]
    telegraph_client = Telegraph(access_token=access_token)
    return telegraph_client


def upload_file(
    file: pathlib.Path,
    telegraph_client: Telegraph,
    try_again: Optional[bool] = True,
) -> Optional[str]:
    try:
        uploaded = telegraph_client.upload_file(file)
    except (
        Exception,
        exceptions.TelegraphException,
        exceptions.RetryAfterError,
    ) as exc:
        error_message = str(exc)
        if "try again" in error_message.lower() or "retry" in error_message.lower():
            sleep(5)
            if try_again:
                telegraph_client = get_new_telegraph_client()
                return upload_file(
                    file=file, telegraph_client=telegraph_client, try_again=False
                )
        return
    if uploaded:
        return uploaded[0]["src"]


def create_page(
    title: str,
    html_content: str,
    telegraph_client: Telegraph,
    try_again: Optional[bool] = True,
) -> str:
    try:
        page = telegraph_client.create_page(title=title, html_content=html_content)
        return page["url"]
    except (
        Exception,
        exceptions.TelegraphException,
        exceptions.RetryAfterError,
    ) as exc:
        error_message = str(exc)
        if "try again" in error_message.lower() or "retry" in error_message.lower():
            sleep(5)
            if try_again:
                telegraph_client = get_new_telegraph_client()
                return create_page(
                    title=title,
                    html_content=html_content,
                    telegraph_client=telegraph_client,
                    try_again=False,
                )


def create_html_template(image_tags: Tuple[str, str]) -> str:
    html_template = """<figure contenteditable="false"><img src="{file_path}"><figcaption dir="auto" class="editable_text" data-placeholder="{title}"></figcaption></figure>"""
    template_tags = []
    for title, image_src in image_tags:
        template_tags.append(html_template.format(file_path=image_src, title=title))

    html_post = "\n".join(template_tags)
    return html_post


def upload_to_telegraph(
    folder: pathlib.Path,
    telegraph_client: Telegraph,
    page_title: Optional[str] = "",
    send_to_telegram: Optional[bool] = False,
) -> str:
    files = sorted(list(folder.iterdir()), key=sort_file)
    title = page_title or folder.name
    title = title.strip().rstrip()

    contents = []
    files_urls = []
    html_template = """<figure contenteditable="false"><img src="{file_path}"><figcaption dir="auto" class="editable_text" data-placeholder="{title}"></figcaption></figure>"""

    uploaded_files_url_path = pathlib.Path(f"{snakecase(title)}.txt")
    if uploaded_files_url_path.exists() and uploaded_files_url_path.stat().st_size > 0:
        contents = uploaded_files_url_path.read_text().split("\n")
    else:
        iterable_files = tqdm(
            files,
            total=len(files),
            desc=f"Uploading files for {folder.name}",
            leave=False,
        )
        image_title = f"{title}"
        for file in iterable_files:
            file_url = upload_file(file, telegraph_client=telegraph_client)
            if not file_url:
                continue
            files_urls.append(file_url)
            contents.append(html_template.format(file_path=file_url, title=image_title))

    if contents:
        content = "\n".join(contents)
        try:
            page_url = create_page(
                title=title,
                html_content=content,
                telegraph_client=telegraph_client,
            )
        except exceptions.TelegraphException as exc:
            return f"Error: {exc} - {title} - {folder}"

        post = f"{title} - {page_url}"

        if send_to_telegram:
            asyncio.run(send_message(post))

        pages_file = get_media_root() / "assets/pages.txt"

        if not pages_file.exists():
            pages_file.touch(exist_ok=True)

        with open(pages_file, "a") as f:
            f.write(f"{post}\n")

        return post

    return "No content, please try again later"


def upload_folders_to_telegraph(
    folder_name: str,
    telegraph_client: Telegraph,
    limit: Optional[int] = 0,
    send_to_channel: Optional[bool] = False,
) -> None:
    folders = []

    if folder_name:
        root = get_media_root() / folder_name
        folders += [f for f in list(root.iterdir()) if f.is_dir()]
    else:
        root_folders = [
            folder for folder in get_media_root().iterdir() if folder.is_dir()
        ]
        for folder in root_folders:
            if folder.is_dir():
                nested_folders = [f for f in folder.iterdir() if f.is_dir()]
                if nested_folders:
                    folders += nested_folders
                else:
                    folders = root_folders

    futures_to_folder = {}
    selected_folders = folders[:limit] if limit else folders
    with ThreadPoolExecutor(max_workers=DEFAULT_THREADS_NUMBER) as executor:
        future_counter = 0
        for folder in selected_folders:
            partial_upload = partial(
                upload_to_telegraph,
                folder,
                send_to_telegram=send_to_channel,
                telegraph_client=telegraph_client,
            )
            future = executor.submit(partial_upload)
            futures_to_folder[future] = folder
            future_counter += 1

        page_urls: list[tuple[str, str]] = []
        for future in tqdm(
            as_completed(futures_to_folder),
            total=future_counter,
            desc=f"Uploading {future_counter} albums to Telegraph...",
        ):
            result = future.result()
            page_urls.append(result)

        content = "\n".join([f"{page_url}" for page_url in page_urls])
        print(content)


def get_pages_from_pagination(url: str, target: str) -> List[str]:
    pagination_params = query_pagination_mapping[target]
    source_urls = set()
    soup = get_soup(url)
    dom = etree.HTML(str(soup))
    pagination_set = soup.select(pagination_params.pages_count_query)

    if not pagination_set:
        for a_tag in dom.xpath(pagination_params.posts_query_xpath):
            if a_tag is not None and a_tag.attrib["href"] not in source_urls:
                source_urls.add(a_tag.attrib["href"])
        return source_urls

    pagination = pagination_set[0]
    pagination_text = pagination.text
    first, last = pagination_text.split("Page")[-1].strip().split("of")
    first_page, last_page = int(first), int(last)

    first_link_pagination = soup.select(pagination_params.pagination_base_url_query)[0]
    href = first_link_pagination.attrs["href"]
    base_pagination_url = href.rsplit("/", 2)[0]

    for a_tag in dom.xpath(pagination_params.posts_query_xpath):
        source_urls.add(a_tag.attrib["href"])

    for index in range(first_page, last_page + 1):
        if index == 1:
            continue

        target_url = f"{base_pagination_url}/{index}/"

        soup = get_soup(target_url)
        dom = etree.HTML(str(soup))
        source_urls.update(
            [
                a_tag.attrib["href"]
                for a_tag in dom.xpath(pagination_params.posts_query_xpath)
            ]
        )

    return list(source_urls)


def print_albums_message(albums_links: List[str]) -> None:
    albums_message = ""

    for album in albums_links:
        albums_message += f"\t- {album}\n"

    message = "All albums have been downloaded and saved to the specified folder.\n"
    message += "Albums saved are the following:\n"
    message += f"{albums_message}"
    print(message)
