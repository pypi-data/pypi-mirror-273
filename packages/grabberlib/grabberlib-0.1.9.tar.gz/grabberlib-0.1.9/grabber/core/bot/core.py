import asyncio
from typing import Optional
from aiogram import Bot
from tqdm import tqdm

from grabber.core.settings import BOT_TOKEN


async def send_message(
    post_text: str,
    channel: Optional[str] = "@cspmst",
    retry: Optional[bool] = False,
    posts_counter: Optional[int] = 0,
    retry_counter: Optional[int] = 0,
    sleep_time: Optional[int] = 0,
    tqdm_iterable: Optional[tqdm] = None,
) -> None:
    if tqdm_iterable is not None:
        console_printer = tqdm_iterable.set_description
    else:
        console_printer = print

    try:
        bot = Bot(token=f"{BOT_TOKEN}")
        async with bot.context():
            await bot.send_message(chat_id=channel, text=post_text)
            console_printer(f"Post sent to the channel: {post_text}")
    except Exception:
        sleep_time = 15
        if retry or posts_counter >= 15:
            retry_counter += 1
            await asyncio.sleep(sleep_time)
            console_printer(f"Retry number {retry_counter} sending post to channel")

        await send_message(
            post_text=post_text,
            channel=channel,
            retry=retry and retry_counter <= 50,
            posts_counter=posts_counter,
            retry_counter=retry_counter,
            sleep_time=sleep_time,
        )
