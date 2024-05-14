from cement import Controller, ex
from telegraph import Telegraph

from grabber.core.settings import TELEGRAPH_TOKEN
from grabber.core.sources.common import get_sources_for_common
from grabber.core.sources.everia import get_sources_for_everia
from grabber.core.sources.graph import get_for_telegraph
from grabber.core.sources.khd import get_sources_for_4khd
from grabber.core.sources.nudecosplay import get_sources_for_nudecosplay
from grabber.core.sources.xiuren import get_sources_for_xiuren
from grabber.core.utils import upload_folders_to_telegraph

from ..core.version import get_version

VERSION_BANNER = f"""
A beautiful CLI utility to download images from the web! {get_version()}
"""


class Base(Controller):
    class Meta:
        label = "base"

        # text displayed at the top of --help output
        description = "A beautiful CLI utility to download images from the web"

        # text displayed at the bottom of --help output
        epilog = "Usage: grabber --entity 4khd --folder 4khd --publish --sources <list of links>"

        # controller level arguments. ex: 'test --version'
        arguments = [
            ### add a version banner
            (
                ["-e", "--entity"],
                {
                    "dest": "entity",
                    "type": str,
                    "help": "Webtsite name from where it will be download",
                },
            ),
            (
                ["-s", "--sources"],
                {
                    "dest": "sources",
                    "type": str,
                    "help": "List of links",
                    "nargs": "+",
                },
            ),
            (
                ["-f", "--folder"],
                {
                    "dest": "folder",
                    "default": "",
                    "type": str,
                    "help": "Folder where to save",
                },
            ),
            (
                ["-l", "--limit"],
                {
                    "dest": "limit",
                    "type": int,
                    "help": "Limit the amount of posts retrieved (used altogether with --tag)",
                    "default": 0,
                },
            ),
            (
                ["-p", "--publish"],
                {
                    "dest": "publish",
                    "action": "store_true",
                    "help": "Publish page to telegraph",
                },
            ),
            (
                ["-u", "--upload"],
                {
                    "dest": "upload",
                    "action": "store_true",
                    "help": "Upload and publish folders to telegraph",
                },
            ),
            (
                ["-t", "--tag"],
                {
                    "dest": "is_tag",
                    "action": "store_true",
                    "help": "Indicates that the link(s) passed is a tag in which the posts are paginated",
                },
            ),
            (
                ["-b", "--bot"],
                {
                    "dest": "bot",
                    "action": "store_true",
                    "help": "Should the newly post be sent to telegram?",
                },
            ),
            (
                ["-v", "--version"],
                {
                    "action": "store_true",
                    "dest": "version",
                    "help": "Version of the lib",
                },
            ),
        ]

    @ex(hide=True)
    def _default(self):
        """Default action if no sub-command is passed."""

        entity = self.app.pargs.entity
        sources = self.app.pargs.sources
        folder = self.app.pargs.folder
        publish = self.app.pargs.publish
        upload = self.app.pargs.upload
        is_tag = self.app.pargs.is_tag
        limit = self.app.pargs.limit
        version = self.app.pargs.version
        send_to_telegram = self.app.pargs.bot
        telegraph_client = Telegraph(access_token=TELEGRAPH_TOKEN)

        if version:
            print(VERSION_BANNER)
            return

        getter_mapping = {
            "4khd": get_sources_for_4khd,
            "telegraph": get_for_telegraph,
            "xiuren": get_sources_for_xiuren,
            "nudecosplay": get_sources_for_nudecosplay,
            "nudebird": get_sources_for_nudecosplay,
            "hotgirl": get_sources_for_nudecosplay,
            "everia": get_sources_for_everia,
            "bestgirlsexy": get_sources_for_common,
            "asigirl": get_sources_for_common,
            "cosplaytele": get_sources_for_common,
        }

        if upload:
            upload_folders_to_telegraph(
                folder_name=folder,
                limit=limit,
                send_to_channel=send_to_telegram,
                telegraph_client=telegraph_client,
            )
        else:
            getter_images = getter_mapping.get(entity, get_for_telegraph)
            getter_images(
                sources=sources,
                entity=entity,
                telegraph_client=telegraph_client,
                final_dest=folder,
                save_to_telegraph=publish,
                is_tag=is_tag,
                limit=limit,
            )
