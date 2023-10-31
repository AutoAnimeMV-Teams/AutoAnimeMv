# 目录
+ [常见问题](/DOCS.md/##常见问题)
    - pip安装出现问题
    - 群晖NAS使用Python出现奇怪的问题


# 常见问题


## 1）pip安装出现问题
*   如果您直接使用pip进行install遇到 `❗Fatal error in launcher: Unable to create process using pip问题`
请使用`python3 -m pip install` 尝试安装

## 2）群晖NAS使用Python出现奇怪的问题
* 在群晖NAS中，套件中心安装的`🐍python3`环境可能出现奇奇怪怪的问题，请使用第三方套件源(第三方源需要手动为`🐍python3`创建软连接至/usr/local/bin/python3)

## 3）下载完后出现权限错误
* 如果是您手动创建的目录后出现此问题，请删除目录让脚本自动创建