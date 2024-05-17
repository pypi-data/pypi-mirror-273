from markdownfeedgenerator.MarkdownFile import MarkdownFile


class Default:
    """
    Default property class.
    """

    def __init__(
        self
    ):
        if type(self) == Default:
            raise Exception("Default property class must be subclassed.")

        self.extensions = {}

    def add(
        self,
        key: str,
        value
    ):
        """
        Add a property value. If the property is part of the object dict, set that. If it is not, add it as an
        extension based value (_key = value).
        """
        if isinstance(value, Default):
            value = value.dump()

        if hasattr(self, key):
            setattr(self, key, value)
            return

        self.extensions[f'_{key}'] = value

    def get(
        self,
        key: str
    ):
        if hasattr(self, key):
            getattr(self, key)
            return

        if f'_{key}' in self.extensions:
            return self.extensions[f'_{key}']

        raise ValueError(f'No value for for key "{key}".')

    def has(
        self,
        key: str
    ) -> bool:
        if hasattr(self, key):
            return True

        if f'_{key}' in self.extensions:
            return True

        return False

    def remove(
        self,
        key: str
    ):
        if hasattr(self, key):
            setattr(self, key, None)
            return

        self.extensions.pop(f'_{key}')

    def dump(
        self
    ):
        """
        Dump the property values. This combines all the instance attributes along with the values in the extensions.
        """
        dump = self.__dict__.copy()
        dump.pop('extensions')
        dump = {key: value for key, value in dump.items() if value is not None}

        for item in dump.copy():
            if isinstance(dump[item], list) and len(dump[item]) == 0:
                dump.pop(item)

        return {**dump, **self.extensions}


class Author(Default):
    """
    Represents the properties of a author.
    """
    def __init__(
        self
    ):
        Default.__init__(self)

        self.name: str | None = None
        self.url: str | None = None
        self.avatar: str | None = None

    def check(
        self
    ):
        if not self.name and not self.url and not self.avatar:
            raise ValueError('You must provide a value for at least one of the "name", "url" or "avatar" properties.')

    @staticmethod
    def load_from_markdown_file(
        markdown_file: MarkdownFile
    ):
        properties = Author()

        for key in markdown_file.front_matter:
            properties.add(key, markdown_file.front_matter[key])

        return properties


class Hub(Default):
    """
    Represents the properties of a hub.
    """
    def __init__(
        self
    ):
        Default.__init__(self)

        self.type: str | None = None
        self.url: str | None = None

    def check(
        self
    ):
        if not self.type or not self.url:
            raise ValueError('You must provide a valid value for both "type" and "url".')

    @staticmethod
    def load_from_markdown_file(
        markdown_file: MarkdownFile
    ):
        properties = Hub()

        for key in markdown_file.front_matter:
            properties.add(key, markdown_file.front_matter[key])

        return properties


class Item(Default):
    """
    Represents the properties of a item.
    """
    def __init__(
        self,
        id: str | None = None,
        url: str | None = None,
        external_url: str | None = None,
        title: str | None = None,
        content_html: str | None = None,
        content_text: str | None = None,
        summary: str | None = None,
        image: str | None = None,
        banner_image: str | None = None,
        date_published: str | None = None,
        date_modified: Author | None = None,
        author: Author | None = None,
        tags: [str] = None
    ):
        Default.__init__(self)

        if not tags:
            tags = []

        self.id: str | None = id
        self.url: str | None = url
        self.external_url: str | None = external_url
        self.title: str | None = title
        self.content_html: str | None = content_html
        self.content_text: str | None = content_text
        self.summary: str | None = summary
        self.image: str | None = image
        self.banner_image: str | None = banner_image
        self.date_published: str | None = date_published
        self.date_modified: Author | None = date_modified
        self.author: Author | None = author
        self.tags: [str] = tags
        self.extensions: {} = {}

    def check(
        self
    ):
        if not self.id:
            raise ValueError('You must provide a valid version for "id".')

        if not self.content_html and not self.content_text:
            raise ValueError('You must provide a value for either "content_html" or "content_text".')

        if self.author and not isinstance(self.author, Author):
            raise ValueError('Author value must be an instance of Author class.')

    @staticmethod
    def load_from_markdown_file(
        markdown_file: MarkdownFile
    ):
        properties = Item()

        for key in markdown_file.front_matter:
            properties.add(key, markdown_file.front_matter[key])

        return properties


class Feed(Default):
    """
    Represents the properties of a feed.
    """
    def __init__(
        self,
        version: str | None = None,
        title: str | None = None,
        home_page_url: str | None = None,
        feed_url: str | None = None,
        description: str | None = None,
        feed: str | None = None,
        user_comment: str | None = None,
        next_url: str | None = None,
        icon: str | None = None,
        fav_icon: str | None = None,
        author: Author | None = None,
        expired: bool | None = None,
        hubs: [Hub] = None,
        items: [Item] = None
    ):
        Default.__init__(self)

        if not hubs:
            hubs = []

        if not items:
            items = []

        self.version: str | None = version
        self.title: str | None = title
        self.home_page_url: str | None = home_page_url
        self.feed_url: str | None = feed_url
        self.description: str | None = description
        self.feed: str | None = feed
        self.user_comment: str | None = user_comment
        self.next_url: str | None = next_url
        self.icon: str | None = icon
        self.fav_icon: str | None = fav_icon
        self.author: Author | None = author
        self.expired: bool | None = expired
        self.hubs: [Hub] = hubs
        self.items = items
        self.extensions: {} = {}

    def check(
        self
    ):
        if not self.version:
            raise ValueError('You must provide a valid version for "version".')

        if not self.title:
            raise ValueError('You must provide a valid version for "title".')

        if self.author:
            self.author.check()

        for hub in self.hubs:
            hub.check()

    @staticmethod
    def load_from_markdown_file(
        markdown_file: MarkdownFile
    ):
        properties = Feed()

        for key in markdown_file.front_matter:
            properties.add(key, markdown_file.front_matter[key])

        return properties
