import json
import os
from datetime import datetime

from global_utils import parse_notes_data, http_post_request
from jikeshijian.global_value import API_NOTE_LIST, directory


def get_notes_parts(course_id, prev=0, results=None):
    if results is None:
        results = []
    payload = {"prev": prev, "size": 100, "type": 0, "pid": course_id, "sort": 2, "filters": []}
    data = http_post_request(API_NOTE_LIST, payload)
    result, prev = parse_notes_data(data)
    if len(data["data"]["list"]) < 100:
        results.extend(result)
        return results
    results.extend(result)
    return get_notes_parts(course_id, prev, results)


def fw_parts_notes(title, course_id):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = directory + f"{title}.md"
    with open(filename, "w", encoding="utf-8") as file:
        parts_notes = get_notes_parts(course_id, 0, [])
        partes_dict = [part.to_dict() for part in parts_notes]
        # print(json.dumps(partes_dict, indent=2))
        # print(f"# 划线")
        file.write(f"# 划线和笔记\n")
        for chapter in parts_notes:
            chapter_name = chapter.chapter_name
            parts = chapter.parts
            notes = chapter.notes
            file.write(f"## {chapter_name}\n")
            for part in parts:
                file.write(f"> {part.content}\n\n")
                # file.write(f"⏰ {part.time}\n\n")
                file.write("\n")

            for note in notes:
                file.write(f"> {note.content}\n\n")
                file.write(f"- 🎯{note.note}\n\n")
                # file.write(f"⏰ {note.time}\n\n")
                file.write("\n")

    print(f"数据已成功导出到 {filename} 文件。")


if __name__ == '__main__':
    fw_parts_notes("从0开始学微服务", 100014401)
