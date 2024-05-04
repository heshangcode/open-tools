import http.client
import json
import re
from datetime import datetime

from jikeshijian.global_value import BASE_URL, HEADERS, cookie, API_COMMENTS


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
