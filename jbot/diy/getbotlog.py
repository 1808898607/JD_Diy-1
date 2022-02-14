#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import traceback

from telethon import events

from .. import chat_id, jdbot, logger, LOG_DIR


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/?e$'))
async def getbotlog(event):
    try:
        file = f"{LOG_DIR}/bot/run.log"
        await jdbot.send_message(chat_id, "这是bot的运行日志，用于排查问题所在", file=file)
    except Exception as e:
        title = "【💥错误💥】\n\n"
        name = f"文件名：{os.path.split(__file__)[-1].split('.')[0]}\n"
        function = f"函数名：{e.__traceback__.tb_frame.f_code.co_name}\n"
        details = f"\n错误详情：第 {str(e.__traceback__.tb_lineno)} 行\n"
        tip = "\n建议百度/谷歌进行查询"
        push = f"{title}{name}{function}错误原因：{str(e)}{details}{traceback.format_exc()}{tip}"
        await jdbot.send_message(chat_id, push)
        logger.error(f"错误 {str(e)}")
