import http.client
import json
import os
import re
from datetime import datetime

course_name = "职场求生攻略"
# 替换为你的 Cookie
cookie = "your cookie"
# 替换为你的下载目录
directory = "/Users/heshang/Documents/jikeshijian/"
course_id = ""
# 常量定义
BASE_URL = "time.geekbang.org"
API_INFO = "/serv/v3/column/info"
API_COMMENTS = "/serv/v1/my/comments"
API_COMMENTS_PRODUCTS_ALL = "/serv/v1/my/comment/products/all"
HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'DNT': '1',
    'Origin': 'https://time.geekbang.org',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}


def get_course_id() -> str:
    payload = {}
    json_data = http_post_request(API_COMMENTS_PRODUCTS_ALL, payload)
    # 遍历数据中的每个部分寻找匹配的标题
    for section in json_data['data']:
        for item in section['list']:
            if item['title'] == course_name:
                print("找到匹配项:")
                print(f"标题: {item['title']}, ID: {item['id']}")
                return item['id']


def http_post_request(path, payload):
    conn = http.client.HTTPSConnection(BASE_URL)
    HEADERS['Cookie'] = cookie
    conn.request("POST", path, json.dumps(payload), HEADERS)
    response = conn.getresponse()
    if response.status == 200:
        data = response.read()
        return json.loads(data.decode("utf-8"))
    else:
        raise Exception(f"HTTP request failed with status {response.status}")


def get_course_name() -> str:
    payload = {"product_id": course_id, "with_recommend_article": True}
    json_data = http_post_request(API_INFO, payload)
    return json_data["data"]["title"]


def get_comments(filename):
    payload = {"product_id": course_id, "prev": 0, "size": 100, "orderby": "comment_ctime"}
    json_data = http_post_request(API_COMMENTS, payload)
    with open(filename, "w", encoding="utf-8") as file:
        # 遍历 JSON 数据中的每个评论对象
        for comment in json_data["data"]["list"]:
            article_title = comment["article_title"]
            comment_content = comment["comment_content"]
            comment_content = re.sub(r'\n\s*\n', '\n', comment_content)
            comment_ctime = datetime.fromtimestamp(comment["comment_ctime"]).strftime("%Y-%m-%d %H:%M:%S")
            replies = []
            for reply in comment["replies"]:
                reply_content = reply['content']
                # 使用正则表达式去掉回复内容中的多余空行
                reply_content = re.sub(r'\n\s*\n', '\n', reply_content)
                reply_str = f"{reply['user_name']}:{reply_content}"
                replies.append(reply_str)
            replies_str = ",".join(replies)

            # 将格式化后的数据写入 Markdown 文件
            file.write(f"## {article_title}\n")
            file.write(f"- 💭 {comment_content}\n")
            file.write(f"- 🕐 {comment_ctime}\n")
            file.write(f"> 📌 {replies_str}\n\n")

    print(f"数据已成功导出到 {filename} 文件。")


if __name__ == "__main__":
    course_id = get_course_id()
    course_name = get_course_name()
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = directory + f"{course_name}.md"
    get_comments(filename)
