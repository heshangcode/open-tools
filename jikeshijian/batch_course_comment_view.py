import os

from jikeshijian.global_utils import http_post_request, get_comments
from jikeshijian.global_value import directory, API_INFO, API_COMMENTS_PRODUCTS_ALL


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


def get_course_name() -> str:
    payload = {"product_id": course_id, "with_recommend_article": True}
    json_data = http_post_request(API_INFO, payload)
    print(json_data)
    return json_data["data"]["title"]


if __name__ == "__main__":
    comments_all_courses = get_comments_all_courses()
    for section in comments_all_courses['data']:
        for item in section['list']:
            title_ = item['title']
            course_id = item['id']
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename = directory + f"{title_}.md"
            get_comments(filename, course_id)
