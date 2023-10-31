
> `工具更新较快,用法和功能都会更新,建议多来看看` 

> **🚀点击左上角打开目录，选择您要阅读的部分**
# ❓ 什么样的番剧能够被识别?
* 工具目前能够识别的类型要求为:
> 存在番剧剧集,且剧集处于剧名后(支持的剧集格式为`1-4位纯数字/XXXX集/第XXXX集/第XXXX话/00/XX.XX(这些SP也可以识别)/XXEND/XXE//XX END//XX E`),若存在`字幕组信息`,`字幕组信息`应在第一个位置,如果不在,则第一个位置应存在`《》`或者是其他情况(后文)
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

## ❓ 什么样的字幕能够被识别?
* 工具目前只支持识别 `简繁日` 字幕，多语种字幕按 `简繁日` 顺序识别一个语种
> 包含 `简` `sc` `chs` `GB` 的会被识别成 `简体字幕`

> 包含 `繁` `tc` `cht` `BIG5` 的会被识别成 `繁体字幕`

> 包含 `日` `jp` 的会被识别成 `日文字幕`

# 配置
* 没有配置文件时工具使用默认配置,存在配置文件时,配置文件会自行加载
* 以下是工具的默认配置信息,也是工具的所有可配置项,您可以在工具目录下的`config.ini`中进行自由配置,
```ini
# Config
PRINTLOGFLAG = True # 打印log开关
USEMODULE = False # 使用模块

# NetConfig
HTTPPROXY = '' # Http代理
HTTPSPROXY = 'http://10.0.0.1:7890' # Https代理
ALLPROXY = '' # 全部代理
USEBGMAPI = True # 使用BgmApi
USETMDBAPI = True #使用TMDBApi

# File处理Config
USELINK = True # 使用硬链接开关
LINKFAILSUSEMOVEFLAGS = False #硬链接失败时使用MOVE
RMLOGSFLAG = False # 日志文件超时删除,填数字代表删除多久前的

# FileName处理Config
JELLYFINFORMAT = False # jellyfin 使用 ISO/639 标准 简体和繁体都使用chi做标识
USETITLTOEP = False # 给每个番剧视频加上番剧Title 

# TgBotConfig
USERTGBOT = True # 使用TgBot进行远程管理
TGBOTDEVICESFLAG = 'qfgXFISHUXMsEycnjqz9' # 您的注册码
USERBOTNOTICE = False # 使用TgBot进行通知

# QBConfig
USERQBAPI = True # 使用QBApi
QBIP = '192.168.1.112' # QB的ip
QBPORT = 8081 # QBApi端口
QBUSERNAME = 'admin' # Qb账号
QBPASSWORD = 'Syn123456!' # Qb密码

# 附加Config
TIMELAPSE = 0 # 延时处理番剧
SEEPSINGLECHARACTER =False # SE EP单字符模式

```
* `config.ini.Template`是配置文件的模板,内容如上


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


* **注意如果有部分新配置没有解释，那么此配置即是内测功能，您可以来Tg群体验**


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
[2023-06-19 18:24:49] INFO: Link-D:\D\Test\\Made-in-Abyss\Season01\S01E01.chs.ass << D:\D\Test\[Airota][Made in Abyss][01][BDRip 1080p HEVC-10bit FLAC].CHS.ass 
[2023-06-19 18:24:49] INFO: --------------------------------------------------------------------------------
[2023-06-19 18:24:49] INFO: 匹配出的剧集 ==> 01
[2023-06-19 18:24:49] INFO: 通过剧集截断文件名 ==> Jigokuraku
[2023-06-19 18:24:53] INFO: Link-D:\D\Test\\Jigokuraku\Season01\S01E01.chs.ass << D:\D\Test\[BeanSub&FZSD&LoliHouse] Jigokuraku - 01 [WebRip 1080p HEVC-10bit AAC ASSx2].简体中文.ass
[2023-06-19 18:24:53] INFO: --------------------------------------------------------------------------------
[2023-06-19 18:24:53] INFO: 匹配出的剧集 ==> 09
[2023-06-19 18:24:53] INFO: 通过剧集截断文件名 ==> Jigokuraku
[2023-06-19 18:24:53] INFO: D:\D\Test\\Jigokuraku\Season01\已存在
[2023-06-19 18:24:54] INFO: Link-D:\D\Test\\Jigokuraku\Season01\S01E09.chs.ass << D:\D\Test\[BeanSub&FZSD&LoliHouse] Jigokuraku - 09 [WebRip 1080p HEVC-10bit AAC ASSx2].简体中文.ass
[2023-06-19 18:24:54] INFO: 一切工作已经完成,用时7.112677097320557
```

### Log 保存位置的解释
* 默认情况下,Log文件会保存在传入的`保存路径`下,当无法访问此路径时,Log保存在工具目录下

### Api功能的解释
> Api功能默认开启,在一般情况下我们不建议关闭
* 当您同时启用 `BGMAPI` 和 `TMDBAPI`时,如果匹配出的是中文,将会优先交给 `BGMAPI` 识别,如果有返回值再把返回值交给 `TMDBAPI` 识别,如果没有则让 `TMDBAPI` 识别原匹配

## 油猴脚本扩展
* `Tampermonkey/main.js` 是给 `mikanani` 提供 `快速添加到qb下载的脚本`
* 要使用此脚本，您需要 `Tampermonkey` 的支持
* 使用效果
><img src="./Image/Example/TKone.jpg" width="600" height="300">
><img src="./Image/Example/TKtwo.jpg" width="600" height="300"> 
* 注意第一次使用您需要脚本的跨域申请
><img src="./Image/Example/TKthree.jpg" width="600" height="300">

## 模块扩展
* 啊吧吧...

## Telegram Bot通知功能(old 版本已废弃,New 版本开发中)
* **内测功能，您可以来Tg群体验**

# 🔥 彩蛋 
* 在配置文件中填上 `#mtf` 或 `#ftm`,再运行工具


# 想要学习早期版本代码
* 仓库`/Backups`存放着`1.0`版本的全部仓库内容，写得烂死了 :( ,有需求的可以前去查看