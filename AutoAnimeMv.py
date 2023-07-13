#!/usr/bin/python3
#coding:utf-8
from sys import argv,executable #获取外部传参和外置配置更新
from os import environ,path,name,getcwd,makedirs,listdir,link,remove,system # os操作
from time import sleep,strftime,localtime,time # 时间相关
from datetime import datetime # 时间相减用
from re import findall,match,search,sub,I # 匹配相关
from shutil import move # 移动File
from ast import literal_eval # srt转化
from zhconv import convert # 繁化简
from urllib.parse import quote,unquote # url encode
from requests import get,post,exceptions # 网络部分
from random import randint # 随机数生成
from threading import Thread # 多线程
#Start 开始部分进行程序的初始化 

def Start_PATH():# 初始化
    # 版本 数据库缓存 Api数据缓存 Log数据集 分隔符
    global Versions,AimeListCache,BgmAPIDataCache,LogData,Separator,Proxy,TgBotMsgData,PyPath
    Versions = '2.4.2'
    AimeListCache = None
    BgmAPIDataCache = {}
    LogData = f'\n\n[{strftime("%Y-%m-%d %H:%M:%S",localtime(time()))}] INFO: Running....'
    Separator = '\\' if name == 'nt' else '/'
    TgBotMsgData = ''
    #PyPath = argv[0].replace('AutoAnimeMv.py','').strip(' ')
    PyPath = getcwd()
    Auxiliary_READConfig()
    Auxiliary_Log((f'当前工具版本为{Versions}',f'当前操作系统识别码为{name},posix/nt/java对应linux/windows/java虚拟机'),'INFO')

def Start_GetArgv():# 获取参数,判断处理模式
    ArgvNumber = len(argv)
    Auxiliary_Log(f'接受到的参数 > {argv}',)
    if 2 <= ArgvNumber <= 3:# 接受1-2个参数
        if argv[1] == ('update' or 'updata'):# 更新模式
            Auxiliary_Updata()
        elif path.exists(argv[1]) == True:# 批处理模式
            if ArgvNumber == 2:
                return argv[1], #待扫描目录
            else:
                return argv[1],argv[2] #待扫描目录和文件分类
        else:
            Auxiliary_Exit('参数出错')
    elif 4 <= ArgvNumber <= 5: #接受3-4参数
            if path.exists(argv[1]) == True:
                if ArgvNumber == 4: # 保存目录 种子名称 文件个数
                    return argv[1],argv[2],argv[3]
                else:# + 文件分类
                    return argv[1],argv[2],argv[3],argv[4]

# Processing 进行程序的开始工作,进行核心处理
def Processing_Mode(ArgvData:list):# 模式选择
    ArgvNumber = len(ArgvData)
    global Path
    Path = ArgvData[0]
    if path.exists(Path) == True:
        # 批处理模式(非分类|分类) or Qb下载模式
        FileListTuporList = Auxiliary_ScanDIR(Path) if ArgvNumber <= 2 or (ArgvData[2] != '1') else [ArgvData[1]]
        Auxiliary_DeleteLogs()
        global CategoryName
        CategoryName = ''
        if ArgvNumber == 2:# 分类识别
            CategoryName = ArgvData[1]
        elif ArgvNumber == 4:
            CategoryName = ArgvData[3]

        if CategoryName != '':
            Auxiliary_Log(f'当前分类 >> {CategoryName}')

        if type(FileListTuporList) == tuple:
            return FileListTuporList # 文件列表元组(视频文件列表,字幕文件列表)
        else:
            for i in FileListTuporList:
                if path.isfile(f'{Path}{Separator}{i}') == False:
                    Auxiliary_Log(f'{Path}{Separator}{i} 不存在的文件','WARNING')
                    FileListTuporList.remove(i)
            if FileListTuporList != []:
                return FileListTuporList  # 元组中唯一有效的文件列表
            Auxiliary_Exit('没有有效的番剧文件')
    else:
        Auxiliary_Exit(f'不存在{Path}目录')
   
def Processing_Main(LorT):# 核心处理
    if type(LorT) == tuple: # (视频文件列表,字幕文件列表)
        for File in LorT[0]:
                flag = Processing_Identification(File)
                if flag == None:
                    break
                SE,EP,RAWSE,RAWEP,RAWName = flag
                ASSList = Auxiliary_IDEASS(RAWName,RAWSE,RAWEP,LorT[1])
                BgmApiName = Auxiliary_BgmApi(RAWName)
                Sorting_Mv(File,RAWName,SE,EP,ASSList,BgmApiName)
    else:# 唯一有效的文件列表
        for File in LorT:
            flag = Processing_Identification(File)
            if flag == None:
                break
            SE,EP,RAWSE,RAWEP,RAWName = flag
            BgmApiName = Auxiliary_BgmApi(RAWName)
            Sorting_Mv(File,RAWName,SE,EP,None,BgmApiName)

def Processing_Identification(File:str):# 识别
    AnimeFileCheckFlag = Auxiliary_AnimeFileCheck(File)
    if AnimeFileCheckFlag == True:
        Auxiliary_Log('-'*80,'INFO')
        NewFile = Auxiliary_RMSubtitlingTeam(Auxiliary_RMOTSTR(Auxiliary_UniformOTSTR(File)))# 字符的统一加剔除
        RAWEP = Auxiliary_IDEEP(NewFile)
        Auxiliary_Log(f'匹配出的剧集 ==> {RAWEP}','INFO')
        RAWName = Auxiliary_IDEVDName(NewFile,RAWEP)
        EP = '0' + RAWEP if len(RAWEP) < 2 or ( '.' in RAWEP and RAWEP[0] != '0') else RAWEP# 美化剧集
        if '.' in RAWEP or RAWEP == '0' or RAWEP == '00':
            SE = '00'
            RAWSE = ''
            SeasonMatchData = r'(季(.*?)第)|(([0-9]{0,1}[0-9]{1})S)|(([0-9]{0,1}[0-9]{1})nosaeS)|(([0-9]{0,1}[0-9]{1}) nosaeS)|(([0-9]{0,1}[0-9]{1})-nosaeS)|(nosaeS-dn([0-9]{1}))'
            RAWName = sub(SeasonMatchData,'',RAWName[::-1],flags=I)[::-1].strip('-')
        else:
            SE,Name,RAWSE = Auxiliary_IDESE(RAWName)
            RAWName = RAWName if Name == None else Name
            SE = '0' + SE if len(SE) == 1 else SE
        return SE,EP,RAWSE,RAWEP,RAWName
    else:
        Auxiliary_Log(f'当前文件属于{AnimeFileCheckFlag},跳过处理','INFO')

# Sorting 进行整理工作
def Sorting_Mv(FileName,RAWName,SE,EP,ASSList,BgmApiName):# 文件处理
    def FileML(src,dst):
        global TgBotMsgData
        if USELINK == True:
            try:
                link(src,dst)
                Auxiliary_Log(f'Link-{dst} << {src}','INFO')
                TgBotMsgData = TgBotMsgData + (f'Link-{src} << {dst}\n')
            except OSError as err:
                if '[WinError 1]' in str(err):
                    Auxiliary_Log('当前文件系统不支持硬链接','ERROR')
                    if LINKFAILSUSEMOVEFLAGS == True:
                        move(src,dst)
                        Auxiliary_Log(f'Move-{src} << {dst}')
                        TgBotMsgData= TgBotMsgData + (f'Move-{src} << {dst}\n')
                else:
                    Auxiliary_Exit(err)
        else:
            move(src,dst)
            Auxiliary_Log(f'Move-{dst} << {src}')
            TgBotMsgData = TgBotMsgData + (f'Move-{src} << {dst}\n')
    NewDir = f'{Path}{Separator}{CategoryName}{Separator}{BgmApiName}{Separator}Season{SE}{Separator}' if BgmApiName != None else f'{Path}{Separator}{CategoryName}{Separator}{RAWName}{Separator}Season{SE}{Separator}'
    NewName = f'S{SE}E{EP}'
    if path.exists(NewDir) == False:
        makedirs(NewDir)
    else:
        Auxiliary_Log(f'{NewDir}已存在','INFO')
    if ASSList != None:
        for ASSFile in ASSList:
            FileType = path.splitext(ASSFile)[1].lower()
            NewASSName = NewName + Auxiliary_ASSFileCA(ASSFile)
            if path.isfile(f'{NewDir}{NewASSName}{FileType}') == False:
                FileML(f'{Path}{Separator}{FileName}',f'{NewDir}{NewASSName}{FileType}')
            else:
                Auxiliary_Log(f'{NewDir}{NewASSName}{FileType}已存在,故跳过','WARNING')
    FileType = path.splitext(FileName)[1].lower()
    if path.isfile(f'{NewDir}{NewName}{FileType}') == False:
        NewName = NewName + Auxiliary_ASSFileCA(FileName) if FileType == ('.ass' or '.str') else NewName
        FileML(f'{Path}{Separator}{FileName}',f'{NewDir}{NewName}{FileType}')
    else: 
        Auxiliary_Log(f'{NewDir}{NewName}{FileType}已存在,故跳过','WARNING')

# Auxiliary 其他辅助
def Auxiliary_Notice(Msg):# 共享内存
    if 'USERTGBOT' in globals():
        global USERTGBOT
        if USERTGBOT == True:
            if 'USERBOTNOTICE' in globals():
                global USERBOTNOTICE
                if USERBOTNOTICE == True: 
                    from mmap import mmap,ACCESS_WRITE
                    from contextlib import closing
                    with open(f'{PyPath}{Separator}CS.dat', 'r+') as f:
                        with closing(mmap(f.fileno(), 1024, access=ACCESS_WRITE)) as m:
                            m.seek(0)
                            Msg.rjust(1024,'\x00')
                            m.write(bytearray(Msg.encode()))
                            Auxiliary_Log('Notice消息已发送')
                            m.flush()

def Auxiliary_READConfig():# 读取外置Config.ini文件并更新
    global HTTPPROXY,HTTPSPROXY,ALLPROXY,USEBGMAPI,USELINK,LINKFAILSUSEMOVEFLAGS,PRINTLOGFLAG,RMLOGSFLAG,USEBOTFLAG,TGBOTTOKEN,BOTUSERIDLIST
    HTTPPROXY = '' # Http代理
    HTTPSPROXY = '' # Https代理
    ALLPROXY = '' # 全部代理
    USEBGMAPI = True # 使用BgmApi
    USELINK = False # 使用硬链接开关
    LINKFAILSUSEMOVEFLAGS = False #硬链接失败时使用MOVE
    PRINTLOGFLAG = False # 打印log开关
    RMLOGSFLAG = '7' # 日志文件超时删除
    USEBOTFLAG = True # 使用TgBot进行通知
    TGBOTTOKEN = '' # TgBot Token
    BOTUSERIDLIST = [] # 使用TgBot的用户列表
    if path.isfile(f'{PyPath}{Separator}config.ini'):
        with open(f'{PyPath}{Separator}config.ini','r',encoding='UTF-8') as ff:
            Auxiliary_Log('正在读取外置ini文件','INFO')
            T = 0
            COEFLAG = False
            for i in ff.readlines():
                i = i.strip('\n') 
                if i[0] != '#' and i != '':
                    ii = i.split("=",1)[0].strip('- ')
                    Auxiliary_Log(f'配置 < {i}','INFO')
                    exec(f'global {ii};{i}')
                    T = T + 1
                elif i == '#mtf' or i == '#ftm':
                    COEFLAG = True
            if T == 0:
                Auxiliary_Log('外置ini文件没有配置','WARNING')
            elif COEFLAG == True:
                COE()
            Auxiliary_PROXY()

def Auxiliary_Log(Msg,MsgFlag='INFO',flag=None,end='\n'):# 日志
    global LogData,PRINTLOGFLAG
    Msg = Msg if type(Msg) == tuple else (Msg,)
    for OneMsg in Msg:
        Msg = f'[{strftime("%Y-%m-%d %H:%M:%S",localtime(time()))}] {MsgFlag}: {OneMsg}'
        if PRINTLOGFLAG == True or flag == 'PRINT':
            print(Msg,end=end)         
        LogData = LogData + '\n' + Msg

def Auxiliary_DeleteLogs():# 日志清理
    RmLogsList = []
    if RMLOGSFLAG != False and 'LogsFileList' in globals() and LogsFileList != []:
        ToDay = datetime.strptime(datetime.now().strftime('%Y-%m-%d'),"%Y-%m-%d").date()
        for Logs in LogsFileList:
            LogDate =  datetime.strptime(Logs.strip('.log'),"%Y-%m-%d").date()
            if (ToDay - LogDate).days >= int(RMLOGSFLAG):
                remove(f'{Path}{Separator}{Logs}')
                RmLogsList.append(Logs)
        if RmLogsList != []:
            Auxiliary_Log(f'清理了保存时间达到和超过{RMLOGSFLAG}天的日志文件 << {RmLogsList}')


def Auxiliary_WriteLog():# 写log文件
    LogPath = argv[1] if path.exists(argv[1]) == True else PyPath
    if LogPath == PyPath:
        Auxiliary_Log(f'Log文件保存在工具目录下','WARNING')
    with open(f'{LogPath}{Separator}{strftime("%Y-%m-%d",localtime(time()))}.log','a+',encoding='UTF-8') as LogFile:
        LogFile.write(LogData)

def Auxiliary_UniformOTSTR(File):# 统一意外字符
    NewFile = convert(File,'zh-hans')# 繁化简
    NewUSTRFile = sub(r',|，| ','-',NewFile,flags=I) 
    NewUSTRFile = sub('[^a-z0-9\s&/\-:：.\(\)（）《》\u4e00-\u9fa5\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF]','=',NewUSTRFile,flags=I)
    #异种剧集统一
    OtEpisodesMatchData = ['第(\d{1,4})集','(\d{1,4})集','(\d{1,4})END','(\d{1,4}) END','(\d{1,4})E']
    for i in OtEpisodesMatchData:
        if search(i,NewUSTRFile,flags=I) != None:
            a = search(i,NewUSTRFile,flags=I)
            NewUSTRFile = NewUSTRFile.replace(a.group(),a.group(1).strip('\u4e00-\u9fa5'))
    return NewUSTRFile

def Auxiliary_RMOTSTR(File):# 剔除意外字符
    #匹配待去除列表
    FuzzyMatchData = [r'=.?月新番.?=',r'\d{4}.\d{2}.\d{2}',r'20\d{2}',r'v\d{1}',r'\d{4}年\d{1,2}月番']
    #精准待去除列表
    PreciseMatchData = ['仅限港澳台地区','国漫','x264','1080p','720p','4k','\(-\)','（-）']
    for i in PreciseMatchData:
        NewPSTRFile = sub(r'%s'%i,'-',File,flags=I)
    for i in FuzzyMatchData:
        NewPSTRFile = sub(i,'-',NewPSTRFile,flags=I)
    return NewPSTRFile

def Auxiliary_IDESE(File):# 识别剧季并截断Name
    SeasonMatchData = r'(季(.*?)第)|(([0-9]{0,1}[0-9]{1})S)|(([0-9]{0,1}[0-9]{1})nosaeS)|(([0-9]{0,1}[0-9]{1}) nosaeS)|(([0-9]{0,1}[0-9]{1})-nosaeS)|(nosaeS-dn([0-9]{1}))'
    if search(SeasonMatchData,File[::-1],flags=I) != None:
        SEData = findall(SeasonMatchData,File[::-1],flags=I)
        SENamelist = []
        SEList = []
        for sedata in SEData:
            for se in sedata:# 取值
                if se != '' and len(se) != 1:
                    SENamelist.append(se)
                elif len(se) == 1:
                    SEList.append(se)
        for i in SENamelist:# 截断Name
            File = sub(r'%s.*'%i[::-1],'',File,flags=I).strip('-') #通过剧季截断文件名
        for i in range(len(SEList)):
            if SEList[i].isdecimal() == True:
                SE = SEList[i]
            elif '\u0e00' <= SEList[i] <= '\u9fa5':# 中文剧季转化
                digit = {'一':'01', '二':'02', '三':'03', '四':'04', '五':'05', '六':'06', '七':'07', '八':'08', '九':'09','壹':'01','贰':'02','叁':'03','肆':'04','伍':'05','陆':'06','柒':'07','捌':'08','玖':'09'}
                SE = digit[SEList[i]]
            return SE,File,SENamelist[0]
    else:
        return '01',File,''

def Auxiliary_IDEEP(File):# 识别剧集
    try:
        if findall(r'[^0-9a-z.\u4e00-\u9fa5\u0800-\u4e00](\d{1}\.[0-9]{1,4})[^0-9a-uw-z.\u4e00-\u9fa5\u0800-\u4e00]',File[::-1],flags=I) != []:
            Episodes = findall(r'[^0-9a-z.\u4e00-\u9fa5\u0800-\u4e00](\d{1}\.[0-9]{1,4})[^0-9a-uw-z.\u4e00-\u9fa5\u0800-\u4e00]',File[::-1],flags=I)[0][::-1].strip(" =-_eEv")
        else:
            Episodes = findall(r'[^0-9a-z.\u4e00-\u9fa5\u0800-\u4e00][0-9]{1,4}[^0-9a-uw-z.\u4e00-\u9fa5\u0800-\u4e00]',File[::-1],flags=I)[0][::-1].strip(" =-_eEv")
    except IndexError:
        Auxiliary_Exit('未匹配出剧集,请检查(程序目前不支持电影动漫)')
    else:
        #Auxiliary_Log(f'匹配出的剧集 ==> {Episodes}','INFO')
        return Episodes

def Auxiliary_RMSubtitlingTeam(File):# 剔除字幕组信息
    File = File.strip('-')
    if File[0] == '《':# 判断有无字幕组信息
        ile = sub(r'《|》','',File,flags=I) 
    else:
        File = sub(r'^=.*?=','',File,flags=I)
    return File

def Auxiliary_IDEVDName(File,RAWEP):# 识别剧名
    VDName = sub(r'%s.*'%RAWEP,'',File,flags=I).strip('=-=-')
    Auxiliary_Log(f'通过剧集截断文件名 ==> {VDName}','INFO')
    return VDName

def Auxiliary_IDEASS(File,SE,EP,ASSList):# 识别当前番剧视频的所属字幕文件
    ASSFileList = []
    for ASSFile in ASSList:
        ASSName = Auxiliary_UniformOTSTR(ASSFile)
        ASSEP = Auxiliary_IDEEP(ASSName)
        if File in ASSName and EP == ASSEP and SE in ASSName:
            ASSFileList.append(ASSFile)
    ASSFileList = None if ASSFileList == [] else ASSFileList
    return ASSFileList

def Auxiliary_ScanDIR(Dir):# 扫描文件目录,返回文件列表
    global LogsFileList
    SuffixList = ['.ass','.srt','.mp4','mkv','.log']
    AssFileList = []
    VDFileList = []
    LogsFileList = []
    for File in listdir(Dir):# 扫描目录,并按文件类型分类
        if search(r'S\d{1,2}E\d{1,4}',File,flags=I) == None:
            for ii in SuffixList:
                if match(ii[::-1],File[::-1],flags=I) != None:
                    if ii == '.ass' or ii == '.srt':
                        AssFileList.append(File)
                    elif ii == '.log':
                        LogsFileList.append(File)
                    else:
                        VDFileList.append(File)
    if  VDFileList != []:# 判断模式,处理字幕还是视频
        if AssFileList != []:
            Auxiliary_Log((f'发现{len(AssFileList)}个字幕文件 ==> {AssFileList}',f'发现{len(VDFileList)}个视频文件 ==> {VDFileList}'),'INFO')
            return VDFileList,AssFileList
        else:
            Auxiliary_Log(f'发现{len(VDFileList)}个视频文件,没有发现字幕文件, ==> {VDFileList}','INFO')
            return VDFileList
    elif AssFileList != []:
        Auxiliary_Log((f'没有发现任何番剧视频文件,但发现{len(AssFileList)}个字幕文件 ==> {AssFileList}','只有字幕文件需要处理'),'INFO')
        return AssFileList
    else:
        Auxiliary_Exit('没有任何番剧文件')

def Auxiliary_AnimeFileCheck(File):# 检查番剧文件
    list = ['OP','CM','SP','PV']
    for i in list:
        if search(i,File,flags=I) != None:
            return i
    return True         

def Auxiliary_ASSFileCA(ASSFile):# 字幕文件的语言分类
    SubtitleList = [['简','sc','chs'],['繁','tc','chi']]
    for i in range(len(SubtitleList)):
        for ii in SubtitleList[i]:
            if search(ii[::-1],ASSFile[::-1],flags=I) != None:
                if i == 0:
                    return '.chs'
                elif i == 1:
                    return '.chi'
            else:
                return '.other'
def Auxiliary_PROXY(): # 代理
    if 'HTTPPROXY' in globals():
        global HTTPPROXY
        environ['http_proxy'] = HTTPPROXY
    if 'HTTPSPROXY' in globals():
        global HTTPSPROXY
        environ['https_proxy'] = HTTPSPROXY
    if 'ALLPROXY' in globals():
        global ALLPROXY
        environ['all_proxy'] = ALLPROXY

def Auxiliary_Http(Url,flag='GET',json=None):# 网络
    headers = {'User-Agent':f'Abcuders/AutoAnimeMv/{Versions}(https://github.com/Abcuders/AutoAnimeMv)'}
    try:
        if flag != 'GET':
            HttpData = post(Url,json,headers=headers) 
        else:
            HttpData = get(Url,headers=headers)
    except exceptions.ConnectionError:
        Auxiliary_Exit(f'访问 {Url} 失败,未能获取到内容,请检查您是否启用了系统代理,如是则您应该在此工具中配置代理信息,否则您则需要检查您的网络能否访问')
    except Exception as err:
        Auxiliary_Exit(f'访问 {Url} 失败,未能获取到内容,请检查您的网络 {err}')
    if HttpData.status_code == 200:
        return HttpData.text
    else:
        Auxiliary_Exit('HttpData Status Code != 200')

def Auxiliary_Updata():# 更新
    Updata = Auxiliary_Http('https://raw.githubusercontent.com/Abcuders/AutoAnimeMv/main/AutoAnimeMv.py')
    if search(r"Versions = '(\d{1}.\d{1,4}.\d{1,4})'",Updata,flags=I) != None:
        if Versions != search(r"Versions = '(\d{1}.\d{1,4}.\d{1,4})'",Updata,flags=I).group(1):
            with open('AutoAnimeMv.py','w+',encoding='UTF-8') as UpdataFile:
                UpdataFile.write(Updata)
                Auxiliary_Exit('更新完成')
        else:
            Auxiliary_Exit('当前即是最新版本')
    else:
        Auxiliary_Exit('更新数据存在问题')

def Auxiliary_BgmApi(Name):# BgmApi相关,返回一个标准的中文名称
    global USEBGMAPI
    if USEBGMAPI == True:
        def NameSplit(Name):
            if findall(r'[\u4e00-\u9fa5]+',Name,flags=I) != []: # 获取匹配到的汉字
                NameList = findall(r'[\u4e00-\u9fa5]+',Name,flags=I) 
            else:# 匹配其他语言
                NameList = Name.split('-')
                for i in range(NameList.count('')):
                    NameList.remove('')
            Auxiliary_Log(f'番剧名称分段 待查询的番剧名称列表 >> {NameList}')
            return NameList
        
        NameList = [Name]
        i = 0
        while True:
            for Name in NameList:
                try:
                    BgmApiData = literal_eval(Auxiliary_Http(f"https://api.bgm.tv/search/subject/{Name}?type=2&responseGroup=small&max_results=1"))
                except:
                    Auxiliary_Log(f'BgmApi无法检索到关于 {Name} 内容','WARNING')
                    if i == 0:
                        NameList = NameSplit(Name)
                        i = 1
                else:
                    break
            break

        if 'BgmApiData' in locals():
            ApiName = unquote(BgmApiData['list'][0]['name_cn'],encoding='UTF-8',errors='replace')
            ApiName = sub('第\d{1,2}季','',ApiName,flags=I).strip('- []【】 ')
            Auxiliary_Log(f'{ApiName} << bgmApi查询结果')
            return ApiName
        else:
            return None
    else:
        Auxiliary_Log('没有使用BgmApi进行检索')
        return None

def Auxiliary_Exit(LogMsg):# 因可预见错误离场
    Auxiliary_Log(LogMsg,'EXIT',flag='PRINT')
    exit()
# Colored Eggs
def COE():#
    Auxiliary_Log('你的存在千真万确毋需置疑,我们一直都在这里,我们一直会爱你,愿每一个人都能自由的生活在阳光下','AAM')

if __name__ == '__main__':
    start = time()
    try:
        Start_PATH()
        ArgvData = Start_GetArgv()
        Processing_Main(Processing_Mode(ArgvData))
    except Exception as err:
        Auxiliary_Log(f'没有预料到的错误 > {err}','ERROR')
    else:
        end = time()
        Auxiliary_Log(f'一切工作已经完成,用时{end - start}','INFO',flag='PRINT')
        Auxiliary_Notice('新的番剧已处理完成')
    finally:
        Auxiliary_WriteLog()