## | AutoAnimeMV:超轻量化快速部署看番遥遥领先！
<div align="center">
  <a href="https://github.com/Abcuders/AutoAnimeMV">
    <img src="./Image/logo.png">
  </a>

**全自动追番新时代！不动手才是硬道理！**


**简体中文 | [English](./README_en.md)**

*! En-README.md 由于我精力不够所以有太多落后未更新的地方,如果您感兴趣并且有时间的希望您能帮助一下我✊*

[![ GitHub 开源许可证](https://img.shields.io/github/license/Abcuders/AutoAnimeMv)](https://github.com/Abcuders/AutoCartoonMv/LICENSE) [![GitHub release](https://img.shields.io/github/v/release/Abcuders/AutoAnimeMv)](https://github.com/Abcuders/AutoAnimeMv/releases/) [![telegram](https://img.shields.io/badge/telegram-AutoAnimeMv-blue?style=flat&logo=telegram)](https://t.me/AutoAnimeMv)

***

 😊这是一个**番剧自动识别**`剧名剧集+自动重命名+自动整理的工具`,**具有部署方便,开箱即用的特点**,用来配合qBittorrent实现Rss订阅下载Emby全自动刮削一条龙到家式爽歪歪服务!

 </div>

> **🚀点击左上角打开目录，选择您要阅读的部分**

## 💡 功能说明
* **部署快速,使用方便的番剧视频/字幕重命名+整理工具**
  >   
      动漫(分类)
      ├── 因为太怕痛就全点防御力了
      │   ├── Season01
      │   │   ├── E01.mp4
      │   │   ├── E02.mp4
      │   │   ├── E03.mp4
      │   │   └── ...
      │   └── Season02
      │       ├── E01.mp4
      │       ├── E02.mp4
      │       ├── E02.chi.srt
      │       └── ...
      |___ 無神世界的神明活動
      |    └── Season01  
      │        ├── E01.mp4
      │        ├── E01.chs.ass
      │        ├── E02.mp4
      │        └── ....
      |
      ......
  
* **一次配置,无感使用**
* **支持硬链接配置,保种必备**
* **支持番剧分类,让一切井井有条**
* **本地批处理和QB下载模式任君选择**
* **快速更新,享受更多新体验**

    ## 待更新的功能
    - [x] 扩展模块功能
    - [x] BgmApi支持 
    - [x] TMDBApi支持
    - [ ] WEB管理
    - [x] 油猴脚本扩展
    - [ ] 番剧订阅
    - [ ] 本地番剧信息缓存
    - [ ] 完全番剧特典支持 
    - [x] 修复模式
    - [x] 清理过时日志
    - [x] Telegram 机器人通知(win/linux)
    - [x] Telegram 机器人远程管理 Qb
    - [x] 🔥 彩蛋

## 🚀 快速开始

### 🏕️ 环境支持
要使用本工具您必须需要 `🐍Python3环境` 支持,我们建议您搭配 `🔵qBittorrent` 下载工具和 `🟩Emby` / `🎶Jellyfin` 等媒体库使用
>  🐍Python使用的依赖库:`sys` `os` `time` `datetime` `re` `ast` `shutil`  `requests` `zhconv`

>以上`requests`(网络访问),`zhconv`(简繁互化)需要您进行安装,如没有 `pip`,可以使用仓库中的 `get-pip.py` 安装
```shell
python3 -m pip install requests
python3 -m pip install zhconv
```
> **注：仓库中的 `get-pip.py` 不仅可以安装`pip`,还可以直接安装模块**
```shell
python3 get-pip.py install 
python3 -m pip install zhconv
```

> `requirements-AAM.txt` 文件是 `AutoAnimeMv.py` 的依赖库安装描述文件

> `requirements.txt` 文件是项目的全部依赖库安装描述文件

**更多解释请参考 [详细文档](##-详细的文档)**


### 使用介绍

* `AutoAnimeMv.py`是核心处理程序,它有两种核心处理方式,模式的切换靠的是传参数量 
* 同时工具自己拥有一些可配置项,详情见[详细文档](##-详细的文档)
* 本工具默认不打印任何信息,如果您有需要,可在配置文件中进行配置,请参考 [详细文档](##-详细的文档)

    #### QB下载模式
    > 在此模式下`AutoAnimeMv.py`支持 3~4 个参数,`下载路径` `下载文件名` `下载文件数` `文件分类`(可选) 
    
    1.将`AutoAnimeMv.py`上传至`🔵qBittorrent`能访问的路径下  
  
    2.在`🔵qBittorrent`中创建`动漫`分类(非必须)  

    3.修改qb配置: `下载`切换`Torrent 内容布局`为`不创建子文件夹`  

    4.修改qb配置: `下载`勾选 `Torrent 完成时运行外部程序`, 在输入框填入如下内容(参数顺序不可更改且参数要用`""`包裹,其中 `/dir/to/AAM.py` 更换为步骤一中脚本放置的绝对路径,如没有配置`分类`,请删除`"%L"`)  

    ```shell
    python3 /dir/to/AAM.py "%D" "%N" "%C" "%L"
    ```
     > <img src="./Image/Example/two.jpg" width="300" height="300"> <img src="./Image/Example/three.jpg" width="300" height="300">

     5.取消做种，修改qb配置: 将`🔵qBittorrent `的`做种限制`改成`当分享率达到0当做种时间达到0分钟然后暂停torrent`

    #### 批处理模式
    > 在此模式下`AutoAnimeMv.py`支持 1~2 个参数,`需要整理的番剧所在路径` `文件分类`(可选) 
    
    传入参数顺序不可更改且参数要用`""`包裹
    ```
    python3 AutoAnimeMv.py "需要整理的番剧所在路径" "文件分类(可选)"
    ```  
    #### Help模式
    ```
    python3 AutoAnimeMv.py help
    ```

    ```
      
       █████╗ ██╗   ██╗████████╗ ██████╗  █████╗ ███╗   ██╗██╗███╗   ███╗███████╗███╗   ███╗██╗   ██╗
      ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██╔══██╗████╗  ██║██║████╗ ████║██╔════╝████╗ ████║██║   ██║
      ███████║██║   ██║   ██║   ██║   ██║███████║██╔██╗ ██║██║██╔████╔██║█████╗  ██╔████╔██║██║   ██║
      ██╔══██║██║   ██║   ██║   ██║   ██║██╔══██║██║╚██╗██║██║██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║╚██╗ ██╔╝
      ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║  ██║██║ ╚████║██║██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║ ╚████╔╝
      ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝  ╚═══╝
      -------------------------------------------------------------------------------------------------
      * 欢迎使用AutoAnimeMv，这是一个番剧自动识别剧名剧集+自动重命名+自动整理的工具
      * Github URL：https://github.com/Abcuders/AutoAnimeMv
      * 一般使用方法请见Github Docs，以下是不常用的使用方法：
          python3 AutoAnimeMv.py [help] [updata] [fixSE]
      * 参数解释：
          help 打印出Help {help}
          updata,update  更新AutoAnimeMv.py {updata}
          fixSE 修复错乱的剧季 {fixSE 需要修复的番剧目录 需要修复的剧季 修复之后的剧季}
    ```

    #### 更新模式
    使用`updata`/`update`来更新`AutoAnimeMv.py`
    ```
    python3 AutoAnimeMv.py updata
    ```
    #### 修复模式
    * 修复错乱的剧季
    ```
    python3 AutoAnimeMv.py fixSE 需要修复的番剧目录 需要修复的剧季 修复之后的剧季
    ```
## 📝 详细的文档

* **[FirstReadMe.md](./Docs/FirstReadMe.md) 提供一个更详细的文档,如果您想要了解更多,可选择参考该文档**

* **[FAQ.md](./Docs/FAQ.md) 包含一些常见问题供您查阅**

* **[傻瓜教程](./TutorialsforDummies.md)**
## 相关群组

交流/工作群: [Telegram](https://t.me/AutoAnimeMv)

## ⭐ 贡献者 ✨

**感谢这些有趣又很棒的人！！！**
> 如果您也想要为这个项目添砖加瓦,可以直接来[Issues](https://github.com/Abcuders/AutoAnimeMv/issues)提出您宝贵的建议或者@我问一下能做些什么

<a href="https://github.com/wzfdgh">
<img src="https://avatars.githubusercontent.com/u/93830081?s=96&v=4"  width="80px" height="80px"> 
</a>
<a href="https://github.com/Nanako718">
<img src="https://avatars.githubusercontent.com/u/60038246?s=96&v=4"  width="80px" height="80px">
</a>
<a href="https://github.com/star-cheat">
<img src="https://avatars.githubusercontent.com/u/124486654?v=4"  width="80px" height="80px">
</a>
<a href="https://github.com/zerodoge">
<img src="https://avatars.githubusercontent.com/u/126881933?v=4"  width="80px" height="80px">
</a>
<a href="https://github.com/ProbiusOfficial">
<img src="https://avatars.githubusercontent.com/u/41804496?v=4"  width="80px" height="80px">
</a>
<a href="https://github.com/Qs315490">
<img src="https://avatars.githubusercontent.com/u/40908389?v=4"  width="80px" height="80px">
</a>

## Star History
<a href="https://star-history.com/##Abcuders/AutoAnimeMv">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Abcuders/AutoAnimeMv&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Abcuders/AutoAnimeMv&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Abcuders/AutoAnimeMv&type=Date" />
  </picture>
</a>

## 🛑 暂缓更新公告
* **AutoAnimeMv（下称“本仓库”）因为某些不可控原因将暂缓更新并非跑路**

* **在本仓库暂缓更新期间，欢迎各位pr新功能以及继续在群内讨论本工具问题，本仓库不会删库或archived**

* **恢复*持续更新*时间待定**

