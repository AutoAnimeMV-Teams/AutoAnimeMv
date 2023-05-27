from AutoAnimeMv import AttributesMatch
from ast import literal_eval

def Log(mess):
    #print(mess)
    pass
def Test():
    print(f"现在进入Test mode,正在read test文件")
    with open(f'test','r',encoding='utf-8') as ff:
        for TestData in ff.readlines():
            TestData = TestData.strip()
            if TestData != None:
                TestData = literal_eval(TestData.strip())
                Season,Episodes,TrueVideoName,FileType = AttributesMatch(TestData['Bt'])
                print(Season,Episodes,TrueVideoName.replace('-',' '),FileType)
                if TrueVideoName.replace('-',' ') == TestData["Name"] and Season == TestData['Season'] and Episodes == TestData['Episodes'] and FileType == TestData['FileType']:
                    print(f'{TestData}....Ok')
                else:
                    print(f'{TestData}....No')
if __name__ == '__main__':
    Test()