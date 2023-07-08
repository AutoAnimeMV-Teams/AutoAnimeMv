# | AutoAnimeMV: 这里是更详细的帮助文档(仓库2.0版本的)
<div align="center">
  <a href="https://github.com/Abcuders/AutoAnimeMV">
    <img src="./Image/logo.png">
  </a>

**全自动追番新时代！不动手才是硬道理！**


**简体中文 | [English](./DOCSE_en.md)**

*! En-README.md 由于我精力不够所以有太多落后未更新的地方,如果您感兴趣并且有时间的希望您能帮助一下我✊*

[![ GitHub 许可证](https://img.shields.io/github/license/Abcuders/AutoAnimeMv)](https://github.com/Abcuders/AutoCartoonMv/LICENSE) [![GitHub release](https://img.shields.io/github/v/release/Abcuders/AutoAnimeMv)](https://github.com/Abcuders/AutoAnimeMv/releases/) [![telegram](https://img.shields.io/badge/telegram-AutoAnimeMv-blue?style=flat&logo=telegram)](https://t.me/+3q1JuBrrPkJkOWJl)

</div>

***
> `工具更新较快,用法和功能都会更新,建议多来看看` 

> **🚀点击左上角打开目录，选择您要阅读的部分**
# ❓ 什么样的番剧能够被识别?
* 工具目前能够识别的类型要求为:
> 存在番剧剧集,且剧集处于剧名后(支持的剧集格式为`1-4位纯数字/XXXX集/第XXXX集/00/XX.XX(这些SP也可以识别)/XXEND/XXE//XX END//XX E`),若存在`字幕组信息`,`字幕组信息`应在第一个位置,如果不在,则第一个位置应存在`《》`或者是其他情况(后文)
```
[DMG&LoliHouse] Kono Subarashil Sekai ni Bakuen wo! - 01 [WebRip 1080p HEVC-10bit AAC ASSx2].mkv
```

```
[漫游字幕组]散华礼弥/僵尸哪有那么萌 第1集 720P MKV（外挂字幕） [274.7MB].mkv
```

```
[织梦字幕组][间谍教室 スパイ教室][11集][1080P][AVC][简日双语] [337.62 MB].mp4
```

```
《江戶前精靈》#9 (日語原聲)【Ani-One Asia】.mp4
```

> torrent中包含`[]` `【】`也可以识别,包含`04月新番` `（僅限港澳台地區）` `2023.04.02`之类的信息也可以剔除干净
```
[Comicat][Jigokuraku][01][1080P][GB&JP][MP4].mp4
```

```
[ANi] 無神世界的神明活動（僅限港澳台地區） - 08 [1080P][Bilibili][WEB-DL][AAC AVC][CHT CHS].mp4
```

```
[c.c動漫][4月新番][無神世界的神明活動][07][BIG5][1080P][MP4][網盤下載]296.9MB.mkv
```

```
[Marukazoku][Sazae-san][2694][2023.04.02][BIG5][1080P][MP4].mp4
```

> torrent中包含`/`的将被工具认为是多语种译名番剧,若存在全英文译名将优先采用,不管哪个译名中存在`S2` `第二季` `Season2` `Season 2` `Season-2` `2nd-Season` 之类的剧季信息也可以识别(如果有需要,后面会开发`シーズン2`之类的剧季识别)
```
【喵萌奶茶屋】★01月新番★[英雄王，为了穷尽武道而转生～然后，成为世界最强的见习骑士♀～ / Eiyuuou, Bu wo Kiwameru Tame Tenseisu][10][720p][简体][招募翻译].mp4
```

```
[桜都字幕组] 因为太怕痛就全点防御力了。第2季/ Itai No Wa Iya Nano De Bougyoryoku Ni Kyokufuri Shitai To Omoimasu. S2 [10][ 1080P@60FPS ][简繁内封].mp4
```
> torrent中包含`v2`之类信息的重修版也是可以识别的(在开头的`v2`信息则会被剔除,字幕组信息还是在第一位)
```
[喵萌Production&LoliHouse] 偶像大师 灰姑娘女孩 U149 / THE IDOLM@STER CINDERELLA GIRLS U149 - 07v2 [WebRip 1080p HEVC-10bit AAC][简繁日内封字幕]675.6MB.mkv
```

```
[V2][织梦字幕组][鬼灭之刃 锻刀村篇 鬼灭の刃 刀锻冶の里编][01集][720P][AVC][繁日双语] [614.11 MB].mp4
```
~~> 番剧特别篇,会按TMDB支持的方式进行整理,即特别篇剧季会认定为`Season 00`,剧集则会按TMDB上的来,比如`我推的孩子`的`7.5`集,在TMDB上则是`第1集`~~
* 以上规则应该涵盖了绝大多番剧torrent

# 配置
* 没有配置文件时工具使用默认配置,存在配置文件时,配置文件会自行加载
* 以下是工具的默认配置信息,也是工具的所有可配置项,您可以在工具目录下的`config.ini`中进行自由配置,
```ini
#Config
PRINTLOGFLAG = True # 打印log开关
HTTPPROXY = '' # Http代理
HTTPSPROXY = 'http://192.168.1.1:7890' # Https代理
ALLPROXY = '' # 全部代理
USELINK = True # 使用硬链接开关
LINKFAILSUSEMOVEFLAGS = False #硬链接失败时使用MOVE
RMLOGSFLAG = '7' # 日志文件超时删除
USERTGBOT = False # 使用TgBot进行远程管理
TGBOTDEVICESFLAG = '' # 您的注册码
USERBOTNOTICE = False # 使用TgBot进行通知
USERQBAPI = False # 使用QBApi
QBIP = '192.168.1.1' # QB的ip
QBPORT = 8080 # QBApi端口
QBUSERNAME = '' # Qb账号
QBPASSWORD = '' # Qb密码
```
* `config.ini.Template`是配置文件的模板,内容如上

* **请注意！config.ini.Template内容已更新，目前模板版本为2.3.1**

***
## 配置介绍
* 如果您想在配置文件中屏蔽一条配置项,在前面添上 `#` 即可
  ```ini
  #PRINTLOGFLAG = True
  ```

* `HTTPPROXY` `HTTPSPROXY` `ALLPROXY` 配置项是用来给您配置代理相关信息的,请按自己情况的来填

* `USELINK` 配置项是 `使用硬链接` 来整理番剧的开关,如果您需要保种请设置为 `True` [什么是硬链接？](https://zh.wikipedia.org/zh-cn/%E7%A1%AC%E9%93%BE%E6%8E%A5)

* `LINKFAILSUSEMOVEFLAGS`配置项,功能是硬链接失败时使用 Move 来整理番剧,部分文件系统不支持硬链接请注意(如 `exFat`)

* `RMLOGSFLAG` 配置项是用来控制工具删除保存天数达到和超过 `RMLOGSFLAG` 的值的配置,默认为 7 天,如果您不想删除请设置为 `False`

* `USEBOTFLAG`用来开启TgBot通知的开关

* **注意如果有部分新配置没有解释，那么此配置即是内测功能，您可以来Tg群体验**

# 常见问题
## pip安装出现问题
*   如果您直接使用pip进行install遇到 `❗Fatal error in launcher: Unable to create process using pip问题`
请使用`python3 -m pip install` 尝试安装

## 群晖NAS使用Python出现奇怪的问题
* 在群晖NAS中，套件中心安装的`🐍python3`环境可能出现奇奇怪怪的问题，请使用第三方套件源(第三方源需要手动为`🐍python3`创建软连接至/usr/local/bin/python3)

# 一些介绍说明
## Log相关
* 在程序运行完成后,无论是否成功都会生成`2023-06-19.log`这种格式的日志文件
```log
[2023-06-19 18:24:47] INFO: Running....
[2023-06-19 18:24:47] INFO: 正在读取外置ini文件
[2023-06-19 18:24:47] INFO: 配置 < PRINTLOGFLAG = True
[2023-06-19 18:24:47] INFO: 配置 < HTTPSPROXY = 'http://192.168.1.112:7890'
[2023-06-19 18:24:47] INFO: 配置 < USELINK = True
[2023-06-19 18:24:47] INFO: 配置 < LINKFAILSUSEMOVEFLAGS = False
[2023-06-19 18:24:47] INFO: 当前工具版本为2.0.(0.5)
[2023-06-19 18:24:47] INFO: 当前操作系统识别码为nt,posix/nt/java对应linux/windows/java虚拟机
[2023-06-19 18:24:47] INFO: 接受到的参数 > ['E:\\D\\fork\\AutoAnimeMv\\AutoAnimeMv.py ', 'D:\\D\\Test']
[2023-06-19 18:24:47] INFO: 没有发现任何番剧视频文件,但发现3个字幕文件 ==> ['[Airota][Made in Abyss][01][BDRip 1080p HEVC-10bit FLAC].CHS.ass', '[BeanSub&FZSD&LoliHouse] Jigokuraku - 01 [WebRip 1080p HEVC-10bit AAC ASSx2].简体中文.ass', '[BeanSub&FZSD&LoliHouse] Jigokuraku - 09 [WebRip 1080p HEVC-10bit AAC ASSx2].简体中文.ass']
[2023-06-19 18:24:47] INFO: 只有字幕文件需要处理
[2023-06-19 18:24:47] INFO: --------------------------------------------------------------------------------
[2023-06-19 18:24:47] INFO: 匹配出的剧集 ==> 01
[2023-06-19 18:24:47] INFO: 通过剧集截断文件名 ==> Made-in-Abyss
[2023-06-19 18:24:47] INFO: D:\D\Test\\Made-in-Abyss\Season01\已存在
[2023-06-19 18:24:49] INFO: Link-D:\D\Test\[Airota][Made in Abyss][01][BDRip 1080p HEVC-10bit FLAC].CHS.ass << D:\D\Test\\Made-in-Abyss\Season01\S01E01.other.ass
[2023-06-19 18:24:49] INFO: --------------------------------------------------------------------------------
[2023-06-19 18:24:49] INFO: 匹配出的剧集 ==> 01
[2023-06-19 18:24:49] INFO: 通过剧集截断文件名 ==> Jigokuraku
[2023-06-19 18:24:53] INFO: Link-D:\D\Test\[BeanSub&FZSD&LoliHouse] Jigokuraku - 01 [WebRip 1080p HEVC-10bit AAC ASSx2].简体中文.ass << D:\D\Test\\Jigokuraku\Season01\S01E01.chs.ass
[2023-06-19 18:24:53] INFO: --------------------------------------------------------------------------------
[2023-06-19 18:24:53] INFO: 匹配出的剧集 ==> 09
[2023-06-19 18:24:53] INFO: 通过剧集截断文件名 ==> Jigokuraku
[2023-06-19 18:24:53] INFO: D:\D\Test\\Jigokuraku\Season01\已存在
[2023-06-19 18:24:54] INFO: Link-D:\D\Test\[BeanSub&FZSD&LoliHouse] Jigokuraku - 09 [WebRip 1080p HEVC-10bit AAC ASSx2].简体中文.ass << D:\D\Test\\Jigokuraku\Season01\S01E09.chs.ass
[2023-06-19 18:24:54] INFO: 一切工作已经完成,用时7.112677097320557
```

### Log 保存位置的解释
* 默认情况下,Log文件会保存在传入的`保存路径`下,当无法访问此路径时,Log保存在工具目录下

## Telegram Bot通知功能(old 版本已废弃,New 版本开发中)
* **内测功能，您可以来Tg群体验**

# 🔥 彩蛋 
* 在配置文件中填上 `#mtf` 或 `#ftm`,再运行工具


# 想要学习早期版本代码
* 仓库`/Backups`存放着`1.0`版本的全部仓库内容,有需求的可以前去查看