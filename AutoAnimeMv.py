#!/usr/bin/python3
#coding:utf-8
from sys import argv
from os import system,path,name
from time import sleep,ctime
from re import findall,search,sub,I

DataLog = "LOG开始记录，完整log条目为8条"

def AttributesMatch(VideoName):
    Season = '01' #定义初始剧季为1
    #匹配待去除
    #FuzzyMatchData = ['字幕','Raws','sub','汉化','搬运','月新番','Airota','Comicat','DMHY','NC-Raws','ANi','LoliHouse','Sakurato','TSDM','LoveEcho','EMe','Sakura','SweetSub','AHU-SUB','VCB-Studio','GM-Team','MingY','cc动漫','推しの子','喵萌奶茶屋','天月搬运组','萝莉社活动室','千夏生活向上委员会','酷漫404','拨雪寻春','霜庭云花Sub','FSD炸鸽社','雪飘工作室','丸子家族','驯兽师联盟','肥猫压制','离谱','虹咲学园烤肉同好会','AQUA工作室','晨曦制作','夜莺家族','Liella!の烧烤摊']
    FuzzyMatchData = ['月新番']
    #精准待去除
    PreciseMatchData = ['仅限港澳台地区']
    FileType = path.splitext(VideoName)[1]
    #FileType = search(r'(.*?\.)',VideoName[::-1],flags=I).group()[::-1] #匹配视频文件格式
    #统一意外字符
    VideoName = sub(r',|，| ','-',VideoName,flags=I) 
    VideoName = sub(r'[^A-Za-z0-9_\s&/\-\u4e00-\u9fa5]','=',VideoName,flags=I)
    #匹配剧集
    Episodes = findall(r'[^0-9a-z\u4e00-\u9fa5][0-2]{1}[0-9]{1}[^0-9\u4e00-\u9fa5]',VideoName,flags=I)[0].strip(" =-_eE")
    Log(f"2.匹配剧集为{Episodes}")
    #通过剧集截断文件名
    VideoName = sub(r'%s.*'%Episodes,'',VideoName,flags=I)
    Log(f"3.通过剧集截断文件名为{VideoName}")
    #开始去除其他字符
    for i in range(len(PreciseMatchData)):
        VideoName = sub(r'%s'%PreciseMatchData[i],'',VideoName,flags=I)
    VideoName = sub(r'^=.*?=','',VideoName,flags=I)
    for i in range(len(FuzzyMatchData)):
        VideoName = sub(r'=.*?%s.*?='%FuzzyMatchData[i],'',VideoName,flags=I)
    VideoName = VideoName.replace('=','').replace(' ','').strip('-')
    Log(f"4.番剧Name为{VideoName}")
    #匹配剧季
    if ('/' in VideoName) == True: #按'/'进行双语言分类
        VideoName = VideoName.split("/", 1)
        #print(VideoName[1].replace('-','').isalnum())
        if VideoName[1].replace('-','').isalnum() == True: #双语言(中英)分类匹配英文Name中的剧季
            if search(r'[0-9]{0,1}[0-9]{1}S',VideoName[1][::-1],flags=I) != None :
                Season = search(r'[0-9]{0,1}[0-9]{1}S',VideoName[1][::-1],flags=I).group(0)[::-1]
                TrueVideoName = VideoName[1].strip(Season)
                Season = search(r'[0-9]{0,1}[0-9]{1}S',VideoName[1][::-1],flags=I).group(0)[::-1].strip('Ss')
                Log(f"5-1.TrueVideoName={TrueVideoName},Season={Season}")
            else:
                TrueVideoName = VideoName[1]
    elif search(r'季.*?第|[0-9]{0,1}[0-9]{1}S',VideoName[::-1],flags=I) != None :#单语言(中/英)匹配是否存在剧季
            Season = search(r'(季.*?第|[0-9]{0,1}[0-9]{1}S)',VideoName[::-1],flags=I).group(0)[::-1]
            TrueVideoName = VideoName.strip(Season)
            Season = search(r'(季.*?第|[0-9]{0,1}[0-9]{1}S)',VideoName[::-1],flags=I).group(0)[::-1].strip('第季Ss')
            if Season.isdigit() == True :
                Log(f"5-2.TrueVideoName={TrueVideoName},Season={Season}")
            else:#中文剧季转化
                digit = {'一':'01', '二':'02', '三':'03', '四':'04', '五':'05', '六':'06', '七':'07', '八':'08', '九':'09'}
                Season = digit[Season]
                Log(f"5-3.TrueVideoName={TrueVideoName},Season={Season}")
    else:
        TrueVideoName = VideoName
    try: 
        TrueVideoName = TrueVideoName.strip('-')
    except:
        pass
    print(TrueVideoName,Season)
    Log(f"5-4.TrueVideoName={TrueVideoName},Season={Season}")
    return Season,Episodes,TrueVideoName,FileType

def GetArgv():#接受参数
    SavePath,VideoName = argv[1],argv[2]
    Log(f"1.接受到{argv}参数")
    #筛选分类,您可以根据不同的类型设置不同路径
    return SavePath,VideoName

def AutoMv(SavePath,VideoName,Season,Episodes,VideoTrueName,FileType):#整理+重命名
    a = ['move /y','mkdir','\\'] if name == 'nt' else ['mv','mkdir -p','/']#识别操作系统
    Log(f"6.当前操作系统识别码为{name},posix/nt/java对应linux/windows/java虚拟机")
    NewName = f"S{Season}E{Episodes}{FileType}"
    NewVideoDir = f"{VideoTrueName}{a[2]}Season_{Season}"
    system(f'{a[1]} {SavePath}{a[2]}{NewVideoDir}')
    Log(f"7.创建{VideoTrueName}{a[2]}Season_{Season}完成")
    sleep(2)
    system(f'{a[0]} "{SavePath}{a[2]}{VideoName}"  "{SavePath}{a[2]}{NewVideoDir}{a[2]}{NewName}"')
    Log(f"8.创建{SavePath}{a[2]}{NewVideoDir}{a[2]}{NewName}完成")

def Log(message):
    global DataLog
    print(message)
    DataLog = DataLog + '\n' + message

if __name__ == "__main__":
   #sleep(15)
   SavePath,VideoName = GetArgv()
   Season,Episodes,VideoTrueName,FileType = AttributesMatch(VideoName)
   AutoMv(SavePath,VideoName,Season,Episodes,VideoTrueName,FileType)
   with open(f"{ctime().replace(' ','_').replace(':','-')}.log","w+",encoding='utf-8') as ff:
       ff.write(DataLog)