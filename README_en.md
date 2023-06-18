# | AutoAnimeMV: Ultra-lightweight and fast deployment anime watching tool is at the forefront!
<div align="center">
  <a href="https://github.com/Abcuders/AutoAnimeMV">
    <img src="./Image/logo.png">
  </a>

The era of fully automated anime tracking! Doing nothing is the only way to go!

English | [简体中文](./README.md)

*! En-README.md has too many outdated parts due to my lack of energy. If you are interested and have time, I hope you can help me✊*

[![ GitHub license](https://img.shields.io/github/license/Abcuders/AutoAnimeMv)](https://github.com/Abcuders/AutoCartoonMv/LICENSE) [![GitHub release](https://img.shields.io/github/v/release/Abcuders/AutoAnimeMv)](https://github.com/Abcuders/AutoAnimeMv/releases/) [![telegram](https://img.shields.io/badge/telegram-AutoAnimeMv-blue?style=flat&logo=telegram)](https://t.me/+3q1JuBrrPkJkOWJl)

***

 😊This is a tool for **identifying** anime names and episodes + automatic renaming + automatic organization. It is characterized by easy deployment and out-of-the-box usability. It is used to achieve Rss subscription download Emby fully automatic scraping and all-in-one home-style smooth service!

 </div>

* *I rewrote the 1.0 code in version 2.0.0, optimized many places, but there are still 1.0 functions that I have not updated to the 2.0 version, please be patient*

> The tool is updated quickly, and the usage and functions will be updated. It is recommended to come and see more

> 🚀Click the upper left corner to open the directory and choose the part you want to read


# 💡 Feature description
* Lightweight anime video / subtitle renaming + organizing tool, quick deployment and easy to use
>   
    Anime (category)
    ├── Because I'm Afraid of Pain, I'll Make the Defense Specialization Full
    │   ├── Season01
    │   │   ├── S01E01.mp4
    │   │   ├── S01E02.mp4
    │   │   ├── S01E03.mp4
    │   │   └── ...
    │   └── Season02
    │       ├── S02E01.mp4
    │       ├── S02E02.mp4
    │       ├── S02E02.chi.srt
    │       └── ...
    |___ Gods of the world without reason
    |    └── Season01  
    │        ├── S01E01.mp4
    │        ├── S01E01.chs.ass
    │        ├── S01E02.mp4
    │        └── ....
    |
    ......
    
* One-time configuration, use effortlessly
* Support hard link configuration, essential for seed preservation
* Support anime categorization, make everything in order
* Both local batch processing and QB download modes are free to choose
* Quick update, enjoy more new experiences

    ## Features to be updated
    * BgmApi support
    * TMDBApi support
    * Local anime cache
    * Complete anime special support

# 🚀 Quick start
* `AutoAnimeMv.py` is the core processing program. It has two processing methods. The mode switching relies on passing parameters [Click here to jump to`AutoAnimeMv.py` and click the upper right corner to start downloading](https://github.com/Abcuders/AutoAnimeMv/blob/main/AutoAnimeMv.py)
    ## QB download mode
    > In this mode, `AutoAnimeMv.py` supports three to four parameters, download path, download file name, number of files downloaded, and file classification (optional)

    * 1. Upload `AutoAnimeMv.py` to a path accessible by `🔵QBittorrent`

    * 2. Create an `Anime` category in `🔵Qbittorrent` (not necessary, of course, you can also not categorize)

    * 3. Modify the qb configuration: Download `switch` Torrent Content Layout `as` Do Not Create Subfolders

    * 4. Modify the qb configuration: Download `check` Torrent Run External Program When Complete, fill in below (the order of incoming parameters cannot be changed, and parameters must be wrapped in `""`)

    python3 AutoAnimeMv.py placement path "download path" "download file name" "number of downloaded files" "file classification (optional)"

    The above three parameters can be passed in by `🔵Qbittorrent`, that is,
    ```
    python3 AutoAnimeMv.py placement path "%D" "%N" "%C" "%L"(optional)
    ```
    > <img src="./Image/Example/two.jpg" width="400" height="300"> <img src="./Image/Example/three.jpg" width="400" height="300">
    * 4. Cancel seeding, modify the qb configuration: Change the `seed limitation` of `🔵QBitTorrent` to pause the torrent when the sharing ratio reaches 0 and seeding time reaches 0 minutes


    ## Batch processing mode
    > In this mode, `AutoAnimeMv.py` supports one to two parameters, the path where the anime to be organized is located, and the file classification (optional)

    * The order of incoming parameters cannot be changed, and the parameters must be wrapped in `""`
    ```
    python3 AutoAnimeMv.py "Path where anime to be organized is located" "File classification (optional)"
    ```

    ## Update Mode
    * Use `updata`/update`to update`AutoAnimeMv.py
    ```
    python3 AutoAnimeMv.py updata
    ```
# Detailed documentation
* [Click here for detailed documents (actually 1.0 documents, as mentioned above, there are some differences between 1.0 and 2.0, I will update the detailed documents of 2.0 as soon as possible)](./Backups/1.20.1/README.md)

# Related groups
* Exchange / Work Group: [Telegram](https://t.me/+3q1JuBrrPkJkOWJl)

# ⭐️ Contributors ✨

Thanks to these interesting and great people! ! !
> If you also want to contribute to this project, you can directly come to [Issues](https://github.com/Abcuders/AutoAnimeMv/issues) to put forward your valuable suggestions or @ me to ask what can be done

<a href="https://github.com/wzfdgh">
<img src="https://avatars.githubusercontent.com/u/93830081?s=96&v=4"  width="60px" height="60px"> 
</a>
<a href="https://github.com/Nanako718">
<img src="https://avatars.githubusercontent.com/u/60038246?s=96&v=4"  width="60px" height="60px">
</a>

# Star History
[![Star History Chart](https://api.star-history.com/svg?repos=Abcuders/AutoAnimeMv&type=Date)](https://star-history.com/#Abcuders/AutoAnimeMv)