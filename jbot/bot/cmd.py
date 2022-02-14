import os
import traceback

from telethon import events

from .utils import cmd
from .. import jdbot, START_CMD, chat_id, logger, BOT_SET, ch_name


@jdbot.on(events.NewMessage(from_users=chat_id, pattern='/cmd'))
async def my_cmd(event):
    """接收/cmd命令后执行程序"""
    logger.info(f'即将执行{event.raw_text}命令')
    msg_text = event.raw_text.split(' ')
    try:
        if isinstance(msg_text, list):
            text = ' '.join(msg_text[1:])
        else:
            text = None
        if START_CMD and text:
            await cmd(text)
            logger.info(text)
        elif START_CMD:
            msg = '''请正确使用/cmd命令，如
            /cmd jlog    # 删除旧日志
            /cmd jup     # 更新所有脚本
            /cmd jcode   # 导出所有互助码
            /cmd jcsv    # 记录豆豆变化情况
            '''
            await jdbot.send_message(chat_id, msg)
        else:
            await jdbot.send_message(chat_id, '未开启CMD命令，如需使用请修改配置文件')
        logger.info(f'执行{event.raw_text}命令完毕')
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
    jdbot.add_event_handler(my_cmd, events.NewMessage(chats=chat_id, pattern=BOT_SET['命令别名']['cmd']))
