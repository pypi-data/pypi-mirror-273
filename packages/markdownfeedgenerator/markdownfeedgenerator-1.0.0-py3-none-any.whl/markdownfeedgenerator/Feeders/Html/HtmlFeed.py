import os.path
import logging

import chevron

from markdownfeedgenerator import read_from_file, write_to_file
from markdownfeedgenerator.BaseFeed import BaseFeed
from markdownfeedgenerator.Feeders.Html import Properties
from markdownfeedgenerator.MarkdownFile import MarkdownFile

logging = logging.getLogger(__name__)


class HtmlFeed(BaseFeed):
    """
    A simple HTML feed.
    """
    DEFAULT_TEMPLATE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'template.html')

    def __init__(
        self,
        feed_properties: Properties.Feed,
        source_directory: str = None,
        target_directory: str = None,
        files_per_page: int = None,
        template_file_path: str = None
    ):

        feed_properties.check()

        """
        Perform some setup.
        """
        BaseFeed.__init__(
            self,
            source_directory,
            target_directory,
            feed_properties.title,
            files_per_page
        )

        self.feed_properties = feed_properties
        self.template_file_path = template_file_path if template_file_path else HtmlFeed.DEFAULT_TEMPLATE

        if not os.path.exists(self.template_file_path):
            raise FileNotFoundError(f'Could not find the Mustache template at path "{self.template_file_path}".')

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
        feed_url = self.get_feed_page_name(current_page)
        next_feed_url = self.get_feed_page_name(current_page + 1) if (current_page + 1) < total_pages else None
        previous_feed_url = self.get_feed_page_name(current_page - 1) if current_page > 0 else None
        feed_file_target = os.path.join(self.target_directory, feed_url)

        if self.feed_base_url:
            next_feed_url = f'{self.feed_base_url}/{next_feed_url}' if next_feed_url is not None else None

        template = read_from_file(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'template.html'))

        content = chevron.render(template, {**{
            'nextPageUrl':
                next_feed_url,
            'previousPageUrl':
                previous_feed_url,
            'title':
                self.title,
            'files':
                [self._serialize_markdown_file(f) for f in markdown_files]
        }, **self.feed_properties.dump()})

        write_to_file(feed_file_target, content)

        logging.info(f'Successfully wrote feed page "{current_page}", containing "{len(markdown_files)}" '
                     f'items to "{feed_file_target}".')

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
        serialized = super()._serialize_markdown_file(markdown_file)
        serialized['date'] = markdown_file.date.strftime('%c')
        return serialized

    @staticmethod
    def get_feed_page_name(
        page_number: int
    ) -> str:
        if page_number == 0:
            return 'index.html'

        return f'{page_number}.html'
