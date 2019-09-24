import requests
import re
import json
from lxml import etree
from JS.functions import Decrypy


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'referer': 'https://www.aliwx.com.cn/reader?bid=7940896&cid=1187884'
}

# 遍历图库的所有页，找到所有所有小说的bookID，从而拼接为novel的第一章节url
def run():
    for i in range(1,33):
        url = "https://www.aliwx.com.cn/store?spm=aliwx.list_store.0.0.480534d4Yodj6r&sz=0&fc=0&wd=0&tm=0&st=0&page=" + str(i)
        book_store_resp = requests.get(url=url,headers=headers)
        book_store_ana = etree.HTML(book_store_resp.text)
        as_detail = book_store_ana.xpath("//ul[contains(@class,'store-ul')]//li/a")
        for temp in as_detail:
            book_detail = temp.xpath("./@href")[0]
            book_name = temp.xpath("./@title")[0]
            bookID = re.search("bid=(.*)",book_detail).group(1)
            one_chapter_url = "https://www.aliwx.com.cn/reader?bid=" + str(bookID)
            get_novel(one_chapter_url,book_name,bookID)



# 获取这部小说所有章节的内容的url 循环
        # 规律 [    {卷[{章节}...{}]}    {[{}...{}]}   {[{}...{}]}    ]
        # 利用上述规律可以得到每章{}中的内容
        # 得到｛｝中的内容，可以得到每章url需要的参数：chapterID 、 ver 、 aut不变 、 sign 、 num 、 isFree 、bookid 、 ut 、 章节名字

# 传入小说的第一页url，小说名字（小说名字用于新建txt文件）
# 将小说内容存储进 对应名称的txt文件中
def get_novel(url,novel_name,bookID):
    bookid = bookID
    aut = None
    one_chapter_url = url
    one_chapter_resp = requests.get(url=one_chapter_url, headers=headers)
    # ①所有章节相关参数在一个[]中， 我首先获取这个[]中所有的
    all = re.search("\[.+?chapterId.+\]", one_chapter_resp.text)
    # ②再获取每一卷的所有内容
    juan_contents = re.findall("{.*?\[.*?\]}", all.group())
    for juan_content in juan_contents:
        # ③然后获取每一卷中的[]中所有内容
        temp = re.search("\[.*\]", juan_content).group()
        # ④再获取每一章{}里面所有的内容
        zhang_contents = re.findall("{.*?}", temp)
        for zhang_content in zhang_contents:
            # ⑤从每章中获取我们想要的参数，从而拼接成每章的url
            # 章节名称
            chapterName = re.search("chapterName&quot;:&quot;(.*?)&", zhang_content).group(1)
            # sign
            temp2 = re.findall("sign=.*?&", zhang_content)
            sign = re.search("sign=(.*)&", temp2[len(temp2) - 1]).group(1)
            # ver
            ver = re.search("ver=(.*?)&", zhang_content).group(1)
            # aut ,只需要获取一次作者信息即可
            if aut == None:
                print("获取作者信息")
                aut = re.search("aut=(.*?)&", zhang_content).group(1)
            # chapterID
            chapterId = re.search("chapterId=(.*?)&", zhang_content).group(1)
            # num
            num = re.search("num=(.*?)&", zhang_content).group(1)
            # ut
            ut = re.search(";ut=(.*?)&", zhang_content).group(1)
            #isFree
            isFree = re.search("isFreeRead&quot;:(.*)}",zhang_content).group(1)
            if isFree == "true":
                url4 = 'https://c13.shuqireader.com/pcapi/chapter/contentfree/?bookId=' + str(bookid) + "&chapterId=" + str(
                    chapterId) + "&ut=" + str(ut) + "&num=" + num + "&ver=" + ver + "&aut=" + str(aut) + "&sign=" + str(sign)
                temp3 = requests.get(url=url4, headers=headers)
                if "sign校验失败" in temp3.text:
                    with open(file="失败的小说章节.txt", mode="a", encoding='utf-8') as fp:
                        fp.write("\r\n" + novel_name + chapterName + "\r\n")
                        fp.write("\r\n" + url4 + "\r\n")

                ChapterContent = json.loads(temp3.text)["ChapterContent"]
                p = Decrypy.content_Decrypy(ChapterContent)
                p = re.sub("<br>|<br/>","\r\n",p)  # 将小说的格式更改的可读性更高
                with open(file="{}.txt".format(novel_name), mode="a", encoding='utf-8') as fp:
                    fp.write("\r\n" + chapterName + "\r\n")
                    fp.write(p)
            else:
                with open(file="{}.txt".format(novel_name), mode="a", encoding='utf-8') as fp:
                    fp.write("\r\n" + chapterName + "\r\n")
                    temp = "之后的章节需要付费阅读"
                    fp.write(temp)
                return None


if __name__ == "__main__":
    run()
