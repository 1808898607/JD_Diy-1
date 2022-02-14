import os
import traceback
from asyncio import exceptions

from telethon import events, Button

from .utils import split_list, press_event, cmd
from .. import jdbot, chat_id, SHORTCUT_FILE, logger, BOT_SET, ch_name


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/a$'))
async def my_a(event):
    markup = []
    SENDER = event.sender_id
    msg = await jdbot.send_message(chat_id, '正在查询您的常用命令，请稍后')
    with open(SHORTCUT_FILE, 'r', encoding='utf-8') as f:
        shortcuts = f.readlines()
    try:
        cmdtext = None
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            markup = [Button.inline(shortcut.split(
                '-->')[0], data=str(shortcut.split('-->')[-1])) for shortcut in shortcuts if '-->' in shortcut]
            markup = split_list(markup, 3)
            markup.append([Button.inline('取消', data='cancel')])
            msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=markup)
            convdata = await conv.wait_event(press_event(SENDER))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                msg = await jdbot.edit_message(msg, '对话已取消')
                conv.cancel()
            else:
                await jdbot.delete_messages(chat_id, msg)
                cmdtext = res
                conv.cancel()
        if cmdtext:
            await cmd(cmdtext.replace('nohup ', ''))
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止')
    except Exception as e:
        title = "【💥错误💥】\n\n"
        name = f"文件名：{os.path.split(__file__)[-1].split('.')[0]}\n"
        function = f"函数名：{e.__traceback__.tb_frame.f_code.co_name}\n"
        details = f"\n错误详情：第 {str(e.__traceback__.tb_lineno)} 行\n"
        tip = "\n建议百度/谷歌进行查询"
        push = f"{title}{name}{function}错误原因：{str(e)}{details}{traceback.format_exc()}{tip}"
        await jdbot.send_message(chat_id, push)
        logger.error(f"错误 {str(e)}")


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/b$'))
async def my_b(event):
    markup = []
    msg = await jdbot.send_message(chat_id, '正在查询您的常用命令，请稍后')
    with open(SHORTCUT_FILE, 'r', encoding='utf-8') as f:
        shortcuts = f.readlines()
    try:
        await jdbot.delete_messages(chat_id, msg)
        markup = [Button.text(shortcut, single_use=True)
                  for shortcut in shortcuts if '-->' not in shortcut]
        markup = split_list(markup, int(BOT_SET['每页列数']))
        await jdbot.send_message(chat_id, '请做出您的选择：', buttons=markup)
    except Exception as e:
        title = "【💥错误💥】\n\n"
        name = f"文件名：{os.path.split(__file__)[-1].split('.')[0]}\n"
        function = f"函数名：{e.__traceback__.tb_frame.f_code.co_name}\n"
        details = f"\n错误详情：第 {str(e.__traceback__.tb_lineno)} 行\n"
        tip = "\n建议百度/谷歌进行查询"
        push = f"{title}{name}{function}错误原因：{str(e)}{details}{traceback.format_exc()}{tip}"
        await jdbot.send_message(chat_id, push)
        logger.error(f"错误 {str(e)}")


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/clearboard$'))
async def my_clear(event):
    try:
        await jdbot.send_message(chat_id, '已清空您的keyboard',buttons=Button.clear())
    except Exception as e:
        title = "【💥错误💥】\n\n"
        name = f"文件名：{os.path.split(__file__)[-1].split('.')[0]}\n"
        function = f"函数名：{e.__traceback__.tb_frame.f_code.co_name}\n"
        details = f"\n错误详情：第 {str(e.__traceback__.tb_lineno)} 行\n"
        tip = "\n建议百度/谷歌进行查询"
        push = f"{title}{name}{function}错误原因：{str(e)}{details}{traceback.format_exc()}{tip}"
        await jdbot.send_message(chat_id, push)
        logger.error(f"错误 {str(e)}")

if ch_name:
    jdbot.add_event_handler(my_a, events.NewMessage(
        from_users=chat_id, pattern=BOT_SET['命令别名']['a']))
    jdbot.add_event_handler(my_b, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['b']))
