#!/usr/bin/python3
#coding:utf-8
from sys import argv
from os import system
from time import sleep
from re import findall,search,match,sub,split,I

def TitleMatch(VideoName):
    Season = '01'
    SubtitleGroupDate = ['字幕','Raws','sub','汉化','搬运','月新番','Airota','Comicat','DMHY','NC-Raws','ANi','LoliHouse','Sakurato','TSDM','LoveEcho','EMe','Sakura','SweetSub','AHU-SUB','VCB-Studio','GM-Team','MingY','cc动漫','推しの子','喵萌奶茶屋','天月搬运组','萝莉社活动室','千夏生活向上委员会','酷漫404','拨雪寻春','霜庭云花Sub','FSD炸鸽社','雪飘工作室','丸子家族','驯兽师联盟','肥猫压制','离谱','虹咲学园烤肉同好会','AQUA工作室','晨曦制作','夜莺家族','Liella!の烧烤摊']
    FileType = search(r'(.*?\.)',VideoName[::-1]).group()[::-1]
    print(FileType)
    VideoName = sub(r',|，| ','-',VideoName,flags=I)
    VideoName = sub(r'[^A-Za-z0-9_\s&/\-\u4e00-\u9fa5]','=',VideoName,flags=I)
    Episodes = findall(r'[^0-9a-z\u4e00-\u9fa5][0-2]{1}[0-9]{1}[^0-9\u4e00-\u9fa5]',VideoName,flags=I)[0].strip(" =_eE")
    print(Episodes)
    VideoName = sub(r'%s.*'%Episodes,'',VideoName,flags=I)
    for i in range(len(SubtitleGroupDate)):
        VideoName = sub(r'=.*?%s.*?='%SubtitleGroupDate[i],'',VideoName,flags=I)
    VideoName = VideoName.replace('=','').replace(' ','').strip('-')
    #print(VideoName)
    if ('/' in VideoName) == True:
        VideoName = VideoName.split("/", 1)
        #print(VideoName[1].replace('-','').isalnum())
        if VideoName[1].replace('-','').isalnum() == True:
            if search(r'[0-9]{0,1}[0-9]{1}S',VideoName[1][::-1],flags=I) != None :
                Season = search(r'[0-9]{0,1}[0-9]{1}S',VideoName[1][::-1],flags=I).group(0)[::-1]
                TrueVideoName = VideoName[1].strip(Season)
                Season = search(r'[0-9]{0,1}[0-9]{1}S',VideoName[1][::-1],flags=I).group(0)[::-1].strip('Ss')
                #print(Season)
    elif search(r'季.*?第|[0-9]{0,1}[0-9]{1}S',VideoName[::-1],flags=I) != None :
            Season = search(r'(季.*?第|[0-9]{0,1}[0-9]{1}S)',VideoName[::-1],flags=I).group(0)[::-1]
            TrueVideoName = VideoName.strip(Season)
            Season = search(r'(季.*?第|[0-9]{0,1}[0-9]{1}S)',VideoName[::-1],flags=I).group(0)[::-1].strip('第季Ss')
            if Season.isdigit() == True :
                #print(Season)
                pass
            else:
                digit = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
                Season = digit[Season]
                #print(Season)
    else:
        TrueVideoName = VideoName 
    print(TrueVideoName.strip('-'),Season)
    return Season,Episodes,TrueVideoName,FileType

def GetArgv():
    SavePath,VideoName,Star = argv[1],argv[2],argv[3]
    if Star != '动漫':
        exit()
    return SavePath,VideoName

def AutoMv(SavePath,VideoName,Season,Episodes,VideoTrueName,FileType):
    NewName = f"S{Season}E{Episodes}{FileType}"
    NewVideoDir = f"{VideoTrueName}/Season_01"
    system(f'mkdir -p {SavePath}/{NewVideoDir}')
    sleep(2)
    system(f'mv "/{SavePath}/{VideoName}"  "{SavePath}/{NewVideoDir}/{NewName}"')

def Test(test):
    TitleMatch(test)

test = ' [桜都字幕组] 因为太怕痛就全点防御力了。第2季/ Itai No Wa Iya Nano De Bougyoryoku Ni Kyokufuri Shitai To Omoimasu. S2 [10][ 1080P@60FPS ][简繁内封].mp4'

if test != '':
    Test(test)

elif __name__ == "__main__":
   #sleep(15)
   SavePath,VideoName = GetArgv()
   Season,Episodes,VideoTrueName,FileType = TitleMatch(VideoName)
   AutoMv(SavePath,VideoName,Season,Episodes,VideoTrueName,FileType)

