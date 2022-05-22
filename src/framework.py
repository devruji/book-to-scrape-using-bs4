from .scraper import Scraper
from .transformer import Transformer
from .config import config as cfg
"""
This file contains the framework that defines how the different classes will 
work together.
"""


def flow() -> None:
    """
        This framework will run the Scraper's job before calling the Transformer
        to transformed the scraped data.
    """
    Scraper(base_url=cfg['base_url']).run()
    transformer = Transformer()
    transformer.run()

