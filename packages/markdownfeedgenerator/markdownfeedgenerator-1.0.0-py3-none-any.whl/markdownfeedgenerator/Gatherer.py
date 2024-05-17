import asyncio


class Gatherer:
    """
    Wrapper class to group feeds and run them async style.
    """
    def __init__(
        self,
        feeds: list = None
    ):
        """
        Provide a list of feeds to generate.
        """
        if feeds is None:
            feeds = []

        self.feeds = feeds

    async def __generate(
        self
    ):
        """
        Generate a feed.
        """
        await asyncio.gather(
            *[generator.run() for generator in self.feeds])

    def generate(
        self
    ):
        """
        Generate all the feeds.
        :return:
        """
        asyncio.run(self.__generate())
