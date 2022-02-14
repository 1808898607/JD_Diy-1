#!/usr/bin/env bash

if [ -d "/jd" ]; then root=/jd; else root=/ql; fi

dir_jbot=$root/jbot
dir_diybot=$root/repo/diybot

file_bot=$root/config/bot.json
file_botset=$root/config/botset.json
file_diybotset=$root/config/diybotset.json

branch="develop"
url="https://github.com/chiupam/JD_Diy.git"

echo "1、安装bot依赖..."
apk --no-cache add -f zlib-dev gcc jpeg-dev python3-dev musl-dev freetype-dev
echo -e "bot依赖安装成功...\n"
if [ -d ${dir_diybot} ]; then rm -rf $dir_diybot; fi # 如果有root/repo/diybot目录则先删除目录
if [ -d ${dir_jbot} ]; then # 如果有root/jbot目录则先备份目录
  if [ ! -d $root/repo/backup ]; then mkdir $root/repo/backup; fi # 如果没有root/repo/backup目录则先新建目录
  dir_backup=$root/repo/backup/$(date +%m%d%H%M) # 确定备份目录名，以当前时间为目录名
  mkdir "$dir_backup" # 新建目录
  mv $root/jbot/* "$dir_backup" # 把root/jbot目录内所有文件移动到备份目录中
fi

echo "2、下载bot所需文件..."
git clone -b $branch $url $dir_diybot
cp -f "$dir_backup"/diy/diy.py "$dir_diybot"/diy/diy.py # 如果有自己写的diy.py则覆盖拉到/root/repo/diybot/diy目录中
cp -rf $dir_diybot/jbot/* $dir_jbot # 复制/reppt/repo/diybot/jbot目录中所有文件到/root/jbot目录中
if [ ! -f $file_bot ]; then cp -f $dir_diybot/config/bot.json $root/config; fi # 如果不存在/root/config/bot.json时候拉取一份进去
if [ ! -f $file_botset ]; then # 如果不存在/root/config/botset.json时候拉取一份进去
  cp $dir_diybot/jbot/set.json $root/config
  mv $root/config/set.json $file_botset # 改一下名字
else
  sed -i 's/user": "True"/user": "False"/' $file_botset
  echo "为安全起见，关闭user监控，请使用 /user 手动开启！"
fi
if [ ! -f $file_diybotset ]; then cp $dir_diybot/config/diybotset.json $root/config; fi # 如果不存在/root/config/diybotset.json时候拉取一份进去
echo -e "bot文件下载成功...\n"

echo "3、安装python3依赖..."
/usr/bin/python3 -m pip install --upgrade pip
pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip3  --no-cache-dir --default-timeout=100 install -r $dir_jbot/requirements.txt
echo -e "python3依赖安装成功...\n"
echo "4、启动bot程序..."
# shellcheck disable=SC2143
if [[ -z $(grep -E "123456789" $file_bot) ]]; then
  pm2 start $dir_jbot/ecosystem.config.js
  echo "bot启动成功..."
else
  echo "配置 $file_bot 后再次运行本程序即可启动机器人"
fi
