'''
Oracle数据格式转换 暂时都全转为str
'''
def convert(obj):
    if hasattr(obj, 'ToString'):
        return obj.ToString()

    return obj