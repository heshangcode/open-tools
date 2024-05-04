import http.client
import json

def parse_data(data):
    parsed_data = json.loads(data.decode("utf-8"))["data"]
    articles = parsed_data["articles"]
    notes = parsed_data["list"]

    results = {}

    # 解析 articles
    for article in articles:
        title = article["title"]
        article_id = article["id"]
        summary = article["summary"]
        results.setdefault(title, []).append({"id": article_id, "summary": summary, "parts": []})

    # 解析 notes
    for note in notes:
        part = note["part"]
        article_id = note["article_id"]
        for entry in results.values():
            matched_article = next((article for article in entry if article["id"] == article_id), None)
            if matched_article:
                matched_article["parts"].append(part)
                break
        else:
            print(f"部分: {part}, ID: {article_id} (未找到对应文章)")

    return results

conn = http.client.HTTPSConnection("time.geekbang.com")
payload = json.dumps({
    "prev": 0,
    "size": 1000,
    "type": 0,
    "pid": 100755401,
    "sort": 2,
    "filters": [
        2
    ]
})
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': 'gksskpitn=fde5c301-9699-41ac-a338-63419c433b2b; gk_process_ev={%22count%22:1%2C%22utime%22:1713617107952%2C%22referrer%22:%22%22}; LF_ID=a8d0086-181dce9-74d41af-40726db; _ga=GA1.2.502936903.1713617109; _ga_JW698SFNND=GS1.2.1713617109.1.0.1713617109.0.0.0; tfstk=fnGrTQi_5WmbJTk30oNUQIM2G4F895KsZXZQ-203Puqke3EEYVifOJcWy6-EYDyIV2x-YXrmJ4iSRYMFyjoNO_tJe2fUOWx6fCOsyLFLth_BLO2_2y30x_uyk5u89WxbSqNjk4navG26UWY4iyaTrWq3qEr05ofu-_4hmEzLmkV3q640izUOK92htfNrKY1428xW9h4Ykt7bEl0uq4gSi-I_j4VRt6qzz8kqro5htjHYPKx0bIS0c20tK-leGsFKlAoEKmYhtkk07czsVIfztxmq_R0vb_Ern0hUNRdF8rkZo0lSue6qYm0tB7ckv_Z-Kqc3cbYCTlDsWSzxOnCuYxDnN8Fdq3zqaVlELg-NvrvnMXLo-9yukrr6uEAK6fITGX7in9BL3oU4fFYGp9eufrr6uqWdp8I4ulT7P; _itt=1; GCID=c71a56e-45193f6-c043381-a4641ef; GRID=c71a56e-45193f6-c043381-a4641ef; Hm_lvt_59c4ff31a9ee6263811b23eb921a5083=1714088426; Hm_lvt_022f847c4e3acd44d4a2481d9187f1e6=1714088426; GCESS=BgcE7svtpwoEAAAAAAIEdEEsZgsCBgAMAQEBCFj9GQAAAAAABQQAAAAAAwR0QSxmBgQsDHQ5CAEDCQEBDQEBBAQAjScA; _gid=GA1.2.1286236226.1714780414; Hm_lpvt_59c4ff31a9ee6263811b23eb921a5083=1714782668; Hm_lpvt_022f847c4e3acd44d4a2481d9187f1e6=1714782668; __tea_cache_tokens_20000743={%22web_id%22:%227361953727827298049%22%2C%22user_unique_id%22:%221703256%22%2C%22timestamp%22:1714782668275%2C%22_type_%22:%22default%22}; _ga_03JGDGP9Y3=GS1.2.1714782648.4.1.1714782668.0.0.0; SERVERID=1fa1f330efedec1559b3abbcb6e30f50|1714783589|1714782098; SERVERID=1fa1f330efedec1559b3abbcb6e30f50|1714783740|1714782098',
    'DNT': '1',
    'Origin': 'https://time.geekbang.com',
    'Referer': 'https://time.geekbang.com/dashboard/notes',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}
conn.request("POST", "/serv/v3/note/list", payload, headers)
res = conn.getresponse()
data = res.read()
results = parse_data(data)
for title, entries in results.items():
    print(f"## {title}")
    for entry in entries:
        article_id = entry["id"]
        summary = entry["summary"]
        parts = entry["parts"]
        print(f"- 摘要📒 {summary}")
        for part in parts:
            print()
            print(f"> 📝{part}")
        # print(f"  ID: {article_id}, 部分: {parts}, 摘要: {summary}")
# for result in results:
#     title = result["title"]
#     article_id = result["id"]
#     summary = result["summary"]
#     part = result.get("part", "")  # 如果没有 part 则为空字符串
#     print(f"## {title}")
#     print(f"摘要 {summary}")
#     print(f"> {part}")


    # print(f"标题: {title},  部分: {part}, 摘要: {summary}")
#
# articles = json.loads(data.decode("utf-8"))["data"]["articles"]
# for article in articles:
#     title = article["title"]
#     article_id = article["id"]
#     summary = article["summary"]
#     print(f"标题: {title}, ID: {article_id}, 摘要: {summary}")
#
# notes = json.loads(data.decode("utf-8"))["data"]["list"]
# for note in notes:
#     part = note["part"]
#     article_id = note["article_id"]
#     print(f"标题: {part}, ID: {article_id}")
