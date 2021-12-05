from enum import Enum

class WebscrapingStatus(str, Enum):
    """
    Status
    """

    IDLE = "idle",
    """
    Webscraping currently not in progress.
    """
    RUNNING = "running",
    """
    Webscraping is in progress.
    """
    FINISHED = "finished"
    """
    Webscraping is finished.
    """
