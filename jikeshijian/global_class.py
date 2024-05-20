class PartNote:
    def __init__(self, chapter_id, chapter_name, parts, notes, comments):
        self.chapter_id = chapter_id
        self.chapter_name = chapter_name
        self.parts = parts  # parts is a list of Part objects
        self.notes = notes  # notes is a list of Note objects
        self.comments = comments  # comments is a list of Comment objects

    def to_dict(self):
        return {
            "chapter_id": self.chapter_id,
            "chapter_name": self.chapter_name,
            "parts": [part.to_dict() for part in self.parts],
            "notes": [note.to_dict() for note in self.notes],
            "comments": [comment.to_dict() for comment in self.comments]
        }

    def __repr__(self):
        return f"PartNote(chapter_id={self.chapter_id}, chapter_name={self.chapter_name}, parts={self.parts}, notes={self.notes}, comments={self.comments})"
class Part:
    def __init__(self, content, time):
        self.content = content
        self.time = time

    def to_dict(self):
        return {
            "content": self.content,
            "time": self.time
        }

    def __repr__(self):
        return f"Part(content={self.content}, time={self.time})"

class Note:
    def __init__(self, content, note, time):
        self.content = content
        self.note = note
        self.time = time

    def to_dict(self):
        return {
            "content": self.content,
            "note": self.note,
            "time": self.time
        }

    def __repr__(self):
        return f"Note(content={self.content}, time={self.time})"

class Comment:
    def __init__(self, message, time, author_reply):
        self.message = message
        self.time = time
        self.author_reply = author_reply

    def to_dict(self):
        return {
            "message": self.message,
            "time": self.time,
            "author_reply": self.author_reply
        }

    def __repr__(self):
        return f"Comment(message={self.message}, time={self.time}, author_reply={self.author_reply})"