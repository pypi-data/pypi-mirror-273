import json
import os.path
import logging

from markdownfeedgenerator import write_to_file
from markdownfeedgenerator.BaseFeed import BaseFeed
from markdownfeedgenerator.Feeders.Json import Properties
from markdownfeedgenerator.Feeders.Json.Properties import Item
from markdownfeedgenerator.MarkdownFile import MarkdownFile

logging = logging.getLogger(__name__)


class JsonFeedV1(BaseFeed):
    """
    A JsonFeed can generate a https://www.jsonfeed.org/version/1/ complaint feed from markdown files stored within
    a specific directory. The markdown files should be in a Jekyll file format, with yaml front-matter and content
    separated by three dashes.
    """
    # The jsonfeed.org version this feed generates
    JSON_FEED_VERSION = f'https://jsonfeed.org/version/1'

    # Indent for the JSON feed, should be 0 if generating for production
    JSON_INDENT = 2

    def __init__(
        self,
        source_directory: str = None,
        target_directory: str = None,
        feed_properties: Properties.Feed = None,
        files_per_page: int = None,
        include_content: bool = False,
        feed_base_url: str = None
    ):
        """
        Constructor for the JsonFeed instance. Performs the setup.
        """
        if not feed_properties:
            raise ValueError('You must provide a valid value for "feed_properties".')

        feed_properties.version = self.JSON_FEED_VERSION
        feed_properties.check()

        BaseFeed.__init__(
            self,
            source_directory=source_directory,
            target_directory=target_directory,
            title=feed_properties.title,
            files_per_page=files_per_page,
            feed_base_url=feed_base_url
        )

        self.feed_properties = feed_properties
        self.include_content = include_content

    def _generate_page(
        self,
        markdown_files: [MarkdownFile],
        current_page: int,
        total_pages: int,
        total_items: int
    ) -> None:
        """
        Generate a feed page.
        :param markdown_files:
        :param current_page:
        :param total_pages:
        :param total_items:
        :return:
        """
        feed_url = 'feed.json' if current_page == 0 else f'{current_page}.json'
        next_feed_url = f'{current_page + 1}.json' if (current_page + 1) < total_pages else None
        feed_file_target = os.path.join(self.target_directory, feed_url)

        self.feed_properties.feed_url = f'{self.feed_base_url}/{feed_url}'
        self.feed_properties.next_url = f'{self.feed_base_url}/{next_feed_url}' if next_feed_url is not None else None
        self.feed_properties.items = [self._serialize_markdown_file(f) for f in markdown_files]

        self.feed_properties.add('total_items_count', total_items)
        self.feed_properties.add('page_items_count', len(self.feed_properties.items))
        self.feed_properties.add('total_pages_count', total_pages)

        self.feed_properties.check()

        write_to_file(
            feed_file_target, json.dumps(
                self.feed_properties.dump(), indent=JsonFeedV1.JSON_INDENT))

        logging.info(
            f'Successfully wrote feed page "{current_page}", containing "{len(markdown_files)}" items '
            f'to "{feed_file_target}".')

    def _serialize_markdown_file(
        self,
        markdown_file: MarkdownFile
    ) -> dict:
        """
        Serialize a markdown file for the feed. Override this function to provide different values.
        :return:
        :param markdown_file:
        :return:
        """
        item_properties = Properties.Item(
            id=markdown_file.id,
            date_published=markdown_file.date.isoformat() if markdown_file.date else None,
            title=markdown_file.title,
            summary=markdown_file.summary)

        [item_properties.add(front_matter_property, markdown_file.front_matter[front_matter_property])
         for front_matter_property in markdown_file.filtered_front_matter]

        # Inject any additional properties
        item_properties = self._inject_extra_properties(item_properties, markdown_file)

        if self.include_content:
            item_properties.content_html = markdown_file.html

        return item_properties.dump()

    def _inject_extra_properties(
        self,
        current_item_properties: Item,
        markdown_file: MarkdownFile
    ) -> Item:
        """
        Inject any additional properties.
        """
        return current_item_properties
