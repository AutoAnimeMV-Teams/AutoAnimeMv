# AutoAnimeMv

[![ GitHub 许可证](https://badgen.net/github/license/Abcuders/AutoCartoonMv)](https://github.com/Abcuders/AutoCartoonMv/LICENSE)

😊这是一个番剧自动识别剧名剧集+自动重命名+自动整理工具,用来配合QBittorrent实现Rss订阅下载全自动刮削一条龙到家式爽歪歪服务!

# ⚠️注意
* 本程序目前只支持Linux🐧,因为我懒
* 本程序显然存在诸多问题，在此恳请各位大佬不吝赐教

# 🕹️ 工具的处理逻辑

开始Run之后将判断是否属于`动漫`分类，如果是才进行自动识别视频文件格式、番剧剧集、截断文件名、去除无效文字、剔除字幕组、保留剧名剧季，并将视频文件重命名为`S01E剧集.文件格式`再移至`下载路径` 下的`剧名\Season_剧季`文件夹（如果没有则会自动创建）

# 📝使用方法 
 `AutoCartoonMv.py`需要三个参数,`下载路径` `下载文件名` `文件分类` 和 🐍Python3环境支持
## 使用场景1-配合Qbittorrent进行使用
  * 1.将`AutoCartoonMv.py`上传至QBittorrent能访问的路径下
  
  * 2.在Qbittorrent中创建`动漫`分类(非必须，你想要用什么名字都可以，去修改`AutoCartoonMv.py`中的判断即可，当然不要分类也可以，自己去改)

  * 3.修改qb配置: `下载`勾选 `Torrent 完成时运行外部程序`, 下面填上(传入参数顺序不可更改)
  
  ```
  python3 AutoCartoonMv.py放置路径 下载路径 下载文件名 文件分类
  ```
  上面三个参数可以由Qbittorrent传入，即
  ```
  python3 AutoCartoonMv.py放置路径 "%D" "%N" "%L"
  ```
  * 4.取消做种，修改qb配置: 将BitTorrent 的`做种限制`改成`当分享率达到0当做种时间达到0分钟然后暂停torrent`

  * 5.现在你就可以下载一个番剧测试效果啦
  > 🚩举例，下面的文件名字都可以被识别`[Comicat][Jigokuraku][01][1080P][GB&JP][MP4].mp4` 
  
  >`【悠哈璃羽字幕社】[虚构推理_Kyokou Suiri ][09][x264 1080p][CHT].mp4`
  
  >` [桜都字幕组] 因为太怕痛就全点防御力了。第2季/ Itai No Wa Iya Nano De Bougyoryoku Ni Kyokufuri Shitai To Omoimasu. S2 [10][ 1080P@60FPS ][简繁内封].mp4`
  
  > 或者是带有干扰项的 `【喵萌奶茶屋】★01月新番★[英雄王，为了穷尽武道而转生～然后，成为世界最强的见习骑士♀～ / Eiyuuou, Bu wo Kiwameru Tame Tenseisu][10][720p][简体][招募翻译].mp4`
  
# 💡提醒
* 在群晖NAS中，套件中心安装的🐍python3环境可能出现奇奇怪怪的问题，请使用第三方套件源(第三方源需要手动为🐍python3创建软连接至/usr/local/bin/python3)
