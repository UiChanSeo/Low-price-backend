import json


class CategoryResonse:
    len: int
    categories: []

    def __init__(self, len: int, categories: []):
        self.len = len
        self.categories = categories

    def __del__(self):
        pass

    def __str__(self):
        return f'len={self.len},' + \
            f'categories={self.categories}'

    def toJson(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)
