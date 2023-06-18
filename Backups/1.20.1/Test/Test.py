#!/usr/bin/python3
#coding:utf-8
from AutoAnimeMv import AttributesMatch,Log
from ast import literal_eval

def Test():
    Log(f"现在进入Test mode,正在read test文件")
    with open(f'test','r',encoding='utf-8') as ff:
        for TestData in ff.readlines():
            TestData = TestData.strip()
            if TestData != '' and TestData[0] != '#':
                TestData = literal_eval(TestData.strip())
                if TestData['Bt'] != '':
                    Season,Episodes,TrueVideoName,FileType,a,b,c = AttributesMatch(TestData['Bt'])
                    if TrueVideoName == TestData["Name"] and Season == TestData['Season'] and Episodes == TestData['Episodes'] and FileType == TestData['FileType']:
                        print(f'{TestData}....Ok\n ')
                    else:
                        print(f'{TestData}....No\n')
if __name__ == '__main__':
    Test()