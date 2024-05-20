import os

from jikeshijian.global_utils import http_post_request, get_comments
from jikeshijian.global_value import directory, API_INFO, API_COMMENTS_PRODUCTS_ALL

course_name = "徐昊 · AI 时代的软件工程"
course_id = ""


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


def get_course_name() -> str:
    payload = {"product_id": course_id, "with_recommend_article": True}
    json_data = http_post_request(API_INFO, payload)
    return json_data["data"]["title"]


if __name__ == "__main__":
    course_id = get_course_id()
    course_name = get_course_name()
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = directory + f"{course_name}.md"
    get_comments(filename, course_id)
