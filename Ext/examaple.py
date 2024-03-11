
Versions = '0.1.0' # 版本号

def Auxiliary_RMSubtitlingTeam(File):
    if File[0] == '《':# 判断有无字幕组信息
        File = sub(r'《|》','',File,flags=I) 
    else:
        ItemName = findall(r'^=.*?=',File,flags=I)
        File = sub(r'^=.*?=','',File,flags=I)
        Auxiliary_Log(f'字幕组 >> {ItemName}')
    return File

def main(Globals,*ConfigDict):
    global sub,I,findall,Auxiliary_Log
    
    sub = Globals['sub']
    I = Globals['I']
    findall = Globals['findall']
    Auxiliary_Log = Globals['Auxiliary_Log']

    if ConfigDict != ():
        for ConfigName in ConfigDict[0]:
            ConfigValue = ConfigDict[0][ConfigName]
            Auxiliary_Log(f'配置 < {ConfigName} = {ConfigValue}','INFO')
            exec(f'global {ConfigName};{ConfigName} = {ConfigValue}')

    
    Globals['Auxiliary_RMSubtitlingTeam'] = Auxiliary_RMSubtitlingTeam


