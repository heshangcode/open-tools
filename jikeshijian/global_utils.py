import http.client
import json
import os
import re
from datetime import datetime

from jikeshijian.global_value import BASE_URL, HEADERS, cookie, API_COMMENTS


def generate_curl_command(path, payload):
    # Constructing the cURL command string
    curl_cmd = f"curl -X POST https://{BASE_URL}{path} "
    curl_cmd += "-H 'Content-Type: application/json' "
    for header, value in HEADERS.items():
        curl_cmd += f"-H '{header}: {value}' "
    if 'Cookie' in HEADERS:
        curl_cmd += f"-H 'Cookie: {HEADERS['Cookie']}' "
    curl_cmd += f"-d '{json.dumps(payload)}'"
    return curl_cmd

def http_post_request(path, payload):
    conn = http.client.HTTPSConnection(BASE_URL)
    HEADERS['Cookie'] = cookie
    conn.request("POST", path, json.dumps(payload), HEADERS)
    curl_command = generate_curl_command(path, payload)
    # print(f"正在发送请求: {curl_command}")
    response = conn.getresponse()
    if response.status == 200:
        data = response.read()
        return json.loads(data.decode("utf-8"))
    else:
        raise Exception(f"HTTP request failed with status {response.status}")

def get_comments(filename, course_id):
    payload = {"product_id": course_id, "prev": 0, "size": 100, "orderby": "comment_ctime"}
    json_data = http_post_request(API_COMMENTS, payload)

    # 打开文件,读取内容
    with open(filename, 'r+', encoding='utf-8') as file:
        content = file.read()

        # 检查是否存在一级标题"我的留言"
        heading_pattern = r'^# 我的留言\n(.*?)(^# |$)'
        match = re.search(heading_pattern, content, re.DOTALL | re.MULTILINE)

        if match:
            # 如果存在,则删除对应内容
            start, end = match.span(1)
            new_content = content[:start] + '\n' + content[end:]
        else:
            new_content = content + '\n\n# 我的留言\n'

        # 将文件指针移动到开头
        file.seek(0)
        file.truncate()  # 清空文件内容

        # 写入新内容
        file.write(new_content)

        # 遍历 JSON 数据中的每个评论对象
        for comment in json_data["data"]["list"]:
            article_title = comment["article_title"]
            comment_content = comment["comment_content"]
            comment_content = re.sub(r'\n\s*\n', '\n', comment_content)
            comment_ctime = datetime.fromtimestamp(comment["comment_ctime"]).strftime("%Y-%m-%d %H:%M:%S")
            replies = []
            for reply in comment["replies"]:
                reply_content = reply['content']
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

def parse_notes_data(data):
    parsed_data = data["data"]
    articles = parsed_data["articles"]
    list = parsed_data["list"]

    results = {}

    # 解析 articles
    for article in articles:
        title = article["title"]
        article_id = article["id"]
        summary = article["summary"]
        results.setdefault(title, []).append({"id": article_id, "summary": summary, "parts": [], "notes": []})

    # 解析 notes
    for single in list:
        part = single["part"]
        note = single["note"]
        article_id = single["article_id"]
        for entry in results.values():
            matched_article = next((article for article in entry if article["id"] == article_id), None)
            if matched_article:
                matched_article["parts"].append(part)
                matched_article["notes"].append(note)
                break
        else:
            print(f"部分: {part}, ID: {article_id} (未找到对应文章)")

    return results
