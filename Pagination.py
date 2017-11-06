class (object):
    def __init__(self, page, per_page, total_count):
        self.page = int(page)
        self.per_page = int(per_page)
        self.total_count = total_count

    def __dict__(self):
        # itered_pages=list(self.iter_pages())
        return {'has_prev': 1 if self.has_prev else 0,
                'has_next': 1 if self.has_next else 0,
                'page': self.page,
                'per_page': self.per_page,
                'total_count': self.total_count}
    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages