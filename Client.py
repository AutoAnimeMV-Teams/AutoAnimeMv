from socket import socket,timeout,SOL_SOCKET,SO_KEEPALIVE
from ast import literal_eval
from sys import argv
from os import environ,path,name,getcwd
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES,PKCS1_v1_5
from base64 import b64encode,b64decode
from time import sleep,time,localtime,strftime
from qbittorrentapi import Client,LoginFailed
from threading import Thread

def QbInit(QbIp,QbPort,QbUserName,QbPassword): 
    QbInfo = dict(
        host=QbIp,
        port=QbPort,
        username=QbUserName,
        password=QbPassword,
        VERIFY_WEBUI_CERTIFICATE=False,# 关闭ssl验证
        RAISE_NOTIMPLEMENTEDERROR_FOR_UNIMPLEMENTED_API_ENDPOINTS=True,# 无Api功能时引发NotImplementedError
    )
    QbClient = Client(**QbInfo)
    try:
        QbClient.auth_log_in()
    except LoginFailed as err:
        Auxiliary_Exit(f'qb登录失败 >> {err}')
    else:
        #print(QbClient.app_version())
        #TorrentInfoData = (QbClient.torrents_info(status_filter='all',offset=0))
        #for Torrent in TorrentInfoData.data:
        #    print(Torrent.name)
        return QbClient

def CatTorrenList(QbClient:Client,Mode='all'):
    TorrenList = []
    TorrentInfoData = (QbClient.torrents_info(status_filter=Mode))
    for Torrent in TorrentInfoData.data:
        if Mode == 'all' or Mode == 'completed':
            TorrenList.append({'Name':Torrent['name'],'Start':strftime("%Y/%m/%d %H:%M:%S",localtime(Torrent['added_on']))})
        elif Mode == 'downloading':
            TorrenList.append({'Name':Torrent['name'],'Start':strftime("%Y/%m/%d %H:%M:%S",localtime(Torrent['added_on'])),'Progress':str(Torrent['progress'])+'%'})
    return TorrenList

def AddTorrent(QbClient,urls,SPath=None):
    if  QbClient.torrents_add(urls,save_path=SPath) == 'Ok.':
        return f'Torrent添加成功'
    else:
        return f'Torrent添加失败'


def AddTo16x(key):# 补全至16的倍数
        key = key.encode() if type(key) == str else key
        new_key = bytearray(key)
        while len(new_key) % 16 != 0:
            new_key.append(0)
        return new_key

def REmEnd0(key):
        return key.rstrip(b"\x00")

def AESEncrypt(Text):
    aes = AES.new(AddTo16x(TGBOTDEVICESFLAG.encode()),AES.MODE_ECB)
    return b64encode(aes.encrypt(AddTo16x(Text)))

def AESDEncrypt(EnText):
    aes = AES.new(AddTo16x(TGBOTDEVICESFLAG.encode()),AES.MODE_ECB)
    return REmEnd0(aes.decrypt(AddTo16x(b64decode(EnText)))).decode()

def RASEncrypt(Text):
    ras = PKCS1_v1_5.new(RSA.importKey(PubilcKey))
    return b64encode(ras.encrypt(Text.encode()))

def MakeClient(Target,OutTime=None,Keep=None):# 创建连接 Target = ('ip',port)
    Client = socket()
    Client.settimeout(None)
    if Keep == True:
        Client.setsockopt(SOL_SOCKET,SO_KEEPALIVE,1)
    Client.connect(Target)
    return Client

def DistributeClient(Ip,DefaultPort):# 分发端口 
    DClient = MakeClient((Ip,DefaultPort),10)
    while True:
        try:
            DClient.sendall(RASEncrypt(TGBOTDEVICESFLAG))
            Data = AESDEncrypt(DClient.recv(1024))
        except timeout:
            Auxiliary_Log('连接超时重试')
            sleep(2)
        else:
            break
    if Data != '':#Data[0] == '(':
        global DistributeData # ('Ip',Port)
        DistributeData = literal_eval(Data)
        Auxiliary_Log(f'获得分发 >> {DistributeData}')
        if DistributeData[0] == '0.0.0.0':
            DistributeData = (Ip,DistributeData[1])
        return DistributeData
    else:
        Auxiliary_Exit('注册失败')

def ConnectClient(DistributeData):# 正式连接
    global QbClient,USERQBAPI
    C = MakeClient(DistributeData,Keep=None)
    #C.sendall(AESEncrypt('ok'.encode()))
    Auxiliary_Log(f'正式链接 >> {DistributeData}')
    while True:
        Auxiliary_Log('等待taskes')
        Data = b' '
        while b' ' in Data:
            Data = C.recv(4096)
            if b' ' not in Data:
                while True:
                    if b'/0000/' in Data:
                            Data = Data.rstrip(b'/0000/')
                            break
        while USERQBAPI == False:
            sleep(60)
        TaskesList = literal_eval(AESDEncrypt(Data))
        Auxiliary_Log(TaskesList)
        TaskesReturnList = {}
        for Taskes in TaskesList:
            Auxiliary_Log(f'Takes >> {Taskes}')
            if 'CatTorrentList' in Taskes:
                TaskesReturnList[Taskes] = CatTorrenList(QbClient,Taskes.replace('CatTorrentList',''))
            elif Taskes == 'AddTorrent':
                TaskesReturnList[Taskes] = AddTorrent(QbClient,urls=TaskesList[Taskes])
        Auxiliary_Log('发送TaskeReturn')
        C.sendall(AESEncrypt(str(TaskesReturnList))+bytes('/0000/'.encode()))


def CMAIN(Ip,DFlag,Lof,DefaultPort=9999,QbIp=None,QbPort=None,QbUserName=None,QbPassword=None): # 主函数
    PubilcKey = '-----BEGIN RSA PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCs64eLxnwfTGW1DEfnbWj5f2clEKPovMdhtxsANwNHIneJoehULfndt64wZDSOY+YvkHhCnK3O4U3+EJhY404PInmoWRqcaDfQi2jzNqfSiUL7Njww0ikSX0Mv+Y+KSSDzqC0SeDoeZo9HvOz5m08098WfvKPcyGzEDIYqFbXK5wIDAQAB\n-----END RSA PUBLIC KEY-----'

def Auxiliary_AddMsgNotice(Msg:bytes):
    global DistributeData
    C2 = MakeClient((DistributeData[0],DistributeData[1]+1))
    C2.sendall(AESEncrypt(Msg)+bytes('/0000/'.encode()))
    Auxiliary_Log('Notice消息已发出')
    C2.close()

def Auxiliary_NoticeS():
    from mmap import mmap,ACCESS_WRITE
    from contextlib import closing
    with open(f"{PyPath}{Separator}CS.dat", "w") as f:
        f.write('\x00' * 1024)
    while True:
        with open(f"{PyPath}{Separator}CS.dat", 'r+') as f:
            with closing(mmap(f.fileno(), 1024, access=ACCESS_WRITE)) as m:
                data = m.read(1024).replace(b'\x00',b'')
                if data != b'':
                    f.write('\x00' * 1024)
                    Auxiliary_AddMsgNotice(data)
                sleep(5)

def Auxiliary_Log(Msg,MsgFlag='INFO',flag=None,end='\n'):# 日志
    global LogData,PRINTLOGFLAG
    Msg = Msg if type(Msg) == tuple else (Msg,)
    for OneMsg in Msg:
        Msg = f'[{strftime("%Y-%m-%d %H:%M:%S",localtime(time()))}] {MsgFlag}: {OneMsg}'
        if PRINTLOGFLAG == True or flag == 'PRINT':
            print(Msg,end=end)         
        LogData = LogData + '\n' + Msg

def Auxiliary_Exit(LogMsg):# 因可预见错误离场
    Auxiliary_Log(LogMsg,'EXIT',flag='PRINT')
    exit()

def Auxiliary_READConfig():
    global PyPath,PRINTLOGFLAG,TGBOTDEVICESFLAG,USERBOTNOTICE,USERQBAPI,QBIP,QBPORT,QBUSERNAME,QBPASSWORD,Separator,QbClient
    USERTGBOT = False # 使用TgBot进行远程管理
    TGBOTDEVICESFLAG = '' # 您的注册码
    USERBOTNOTICE = False # 使用TgBot进行通知
    USERQBAPI = False # 使用QBApi
    QBIP = '' # QB的ip
    QBPORT = 8080 # QBApi端口
    QBUSERNAME = '' # Qb账号
    QBPASSWORD = '' # Qb密码
    #PyPath = argv[0].replace('Client.py','').strip(' ')
    PyPath = getcwd()
    Separator = '\\' if name == 'nt' else '/'
    if path.isfile(f'{PyPath}{Separator}config.ini'):
        with open(f'{PyPath}{Separator}config.ini','r',encoding='UTF-8') as ff:
            Auxiliary_Log('正在读取外置ini文件','INFO')
            T = 0
            for i in ff.readlines():
                i = i.strip('\n') 
                if i[0] != '#' and i != '':
                    ii = i.split("=",1)[0].strip('- ')
                    Auxiliary_Log(f'配置 < {i}','INFO')
                    exec(f'global {ii};{i}')
                    T = T + 1
            if T == 0:
                Auxiliary_Exit('外置ini文件没有配置','WARNING')
            if 'HTTPPROXY' in globals():
                global HTTPPROXY
                environ['http_proxy'] = HTTPPROXY
            if 'HTTPSPROXY' in globals():
                global HTTPSPROXY
                environ['https_proxy'] = HTTPSPROXY
            if 'ALLPROXY' in globals():
                global ALLPROXY
                environ['all_proxy'] = ALLPROXY

            if 'USERQBAPI' in globals() and USERQBAPI == True:
                QbClient = QbInit(QBIP,QBPORT,QBUSERNAME,QBPASSWORD)
                Auxiliary_Log('QB 已连接')
            while True:
                try:
                    DistributeData = DistributeClient(Ip,DefaultPort)
                    if 'USERBOTNOTICE' in globals() and USERBOTNOTICE == True:
                        Auxiliary_Log('共享内存正在监听')
                        Thread(target=Auxiliary_NoticeS).start()
                    ConnectClient(DistributeData)
                except Exception as err:
                    Auxiliary_Log(f'连接失败重试{err}')
                    sleep(10)
    else:
        Auxiliary_Log('不存在config.ini,使用内置变量')   

if __name__ == '__main__':
    Versions = '0.1.1'
    Ip = '103.101.204.76'
    #Ip = '127.0.0.1'
    DefaultPort = 13324
    PubilcKey = '-----BEGIN RSA PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCs64eLxnwfTGW1DEfnbWj5f2clEKPovMdhtxsANwNHIneJoehULfndt64wZDSOY+YvkHhCnK3O4U3+EJhY404PInmoWRqcaDfQi2jzNqfSiUL7Njww0ikSX0Mv+Y+KSSDzqC0SeDoeZo9HvOz5m08098WfvKPcyGzEDIYqFbXK5wIDAQAB\n-----END RSA PUBLIC KEY-----'
    LogData = f'\n\n[{strftime("%Y-%m-%d %H:%M:%S",localtime(time()))}] INFO: Running....'
    PRINTLOGFLAG = True
    Auxiliary_Log((f'当前工具版本为{Versions}',f'当前操作系统识别码为{name},posix/nt/java对应linux/windows/java虚拟机'),'INFO')
    Auxiliary_READConfig()