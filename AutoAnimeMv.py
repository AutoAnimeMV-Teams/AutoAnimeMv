#!/usr/bin/python3
#coding:utf-8
from sys import argv
from os import path,name,makedirs,listdir,getcwd,chdir,link
from time import sleep,strftime,localtime,time
from re import findall,match,search,sub,I
from shutil import move
from ast import literal_eval

#config
WINTOASTFLAGS = False #win弹窗通知开关 
OPDETAILEDLOGFLAGS = True #详细日志输出开关
USEFILELINKFLAGS = True #不使用MOVE改为使用硬链接进行番剧的整理(保种使用)
LINKFAILSUSEMOVEFLAGS = False #硬链接失败时使用MOVE
AUTOUPDATEFLAGS = True #自动更新开关
UPDATEURLPATH = 'https://raw.githubusercontent.com/Abcuders/AutoAnimeMv/main/' #UPDATEURL
USEGITHUBANIMELISTFLAG = True #使用Github上的AnimeList文件
USELOCALANIMELISTFLAGS = False #使用本地的AnimeList文件
USINGPROXYFLAGS = True #使用代理开关,如果您的代理服务器需要认证,请使用 账号:密码@ip:port 这样的格式
HTTPPROXY = 'http://127.0.0.1:7890' #Http代理,请根据您的实际情况填写  
HTTPSPROXY = 'http://127.0.0.1:7890' #Https代理,请根据您的实际情况填写
SOCKS5PROXY = '' #SOCKS5代理,请根据您的实际情况填写
USEBGMAPIFLAGS = True #使用BgmApi进行更准确的识别
FORCEDUSEBGMAPI = False #强制使用BgmApi进行识别,不查询AimeList文件
BGMAPIURLPATH = 'https://api.bgm.tv/search/subject/' #BGMAPIURL


def WinTaoast(title,msg):
    a = ToastNotifier().show_toast(title, msg,duration=5,threaded=True)   

def VDFileMatch(FileList):
    SuffixList = ['.ass','.srt','.mp4','mkv']
    ChAssFileList = []
    VdFileList = []
    for File in FileList:
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
    else:
        Log('ERROR: 该目录下没有匹配的番剧视频...EXIT',FLAGS='PRINT')
        exit()

def AttributesMatch(VideoName,Flag=None):
    Season = '01' #定义初始剧季和剧集为1
    Episodes = '01'
    RAWVideoName = VideoName
    #匹配待去除
    FuzzyMatchData = [r'=.*?月新番.*?=',r'\d{4}.\d{2}.\d{2}',r'20\d{2}',r'v\d{1}',r'\d{4}年\d{1,2}月番']
    #精准待去除
    PreciseMatchData = ['仅限港澳台地区','僅限港澳台地區','日語原聲','国漫','TVアニメ','x264','1080p','720p','4k','\(-\)','（-）']
    OtEpisodesMatchData = ['第(\d{1,4})集','(\d{1,4})集']
    FileType = path.splitext(VideoName)[1]
    #FileType = search(r'(.*?\.)',VideoName[::-1],flags=I).group()[::-1] #匹配视频文件格式
    #统一意外字符
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
        Episodes = findall(r'[^0-9a-z.\u4e00-\u9fa5\u0800-\u4e00][0-9]{1,4}[^0-9a-uw-z.\u4e00-\u9fa5\u0800-\u4e00]',VideoName[::-1],flags=I)[0][::-1].strip(" =-_eEv")
        VideoName = VideoName.strip('-')
        if VideoName[0] == '《':#判断有无字幕组
            VideoName = sub(r'《|》','',VideoName,flags=I) 
        else:
            VideoName = sub(r'^=.*?=','',VideoName,flags=I)
    except IndexError:
        Log('ERROR: 未匹配出剧集,请检查(程序目前不支持特典和电影)...EXIT',FLAGS='PRINT')
        #Log('WARNING: 未匹配出剧集,可能是特典番剧',FLAGS='PRINT')
        exit()
        #if search(r'ED',VideoName,flags=I) != None :
        #    TrueVideoName = sub(r'ED.*','',VideoName,flags=I)
    else:        
        RAWEpisodes = Episodes
        Episodes = f"0{Episodes}" if len(Episodes) == 1 else Episodes
        Log(f"INFO: 匹配剧集 ==> {Episodes}")
        #通过剧集截断文件名
        VideoName = sub(r'%s.*'%RAWEpisodes,'',VideoName,flags=I)
        Log(f"INFO: 通过剧集截断文件名 ==> {VideoName}")
        VideoName = VideoName.replace('=','').replace(' ','').strip('-')
        Log(f"INFO: 番剧Name ==> {VideoName}")
        #匹配剧季
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
                        Season = f"0{Season}" if len(Season) == 1 else Season
                        Log(f"INFO: id 1 TrueVideoName ==> {TrueVideoName},Season ==> {Season}")
                        break
                    elif i ==  len(VideoName)-1 :
                        TrueVideoName = VideoName[0]
        elif search(SeasonMatchData2,VideoName[::-1],flags=I) != None :#单语言(中/英)匹配是否存在剧季
                Season = search(SeasonMatchData2,VideoName[::-1],flags=I).group(0)[::-1]
                #TrueVideoName = VideoName.strip(Season)
                TrueVideoName = sub(r'%s.*'%Season,'',VideoName,flags=I) #通过剧季截断文件名
                Season = search(SeasonMatchData2,VideoName[::-1],flags=I).group(0)[::-1].strip('第季SeasonndSs-')
                RAWSeason = Season
                if Season.isdigit() == True :
                    Season = f"0{Season}" if len(Season) == 1 else Season
                    Log(f"INFO: id 2 TrueVideoName ==> {TrueVideoName},Season ==> {Season}")
                else:#中文剧季转化
                    digit = {'一':'01', '二':'02', '三':'03', '四':'04', '五':'05', '六':'06', '七':'07', '八':'08', '九':'09','壹':'01','贰':'02','叁':'03','肆':'04','伍':'05','陆':'06','柒':'07','捌':'08','玖':'09'}
                    Season = digit[Season]
                    Log(f"INFO: id 3 TrueVideoName ==> {TrueVideoName},Season ==> {Season}")
        else:
            TrueVideoName = VideoName
            RAWSeason = ''
            Log(f"INFO: id 4 TrueVideoName ==> {TrueVideoName},Season ==> {Season}")
    TrueVideoName = TrueVideoName.strip('-=_')
    Log(f'INFO: {TrueVideoName} {Season} {Episodes} {FileType} << {RAWVideoName}',FLAGS='PRINT')
    if Flag != 'ANIMELIST' or FORCEDUSEBGMAPI == True:
            if findall('[\d\u4e00-\u9fa5\d]+',TrueVideoName) != []:
                #print(findall('啊啊啊,好累呀',TrueVideoName))
                data = findall('[\d\u4e00-\u9fa5\d]+',TrueVideoName)
                for i in data:
                    ApiVideoName = ProcessingBgmAPIDate(i)
                    if ApiVideoName != None:
                        TrueVideoName = ApiVideoName
                        break
            else:
                ApiVideoName = ProcessingBgmAPIDate(TrueVideoName)
    return Season,Episodes,TrueVideoName,ApiVideoName,FileType,RAWSeason,RAWEpisodes

def GetArgv():#接受参数
    Log(f"INFO: 接受到参数 ==> {argv}")
    #筛选分类,您可以根据不同的类型设置不同路径
    #if len(argv) == 2 or len(argv) == 3:
    try:
        if argv[1] == 'update' or argv[1] == 'UPDATE':
            if AUTOUPDATEFLAGS == True:
                Log('INFO: 准备更新中')
                UpDate(CheckUpdate())
                Log('INFO: 全部已更新完毕')
                exit()
            else:
                Log('ERROR AUTOUPDATEFLAGS = False')
                exit()
    except IndexError:
        Log(f'ERROR 未知的参数 ==> {argv}',FLAGS='PRINT')
        exit()
    if 2 <= len(argv) <=  3:
        SavePath,CategoryName = argv[1],None
        Log(f'INFO: 现在是本地番剧文件批处理模式,正在扫描Path ==> {SavePath}')
        if len(argv) == 3:
            CategoryName = argv[2]
            Log(f'INFO: 分类模式已启用,当前分类 ==> {CategoryName}')
        FileList = listdir(SavePath)
        VDFileNameL,ASSFileN = VDFileMatch(FileList)
        return SavePath,VDFileNameL,ASSFileN,CategoryName
            
    #elif len(argv) == 4 or len(argv) == 5:
    elif 4 <= len(argv) <= 5:
        SavePath,VideoName,CategoryName = argv[1],argv[2],None
        if len(argv) == 5:
            CategoryName = argv[4]
            Log(f'INFO: 分类模式已启用,当前分类 ==> {CategoryName}')
        if argv[3] == '1': #NumberOfFile == 1
            return SavePath,VideoName,None,None
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
            return SavePath,VDFileName,ASSFileN,CategoryName
    else:
        Log(f'ERROR 错误的参数 ==> {argv}',FLAGS='PRINT')
        exit()

def AutoMv(SavePath,VideoName,Season,Episodes,VideoTrueName,FileType,AssList,CategoryName):#整理+重命名
    #a = ['move /y','mkdir','\\'] if name == 'nt' else ['mv','mkdir -p','/']#识别操作系统
    NewName = f"S{Season}E{Episodes}{FileType}"
    NewVideoDir = f"{VideoTrueName}{a}Season_{Season}"
    SavePath = SavePath.strip('\\')
    if CategoryName != None:
        NewVideoDir = f"{CategoryName}{a}{VideoTrueName}{a}Season_{Season}"
    #system(f'{a[1]} {SavePath}{a[2]}{NewVideoDir}')
    try:
        makedirs(f'{SavePath}{a}{NewVideoDir}')
    except OSError:
        Log(f"WARNING: 创建 {SavePath}{a}{VideoTrueName}{a}Season_{Season} 失败(可能是指定目录已存在)",FLAGS='PRINT')
    except :
        pass
    else:   
        Log(f"INFO: 创建 {VideoTrueName}{a}Season_{Season} 完成")
    if AssList != None and VideoName in AssList:
        for i in range(len(AssList[VideoName])):
            if path.isfile(f'{SavePath}{a}{AssList[VideoName][i]}') == True:
                AssFileType = path.splitext(AssList[VideoName][i])[1]
                if USEFILELINKFLAGS == True:
                    try:
                        link(f'{SavePath}{a}{AssList[VideoName][i]}',f'{SavePath}{a}{NewVideoDir}{a}S{Season}E{Episodes}.Chinese(版本{i+1}){AssFileType}')
                    except OSError as err:
                        if '[WinError 1]' in str(err):
                            Log(f'ERROR: 当前文件系统不支持硬链接',FLAGS='PRINT')
                        else:
                            Log(f'ERROR: {err}')
                        if LINKFAILSUSEMOVEFLAGS == True:
                            move(f'{SavePath}{a}{AssList[VideoName][i]}',f'{SavePath}{a}{NewVideoDir}{a}S{Season}E{Episodes}.Chinese(版本{i+1}){AssFileType}')
                            Log(f'INFO: 硬链接失败,使用MOVE导入字幕文件{AssList[VideoName][i]}',FLAGS='PRINT')
                        else:
                            exit()
                    else:
                        Log(f'INFO: 字幕文件{AssList[VideoName][i]}已导入(硬链接)',FLAGS='PRINT')
                else:
                    move(f'{SavePath}{a}{AssList[VideoName][i]}',f'{SavePath}{a}{NewVideoDir}{a}S{Season}E{Episodes}.Chinese(版本{i+1}){AssFileType}')
                    Log(f'INFO: 字幕文件{AssList[VideoName][i]}已导入',FLAGS='PRINT')
    sleep(0.5)
    #system(f'{a[0]} "{SavePath}{a[2]}{VideoName}"  "{SavePath}{a[2]}{NewVideoDir}{a[2]}{NewName}"')
    if path.isfile(f'{SavePath}{a}{VideoName}') == False:
        Log(f'ERROR: 不存在 {SavePath}{a}{VideoName} 文件...EXIT',FLAGS='PRINT')
        #exit()
    else:
        if USEFILELINKFLAGS == True:
            try:
                link(f'{SavePath}{a}{VideoName}',f'{SavePath}{a}{NewVideoDir}{a}{NewName}')
            except OSError as err:
                if '[WinError 1]' in str(err):
                    Log(f'ERROR: 当前文件系统不支持硬链接')
                else:
                    Log(f'ERROR: {err}')
                if LINKFAILSUSEMOVEFLAGS == True:
                    move(f'{SavePath}{a}{VideoName}',f'{SavePath}{a}{NewVideoDir}{a}{NewName}')
                    Log(f"INFO: 硬链接失败,使用MOVE创建 {SavePath}{a}{NewVideoDir}{a}{NewName} 完成...一切已经准备就绪")
                else:
                    exit()
            else:
                Log(f"INFO: 硬链接至 {SavePath}{a}{NewVideoDir}{a}{NewName} 完成...一切已经准备就绪")
        else:    
            move(f'{SavePath}{a}{VideoName}',f'{SavePath}{a}{NewVideoDir}{a}{NewName}')
            Log(f"INFO: 创建 {SavePath}{a}{NewVideoDir}{a}{NewName} 完成...一切已经准备就绪")
    if name == 'nt' and WINTOASTFLAGS == True:
        WinTaoast('番剧下载整理完毕',f'{VideoTrueName}已经准备就绪了')

def Log(message,FLAGS=None):
    global DataLog
    global OPDETAILEDLOGFLAGS
    message = f'[{strftime("%Y-%m-%d %H:%M:%S",localtime(time()))}] {message}'
    if OPDETAILEDLOGFLAGS == True or FLAGS == 'PRINT' :
        print(message)
    #print(message)  
    DataLog = DataLog + '\n' + message

def GetHttpData(Path,Flag=None):
    from requests import get,exceptions
    proxy = {'http':HTTPPROXY,'https':HTTPSPROXY,'socks5':SOCKS5PROXY}
    if Flag == 'UPDATE':    
        Path = UPDATEURLPATH + Path 
    try:
        Httpdate = get(Path,proxies=proxy) if USINGPROXYFLAGS == True else get(Path)
    except exceptions.ConnectionError:
        Log(f'ERROR: Get {Path} 失败,未能获取到内容,请检查您是否启用了系统代理,如是则您应该在此工具中配置代理信息,否您则需要检查您的网络能否访问raw.githubusercontent.com',FLAGS='PRINT')
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
    if USEGITHUBANIMELISTFLAG == True:
        data = GetHttpData('AnimeList',Flag='UPDATE')
        if data != None:
            Log(f'INFO: 正在获取GITHUB AnimeList ==>  {data}')
            return data
        else:
            return None
    else:
        with open(f'{SavePath}{a}AnimeList','r+',encoding='UTF-8') as ff:
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
        
def UpDate(UpdateFileList):
   chdir(getcwd())
   for i in UpdateFileList:
        Update = GetHttpData(i,Flag='UPDATE')
        with open(i,'w+',encoding='utf-8') as ff:
            ff.write(Update)
            Log(f'INFO: 更新 ==> {i}')

def CheckUpdate():
    CheckUpdate = literal_eval(GetHttpData('update',Flag='UPDATE'))
    if CheckUpdate['V'] == V:
        Log('INFO: 当前即是最新版不需要更新')
        exit()
    else:
        Log(f'INFO: 最新版 ==> {CheckUpdate["V"]},可更新的文件 ==> {CheckUpdate["File"]}')
    return CheckUpdate['File']

def ProcessingBgmAPIDate(Name):
    from urllib.parse import quote,unquote
    UrlEDName = quote(Name, safe='/', encoding='UTF-8', errors=None)
    data = GetHttpData(f'{BGMAPIURLPATH}{UrlEDName}?max_results=1')
    if data != None:
        try:                                               
            Name = unquote(literal_eval(data)['list'][0]['name_cn'],encoding='utf-8',errors='replace')
            Name = Name.replace(' ','-') if ' ' in Name else Name
            Log(f'INFO: {Name} << bgmApi精确查询结果',FLAGS='PRINT')
            return Name
        except SyntaxError:
             Log(f'INFO: bgmApi没有查询出结果',FLAGS='PRINT')
             return None
    else:
        return None

def MainOperate(VideoName,AssList,CategoryName,Flags=None):
    chdir(getcwd())
    AimeList = None
    if path.isfile(f'AnimeList') or USEGITHUBANIMELISTFLAG == True or USELOCALANIMELISTFLAGS == True:
        AimeList = RWAnimeList()
    if AimeList != None:
        VideoTrueName = []
        AimeList = literal_eval(AimeList)
        if FORCEDUSEBGMAPI == False:
            ii = VideoName.replace(' ','-') if ' ' in VideoName else VideoName
            for i in AimeList['AnimeList']:
                if i in ii:
                    VideoTrueName = AimeList['AnimeAlias'][i]
                    break
       
        if VideoTrueName != [] :
            Log(f'INFO: {VideoTrueName} << AnimeList')
            Season,Episodes,VideoTrueName,ApiVideoTrueName,FileType,RAWSeason,RAWEpisodes = AttributesMatch(VideoName,Flag='AnimeList')
        #else:
        #    Season,Episodes,VideoTrueName,FileType = AttributesMatch(VideoName)
        #    AimeList['AnimeList'].append(VideoTrueName)
        #    AimeList['AnimeAlias'][VideoName] = VideoTrueName
        #    RWAnimeList(AimeList)
        else: 
            Season,Episodes,VideoTrueName,ApiVideoTrueName,FileType,RAWSeason,RAWEpisodes = AttributesMatch(VideoName)
        #RWAnimeList(f'{"AnimeList":[{VideoTrueName}],"AnimeAlias":{{VideoTrueName}:{VideoTrueName}}}')
        #RWAnimeList(f'{"AnimeList":[""],"AnimeAlias":{"":""}}')
    else:
        Season,Episodes,VideoTrueName,ApiVideoTrueName,FileType,RAWSeason,RAWEpisodes = AttributesMatch(VideoName)
    if Flags != None:
        if AssList != None:
            AssForVideo = {}
            for i in AssList:
                ii = i.replace(' ','-') if ' ' in i else i
                if VideoTrueName in ii and RAWEpisodes in ii and RAWSeason in ii:
                    if VideoName in AssForVideo:
                        AssForVideo[VideoName] = AssForVideo[VideoName].append(i)
                    else:
                        AssForVideo[VideoName] = [i]
                    AssList.remove(i)
            if len(AssForVideo) != 0:
                AssList = AssForVideo   
    if ApiVideoTrueName != None:
        VideoTrueName = ApiVideoTrueName
    AutoMv(SavePath,VideoName,Season,Episodes,VideoTrueName,FileType,AssList,CategoryName)

V = '1.17.1'
DataLog = f'\n[{strftime("%Y-%m-%d %H:%M:%S",localtime(time()))}] INFO: Running....'
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
                if i[0] != '#':
                    i = i.strip('\n') 
                    Log(f"INFO: 配置 < {i}")
                    exec(i)
                    T = T + 1
            if T == 0:
                Log('WARNING: 外置ini文件没有配置',FLAGS='PRINT')
    SavePath,VideoName,AssList,CategoryName = GetArgv()
    try:
        if type(VideoName) == list:
            Log(f'INFO: 发现{len(VideoName)}个番剧视频 ==> {VideoName}',FLAGS='PRINT')
            for i in VideoName:
                MainOperate(i,AssList,CategoryName,0)
        else:
            MainOperate(VideoName,AssList,CategoryName)
    except SystemError:
        if len(argv) == 1: 
            SavePath = getcwd()
    finally:
        with open(f"{SavePath}{a}{strftime('%Y-%m-%d',localtime(time()))}.log","a+",encoding='utf-8') as ff:
            ff.write(DataLog)