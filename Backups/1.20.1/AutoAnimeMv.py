#!/usr/bin/python3
#coding:utf-8
from sys import argv,executable
from os import path,name,makedirs,listdir,getcwd,chdir,link
from time import sleep,strftime,localtime,time
from re import findall,match,search,sub,I
from shutil import move
from ast import literal_eval
from zhconv import convert


#config
OPDETAILEDLOGFLAGS = True #详细日志输出开关
WINTOASTFLAGS = False #win弹窗通知开关 
USEFILELINKFLAGS = True #不使用MOVE改为使用硬链接进行番剧的整理(保种使用)
LINKFAILSUSEMOVEFLAGS = False #硬链接失败时使用MOVE
AUTOUPDATEFLAGS = True #自动更新开关
UPDATEURLPATH = 'https://raw.githubusercontent.com/Abcuders/AutoAnimeMv/main/' #UPDATEURL
NOUPDATELIST = '' #不更新列表
SKIPCHECKBEFOREUPDATEFLAGS = False #跳过自动解决更新前检查到的问题(更新覆盖内置自定义配置)
USEGITHUBANIMELISTFLAG = False #使用Github上的AnimeList文件
USELOCALANIMELISTFLAGS = False #使用本地的AnimeList文件
USINGPROXYFLAGS = True #使用代理开关,如果您的代理服务器需要认证,请使用 账号:密码@ip:port 这样的格式
HTTPPROXY = 'http://127.0.0.1:7890' #Http代理,请根据您的实际情况填写  
HTTPSPROXY = 'http://192.168.1.112:7890' #Https代理,请根据您的实际情况填写
SOCKS5PROXY = '' #SOCKS5代理,请根据您的实际情况填写
USEBGMAPIFLAGS = True #使用BgmApi进行更准确的识别
FORCEDUSEBGMAPI = False #强制使用BgmApi进行识别,不查询AimeList文件
BGMAPIURLPATH = 'https://api.bgm.tv/' #BGMAPIURL


def WinTaoast(title,msg):
    a = ToastNotifier().show_toast(title, msg,duration=5,threaded=True)   

def CheckAnimeSeason(Ep,Eplist):
    if Ep < min(Eplist):
        Log('WARNING: 当前番剧剧季存在问题,尝试矫正')
        if int(min(Eplist))-int(Ep) <= 12:
            return -1
        elif int(min(Eplist))-int(Ep) < 23:
            return -2
    elif Ep > max(Eplist):
        Log('WARNING: 当前番剧剧季存在问题,尝试矫正')
        if int(Ep)-int(min(Eplist)) <= 12:
            return +1
        elif int(Ep)-int(min(Eplist)) < 23:
            return +2
    else:
        for i in Eplist:
            if Ep == i:
                return 0

def CheckAnimeOthe(FileName):
    list = ['OP','CM','SP','PV']
    for i in list:
        if search(i,FileName,flags=I) != None:
            return i
    return True

def VDFileMatch(FileList):
    SuffixList = ['.ass','.srt','.mp4','mkv']
    ChAssFileList = []
    VdFileList = []
    for File in FileList:
        if search(r'S\d{1,2}E\d{1,4}',File,flags=I) == None:
            for ii in SuffixList:
                if match(ii[::-1],File[::-1],flags=I) != None:
                    if ii == '.ass' or ii == '.srt':
                        ChAssFileList.append(File)
                    else:
                        VdFileList.append(File)
    if  VdFileList != []:
        if ChAssFileList != []:
            Log(f'INFO: 发现{len(ChAssFileList)}个字幕文件 ==> {ChAssFileList}',FLAGS='PRINT')
            return VdFileList,ChAssFileList
        else:
            return VdFileList,None
    elif ChAssFileList != []:
        Log(f'INFO: 没有发现任何番剧视频文件,但发现{len(ChAssFileList)}个字幕文件 ==> {ChAssFileList}',FLAGS='PRINT')
        return None,ChAssFileList
    else:
        Log('ERROR: 没有任何番剧文件...EXIT')
        exit()

def AttributesMatch(VideoName,Flag=None):
    Season = '01' #定义初始剧季和剧集为1
    Episodes = '01'
    RAWVideoName = VideoName
    #匹配待去除
    FuzzyMatchData = [r'=.?月新番.?=',r'\d{4}.\d{2}.\d{2}',r'20\d{2}',r'v\d{1}',r'\d{4}年\d{1,2}月番']
    #精准待去除
    PreciseMatchData = ['仅限港澳台地区','僅限港澳台地區','日語原聲','国漫','TVアニメ','x264','1080p','720p','4k','\(-\)','（-）']
    OtEpisodesMatchData = ['第(\d{1,4})集','(\d{1,4})集']
    FileType = path.splitext(VideoName)[1]
    #FileType = search(r'(.*?\.)',VideoName[::-1],flags=I).group()[::-1] #匹配视频文件格式
    #统一意外字符
    Log('-'*100)
    VideoName = sub(r',|，| ','-',VideoName,flags=I) 
    VideoName = sub('[^a-z0-9\s&/\-:：.\(\)（）《》\u4e00-\u9fa5\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF]','=',VideoName,flags=I)
    #异种剧集统一
    for i in OtEpisodesMatchData:
        if search(i,VideoName,flags=I) != None:
            a = search(i,VideoName,flags=I)
            VideoName = VideoName.replace(a.group(),a.group(1).strip('\u4e00-\u9fa5'))
    #开始去除其他字符
    for i in PreciseMatchData:
        VideoName = sub(r'%s'%i,'-',VideoName,flags=I)
    for i in FuzzyMatchData:
        VideoName = sub(i,'-',VideoName,flags=I)
    #匹配剧集
    try:
        if findall(r'[^0-9a-z.\u4e00-\u9fa5\u0800-\u4e00](\d{1}\.[0-9]{1,4})[^0-9a-uw-z.\u4e00-\u9fa5\u0800-\u4e00]',VideoName[::-1],flags=I) != []:
            Episodes = findall(r'[^0-9a-z.\u4e00-\u9fa5\u0800-\u4e00](\d{1}\.[0-9]{1,4})[^0-9a-uw-z.\u4e00-\u9fa5\u0800-\u4e00]',VideoName[::-1],flags=I)[0][::-1].strip(" =-_eEv")
        else:
            Episodes = findall(r'[^0-9a-z.\u4e00-\u9fa5\u0800-\u4e00][0-9]{1,4}[^0-9a-uw-z.\u4e00-\u9fa5\u0800-\u4e00]',VideoName[::-1],flags=I)[0][::-1].strip(" =-_eEv")
        VideoName = VideoName.strip('-')
        if VideoName[0] == '《':#判断有无字幕组
            VideoName = sub(r'《|》','',VideoName,flags=I) 
        else:
            VideoName = sub(r'^=.*?=','',VideoName,flags=I)
    except IndexError:
        Log('ERROR: 未匹配出剧集,请检查(程序目前不支持电影动漫)...EXIT',FLAGS='PRINT')
        #Log('WARNING: 未匹配出剧集,可能是电影番剧',FLAGS='PRINT')
        exit()
        #if search(r'ED',VideoName,flags=I) != None :
        #    TrueVideoName = sub(r'ED.*','',VideoName,flags=I)
    else:        
        RAWEpisodes = Episodes
        #Episodes = f"0{Episodes}" if len(Episodes) == 1 and Episodes != 0 else Episodes
        #Episodes = f"0{Episodes}" if '.' in Episodes and Episodes[0] != '0' else Episodes
        #if ('.' in Episodes and len(Episodes)>3 and Episodes[0] == 0):
        #        Episodes = Episodes.lstrip('0')
        #elif Episodes[0] == Episodes[1] == '0':
        #    Episodes = '0'
        Log(f"INFO: 匹配剧集 ==> {Episodes}")
        #通过剧集截断文件名
        VideoName = sub(r'%s.*'%RAWEpisodes,'',VideoName,flags=I)
        Log(f"INFO: 通过剧集截断文件名 ==> {VideoName}")
        VideoName = convert(VideoName.replace('=','').replace(' ','').strip('-'),'zh-hans')
        Log(f"INFO: 番剧Name ==> {VideoName}")
        #匹配剧季
        EpList = None
        ApiVideoName = None 
        if USEBGMAPIFLAGS == True and (Flag != 'ANIMELIST' or FORCEDUSEBGMAPI == True):
                if findall('[\d\u4e00-\u9fa5\d]+',VideoName) != []:
                    #print(findall('啊啊啊,好累呀',TrueVideoName))
                    data = findall('[\d\u4e00-\u9fa5\d]+',VideoName)
                    VideoName = data[0]
               
                global BgmAPIDateCache
                if VideoName in BgmAPIDateCache:
                    ApiVideoName,AnimeId,EpList = BgmAPIDateCache[VideoName][0:3]
                else:
                    ApiVideoName,AnimeId,EpList = ProcessingBgmAPIDate(VideoName)
                    if ApiVideoName != None:
                        BgmAPIDateCache[VideoName] = [ApiVideoName,AnimeId,EpList]
                if Season == '00':
                    SP = ProcessingBgmAPIDate(AnimeID=AnimeId,EP=Episodes)[0]
                    Episodes = SP if SP != None else Episodes
        Episodes = f"0{Episodes}" if len(Episodes) == 1 else Episodes
        if '.' in RAWEpisodes or RAWEpisodes == '0':
            Season = '00'
            RAWSeason = None
            #TrueVideoName = VideoName if ApiVideoName == None else ApiVideoName
            Log(f'INFO: id SP TrueVideoName ==> {TrueVideoName},Season ==> 00 ')

            #DEV 这里应该重写Episodes,以支持SP,但这个功能的前提条件我还没有做
        else:
            #VideoName = VideoName if ApiVideoName == None else ApiVideoName
            SeasonMatchData1 = r'[0-9]{0,1}[0-9]{1}S|([0-9]{0,1}[0-9])nosaeS|([0-9]{0,1}[0-9]{1})-nosaeS|nosaeS-dn([0-9]{1})'
            SeasonMatchData2 = r'(季.*?第|[0-9]{0,1}[0-9]{1}S)|([0-9]{0,1}[0-9]{1})nosaeS|([0-9]{0,1}[0-9]{1})-nosaeS|nosaeS-dn([0-9]{1})'
            if ('/' in VideoName) == True: #按'/'进行多语言分类
                VideoName = VideoName.split("/", )
                for i in range(len(VideoName)):
                    if VideoName[i].replace('-','').replace(':','').isalnum() == True: #多语言分类匹配英文Name中的剧季
                        if search(SeasonMatchData1,VideoName[i][::-1],flags=I) != None :
                            Season = search(SeasonMatchData1,VideoName[i][::-1],flags=I).group(0)[::-1]
                            TrueVideoName = sub(r'%s.*'%Season,'',VideoName[i],flags=I).strip('-') #通过剧季截断文件名
                            Season = search(SeasonMatchData1,VideoName[i][::-1],flags=I).group(0)[::-1].strip('SeasonndSSs-')
                            RAWSeason = Season
                            if EpList != None:
                                Season = str(int(Season) + CheckAnimeSeason(RAWEpisodes,EpList))
                            Season = f"0{Season}" if len(Season) == 1 else Season
                            Log(f"INFO: id 1 TrueVideoName ==> {TrueVideoName},Season ==> {Season}")
                            break
                        elif i ==  len(VideoName)-1 :
                            RAWSeason = Season
                            TrueVideoName = VideoName[0]
            elif search(SeasonMatchData2,VideoName[::-1],flags=I) != None :#单语言(中/英)匹配是否存在剧季
                    Season = search(SeasonMatchData2,VideoName[::-1],flags=I).group(0)[::-1]
                    #TrueVideoName = VideoName.strip(Season)
                    TrueVideoName = sub(r'%s.*'%Season,'',VideoName,flags=I) #通过剧季截断文件名
                    Season = search(SeasonMatchData2,VideoName[::-1],flags=I).group(0)[::-1].strip('第季SeasonndSs-')
                    RAWSeason = Season
                    if Season.isdigit() == True :
                        if EpList != None:
                                Season = str(int(Season) + CheckAnimeSeason(RAWEpisodes,EpList))
                        Season = f"0{Season}" if len(Season) == 1 else Season
                        Log(f"INFO: id 2 TrueVideoName ==> {TrueVideoName},Season ==> {Season}")
                    else:#中文剧季转化
                        digit = {'一':'01', '二':'02', '三':'03', '四':'04', '五':'05', '六':'06', '七':'07', '八':'08', '九':'09','壹':'01','贰':'02','叁':'03','肆':'04','伍':'05','陆':'06','柒':'07','捌':'08','玖':'09'}
                        Season = digit[Season]
                        if EpList != None:
                            Season = str(int(Season) + CheckAnimeSeason(RAWEpisodes,EpList))
                            Season = f"0{Season}" if len(Season) == 1 else Season
                        Log(f"INFO: id 3 TrueVideoName ==> {TrueVideoName},Season ==> {Season}")
            else:
                TrueVideoName = VideoName
                RAWSeason = ''
                if EpList != None:
                    Season = str(int(Season) + CheckAnimeSeason(RAWEpisodes,EpList))
                Log(f"INFO: id 4 TrueVideoName ==> {TrueVideoName},Season ==> {Season}")
        TrueVideoName = TrueVideoName.strip('-=_')
        Log(f'INFO: {TrueVideoName} {Season} {Episodes} {FileType} << {RAWVideoName}',FLAGS='PRINT')
        return Season,Episodes,TrueVideoName,ApiVideoName,FileType,RAWSeason,RAWEpisodes

def GetArgv():#接受参数
    Log(f"INFO: 接受到参数 ==> {argv}")
    #筛选分类,您可以根据不同的类型设置不同路径
    #if len(argv) == 2 or len(argv) == 3:
    try:
        if argv[1] == 'update':
            flag = 'PY' if 'python' in executable else  'EXE'
            flag = argv[2] if len(argv) == 3 else flag
            if AUTOUPDATEFLAGS == True:
                Log(f'INFO: 准备更新中-{flag}')
                UpDate(CheckUpdate(flag))
                Log('INFO: 全部已更新完毕')
                exit()
            else:
                Log('ERROR AUTOUPDATEFLAGS = False')
                exit()
    except IndexError:
        Log(f'ERROR 未知的参数 ==> {argv}',FLAGS='PRINT')
        exit()
    if 2 <= len(argv) <=  3:#批处理模式
        SavePath,CategoryName = argv[1],None
        Log(f'INFO: 现在是本地番剧文件批处理模式,正在扫描Path ==> {SavePath}')
        if len(argv) == 3:
            CategoryName = argv[2]
            Log(f'INFO: 分类模式已启用,当前分类 ==> {CategoryName}')
        FileList = listdir(SavePath)
        VDFileNameL,ASSFileN = VDFileMatch(FileList)
        if VDFileNameL == None:
            Log('INFO: 只有字幕文件需要处理')
            return SavePath,VDFileNameL,ASSFileN,CategoryName,'ASS'
        return SavePath,VDFileNameL,ASSFileN,CategoryName,None
    #elif len(argv) == 4 or len(argv) == 5:
    elif 4 <= len(argv) <= 5:#BT
        SavePath,VideoName,CategoryName = argv[1],argv[2],None
        if len(argv) == 5:
            CategoryName = argv[4]
            Log(f'INFO: 分类模式已启用,当前分类 ==> {CategoryName}')
        if argv[3] == '1': #NumberOfFile == 1
            return SavePath,VideoName,None,None,None
        else:
            FileList = listdir(SavePath)
            VDFileList = []
            for i in range(len(FileList)):
                if VideoName in FileList[i] :
                    VDFileList.append(FileList[i])
        if  VDFileList == []:
            Log('ERROR: 根据传入的torrent名称找不到video文件...EXIT',FLAGS='PRINT')
            exit()
        else:
            VDFileName,ASSFileN = VDFileMatch(VDFileList)
            return SavePath,VDFileName,ASSFileN,CategoryName,None
    else:
        Log(f'ERROR 错误的参数 ==> {argv}',FLAGS='PRINT')
        exit()

def AutoMv(SavePath,VideoName,RAWVideoName,Season,Episodes,VideoTrueName,FileType,AssList,CategoryName):#整理+重命名
    def ASSCategory(ASSFileName):
        #flag = 'Other'
        #if '中文' in ASSFileName :
        #    flag = 'chinese'
        #    if '简体' in ASSFileName or '简中' in ASSFileName or '简繁' in ASSFileName or '简' in ASSFileName or search():
        #        flag = 'chs'
        #    elif '繁体' in ASSFileName or '繁中' in ASSFileName or '繁' in ASSFileName:
        #        flag = 'cht'
        #elif '日文' in ASSFileName:
        #    flag = 'jp'
        #return flag
        SubtitleList = [['简','sc'],['繁','tc']]
        for i in range(len(SubtitleList)):
            for ii in SubtitleList[i]:
                if search(ii[::-1],ASSFileName[::-1],flags=I) != None:
                    if i == 0:
                        return 'chs'
                    elif i == 1:
                        return 'chi'
                    else:
                        return 'other'
                    


    def FileMV(FileName,NewVideoDir,FileType,NewFileName,flag):
        if path.isfile(f'{SavePath}{a}{NewVideoDir}{a}{NewFileName}{FileType}') == False:      
            if USEFILELINKFLAGS == True:
                    try:
                        #link(f'{SavePath}{a}{FileName}',f'{SavePath}{a}{NewVideoDir}{a}S{Season}E{Episodes}.Chinese(版本{i+1}){FileType}')
                        link(f'{SavePath}{a}{FileName}',f'{SavePath}{a}{NewVideoDir}{a}{NewFileName}{FileType}')
                    except OSError as err:
                        if '[WinError 1]' in str(err):
                            Log(f'ERROR: 当前文件系统不支持硬链接',FLAGS='PRINT')
                        else:
                            Log(f'ERROR: {err}')
                        if LINKFAILSUSEMOVEFLAGS == True:
                            move(f'{SavePath}{a}{FileName}',f'{SavePath}{a}{NewVideoDir}{a}{NewFileName}{FileType}')
                            log = f'INFO: 硬链接失败,使用MOVE导入字幕文件{FileName}' if flag == 'ASS' else f"INFO: 硬链接失败,使用MOVE创建 {SavePath}{a}{NewVideoDir}{a}{NewFileName}{FileType} 完成...一切已经准备就绪"
                            Log(log,FLAGS='PRINT')
                        else:
                            pass
                    else:
                        log = f'INFO: 字幕文件{FileName}已导入(硬链接)' if flag == 'ASS' else f"INFO: 硬链接: {SavePath}{a}{NewVideoDir}{a}{NewName}{FileType} 完成...一切已经准备就绪"
                        Log(log,FLAGS='PRINT')
            else:
                move(f'{SavePath}{a}{FileName}',f'{SavePath}{a}{NewVideoDir}{a}{NewFileName}{FileType}')
                log = f'INFO: 字幕文件{FileName}已导入' if flag == 'ASS' else f"INFO: MOVE至 {SavePath}{a}{NewVideoDir}{a}{NewName}{FileType} 完成...一切已经准备就绪"
                Log(log,FLAGS='PRINT')
        else:
            Log(f'ERROR: {SavePath}{a}{NewVideoDir}{a}{NewFileName}{FileType}已存在,程序跳过')

    #a = ['move /y','mkdir','\\'] if name == 'nt' else ['mv','mkdir -p','/']#识别操作系统
    #NewName =  f"S{Season}SP{Episodes}" if '.' in NewName or Episodes == 00 else f"S{Season}E{Episodes}"
    NewName = f"S{Season}E{Episodes}"
    NewVideoDir = f"{CategoryName}{a}{VideoTrueName}{a}Season_{Season}" if CategoryName != None else f"{VideoTrueName}{a}Season_{Season}"
    SavePath = SavePath.strip('\\')
    #system(f'{a[1]} {SavePath}{a[2]}{NewVideoDir}')
    try:
        makedirs(f'{SavePath}{a}{NewVideoDir}')
    except OSError:
        Log(f"WARNING: 创建 {SavePath}{a}{NewVideoDir} 失败(可能是指定目录已存在)",FLAGS='PRINT')
    except :
        pass
    else:   
        Log(f"INFO: 创建 {SavePath}{a}{NewVideoDir} 完成")
    ASS = RAWVideoName if type(AssList) != dict else AssList
    if AssList != None and RAWVideoName in ASS:
        if  VideoName == AssList:
            if path.isfile(f'{SavePath}{a}{AssList}') == True:
                    NewAssFileName = NewName + '.' + ASSCategory(AssList)
                    FileMV(AssList,NewVideoDir,FileType,NewAssFileName,'ASS')
        else:
            for i in AssList[VideoName]:
                NewAssFileName = NewName + '.' + ASSCategory(i)
                ASSFileType = path.splitext(i)[1]
                if path.isfile(f'{SavePath}{a}{i}') == True:
                    FileMV(i,NewVideoDir,ASSFileType,NewAssFileName,'ASS')
                    
        
    sleep(0.5)
    #system(f'{a[0]} "{SavePath}{a[2]}{VideoName}"  "{SavePath}{a[2]}{NewVideoDir}{a[2]}{NewName}"')
    if VideoName != AssList:   
        if path.isfile(f'{SavePath}{a}{VideoName}') == False:
            Log(f'ERROR: 不存在 {SavePath}{a}{VideoName} 文件...EXIT',FLAGS='PRINT')
            #exit()
        else:
            FileMV(VideoName,NewVideoDir,FileType,NewName,None)
            if name == 'nt' and WINTOASTFLAGS == True:
                WinTaoast('番剧下载整理完毕',f'{VideoTrueName}已经准备就绪了')
   

def Log(message,FLAGS=None):
    global DataLog
    #global OPDETAILEDLOGFLAGS
    message = f'[{strftime("%Y-%m-%d %H:%M:%S",localtime(time()))}] {message}'
    if OPDETAILEDLOGFLAGS == True or FLAGS == 'PRINT' :
        print(message)
    #print(message) 
    DataLog = DataLog + '\n' + message

def GetHttpData(Path,Flag=None):
    from requests import get,exceptions
    proxy = {'http':HTTPPROXY,'https':HTTPSPROXY,'socks5':SOCKS5PROXY}
    headers = {'User-Agent':f'Abcuders/AutoAnimeMv/{V}(https://github.com/Abcuders/AutoAnimeMv)'}
    if Flag == 'UPDATE':    
        Path = UPDATEURLPATH + Path 
    try:
        Httpdate = get(Path,proxies=proxy,headers=headers) if USINGPROXYFLAGS == True else get(Path,headers=headers)
    except exceptions.ConnectionError:
        Log(f'ERROR: Get {Path} 失败,未能获取到内容,请检查您是否启用了系统代理,如是则您应该在此工具中配置代理信息,否您则需要检查您的网络能否访问',FLAGS='PRINT')
        if Flag == 'UPDATE':   
            exit()
        else:
            return None
    except:
        Log(f'ERROR: Get {Path} 失败,未能获取到内容,请检查您的网络',FLAGS='PRINT')
        if Flag == 'UPDATE':       
            exit()
        return None
    else:
        if Httpdate.status_code == 200:
            return Httpdate.text
        else:
            Log('INFO: GETDATE Status-Code NO 200')
            if Flag == 'UPDATE':   
                exit()  
            else:
                return None

def RWAnimeList(WriteData=None):
    chdir(getcwd())
    if USEGITHUBANIMELISTFLAG == True:
        data = GetHttpData('AnimeList',Flag='UPDATE')
        if data != None:
            Log(f'INFO: 正在获取GITHUB AnimeList ==>  {data}')
            return data
        else:
            return None
    else:
        with open(f'AnimeList','r+',encoding='UTF-8') as ff:
            if WriteData == None:
                data = ff.read()
                if data != ' ':
                    Log(f'INFO: 正在读取AnimeList ==> {data}')
                    return data
                else:
                    return None
            elif WriteData != None:
                Log(f'INFO: 正在写入AnimeList <== {WriteData}')
                ff.write(str(WriteData))
            else:
                return None
def CheckBeforeUpdate():
    chdir(getcwd())
    if path.isfile('config.ini') == False:
        Log('WARNING: 更新主程序前检查到您没有配置外置config.ini,如果直接更新您的自定义配置将变为默认配置')
        if SKIPCHECKBEFOREUPDATEFLAGS == False:
            Log('INFO: 正在将您自定义的内置配置重写至config.ini文件中')
            with open('config.ini','w+',encoding='utf-8') as ff:
                data = f'''#config
OPDETAILEDLOGFLAGS = '{OPDETAILEDLOGFLAGS}' #详细日志输出开关
WINTOASTFLAGS = '{WINTOASTFLAGS}' #win弹窗通知开关 
USEFILELINKFLAGS = '{USEFILELINKFLAGS}' #不使用MOVE改为使用硬链接进行番剧的整理(保种使用)
LINKFAILSUSEMOVEFLAGS = '{LINKFAILSUSEMOVEFLAGS}' #硬链接失败时使用MOVE
AUTOUPDATEFLAGS = '{AUTOUPDATEFLAGS}' #自动更新开关
UPDATEURLPATH = '{UPDATEURLPATH}' #UPDATEURL
NOUPDATELIST = '{NOUPDATELIST}' #不更新列表
SKIPCHECKBEFOREUPDATEFLAGS = '{SKIPCHECKBEFOREUPDATEFLAGS}' #跳过自动解决更新前检查到的问题(更新覆盖内置自定义配置)
USEGITHUBANIMELISTFLAG = '{USEGITHUBANIMELISTFLAG}' #使用Github上的AnimeList文件
USELOCALANIMELISTFLAGS = '{USELOCALANIMELISTFLAGS}' #使用本地的AnimeList文件
USINGPROXYFLAGS = '{USINGPROXYFLAGS}' #使用代理开关,如果您的代理服务器需要认证,请使用 账号:密码@ip:port 这样的格式
HTTPPROXY = '{HTTPPROXY}' #Http代理,请根据您的实际情况填写  
HTTPSPROXY = '{HTTPSPROXY}' #Https代理,请根据您的实际情况填写
SOCKS5PROXY = '{SOCKS5PROXY}' #SOCKS5代理,请根据您的实际情况填写
USEBGMAPIFLAGS = '{USEBGMAPIFLAGS}' #使用BgmApi进行更准确的识别
FORCEDUSEBGMAPI = '{FORCEDUSEBGMAPI}' #强制使用BgmApi进行识别,不查询AimeList文件
BGMAPIURLPATH = '{BGMAPIURLPATH}' #BGMAPIURL
                '''
                ff.write(data)

def UpDate(UpdateFileList):
    chdir(getcwd())
    #UpdateFileList = [] if flag != 'PY' and flag != 'EXE' else UpdateFileList
    #flag = UpdateFileList.append(flag) if UpdateFileList == [] else flag
    #UpdateFileList = None if flag == 'EXE' else UpdateFileList
    if type(UpdateFileList) == list:
        for i in UpdateFileList:
            if i in NOUPDATELIST:
                Log(f'INFO: {i} 在更新排除列表里,故跳过更新')
            else:
                CheckBeforeUpdate()
                Update = GetHttpData(i,Flag='UPDATE')
                with open(i,'w+',encoding='utf-8') as ff:
                    ff.write(Update)
                    Log(f'INFO: 更新 ==> {i}')
    else:
        Update = GetHttpData(UpdateFileList,Flag='UPDATE')
        if 'AutoAnimeMv' in UpdateFileList:
            CheckBeforeUpdate()
        with open(UpdateFileList,'w+',encoding='utf-8') as ff:
                ff.write(Update)
                Log(f'INFO: 自定义更新 ==> {UpdateFileList}')

def CheckUpdate(flag):
    CheckUpdate = literal_eval(GetHttpData('update',Flag='UPDATE'))
    if flag == 'PY' or flag == 'EXE':
        if CheckUpdate['V'] == V:
            Log('INFO: 当前即是最新版不需要更新')
            exit()
        else:
            CheckUpdate["File"] = literal_eval(str(CheckUpdate["File"]).replace('AutoAnimeMv.py','AutoAnimeMv.exe')) if flag == 'EXE' else CheckUpdate["File"]
            Log(f'INFO: 最新版 ==> {CheckUpdate["V"]},可更新的文件 ==> {CheckUpdate["File"]}')
        return CheckUpdate['File']
    else:
        Log(f'INFO: 指定的更新文件 ==> {flag}')
        return flag

def ProcessingBgmAPIDate(Name=None,AnimeId=None,EP=None):
    from urllib.parse import quote,unquote
    if AnimeId == None:
        UrlEDName = quote(Name, safe='/', encoding='UTF-8', errors=None)
        data = GetHttpData(f'{BGMAPIURLPATH}search/subject/{UrlEDName}?type=2&responseGroup=small&max_results=1')
    elif EP != None:
        data = GetHttpData(f'{BGMAPIURLPATH}v0/episodes?subject_id={AnimeId}&type=1&limit=100&offset=0')
    else:
        data = GetHttpData(f'{BGMAPIURLPATH}v0/episodes?subject_id={AnimeId}&type=0&limit=100&offset=0')
    if data != None:
        if AnimeId == None:
            try:
                data = literal_eval(data)                                               
                Name = unquote(data['list'][0]['name_cn'],encoding='utf-8',errors='replace')
                Name = Name.replace(' ','-') if ' ' in Name else Name
                AnimeId = str(data['list'][0]['id'])
                EpList = ProcessingBgmAPIDate(AnimeId=AnimeId)
                Log(f'INFO: id:{AnimeId} {Name} << bgmApi精确查询结果',FLAGS='PRINT')
                return Name,str(AnimeId),EpList
            except SyntaxError:
                Log(f'INFO: bgmApi没有查询出结果',FLAGS='PRINT')
                return None,None
        elif EP != None:
            try:
                SPList = literal_eval(data)['data']
                for i in range(len(SPList)):
                    if str(SPList[i]['sort']) == EP:
                        Log(f'INFO: {EP} 特别篇 ==> {i}')
                        return str(i),None
                Log('INFO: 当前特别篇无法整理')
            except SyntaxError:
                Log(f'INFO: bgmApi没有查询出结果',FLAGS='PRINT')
                return None,None
        else:
            EpListApi = literal_eval(data)['data']
            Eplist = []
            for i in EpListApi:
                Eplist.append(str(i['sort']))
            return Eplist
    else:
        return None,None,None

def MainOperate(FileName,AssFL,CategoryName,Flags=None):
    FileN = AssFL if FileName == None and type(AssFL) != list else FileName
    CheckAnimeFlag = CheckAnimeOthe(FileN)
    RAWVideoName = FileName if FileName != None else AssFL
    if CheckAnimeFlag == True: 
        global AimeList
        chdir(getcwd())
        if FileName == None:
            FileName = AssFL
        if AimeList != None:
            Log(f'INFO: 正在读取AimeList Cache(缓存) ==> {AimeList}',FLAGS='PRINT')
        elif USEGITHUBANIMELISTFLAG == True or USELOCALANIMELISTFLAGS == True:
            if path.isfile(f'AnimeList'):
                AimeList = RWAnimeList()
        if AimeList != None:
            VideoTrueName = []
            AimeList = literal_eval(AimeList) if type(AimeList) == str else AimeList
            if FORCEDUSEBGMAPI == False:
                ii = FileName.replace(' ','-') if ' ' in FileName else FileName
                for i in AimeList['AnimeList']:
                    if i in ii:
                        VideoTrueName = AimeList['AnimeAlias'][i]
                        break
        
            if VideoTrueName != []:
                Log(f'INFO: {VideoTrueName} << AnimeList')
                FileName = FileName if FileName != None else AssFL
                Season,Episodes,VideoTrueName,ApiVideoTrueName,FileType,RAWSeason,RAWEpisodes = AttributesMatch(FileName,Flag='AnimeList')
            #else:
            #    Season,Episodes,VideoTrueName,FileType = AttributesMatch(VideoName)
            #    AimeList['AnimeList'].append(VideoTrueName)
            #    AimeList['AnimeAlias'][VideoName] = VideoTrueName
            #    RWAnimeList(AimeList)
            else:
                FileName = FileName if FileName != None else AssFL 
                Season,Episodes,VideoTrueName,ApiVideoTrueName,FileType,RAWSeason,RAWEpisodes = AttributesMatch(FileName)
            #RWAnimeList(f'{"AnimeList":[{VideoTrueName}],"AnimeAlias":{{VideoTrueName}:{VideoTrueName}}}')
            #RWAnimeList(f'{"AnimeList":[""],"AnimeAlias":{"":""}}')
        else:
            Season,Episodes,VideoTrueName,ApiVideoTrueName,FileType,RAWSeason,RAWEpisodes = AttributesMatch(FileName)
        if Flags != 'ASS':
            if AssFL != None:
                AssForVideo = {}
                for i in AssFL:
                    ii = i.replace(' ','-') if ' ' in i else i
                    if VideoTrueName in ii and RAWEpisodes in ii and RAWSeason in ii:
                        if FileName in AssForVideo:
                            AssForVideo[FileName].append(i)
                        else:
                            AssForVideo[FileName] = [i]
                        #AssFL.remove(i)
                if len(AssForVideo) != 0:
                    AssFL = AssForVideo   
        #if ApiVideoTrueName != None:
        #    VideoTrueName = ApiVideoTrueName
        #AutoMv(SavePath,FileName,RAWVideoName,Season,Episodes,VideoTrueName,FileType,AssFL,CategoryName)
        AutoMv(SavePath,FileName,RAWVideoName,Season,Episodes,VideoTrueName,FileType,AssFL,CategoryName)
    else:
        Log(f'INFO: {CheckAnimeFlag}番剧,不进行整理',FLAGS='PRINT')
        exit()

V = '1.20.1'
AimeList = None
BgmAPIDateCache = {}
DataLog = f'\n\n[{strftime("%Y-%m-%d %H:%M:%S",localtime(time()))}] INFO: Running....'
a = '\\' if name == 'nt' else '/'
if name == 'nt' and WINTOASTFLAGS == True: from win10toast import ToastNotifier

if __name__ == "__main__":
    Log(f'INFO: 当前工具版本为{V}')
    Log(f"INFO: 当前操作系统识别码为{name},posix/nt/java对应linux/windows/java虚拟机")
    chdir(getcwd())
    if path.isfile('config.ini'):
        with open('config.ini','r',encoding='UTF-8') as ff:
            Log('INFO: 正在读取外置ini文件',FLAGS='PRINT')
            T = 0
            for i in ff.readlines():
                if i[0] != '#' and i != '':
                    i = i.strip('\n') 
                    Log(f'INFO: 配置 < {i}')
                    exec(i)
                    T = T + 1
            if T == 0:
                Log('WARNING: 外置ini文件没有配置',FLAGS='PRINT')
    try:
        SavePath,VideoName,AssList,CategoryName,flag = GetArgv()
        if type(VideoName) == list :
            Log(f'INFO: 发现{len(VideoName)}个番剧视频 ==> {VideoName}',FLAGS='PRINT')
            for i in VideoName:
                MainOperate(i,AssList,CategoryName,flag)
        elif flag == 'ASS' and type(AssList) == list:
            for i in AssList:
                MainOperate(None,i,CategoryName,flag)
        elif flag == 'ASS':
            MainOperate(None,AssList,CategoryName,flag)
        else:
            MainOperate(VideoName,AssList,CategoryName,flag)
    except Exception as err:
        Log(f'ERROR: 严重BUG:{err}',FLAGS='PRINT')
    except SystemExit:
        Log('INFO: 程序自主退出')
    else:
        Log('INFO: 所有工作已经全部完成')
    finally:
        if len(argv) > 1 and path.exists(argv[1]) :
            SavePath = argv[1]
        elif len(argv) == 1 or argv[1] == 'update' or path.exists(argv[1]) == False: 
            SavePath = getcwd()
            Log(F'INFO: 不可访问保存路径,Log已存放至AutoAnimeMV工具目录下')
        with open(f"{SavePath}{a}{strftime('%Y-%m-%d',localtime(time()))}.log","a+",encoding='utf-8') as ff:
            ff.write(DataLog)