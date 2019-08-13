import requests
import re
import os
import time
from multiprocessing.dummy import Pool
start=time.time()
start_html='https://www.kanunu8.com/book3/6879/'
def get_html(url):  #网页源代码抓取模块
    html = requests.get(url)
    return html.content.decode('gbk') #这个网页需要使用gbk方式解码才能让中文正常显示

def get_toc(html):  #抓取每个章节的网址模块
    toc_block=[]
    toc_list=[]
    toc_html=[]
    toc_block=re.findall('正文(.*?)</tbody>',html,re.S)
    toc_html=re.findall('href="(.*?)"',toc_block[0],re.S)  #注意有toc_block[0]，toc_html是列表
    for ur1 in toc_html:
        toc_list.append(start_html+ur1)
    return toc_list

def get_article(html): #抓取章节标题和内容模块
    chapter_name=re.search('size="4">(.*?)<',html,re.S).group(1)
    text_block=re.search('<p>(.*?)</p>',html,re.S).group(1)
    text_block=text_block.replace('<br />','')
    return chapter_name,text_block
def save(chapter,article):
    os.makedirs('动物农场',exist_ok=True) #创建一个文件夹
    with open(os.path.join('动物农场',chapter+'.txt'),'w',encoding='utf-8') as f: #写文件,目录用os模块中的path.join方法自动生成路径
        f.write(article)                                                         #动物农场/chapter.txt
def every_article(url):   #输入每个章节网址，抓取每个章节然后保存
    article_html = get_html(url)
    chapter_name, article_text = get_article(article_html)
    save(chapter_name, article_text)
if __name__ == '__main__':
    toc_html = get_html(start_html)
    toc_list = get_toc(toc_html)
    pool = Pool(4) #线程池为4
    pool.map(every_article, toc_list)
end=time.time()
print('爬取整个小说耗时：{}\n'.format(end-start))
print('小说可去代码所在目录处查看')
