#!/usr/bin/python3
#coding:utf-8
from sys import argv
from os import path,name,makedirs,listdir
from time import sleep,strftime,localtime,time
from re import findall,match,search,sub,I
from shutil import move


#config
WINTOASTFLAGS = False
OPDETAILEDLOGFLAGS = False


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
    Log(f'INFO: 发现{len(ChAssFileList)}个字幕文件',FLAGS='PRINT')
    if len(VdFileList) == 1:
        if ChAssFileList != []:
            return VdFileList[0],ChAssFileList
        else:
            return VdFileList[0],None
    else:
        Log('ERROR: 不只存在一个视频文件...EXIT')
        exit()

def AttributesMatch(VideoName,FLAGS=None):
    Season = '01' #定义初始剧季和剧集为1
    Episodes = '01'
    RAWVideoName = VideoName
    #匹配待去除
    FuzzyMatchData = [r'=.*?月新番.*?=',r'\d{4}.\d{2}.\d{2}',r'v\d{1}',r'\d{4}年\d{1,2}月番']
    #精准待去除
    PreciseMatchData = ['仅限港澳台地区','僅限港澳台地區','日語原聲','TVアニメ','1080p','720p','4k','\(-\)','（-）']
    FileType = path.splitext(VideoName)[1]
    #FileType = search(r'(.*?\.)',VideoName[::-1],flags=I).group()[::-1] #匹配视频文件格式
    #统一意外字符
    VideoName = sub(r',|，| ','-',VideoName,flags=I) 
    VideoName = sub('[^a-z0-9_\s&/\-:：.\(\)（）《》\u4e00-\u9fa5\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF]','=',VideoName,flags=I)
    #print(VideoName)
    #去除日期(作废)
    #VideoName = sub(r'','',VideoName,flags=I)
    #开始去除其他字符
    for i in range(len(PreciseMatchData)):
        VideoName = sub(r'%s'%PreciseMatchData[i],'-',VideoName,flags=I)
    if VideoName[0] == '《':#判断有无字幕组
        VideoName = sub(r'《|》','',VideoName,flags=I) 
    else:
        VideoName = sub(r'^=.*?=','',VideoName,flags=I)
    for i in range(len(FuzzyMatchData)):
        VideoName = sub(r'=.*?%s.*?='%FuzzyMatchData[i],'-',VideoName,flags=I)
    #匹配剧集
    try:
        Episodes = findall(r'[^0-9a-z.\u4e00-\u9fa5\u0800-\u4e00][0-9]{1,4}[^0-9a-z.\u4e00-\u9fa5\u0800-\u4e00]',VideoName,flags=I)[0].strip(" =-_eE")
    except IndexError:
        Log('ERROR: 未匹配出剧集,请检查(程序目前不支持特典和电影)...EXIT',FLAGS='PRINT')
        #Log('WARNING: 未匹配出剧集,可能是特典番剧',FLAGS='PRINT')
        exit()
        #if search(r'ED',VideoName,flags=I) != None :
        #    TrueVideoName = sub(r'ED.*','',VideoName,flags=I)
    else:        
        RAWEpisodes = Episodes
        Episodes = f"0{Episodes}" if len(Episodes) == 1 else Episodes
        Log(f"INFO: 匹配剧集为{Episodes}",FLAGS)
        #通过剧集截断文件名
        VideoName = sub(r'%s.*'%RAWEpisodes,'',VideoName,flags=I)
        Log(f"INFO: 通过剧集截断文件名为{VideoName}",FLAGS)
        VideoName = VideoName.replace('=','').replace(' ','').strip('-')
        Log(f"INFO: 番剧Name为{VideoName}",FLAGS)
        #匹配剧季
        if ('/' in VideoName) == True: #按'/'进行多语言分类
            VideoName = VideoName.split("/", )
            for i in range(len(VideoName)):
                if VideoName[i].replace('-','').replace(':','').isalnum() == True: #多语言分类匹配英文Name中的剧季
                    if search(r'[0-9]{0,1}[0-9]{1}S',VideoName[i][::-1],flags=I) != None :
                        Season = search(r'[0-9]{0,1}[0-9]{1}S',VideoName[i][::-1],flags=I).group(0)[::-1]
                        TrueVideoName = VideoName[i].strip(Season)
                        VideoName = sub(r'%s.*'%Season,'',VideoName,flags=I) #通过剧季截断文件名
                        Season = search(r'[0-9]{0,1}[0-9]{1}S',VideoName[i][::-1],flags=I).group(0)[::-1].strip('Ss')
                        Season = f"0{Season}" if len(Season) == 1 else Season
                        Log(f"INFO: id 1 TrueVideoName={TrueVideoName},Season={Season}",FLAGS)
                        break
                    elif i ==  len(VideoName)-1 :
                        TrueVideoName = VideoName[1]
        elif search(r'季.*?第|[0-9]{0,1}[0-9]{1}S',VideoName[::-1],flags=I) != None :#单语言(中/英)匹配是否存在剧季
                Season = search(r'(季.*?第|[0-9]{0,1}[0-9]{1}S)',VideoName[::-1],flags=I).group(0)[::-1]
                TrueVideoName = VideoName.strip(Season)
                VideoName = sub(r'%s.*'%Season,'',VideoName,flags=I) #通过剧季截断文件名
                Season = search(r'(季.*?第|[0-9]{0,1}[0-9]{1}S)',VideoName[::-1],flags=I).group(0)[::-1].strip('第季Ss')
                if Season.isdigit() == True :
                    Season = f"0{Season}" if len(Season) == 1 else Season
                    Log(f"INFO: id 2 TrueVideoName={TrueVideoName},Season={Season}",FLAGS)
                else:#中文剧季转化
                    digit = {'一':'01', '二':'02', '三':'03', '四':'04', '五':'05', '六':'06', '七':'07', '八':'08', '九':'09'}
                    Season = digit[Season]
                    Log(f"INFO: id 3 TrueVideoName={TrueVideoName},Season={Season}",FLAGS)
        else:
            TrueVideoName = VideoName
            Log(f"INFO: id 4 TrueVideoName={TrueVideoName},Season={Season}",FLAGS)
    TrueVideoName = TrueVideoName.strip('-=')
    Log(f'INFO: {TrueVideoName} {Season} {Episodes} {FileType} << {RAWVideoName}',FLAGS='PRINT')
    return Season,Episodes,TrueVideoName,FileType

def GetArgv():#接受参数
    try:
        SavePath,VideoName = argv[1],argv[2]
        Log(f"INFO: 接受到{argv}参数")
    #筛选分类,您可以根据不同的类型设置不同路径
    except IndexError:
        Log(f'ERROR 错误的参数: {argv}',FLAGS='PRINT')
        exit()
    else:
        if argv[3] == '1': #NumberOfFile == 1
            return SavePath,VideoName,None
        else:
            FileList = listdir(SavePath)
            VDFileList = []
            for i in range(len(FileList)):
                #print(path.isfile(f'{SavePath}{a}{FileList[i]}'))
                #print( VideoName in FileList[i])
                #if path.isfile(f'{SavePath}{a}{FileList[i]}') == True and VideoName in FileList[i] == True:
                if VideoName in FileList[i] :
                   VDFileList.append(FileList[i])
        if  VDFileList == []:
            Log('ERROR: 根据传入的torrent名称找不到video文件...EXIT',FLAGS='PRINT')
            exit()
        else:
            VDFileName,ASSFileN = VDFileMatch(VDFileList)
            return SavePath,VDFileName,ASSFileN


def AutoMv(SavePath,VideoName,Season,Episodes,VideoTrueName,FileType,AssFileList):#整理+重命名
    #a = ['move /y','mkdir','\\'] if name == 'nt' else ['mv','mkdir -p','/']#识别操作系统
    global a
    NewName = f"S{Season}E{Episodes}{FileType}"
    NewVideoDir = f"{VideoTrueName}{a}Season_{Season}"
    #system(f'{a[1]} {SavePath}{a[2]}{NewVideoDir}')
    try:
        makedirs(f'{SavePath}{a}{NewVideoDir}')
    except OSError:
        Log(f"WARNING: 创建 {SavePath}{a}{VideoTrueName}{a}Season_{Season} 失败(可能是指定目录已存在)",FLAGS='PRINT')
    except :
        pass
    else:   
        Log(f"INFO: 创建 {VideoTrueName}{a}Season_{Season} 完成")
    if AssList != None:
        for i in range(len(AssList)):
            if path.isfile(f'{SavePath}{a}{AssList[i]}') == True:
                AssFileType = path.splitext(AssList[i])[1]
                move(f'{SavePath}{a}{AssList[i]}',f'{SavePath}{a}{NewVideoDir}{a}S{Season}E{Episodes}.Chinese(版本{i+1}){AssFileType}')
                Log(f'INFO: 字幕文件{AssList[i]}已导入',FLAGS='PRINT')
    sleep(2)
    #system(f'{a[0]} "{SavePath}{a[2]}{VideoName}"  "{SavePath}{a[2]}{NewVideoDir}{a[2]}{NewName}"')
    if path.isfile(f'{SavePath}{a}{VideoName}') == False:
        Log(f'ERROR: 不存在 {SavePath}{a}{VideoName} 文件...EXIT',FLAGS='PRINT')
        #exit()
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

DataLog = f'\n[{strftime("%Y-%m-%d %H:%M:%S",localtime(time()))}] INFO Running....'
a = '\\' if name == 'nt' else '/'
if name == 'nt': from win10toast import ToastNotifier

if __name__ == "__main__":
   #sleep(15)
    Log(f"INFO: 当前操作系统识别码为{name},posix/nt/java对应linux/windows/java虚拟机")
    try:
        SavePath,VideoName,AssList = GetArgv()
    except:
        exit()
    try:
        Season,Episodes,VideoTrueName,FileType = AttributesMatch(VideoName)
        AutoMv(SavePath,VideoName,Season,Episodes,VideoTrueName,FileType,AssList)
    except :
        pass
    finally:
        with open(f"{SavePath}{a}{strftime('%Y-%m-%d',localtime(time()))}.log","a+",encoding='utf-8') as ff:
            ff.write(DataLog)