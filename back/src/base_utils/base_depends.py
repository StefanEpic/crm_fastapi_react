from fastapi import Query


class Pagination:
    def __init__(self, skip: int = 0, limit: int = Query(default=100, lte=100)):
        self.skip = skip
        self.limit = limit
