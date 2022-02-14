import os
import traceback
from asyncio import sleep

from telethon import events

from .login import user
from .. import jdbot, chat_id, logger


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r"^/check$"))
async def check(event):
    try:
        if user.is_connected():
            await event.reply("`user成功连接Telegram服务器！`")
            await sleep(5)
            await event.delete()
        else:
            await event.reply("`user无法连接Telegram服务器！`")
    except Exception as e:
        title = "【💥错误💥】\n\n"
        name = f"文件名：{os.path.split(__file__)[-1].split('.')[0]}\n"
        function = f"函数名：{e.__traceback__.tb_frame.f_code.co_name}\n"
        details = f"\n错误详情：第 {str(e.__traceback__.tb_lineno)} 行\n"
        tip = "\n建议百度/谷歌进行查询"
        push = f"{title}{name}{function}错误原因：{str(e)}{details}{traceback.format_exc()}{tip}"
        await jdbot.send_message(chat_id, push)
        logger.error(f"错误 {str(e)}")
