from xml.dom import minidom
from fontTools.ttLib import TTFont
import re

# 将本地图像模型转化为xml文件
# font3 = TTFont(r"C:\Users\zhangk\Desktop\61\1\ChcCQ1sUz1mARY5zAABj6AkntG440..ttf")
# font3.saveXML("qiche3.xml")


# 获取作为参照的xml中所有点的坐标
def get_ptsxy(xmlPath, name):
    ptsxy = []
    domobj = minidom.parse(xmlPath)
    TTGlyphs = domobj.getElementsByTagName("TTGlyph")
    for TTGlyph in TTGlyphs:
        if TTGlyph.getAttribute("name") == name:
            pts = TTGlyph.getElementsByTagName("pt")
            for pt in pts:
                ptsxy.append([pt.getAttribute("x"), pt.getAttribute("y")])
    return ptsxy

# 比较两个图像的像素点  x、y坐标的差值，从而判定两个图像是否代表的同一个字符 返回True False
def compare_ptsxy(ptsxy_A,ptsxy_B):
    isSame = True
    for i in range(0,len(ptsxy_A)):
        x_comp = abs(int(ptsxy_A[i][0]) - int(ptsxy_B[i][0]))
        y_comp = abs(int(ptsxy_A[i][1]) - int(ptsxy_B[i][1]))
        if x_comp > 55 | y_comp >55:
            isSame = False
            return isSame
    return isSame

# 建立对应关系
rel = {
    "了" : get_ptsxy("qiche1.xml","uniED1A"),
    "上" : get_ptsxy("qiche1.xml","uniEC66"),
    "和" : get_ptsxy("qiche1.xml","uniEDA7"),
    "九" : get_ptsxy("qiche1.xml","uniEDF9"),
    "三" : get_ptsxy("qiche1.xml","uniED45"),
    "大" : get_ptsxy("qiche1.xml","uniEC92"),
    "一" : get_ptsxy("qiche1.xml","uniECE4"),
    "好" : get_ptsxy("qiche1.xml","uniEC30"),
    "着" : get_ptsxy("qiche1.xml","uniEC82"),
    "少" : get_ptsxy("qiche1.xml","uniEDC3"),
    "二" : get_ptsxy("qiche1.xml","uniED0F"),
    "小" : get_ptsxy("qiche1.xml","uniED61"),
    "长" : get_ptsxy("qiche1.xml","uniECAE"),
    "呢" : get_ptsxy("qiche1.xml","uniEDEE"),
    "矮" : get_ptsxy("qiche1.xml","uniEC4C"),
    "不" : get_ptsxy("qiche1.xml","uniED8D"),
    "八" : get_ptsxy("qiche1.xml","uniEDDE"),
    "得" : get_ptsxy("qiche1.xml","uniED2B"),
    "近" : get_ptsxy("qiche1.xml","uniEC78"),
    "右" : get_ptsxy("qiche1.xml","uniECC9"),
    "四" : get_ptsxy("qiche1.xml","uniEE0A"),
    "十" : get_ptsxy("qiche1.xml","uniED57"),
    "远" : get_ptsxy("qiche1.xml","uniEDA8"),
    "更" : get_ptsxy("qiche1.xml","uniECF5"),
    "的" : get_ptsxy("qiche1.xml","uniED47"),
    "高" : get_ptsxy("qiche1.xml","uniEC93"),
    "六" : get_ptsxy("qiche1.xml","uniEDD4"),
    "很" : get_ptsxy("qiche1.xml","uniEC32"),
    "多" : get_ptsxy("qiche1.xml","uniED72"),
    "左" : get_ptsxy("qiche1.xml","uniECBF"),
    "短" : get_ptsxy("qiche1.xml","uniED11"),
    "五" : get_ptsxy("qiche1.xml","uniEC5D"),
    "是" : get_ptsxy("qiche1.xml","uniECAF"),
    "七" : get_ptsxy("qiche1.xml","uniEDF0"),
    "地" : get_ptsxy("qiche1.xml","uniED3C"),
    "坏" : get_ptsxy("qiche1.xml","uniED8E"),
    "下" : get_ptsxy("qiche1.xml","uniECDB"),
    "低" : get_ptsxy("qiche1.xml","uniEC28")
}

if __name__ == "__main__":
    # temp为获取网页中使用自定义字体的网页代码
    temp = "&#xecbf"  # 输入你想要测试的字符
    temp = re.sub("&#X","uni",temp.upper())
    Now_ptsxy = get_ptsxy("qiche3.xml",temp)
    if len(Now_ptsxy) >0 :
        for i in rel.keys():
            if compare_ptsxy(Now_ptsxy,rel.get(i)):
                print(i)
    else:
        print("字符与下载的文件不能匹配")


