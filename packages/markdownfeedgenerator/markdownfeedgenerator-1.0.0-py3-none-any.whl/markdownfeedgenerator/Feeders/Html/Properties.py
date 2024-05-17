from markdownfeedgenerator.Feeders.Json.Properties import Default


class Item(Default):
    def __init__(
        self,
        title: str | None = None,
        url: str | None = None
    ):
        Default.__init__(self)

        self.title: str | None = title
        self.url: str | None = url

    def check(
        self
    ):
        if not self.title:
            raise ValueError('You must provide a valid version for "title".')

        if not self.url:
            raise ValueError('You must provide a valid version for "url".')


class Feed(Default):
    def __init__(
        self,
        title: str | None = None,
        next_page_url: str | None = None,
        previous_page_url: str | None = None,
        items: [Item] = None
    ):
        Default.__init__(self)

        if not items:
            items = []

        self.title: str | None = title
        self.next_page_url: str | None = next_page_url
        self.previous_page_url: str | None = previous_page_url
        self.items = items

    def check(
        self
    ):
        if not self.title:
            raise ValueError('You must provide a valid version for "title".')
