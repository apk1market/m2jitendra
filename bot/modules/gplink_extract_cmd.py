# (c) @AbirHasan2005

import requests
from threading import Event
from telegram.ext import CommandHandler
from bot import dispatcher
from bot.helper.ext_utils.bot_utils import new_thread
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage


def gplinks_bypass(url):
    GPLinksApi = "https://api.abirhasan.wtf/gplink?url={}"
    try:
        return requests.get(GPLinksApi.format(url)).json()
    except:
        return {}


@new_thread
def gp_link_extract_cmd_handler(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) > 1:
        link = args[1]
    else:
        return sendMessage(f"/{BotCommands.GpLinkCommand} [gplink]", context.bot, update)
    msg = sendMessage("Extracting ...", context.bot, update)
    gp_data = gplinks_bypass(link)
    if not gp_data:
        deleteMessage(context.bot, msg)
        return sendMessage("Failed to extract main link from GPLink!", context.bot, update)
    sendMessage(f"Here is main link:\n\n{gp_data['url']}")


gp_cmd_handler = CommandHandler(BotCommands.GpLinkCommand, gp_link_extract_cmd_handler, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(gp_cmd_handler)
