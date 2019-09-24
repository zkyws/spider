#  目标：使用selenium爬取拉勾网关于'python爬虫'相关职位信息
#  职位信息中需要包括：薪资、岗位需求、公司名称、职位名称
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # 等待
from selenium.webdriver.support import expected_conditions # 等待条件
from selenium.webdriver.common.by import By # 元素类型
from lxml import etree
import re
from selenium.webdriver.chrome.options import Options

job_details = []  # 存储信息的列表
number = 1  # 用来统计职位的数量


# 初始化浏览器驱c动
chormedriver_path = r"D:\迅雷下载\chrome_driver\chromedriver.exe"
# 设置为无界面模式
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# 打开拉勾的官网首页
html_driver = webdriver.Chrome(executable_path=chormedriver_path,options=chrome_options)


html_driver.get(r"https://www.lagou.com/")

# 找到搜索输入框

# 等待  直到search_input元素被找到
# 输入 python爬虫
# 点击搜索（会重定向到新的页面）
city_box = WebDriverWait(html_driver, 30).until(expected_conditions.presence_of_element_located((By.ID, 'cboxClose')))
city_box.click()
time.sleep(1)  # 两个等待之间要至少等待1s
input_box = WebDriverWait(html_driver, 60).until(expected_conditions.presence_of_element_located((By.ID, 'search_input')))
    #input_box = html_driver.find_element_by_id('search_input')
input_box.send_keys('python')
confirm_box = html_driver.find_element_by_id('search_button')
confirm_box.click()


while True:
    # 获取当前页面的页面内容
    html_text = html_driver.page_source
    html_analysis = etree.HTML(html_text)
    urls = html_analysis.xpath("//a[@class='position_link']/@href")

    # 获取每一个职位对应的url，并针对每一个职位信息页面做以下操作
    # start循环
    # 打开职位对应的url新页面，并跳转到新页面
    for url in urls:
        job_detail = {} # 存储一个职位的具体各方面的信息 ，字典
        #html_driver.execute_script("window.open('" + url + "')")
        html_driver.execute_script("window.open('%s')"%(url))
        html_driver.switch_to.window(html_driver.window_handles[1])
    # 提取我们需要的数据
        job_text = html_driver.page_source
        job_analysis = etree.HTML(job_text)

        job_require = job_analysis.xpath("//dd[@class='job_bt']//text()")   #因为有很多/n 所以先转换为str，然后去掉多余的换行
        string = ""
        for xx in job_require:
            string += str(xx)
        string = re.sub(" ", "", string)
        string = re.sub("\\xa0", "", string)
        string = re.sub("\n\n", "\n", string)
        string = string.strip()
        job_detail['job_require'] = string   # 职位要求

        job_salary = job_analysis.xpath("//span[@class='salary']/text()")  # 职位薪资
        job_detail['job_salary'] = job_salary[0].strip()
        job_company = job_analysis.xpath("//em[@class='fl-cn']/text()")  # 所属公司
        job_detail['job_company'] = job_company[0].strip()
        job_name = job_analysis.xpath("//h2[@class='name']/text()")  # 职位名称
        job_detail['job_name'] = job_name[0].strip()

        with open(file='jobs_python.txt', mode='a', encoding='utf-8', ) as temp:
            string = ""
            str0 = str(number)
            str1 = 'job_company: ' + job_detail['job_company']
            str2 = 'job_name: ' + job_detail['job_name']
            str3 = 'job_salary: ' + job_detail['job_salary']
            str4 = 'job_require: ' + job_detail['job_require']
            string = str0 + '\n' + str1 + '\n' + str2 + '\n' + str3 + '\n' + str4 + '\n\n'
            temp.write(string)
            number += 1

        # 关闭职位信息页面，跳转回到查询结果页面
        html_driver.close()
        html_driver.switch_to.window(html_driver.window_handles[0])
    # end循环

    # 找到下一页的点击按钮元素
    # 查看是否可用

    # 点击下一页（如果下一页还能够点击的情况下）

    next_page_disable = html_driver.find_elements_by_class_name('pager_next_disabled')
    next_page_enable = html_driver.find_elements_by_class_name('pager_next ')
    print(len(next_page_disable))
    print(len(next_page_enable))
    if len(next_page_disable) == 1:
        break
    else:
        next_page_enable[0].click()
        time.sleep(20)




