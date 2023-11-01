
# 提供更多正则表达式来预处理番剧名称
def Auxiliary_RMOTSTR(File):
    NewPSTRFile = File
    #匹配待去除列表
    FuzzyMatchData = [r'(.*?|=)月新番(.*?|=)',r'\d{4}.\d{2}.\d{2}',r'20\d{2}',r'v[2-9]',r'\d{4}年\d{1,2}月番']
    #精准待去除列表
    PreciseMatchData = ['仅限港澳台地区','国漫','x264','1080p','720p','4k','\(-\)','（-）']
    for i in PreciseMatchData:
        NewPSTRFile = sub(r'%s'%i,'-',NewPSTRFile,flags=I)
    for i in FuzzyMatchData:
        NewPSTRFile = sub(i,'-',NewPSTRFile,flags=I)
    return NewPSTRFile

# 预加载函数
def func(GlobalsFunc):
    global GFuncs,sub,I
    GFuncs = GlobalsFunc

    sub = GlobalsFunc['sub']
    I = GlobalsFunc['I']

    return [['Auxiliary_RMOTSTR',Auxiliary_RMOTSTR]]