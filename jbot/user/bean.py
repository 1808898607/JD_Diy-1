#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: XuanPro
Date: 2022/01/11
"""

import asyncio
import os
import re
import traceback

from telethon import events

from .login import user
from .. import chat_id, jdbot, logger, LOG_DIR
from ..user.utils import bot_id


@user.on(events.NewMessage(from_users=chat_id, pattern=r"^-[bc]\s\d+$"))
async def beanchange(event):
    """
    京豆收支变化
    """
    try:
        message = event.message.text
        if re.search(r"\d", message):
            num = re.findall("\d+", message)[0]
        else:
            num = 1
        if "b" in message:
            cmdline = f"/bean {num}"
            jpeg = f"{LOG_DIR}/bean.jpg"
        else:
            cmdline = f"/chart {num}"
            jpeg = f"{LOG_DIR}/bot/bean.jpeg"
        if event.chat_id != bot_id:
            msg = await event.edit("正在查询，请稍后")
            await user.send_message(bot_id, cmdline)
            await asyncio.sleep(7)
            await msg.delete()
            await user.send_message(event.chat_id, f"您的账号{num}收支情况", file=jpeg)
        else:
            await event.delete()
            await user.send_message(bot_id, cmdline)
    except Exception as e:
        title = "【💥错误💥】\n\n"
        name = f"文件名：{os.path.split(__file__)[-1].split('.')[0]}\n"
        function = f"函数名：{e.__traceback__.tb_frame.f_code.co_name}\n"
        details = f"\n错误详情：第 {str(e.__traceback__.tb_lineno)} 行\n"
        tip = "\n建议百度/谷歌进行查询"
        push = f"{title}{name}{function}错误原因：{str(e)}{details}{traceback.format_exc()}{tip}"
        await jdbot.send_message(chat_id, push)
        logger.error(f"错误 {str(e)}")
