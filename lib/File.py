import json


class File:
    def write_json(path: str, data):
        f = open(path, "w", encoding="utf8")
        f.write(
            json.dumps(
                data,
                default=lambda obj: obj.__dict__,
                ensure_ascii=False
            )
        )
        f.close()
