#!/bin/python
#Coding="utf-8"

import sys
import requests
from bs4 import BeautifulSoup
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header


# 爬取访问量、排名等信息
def getResult(XUEQIU_STOCK_ID):

    # 先和正常访问一下，到页面获取cookie相关的一些值

    dc_url = "http://guba.eastmoney.com/list," + XUEQIU_STOCK_ID + ".html"
    url = "https://xueqiu.com/S/" + XUEQIU_STOCK_ID
    headers = {
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-language": "zh-CN,zh;q=0.9"
    }

    response = requests.get(dc_url, headers=headers)


    if response.status_code == 200:
        result = {
            "nick_name": "",
            "blog_title": "",
            "profile": {}
        }

        # # 实例化对象
        # session = requests.session()

        # # 发起请求之前，我们可以打印一下session上下文请求对象里面的cookies
        # cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)

        # print(cookies_dict)

        # # 给 requests.session() 对象设置cookie信息
        # session.cookies = requests.utils.cookiejar_from_dict(cookies_dict)

        # print(response.text)

        with open("response.out", 'w', encoding="utf-8") as resText:
            resText.writelines(response.text)


        soup = BeautifulSoup(response.text, "html.parser")
        print(soup)


        art_bodys = soup.find_all("div", attrs={"class": "articleh"})
        
        print(art_bodys)
        for content in art_bodys:
            print("="*20)
            print(content)
            print("*"*20)
            _visits = content.find("span", attrs={"class": "a1"}).get_text().strip()
            print("浏览:", _visits)

            _comments = content.find("span", attrs={"class": "a2"}).get_text().strip()
            print("阅读:", _comments)

            _post = content.find("span", attrs={"class": "a3"}).find("a")

            _title = _post.get_text().strip()
            print("标题:", _title)

            _postId = _post.attrs["href"]
            print("Id:", _postId)

        return



        url2 = "https://stock.xueqiu.com/v5/stock/portfolio/stock/follower_list.json?symbol=" + XUEQIU_STOCK_ID + "&page=1&size=20&anonymous_filter=true"
        response2 = requests.get(url2, headers=headers, cookies=response.cookies)

        with open("response2.out", 'w', encoding="utf-8") as resText:
            resText.writelines(response2.text)

        print(response2.text)

        json_dict = json.loads(response2.text)

        print(json_dict)
        print(json_dict['data']['count'])

        res_result = {
            'follows': json_dict['data']['count']
        }

        res_result_str = json.dumps(res_result)

        with open("res_result.out", 'w', encoding="utf-8") as resResult:
            resResult.writelines(res_result_str)

        ### 把需要的信息整合成json格式.. 方便以no-sql形式保存

        # # 爬取asideProfile信息
        # nick_name = soup.find("a", id="uid").get("title")
        # blog_title = soup.find("a", attrs={"href": url}).get_text().strip()
        # result["nick_name"] = nick_name
        # result["blog_title"] = blog_title

        # profile = {}
        # profile_data = []
        # data_info = soup.find("div", attrs={"class": "data-info d-flex item-tiling"})
        # data = data_info.find_all("dl", attrs={"class": "text-center"})
        # for num in data:
        #     profile_data.append(num.attrs["title"])

        # grade_info = soup.find("div", attrs={"class": "grade-box clearfix"}).contents
        # point = grade_info[5].find("dd").attrs["title"]
        # week_rank = grade_info[3].attrs["title"]
        # total_rank = grade_info[7].attrs["title"]

        # profile["original"] = profile_data[0]
        # profile["fans"] = profile_data[1]
        # profile["like"] = profile_data[2]
        # profile["comment"] = profile_data[3]
        # profile["read"] = profile_data[4]
        # profile["point"] = point
        # profile["week_rank"] = week_rank
        # profile["total_rank"] = total_rank
        # result["profile"] = profile

        return result


# # 生成信息
# def formatMessage(result):
#     return False
#     message = ""
#     call = "亲爱的 " + result["nick_name"] + "，您的 CSDN profile 到啦\n\n"
#     profile = result["profile"]
#     original = "原创文章数目： " + profile["original"] + "\n"
#     fans = "粉丝： " + profile["fans"] + "\n"
#     like = "获赞： " + profile["like"] + "\n"
#     comment = "评论： " + profile["comment"] + "\n"
#     read = "访问量： " + profile["read"] + "\n"
#     point = "积分： " + profile["point"] + "\n"
#     week_rank = "周排名： " + profile["week_rank"] + "\n"
#     total_rank = "总排名： " + profile["total_rank"]

#     message += call + original + fans + like + comment + read + point + week_rank + total_rank
#     return message

def getFollow(XUEQIU_STOCK_ID):

    url = "https://stock.xueqiu.com/v5/stock/portfolio/stock/follower_list.json?symbol=" + XUEQIU_STOCK_ID + "&page=1&size=20&anonymous_filter=true"
    print(url)
    headers = {
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-language": "zh-CN,zh;q=0.9"
    }
    response = requests.get(url, headers=headers, params={'symbol': XUEQIU_STOCK_ID})
    print(response)

    if response.status_code == 200:
        print(response.text)

# # 发送邮件
# def sendEmail(content):
#     message = MIMEText(content, 'plain', 'utf-8')
#     message['From'] = "GitHub Actions<" + sender + ">"
#     message['To'] = "<" + receiver + ">"

#     subject = "CSDN Report"
#     message['Subject'] = Header(subject, 'utf-8')

#     try:
#         smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
#         smtpObj.login(mail_user, mail_password)
#         smtpObj.sendmail(sender, receiver, message.as_string())
#         print("邮件发送成功")

#     except smtplib.SMTPException:
#         print("Error: 无法发送邮件")


# 保存email内容
def saveEmail(email_path, message):
    with open(email_path, 'w', encoding="utf-8") as email:
        email.writelines(message)


if __name__ == "__main__":

    CSDN_ID = sys.argv[1]

    res = getResult(CSDN_ID)
    #message = formatMessage(res)
    #email_path = "email.txt"
    #saveEmail(email_path, message)