class ScopevisioApiIterator:
    """
    Iterator for Personio paged API responses
    """

    def __init__(self, scopevisio_session, url, limit=100, **kwargs):
        self.scopevisio_session = scopevisio_session
        self.url = url
        self.limit = limit
        self.kwargs = kwargs
        self.params = self.kwargs.pop('params', {})

    def __iter__(self):
        self.index = 0
        self.page = None  # last fetched page
        return self

    def __next__(self):
        needed_page = self.index // self.limit
        if self.page != needed_page:
            # fetch next page
            self.page = needed_page
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            payload = {
                'page': self.page,
                'pageSize': self.limit,
                'order': self.kwargs.pop('order', [])
            }
            response = self.scopevisio_session.request_json("POST", self.url, headers=headers,
                                                            json=payload, params=self.params, **self.kwargs)
            self.batch = response['records']
        batch_index = self.index % self.limit
        if batch_index >= len(self.batch):
            raise StopIteration
        next_item = self.batch[batch_index]
        self.index += 1
        return next_item
