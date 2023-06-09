from requests import get
from os import path,getcwd,chdir
from ast import literal_eval

#config
AutoAnimeMvPath = 'AutoAnimeMv.py'#如果你看不懂下面的code就不要改

def FileWrite(FileName,FileData):
    with open(FileName,'w+',encoding='utf-8') as ff:
        ff.write(FileData)

def Update(File):
    for i in File:
        UpdateUrl = UpdateURL + i
        try:
            data = get(UpdateUrl)
        except:
            print(f'{UpdateUrl}get失败')
        else:
            if data.status_code == 200:
                Filedata = data.text
                FileWrite(i,Filedata)
            else:
                print('get返回码！=200')

def CheckUpdate():
    CheckUpdateUrl = UpdateURL + 'update' 
    chdir(getcwd())
    try:
        data = get(CheckUpdateUrl)
    except:
        print(f'{CheckUpdateUrl}get失败')
    else:
        if data.status_code == 200 and data.text != '':
            data = literal_eval(data.text)
    if path.isfile(AutoAnimeMvPath):
        from AutoAnimeMv import V
        if V == data[V]:
           print('最新版不需要更新')
        else:
            Update(data['File'])
    else:
        Update(['AutoAnimeMv.py'])

if __name__ == '__main__':
    UpdateURL = 'https://raw.githubusercontent.com/Abcuders/AutoAnimeMv/main/'
    CheckUpdate()