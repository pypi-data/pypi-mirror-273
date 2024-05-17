import asyncio
import logging
import os
from math import ceil
from pathlib import Path

from markdownfeedgenerator.MarkdownFile import MarkdownFile


class BaseFeed:
    """
    Represents a feed, generated from markdown files. You can extend this class to provide JSON feeds, HTML feeds
    or just plain old XML RSS feeds.
    """

    DEFAULT_FILES_PER_PAGE = 75

    # A default list of markdown files to skip
    DEFAULT_SKIP_FILES = [
        'readme.md', 'contributing.md'
    ]

    def __init__(
        self,
        source_directory: str = None,
        target_directory: str = None,
        title: str = None,
        front_matter_properties: list = None,
        files_per_page: int = None,
        feed_base_url: str = None
    ):
        if not source_directory:
            source_directory = os.getcwd()

        if not target_directory:
            target_directory = os.getcwd()

        if not title:
            title = os.path.dirname(target_directory) + ' Feed'

        if not front_matter_properties:
            front_matter_properties = []

        if not files_per_page:
            files_per_page = BaseFeed.DEFAULT_FILES_PER_PAGE

        if not os.path.exists(source_directory):
            raise ValueError(f'The source directory "{source_directory}", does not exist.')

        if not os.path.exists(target_directory):
            logging.warning(f'Target directory "{target_directory}" does not exist, creating it...')
            os.makedirs(target_directory)

        self.source_directory = source_directory
        self.target_directory = target_directory
        self.title = title
        self.front_matter_properties = front_matter_properties
        self.files_per_page = files_per_page
        self.feed_base_url = feed_base_url.rstrip('/') if feed_base_url else feed_base_url

        self.skip_files = self.DEFAULT_SKIP_FILES

    async def run(
        self
    ) -> None:
        """
        Generates a feed based on all the found markdown files.
        """
        # Get a list of markdown files
        markdown_file_list = self.locate_markdown_files(self.source_directory, self.skip_files)

        # Sort them by file name, this will order newest first assuming date in filename
        markdown_file_list.sort(reverse=True, key=lambda x: os.path.basename(x))

        # How many pages do we have?
        total_pages = ceil(len(markdown_file_list) / self.files_per_page) if self.files_per_page else 1

        # Run through each chunk, async style and await the result
        page_queue = []
        current_page = 0
        for file_list_chunk in self._chunk(markdown_file_list, self.files_per_page):
            page_queue.append(
                self.__convert_file_list(
                    file_list_chunk, current_page, total_pages))

            current_page += 1

        # Since we are generated pages async style, await for them all to finish generating
        await asyncio.gather(*page_queue)

    def run_standalone(
        self
    ):
        """
        Run this in synchronous mode.
        """
        asyncio.run(self.run())

    async def __convert_file_list(
        self,
        markdown_file_list: [str],
        current_page: int,
        total_pages: int = None
    ):
        """
        This function takes a list of file paths and converts them into a list of markdown files, passing them
        through a process function and ultimately exporting those files by calling the export function.
        """
        # A list of converted markdown files
        markdown_files: [MarkdownFile] = []

        for markdown_file_path in markdown_file_list:
            logging.info(f'Loading markdown file "{markdown_file_path}".')

            markdown_file = self._load_markdown_contents(markdown_file_path)

            logging.info(f'Processing markdown file "{markdown_file_path}".')

            markdown_file = self._process_markdown_file(markdown_file)

            logging.info(f'Processed markdown file "{markdown_file_path}" successfully.')

            markdown_files.append(markdown_file)

        self._generate_page(
            markdown_files, current_page, total_pages, len(markdown_files))

        logging.info(f'Successfully generated feed page {current_page}.')

    def _load_markdown_contents(
        self,
        markdown_file_path: str
    ) -> MarkdownFile:
        """
        Load markdown file contents.
        """
        return MarkdownFile.load(markdown_file_path)

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
        raise NotImplementedError('Function _generate_page must be implemented.')

    def _process_markdown_file(
        self,
        markdown_file: MarkdownFile
    ) -> MarkdownFile:
        """
        Process a markdown file. Override to do something interesting with file, such as exporting HTML contents.
        :param markdown_file:
        :return:
        """
        return markdown_file

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
        serialized = markdown_file.front_matter

        return {**serialized, **{
            'id':
                markdown_file.id,
            'date':
                markdown_file.date.isoformat() if markdown_file.date else None,
            'title':
                markdown_file.title,
            'description':
                markdown_file.summary,
        }}

    def locate_markdown_files(
        self,
        directory_path: str,
        skip_files: list = None
    ) -> [str]:
        """
        Locate all markdown files within a provided directory, skipping some files if needed.
        """
        if skip_files is None:
            skip_files = []

        if not os.path.isdir(directory_path):
            raise Exception(f'The provided path "{directory_path}", must be a directory.')

        return list(
            filter(
                lambda x: os.path.basename(x) not in skip_files,
                [str(path) for path in Path(directory_path).glob('**/*.md')]))

    @staticmethod
    def _chunk(
        lst,
        length: int = None
    ) -> list:
        """
        Chunk a list into a specific length.
        :param length:
        :param lst:
        :return:
        """
        if length is None:
            yield lst
            return

        for i in range(0, len(lst), length):
            yield lst[i:i + length]
