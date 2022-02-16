# (c) @AbirHasan2005

import requests
import mimetypes
from urllib.parse import unquote_plus
from telegram.ext import CommandHandler
from subprocess import run
from bot import dispatcher
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import get_readable_file_size
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.ext_utils.telegraph_helper import telegraph


def extract_mediainfo(link: str, bot, update):
    __response = requests.head(link, stream=True)
    msg = sendMessage("Extracting ...", bot, update)
    try:
        file_size = get_readable_file_size(int(__response.headers["Content-Length"].strip()))
        file_name = unquote_plus(link).rsplit('/', 1)[-1]
        mime_type = __response.headers.get("Content-Type", mimetypes.guess_type(file_name)).rsplit(";", 1)[0]
        result = run(f'mediainfo "{link}"', capture_output=True, shell=True)
        stderr = result.stderr.decode('utf-8')
        stdout = result.stdout.decode('utf-8')
        metadata = stdout.replace("\r", "").replace(link, file_name)
        html = "<h3>Metadata of {}</h3>" \
               "<br><br>" \
               "<pre>{}</pre>"
        page = telegraph.create_page(
            title="Metadata of Video",
            author_name="@mayurv03",
            author_url="https://t.me/mayurv03",
            html_content=html.format(file_name, metadata)
        )
        deleteMessage(bot, msg)
        sendMessage(
            f"**File Name:** `{file_name}`\n"
            f"**File Size:** `{file_size}`\n"
            f"**Mime Type:** `{mime_type}`\n\n"
            f"**Here all metadata of your video:**\n"
            f"https://telegra.ph/{page['path'][0]}",
            bot, update
        )
    except KeyError:
        deleteMessage(bot, msg)
        sendMessage("Not a valid direct downloadable video!", bot, update)


def mediainfo_cmd_handler(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) > 1:
        link = args[1]
    else:
        return sendMessage(f"/{BotCommands.MediaInfoCommand} [video_link]", context.bot, update)
    extract_mediainfo(link, context.bot, update)


mi_cmd_handler = CommandHandler(
    BotCommands.MediaInfoCommand,
    mediainfo_cmd_handler,
    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
    run_async=True
)
dispatcher.add_handler(mi_cmd_handler)
