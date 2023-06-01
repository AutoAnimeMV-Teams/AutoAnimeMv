# | AutoAnimeMV:超轻量化快速部署看番遥遥领先！
<p align="center">
  <a href="https://github.com/Abcuders/AutoAnimeMV">
    <img src="https://github.com/Abcuders/AutoAnimeMV/blob/main/Image/logo.png">
  </a>
<p>

***
[![ GitHub 许可证](https://img.shields.io/github/license/Abcuders/AutoAnimeMv)](https://github.com/Abcuders/AutoCartoonMv/LICENSE) [![GitHub release](https://img.shields.io/github/v/release/Abcuders/AutoAnimeMv)](https://github.com/Abcuders/AutoAnimeMv/releases/) [![telegram](https://img.shields.io/badge/telegram-AutoAnimeMv-blue?style=flat&logo=telegram)](https://t.me/AutoAnimeMv)
> 😊这是一个**番剧自动识别剧名剧集+自动重命名+自动整理工具,具有部署方便,开箱即用的特点**,用来配合QBittorrent实现Rss订阅下载全自动刮削一条龙到家式爽歪歪服务!
 
 **本工具现在支持Linux🐧和Windowsℹ️了并且有了自己的项目群耶（点击上面tg小蓝标直通车）👏👏👏**
> **🚀点击左上角打开目录，选择您要阅读的部分**

**简体中文 | [English](https://github.com/Abcuders/AutoAnimeMV/blob/main/README_en.md)**

# 🏕️ 环境支持

要使用本工具您必须需要`🐍Python3环境`支持，我们建议您搭配`🔵Qbittorrent`使用

# 💡 帮助&提醒

 * **`🐍Python3环境`**:您可以在[🐍Python官网](https://www.python.org/downloads/windows/)下载合适的版本进行安装,我们建议安装3.9及以上的版本
   >  🐍Python使用的依赖库:`sys` `os` `time` `re` `ast`(Test.py用)
   以上依赖应该不需要您进行安装
 * 如果您直接使用pip进行install遇到 `❗Fatal error in launcher: Unable to create process using pip问题` ,请使用`python3 -m pip install`
 * <img style="vertical-align:sub;" src="https://github.com/Abcuders/AutoAnimeMV/blob/main/Image/rss.png" height="15" width="35" > **`番剧网站`**:如果您需要RSS或BT或番剧支持，您可以来我们的Tg群寻找帮助
   
## 🕹️ 工具的处理逻辑

  * 开始Run之后会进行自动识别视频文件格式、番剧剧集、截断文件名、去除无效文字、剔除字幕组、保留剧名剧季，并将视频文件重命名为`S01E剧集.文件格式`再移至`下载路径` 下的`剧名\Season_剧季`文件夹(如果没有则会自动创建)就像下面一样:
    ```
    [ANi] 无神世界的神明活动（仅限港澳台地区） - 01 [1080P][Bilibili][WEB-DL]  [AAC AVC][CHT CHS][MP4].MP4
    >>无神世界的神明活动/Season_01/S01E01.mp4
    ```
    > *我们将 判断是否属于`动漫`分类功能注释了，现在它是一个可选功能，您可以根据不同的类型设置不同的Video保存路径*

     🍟同时，在脚本目录会生成以时间命名的Log文件,其内容为
     
     > Sun_May_28_02-16-36_2023.log

     ```
    LOG开始记录，完整log条目为8条
    1.接受到['.\\AutoAnimeMv.py', 'E:\\D\\Test', '[DMG&LoliHouse] Kono Subarashil Sekai ni Bakuen wo! - 01 [WebRip 1080p HEVC-10bit AAC ASSx2].mkv']参数
    2.匹配剧集为01
    3.通过剧集截断文件名为=DMG&LoliHouse=-Kono-Subarashil-Sekai-ni-Bakuen-wo=---
    4.番剧Name为Kono-Subarashil-Sekai-ni-Bakuen-wo
    5-4.TrueVideoName=Kono-Subarashil-Sekai-ni-Bakuen-wo,Season=01
    6.当前操作系统识别码为nt,posix/nt/java对应linux/windows/java虚拟机
    7.创建Kono-Subarashil-Sekai-ni-Bakuen-wo\Season_01完成
    8.创建E:\D\Test\Kono-Subarashil-Sekai-ni-Bakuen-wo\Season_01\S01E01.mkv完成 
    ```
## 🧰 测试工具 
* 自🍞`v1.5.0`以后，您可以使用`Test.py`对`AutoCartoonMv.py`进行Bt识别测试，以下是`Test.py`的使用方法
  > `Test.py` 不需要任何参数，但是需要`tese`文件，其内容为
    ```json
   {"Bt":"","Name":"","Season":"","Episodes":"","FileType":""}
    ```
  > `Bt`参数为种子名称 `Name`参数为番剧名称(可选) `Season`为剧季数(可选) `Episodes`为剧集数(可选) `FileType`为视频文件格式(可选)

 
* 🍚举例,以下是规范的Test格式,您也可以写入多行Tests数据
  ```json
   {"Bt":"[DMG&LoliHouse] Kono Subarashil Sekai ni Bakuen wo! - 01 [WebRip 1080p HEVC-10bit AAC ASSx2].mkv","Name":"Kono Subarashil Sekai ni Bakuen wo","Season":"01","Episodes":"01","FileType":".mkv"}
  ```
  > 这些test测试数据可以用来在未来更新了匹配机制的情况下快速测试这个算法
* 执行以下代码即可进行测试
  ```
  python3 Test.py 
  ```
* 输出内容(debug用):
    ```
  现在进入Test mode,正在read test文件
  2.匹配剧集为01
  3.通过剧集截断文件名为=DMG&LoliHouse=-Kono-Subarashil-Sekai-ni-Bakuen-wo=---
  4.番剧Name为Kono-Subarashil-Sekai-ni-Bakuen-wo
  Kono-Subarashil-Sekai-ni-Bakuen-wo 01
  5-4.TrueVideoName=Kono-Subarashil-Sekai-ni-Bakuen-wo,Season=01
  01 01 Kono-Subarashil-Sekai-ni-Bakuen-wo .mkv
  {'Bt': '[DMG&LoliHouse] Kono Subarashil Sekai ni Bakuen wo! - 01 [WebRip 1080p HEVC-10bit AAC ASSx2].mkv', 'Name': 'Kono Subarashil Sekai ni Bakuen wo', 'Season': '01', 'Episodes': '01', 'FileType': '.mkv'}....Ok
    ```
  
* 如果您想在`Test`文件中屏蔽某一条test测试数据,直接在开头添加`#`即可
  ```json
  #{"Bt":"[DMG&LoliHouse] Kono Subarashil Sekai ni Bakuen wo! - 01 [WebRip 1080p HEVC-10bit AAC ASSx2].mkv","Name":"Kono Subarashil Sekai ni Bakuen wo","Season":"01","Episodes":"01","FileType":".mkv"}
  ```
## 📻 常见问题建议

* 在群晖NAS中，套件中心安装的`🐍python3`环境可能出现奇奇怪怪的问题，请使用第三方套件源(第三方源需要手动为`🐍python3`创建软连接至/usr/local/bin/python3)

* 如果你使用的是群晖NAS `🐳Docker`版的`🔵QBitTorrent`,你可以在容器日志中直接看到`AutoCartoonMv.py`输出的Log信息
  
# 📝 使用方法 

 > `AutoCartoonMv.py`需要三个参数,`下载路径` `下载文件名` `文件分类`(可选) 
## 使用场景1-配合NAS Qbittorrent进行使用
  * 1.将`AutoCartoonMv.py`上传至`🔵QBittorrent`能访问的路径下
  
  * 2.在`🔵Qbittorrent`中创建`动漫`分类(非必须，你想要用什么名字都可以，去修改`AutoCartoonMv.py`中的判断即可，当然不要分类也可以)

  * 3.修改qb配置: `下载`勾选 `Torrent 完成时运行外部程序`, 下面填上(传入参数顺序不可更改)
  
    ```
    python3 AutoCartoonMv.py放置路径 下载路径 下载文件名 文件分类
    ```
    上面三个参数可以由`🔵Qbittorrent`传入，即
    ```
    python3 AutoCartoonMv.py放置路径 "%D" "%N" "%L"(可选,您需要自己在源码里修改)
    ```
  * 4.取消做种，修改qb配置: 将`🔵QBitTorrent `的`做种限制`改成`当分享率达到0当做种时间达到0分钟然后暂停torrent`

  * 5.现在你就可以下载一个番剧测试效果啦
    > 🚩举例，下面的文件名字都可以被识别`[Comicat][Jigokuraku][01][1080P][GB&JP][MP4].mp4` 
  
    >`【悠哈璃羽字幕社】[虚构推理_Kyokou Suiri ][09][x264 1080p][CHT].mp4`
  
    >` [桜都字幕组] 因为太怕痛就全点防御力了。第2季/ Itai No Wa Iya Nano De Bougyoryoku Ni Kyokufuri Shitai To Omoimasu. S2 [10][ 1080P@60FPS ][简繁内封].mp4`
  
    > 或者是带有干扰项的 `【喵萌奶茶屋】★01月新番★[英雄王，为了穷尽武道而转生～然后，成为世界最强的见习骑士♀～ / Eiyuuou, Bu wo Kiwameru Tame Tenseisu][10][720p][简体][招募翻译].mp4`

# 🧉 BB一下

* ⚠️本程序显然存在诸多问题，在此恳请各位大佬不吝赐教
* 23/5/26:下周我推要播总集篇，每周的精神食粮要断粮了😭😭没有你我怎么活呀，燕子！
* 23/6/1:嘿嘿嘿，无神真好看🤤

# ⭐ 贡献者 ✨

**感谢这些有趣又很棒的人！！！**
> 如果您也想要为这个项目添砖加瓦,可以直接来[Issues](https://github.com/Abcuders/AutoAnimeMv/issues)提出您宝贵的建议或者@我问一下能做些什么

<a href="https://github.com/wzfdgh">
<img src="https://avatars.githubusercontent.com/u/93830081?s=96&v=4"  width="60px" height="60px"> 
</a>
<a href="https://github.com/Nanako718">
<img src="https://avatars.githubusercontent.com/u/60038246?s=96&v=4"  width="60px" height="60px">
</a>

# 🧾 声明

**该仅供个人合法用途,任何使用该工具进行直接或者间接非法盈利活动的行为,均不属于授权范围,也不受到任何支持和认可**
