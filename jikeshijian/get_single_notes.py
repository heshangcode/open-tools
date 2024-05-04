import os
from datetime import datetime

from global_utils import parse_notes_data, http_post_request
from jikeshijian.global_value import API_NOTE_LIST, directory


def get_parts_notes(payload):
    data = http_post_request(API_NOTE_LIST, payload)
    results = parse_notes_data(data)
    formatted_results = []
    for title, entries in results.items():
        formatted_title = {"title": title, "entries": []}
        for entry in entries:
            summary = entry["summary"]
            parts = entry["parts"]
            notes = entry["notes"]
            score = entry["score"]
            time = datetime.fromtimestamp(score).strftime("%Y-%m-%d %H:%M:%S")
            formatted_entry = {
                "summary": summary,
                "parts": parts,
                "notes": notes,
                "time": time
            }
            formatted_title["entries"].append(formatted_entry)
        formatted_results.append(formatted_title)
    return formatted_results


def get_my_notes(course_id):
    payload = {"prev": 0, "size": 1000, "type": 0, "pid": course_id, "sort": 2, "filters": [2]}
    return get_parts_notes(payload)


def get_parts(course_id):
    payload = {"prev": 0, "size": 1000, "type": 0, "pid": course_id, "sort": 2, "filters": [1]}
    return get_parts_notes(payload)


def fw_parts_notes(title, course_id):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = directory + f"{title}.md"
    with open(filename, "w", encoding="utf-8") as file:
        partes = get_parts(course_id)
        # print(f"# 划线")
        file.write(f"# 划线\n")
        for part in partes:
            # print(f"## {part['title']}")
            for entry in part['entries']:
                summary = entry["summary"]
                parts = entry["parts"]
                # print(f"- 📒摘要 {summary}")
                file.write(f"## {part['title']}\n")
                for part in parts:
                    # print(f"> {part}")
                    file.write(f"> {part}\n\n")
                    # print()

        # 循环遍历打印 get_my_notes() 的返回值
        # print(f"# 我的笔记")
        file.write(f"# 我的笔记\n")
        my_notes = get_my_notes(course_id)
        for note in my_notes:
            # print(f"## {note['title']}")
            file.write(f"## {note['title']}\n")
            for entry in note['entries']:
                summary = entry["summary"]
                parts = entry["parts"]
                notes = entry["notes"]
                # print(f"- 📒摘要 {summary}")
                file.write(f"- 📒摘要 {summary}\n")
                # print(f"> {parts[0]}")
                file.write(f"> {parts[0]}\n\n")
                # print()
                # print(f"🎯{notes[0]}")
                file.write(f"🎯{notes[0]}\n")

    print(f"数据已成功导出到 {filename} 文件。")


if __name__ == '__main__':
    fw_parts_notes("职场求生攻略", 100052201)
