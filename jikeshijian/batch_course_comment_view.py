import http.client
import json
import re
from datetime import datetime

# 替换为你的 Cookie
cookie = "gksskpitn=fde5c301-9699-41ac-a338-63419c433b2b; gk_process_ev={%22count%22:1%2C%22utime%22:1713617107952%2C%22referrer%22:%22%22}; LF_ID=a8d0086-181dce9-74d41af-40726db; _ga=GA1.2.502936903.1713617109; _ga_JW698SFNND=GS1.2.1713617109.1.0.1713617109.0.0.0; tfstk=fnGrTQi_5WmbJTk30oNUQIM2G4F895KsZXZQ-203Puqke3EEYVifOJcWy6-EYDyIV2x-YXrmJ4iSRYMFyjoNO_tJe2fUOWx6fCOsyLFLth_BLO2_2y30x_uyk5u89WxbSqNjk4navG26UWY4iyaTrWq3qEr05ofu-_4hmEzLmkV3q640izUOK92htfNrKY1428xW9h4Ykt7bEl0uq4gSi-I_j4VRt6qzz8kqro5htjHYPKx0bIS0c20tK-leGsFKlAoEKmYhtkk07czsVIfztxmq_R0vb_Ern0hUNRdF8rkZo0lSue6qYm0tB7ckv_Z-Kqc3cbYCTlDsWSzxOnCuYxDnN8Fdq3zqaVlELg-NvrvnMXLo-9yukrr6uEAK6fITGX7in9BL3oU4fFYGp9eufrr6uqWdp8I4ulT7P; _itt=1; GCID=c71a56e-45193f6-c043381-a4641ef; GRID=c71a56e-45193f6-c043381-a4641ef; Hm_lvt_59c4ff31a9ee6263811b23eb921a5083=1714088426; Hm_lvt_022f847c4e3acd44d4a2481d9187f1e6=1714088426; GCESS=BgcE7svtpwoEAAAAAAIEdEEsZgsCBgAMAQEBCFj9GQAAAAAABQQAAAAAAwR0QSxmBgQsDHQ5CAEDCQEBDQEBBAQAjScA; _gid=GA1.2.1286236226.1714780414; _gat=1; Hm_lpvt_59c4ff31a9ee6263811b23eb921a5083=1714780417; Hm_lpvt_022f847c4e3acd44d4a2481d9187f1e6=1714780417; __tea_cache_tokens_20000743={%22web_id%22:%227361953727827298049%22%2C%22user_unique_id%22:%221703256%22%2C%22timestamp%22:1714780416981%2C%22_type_%22:%22default%22}; SERVERID=1fa1f330efedec1559b3abbcb6e30f50|1714780417|1714780412; _ga_03JGDGP9Y3=GS1.2.1714780414.3.1.1714780417.0.0.0"
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


def get_comments_all_courses() -> dict:
    payload = {}
    json_data = http_post_request(API_COMMENTS_PRODUCTS_ALL, payload)
    return json_data


def get_course_id(course_name) -> str:
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
    print(json_data)
    return json_data["data"]["title"]


def get_comments(filename, course_id):
    payload = {"product_id": course_id, "prev": 0, "size": 100, "orderby": "comment_ctime"}
    json_data = http_post_request(API_COMMENTS, payload)
    # print(json.dumps(json_data, indent=2, ensure_ascii=False))
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
    # course_id = get_course_id()
    comments_all_courses = get_comments_all_courses()
    for section in comments_all_courses['data']:
        for item in section['list']:
            title_ = item['title']
            course_id = item['id']
            filename = f"{title_}.md"
            get_comments(filename, course_id)
            # if course_name != "" and title_ == course_name:
            #     print("找到匹配项:")
            #     print(f"标题: {title_}, ID: {course_id}")
            #     filename = f"{title_}.md"
            #     get_comments(filename, course_id)
            # else:
            #     filename = f"{title_}.md"
            #     get_comments(filename, course_id)
