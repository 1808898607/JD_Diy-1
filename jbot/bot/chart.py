import os
import traceback

from telethon import events

from .beandata import get_bean_data
from .. import jdbot, chat_id, LOG_DIR, logger, BOT_SET, ch_name
from ..bot.quickchart import QuickChart

BEAN_IMG = f'{LOG_DIR}/bot/bean.jpeg'


@jdbot.on(events.NewMessage(chats=chat_id, pattern=r'^/chart'))
async def my_chart(event):
    msg_text = event.raw_text.split(' ')
    msg = await jdbot.send_message(chat_id, '正在查询，请稍后')
    try:
        if isinstance(msg_text, list) and len(msg_text) == 2:
            text = msg_text[-1]
        else:
            text = None
        if text:
            res = get_bean_data(int(text))
            if res['code'] != 200:
                msg = await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{str(res["data"])}')
            else:
                creat_chart(res['data'][3], f'账号{str(text)}', res['data'][0], res['data'][1], res['data'][2][1:])
                await jdbot.edit_message(msg, f'您的账号{text}收支情况', file=BEAN_IMG)
        else:
            await jdbot.edit_message(msg, '请正确使用命令\n/chart n n为第n个账号')
    except Exception as e:
        title = "【💥错误💥】\n\n"
        name = f"文件名：{os.path.split(__file__)[-1].split('.')[0]}\n"
        function = f"函数名：{e.__traceback__.tb_frame.f_code.co_name}\n"
        details = f"\n错误详情：第 {str(e.__traceback__.tb_lineno)} 行\n"
        tip = "\n建议百度/谷歌进行查询"
        push = f"{title}{name}{function}错误原因：{str(e)}{details}{traceback.format_exc()}{tip}"
        await jdbot.send_message(chat_id, push)
        logger.error(f"错误 {str(e)}")


def creat_chart(xdata, title, bardata, bardata2, linedate):
    qc = QuickChart()
    qc.background_color = '#fff'
    qc.width = "1000"
    qc.height = "600"
    qc.config = {
        "type": "bar",
        "data": {
            "labels": xdata,
            "datasets": [
                {
                    "label": "IN",
                    "backgroundColor": [
                        "rgb(255, 99, 132)",
                        "rgb(255, 159, 64)",
                        "rgb(255, 205, 86)",
                        "rgb(75, 192, 192)",
                        "rgb(54, 162, 235)",
                        "rgb(153, 102, 255)",
                        "rgb(255, 99, 132)"
                    ],
                    "yAxisID": "y1",
                    "data": bardata
                },
                {
                    "label": "OUT",
                    "backgroundColor": [
                        "rgb(255, 99, 132)",
                        "rgb(255, 159, 64)",
                        "rgb(255, 205, 86)",
                        "rgb(75, 192, 192)",
                        "rgb(54, 162, 235)",
                        "rgb(153, 102, 255)",
                        "rgb(255, 99, 132)"
                    ],
                    "yAxisID": "y1",
                    "data": bardata2
                },
                {
                    "label": "TOTAL",
                    "type": "line",
                    "fill": False,
                    "backgroundColor": "rgb(201, 203, 207)",
                    "yAxisID": "y2",
                    "data": linedate
                }
            ]
        },
        "options": {
            "plugins": {
                "datalabels": {
                    "anchor": 'end',
                    "align": -100,
                    "color": '#666',
                    "font": {
                        "size": 20,
                    }
                },
            },
            "legend": {
                "labels": {
                    "fontSize": 20,
                    "fontStyle": 'bold',
                }
            },
            "title": {
                "display": True,
                "text": f'{title}   收支情况',
                "fontSize": 24,
            },
            "scales": {
                "xAxes": [{
                    "ticks": {
                        "fontSize": 24,
                    }
                }],
                "yAxes": [
                    {
                        "id": "y1",
                        "type": "linear",
                        "display": False,
                        "position": "left",
                        "ticks": {
                            "max": int(int(max([max(bardata), max(bardata2)])+100)*2)
                        },
                        "scaleLabel": {
                            "fontSize": 20,
                            "fontStyle": 'bold',
                        }
                    },
                    {
                        "id": "y2",
                        "type": "linear",
                        "display": False,
                        "ticks": {
                            "min": int(min(linedate)*2-(max(linedate))-100),
                            "max": int(int(max(linedate)))
                        },
                        "position": "right"
                    }
                ]
            }
        }
    }
    qc.to_file(BEAN_IMG)


if ch_name:
    jdbot.add_event_handler(my_chart, events.NewMessage(chats=chat_id, pattern=BOT_SET['命令别名']['chart']))