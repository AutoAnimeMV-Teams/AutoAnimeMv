#!/usr/bin/python3
#coding:utf-8
from sys import argv
from os import system,path,name
from time import sleep,strftime,localtime,time,ctime
from re import findall,search,sub,I

DataLog = 'Running....'

def AttributesMatch(VideoName):
    Season = '01' #定义初始剧季和剧集为1
    Episodes = '01'
    videname = VideoName
    #匹配待去除
    FuzzyMatchData = ['=.*?月新番.*?=','v\d{1}','\d{4}年\d{1,2}月番']
    #精准待去除
    PreciseMatchData = ['仅限港澳台地区','1080p','720p','4k']
    FileType = path.splitext(VideoName)[1]
    #FileType = search(r'(.*?\.)',VideoName[::-1],flags=I).group()[::-1] #匹配视频文件格式
    #统一意外字符
    VideoName = sub(r',|，| ','-',VideoName,flags=I) 
    VideoName = sub('[^a-z0-9_\s&/\-::/.()（）\u4e00-\u9fa5]','=',VideoName,flags=I)
    #print(VideoName)
    #去除日期
    VideoName = sub(r'\d{4}.\d{2}.\d{2}','',VideoName,flags=I)
    #开始去除其他字符
    for i in range(len(PreciseMatchData)):
        VideoName = sub(r'%s'%PreciseMatchData[i],'-',VideoName,flags=I)
    VideoName = sub(r'^=.*?=','',VideoName,flags=I)
    for i in range(len(FuzzyMatchData)):
        #VideoName = sub(r'=.*?%s.*?='%FuzzyMatchData[i],'-',VideoName,flags=I)
        VideoName = sub(fr'{FuzzyMatchData[i]}','-',VideoName,flags=I)
    #匹配剧集
    Episodes = findall(r'[^0-9a-z.\u4e00-\u9fa5\u0800-\u4e00][0-9]{1,4}[^0-9a-z.\u4e00-\u9fa5\u0800-\u4e00]',VideoName,flags=I)[0].strip(" =-_eE")
    Episodes = f"0{Episodes}" if len(Episodes) == 1 else Episodes
    Log(f"INFO: 匹配剧集为{Episodes}")
    #通过剧集截断文件名
    VideoName = sub(r'%s.*'%Episodes,'',VideoName,flags=I)
    Log(f"INFO: 通过剧集截断文件名为{VideoName}")
    VideoName = VideoName.replace('=','').replace(' ','').strip('-')
    Log(f"INFO: 番剧Name为{VideoName}")
    #匹配剧季
    if ('/' in VideoName) == True: #按'/'进行多语言分类
        VideoName = VideoName.split("/", )
        for i in range(len(VideoName)):
            if VideoName[i].replace('-','').replace(':','').isalnum() == True: #多语言分类匹配英文Name中的剧季
                if search(r'[0-9]{0,1}[0-9]{1}S',VideoName[i][::-1],flags=I) != None :
                    Season = search(r'[0-9]{0,1}[0-9]{1}S',VideoName[i][::-1],flags=I).group(0)[::-1]
                    TrueVideoName = VideoName[i].strip(Season)
                    Season = search(r'[0-9]{0,1}[0-9]{1}S',VideoName[i][::-1],flags=I).group(0)[::-1].strip('Ss')
                    Season = f"0{Season}" if len(Season) == 1 else Season
                    Log(f"INFO: id 1 TrueVideoName={TrueVideoName},Season={Season}")
                    break
                elif i ==  len(VideoName)-1 :
                    TrueVideoName = VideoName[1]
    elif search(r'季.*?第|[0-9]{0,1}[0-9]{1}S',VideoName[::-1],flags=I) != None :#单语言(中/英)匹配是否存在剧季
            Season = search(r'(季.*?第|[0-9]{0,1}[0-9]{1}S)',VideoName[::-1],flags=I).group(0)[::-1]
            TrueVideoName = VideoName.strip(Season)
            Season = search(r'(季.*?第|[0-9]{0,1}[0-9]{1}S)',VideoName[::-1],flags=I).group(0)[::-1].strip('第季Ss')
            if Season.isdigit() == True :
                Season = f"0{Season}" if len(Season) == 1 else Season
                Log(f"INFO: id 2 TrueVideoName={TrueVideoName},Season={Season}")
            else:#中文剧季转化
                digit = {'一':'01', '二':'02', '三':'03', '四':'04', '五':'05', '六':'06', '七':'07', '八':'08', '九':'09'}
                Season = digit[Season]
                Log(f"INFO: id 3 TrueVideoName={TrueVideoName},Season={Season}")
    else:
        TrueVideoName = VideoName
        Log(f"INFO: id 4 TrueVideoName={TrueVideoName},Season={Season}")
    TrueVideoName = TrueVideoName.strip('-')
    Log(f'INFO: {TrueVideoName} {Season} {Episodes} {FileType} << {videname}',FLAGS='PRINT')
    return Season,Episodes,TrueVideoName,FileType

def GetArgv():#接受参数
    SavePath,VideoName = argv[1],argv[2]
    Log(f"INFO: 接受到{argv}参数")
    #筛选分类,您可以根据不同的类型设置不同路径
    return SavePath,VideoName

def AutoMv(SavePath,VideoName,Season,Episodes,VideoTrueName,FileType):#整理+重命名
    a = ['move /y','mkdir','\\'] if name == 'nt' else ['mv','mkdir -p','/']#识别操作系统
    Log(f"INFO: 当前操作系统识别码为{name},posix/nt/java对应linux/windows/java虚拟机")
    NewName = f"S{Season}E{Episodes}{FileType}"
    NewVideoDir = f"{VideoTrueName}{a[2]}Season_{Season}"
    system(f'{a[1]} {SavePath}{a[2]}{NewVideoDir}')
    Log(f"INFO: 创建{VideoTrueName}{a[2]}Season_{Season}完成")
    sleep(2)
    system(f'{a[0]} "{SavePath}{a[2]}{VideoName}"  "{SavePath}{a[2]}{NewVideoDir}{a[2]}{NewName}"')
    Log(f"INFO: 创建{SavePath}{a[2]}{NewVideoDir}{a[2]}{NewName}完成...一切已经准备就绪")

def Log(message,FLAGS=None):
    global DataLog
    message = f'[{strftime("%Y-%m-%d %H:%M:%S",localtime(time()))}] {message}'
    if FLAGS == 'PRINT':
        print(message)
    print(message)  
    DataLog = DataLog + '\n' + message

if __name__ == "__main__":
   #sleep(15)
    SavePath,VideoName = GetArgv()
    try:
        Season,Episodes,VideoTrueName,FileType = AttributesMatch(VideoName)
        AutoMv(SavePath,VideoName,Season,Episodes,VideoTrueName,FileType)
    except IndexError:
        Log('ERROR 未匹配出剧集,请检查(程序目前不支持特典和电影)...EXIT')
    except :
        pass
   #with open(f"{ctime().replace(' ','_').replace(':','-')}.log","w+",encoding='utf-8') as ff:
    with open(f"{strftime('%Y-%m-%d',localtime(time()))}.log","a+",encoding='utf-8') as ff:
       ff.write(DataLog)