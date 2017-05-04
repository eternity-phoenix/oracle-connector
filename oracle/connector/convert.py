'''
Oracle数据格式转换
'''
def convert(obj):
    if hasattr(obj, 'ToString'):
        return obj.ToString()
    
    return obj