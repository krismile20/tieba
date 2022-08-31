import requests
from bs4 import BeautifulSoup
import re
import time
 
myHeader = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
}
myCookies = {
    "Cookie": 'BIDUPSID=3E3BDC19B9F4EC45BB167F3A9E29A1CE; PSTM=1661131296; BAIDUID=3E3BDC19B9F4EC45B73DD62E5B6F279C:FG=1; ZFY=IAICUl4k:AYw1KH0ZlIv81RM51FtwEVrWuvUn2qoz93E:C; BAIDUID_BFESS=3E3BDC19B9F4EC45B73DD62E5B6F279C:FG=1; BDUSS=N6UEdJMmxnbjZ5ZjBvRXU1eHV5MFhJZjUxOEl0Z21DZXp2dFNUZ2xERmVHQzlqSVFBQUFBJCQAAAAAAAAAAAEAAAATLpZfRmVybmVteTMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF6LB2NeiwdjRE; BDUSS_BFESS=N6UEdJMmxnbjZ5ZjBvRXU1eHV5MFhJZjUxOEl0Z21DZXp2dFNUZ2xERmVHQzlqSVFBQUFBJCQAAAAAAAAAAAEAAAATLpZfRmVybmVteTMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF6LB2NeiwdjRE; BAIDU_WISE_UID=wapp_1661874154685_717; BA_HECTOR=048585012l812g8g2g0g6sq21hgsf6m17; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; RT="z=1&dm=baidu.com&si=9ec18617-c22b-4ea4-84b0-f3faca8c3793&ss=l7h0e2qb&sl=7&tt=6ge&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=7vt5&ul=7vnx&nu=j83gp33&cl=7vo3&hd=7w0d"; ab_sr=1.0.1_YmMxZGExZWZlMTlhOTAwNmVlOGNhZTMzZTJlNzZkOTZmNjNiMzk5NDFjYmVjOGJmYWViM2RiYWIzMzc4NTYxYmI5M2JhNTk1NDExMGIwZTRhN2E0YjJkMzFlM2Q5MWQ5YjlmZWJlOGI3YmVkNjhhYzAyZTk2MjQxZmVmMTQxNTEwMjI3YTM4ZGFmZDA5YzU5ZDAxMGU3MDhkMzY0YTQ3ZTFhMTU3MjE5YjAxMDY2ZGQ4ZGM3YzNmYjQzNmRhZTlj'
 
}
url = "https://tieba.baidu.com/sign/add"
 
def getTblikes():
    i = 0
    url = "https://tieba.baidu.com/f/like/mylike"
    contain1 = BeautifulSoup(requests.get(url=url, cookies=myCookies, headers=myHeader).text, "html.parser")
 
    if contain1.find("div", attrs={"class": "pagination"}):
        pageNum = len(contain1.find("div", attrs={"class": "pagination"}).findAll("a"))
    else:
        pageNum = 2
    a = 1
    while a < pageNum:
        urlLike = f"https://tieba.baidu.com/f/like/mylike?&pn={a}"
        contain = BeautifulSoup(requests.get(url=urlLike, cookies=myCookies, headers=myHeader).text, "html.parser")
        first = contain.find_all("tr")
        for result in first[1:]:
            second = result.find_next("td")
            name = second.find_next("a")['title']
            singUp(name)
            time.sleep(5)
            i += 1
        a += 1
    print(f"签到完毕！总共签到完成{i}个贴吧")
 
def getTbs(name):
    urls = f"https://tieba.baidu.com/f?kw={name}"
    contain = BeautifulSoup(requests.get(urls, headers=myHeader, cookies=myCookies).text, "html.parser")
    first = contain.find_all("script")
    try:
        second = re.findall('\'tbs\': "(.*?)" ', str(first[1]))[0]
        return second
    finally:
        return re.findall('\'tbs\': "(.*?)" ', str(first[1]))
 
def singUp(tb):
    myDate = {
        "ie": "utf-8",
        "kw": tb,
        "tbs": getTbs(tb)
    }
    resp = requests.post(url, data=myDate, headers=myHeader, cookies=myCookies)
    result = re.findall('"error":"(.*?)"', str(resp.text))[0]
    if result.encode().decode("unicode_escape") == "":
        print(f"在{tb}签到成功了！！")
    else:
        print(f"在{tb}签到失败了，返回信息: " + result.encode().decode("unicode_escape"))
 
getTblikes()
