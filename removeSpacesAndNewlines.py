#删除字符串中空格和回车
def removeSpacesAndNewlines(s):
    # 替换空格
    s = s.replace(" ", "")
    # 替换回车
    s = s.replace("\n", "")
    # 替换制表符
    s = s.replace("\t", "")
    return s

if __name__ == "__main__":
    test="ds  a f   ds "
    test=removeSpacesAndNewlines(test)
    print(test)
