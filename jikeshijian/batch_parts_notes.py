import http.client

from jikeshijian.get_single_notes import fw_parts_notes
from jikeshijian.global_utils import http_post_request
from jikeshijian.global_value import API_NOTE_PRODUCTS

conn = http.client.HTTPSConnection("time.geekbang.com")
payload = {"type": 1, "note_type": 0, "filters": [1]}
json_data = http_post_request(API_NOTE_PRODUCTS, payload)
products_ = json_data["data"]["products"]
for product in products_:
    title_ = product["title"]
    course_id = product["id"]
    # print(f"标题: {title_}, ID: {course_id}")
    fw_parts_notes(title_, course_id)
