import logging


def setup_logger():
    """
    >>> setup_logger()
    >>> logger = logging.getLogger('DOCTEST LOGGER')
    >>> logger.warning('DOCTEST')
    """
    log_format = '%(asctime)s: %(levelname)s: %(name)s: %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        datefmt=datefmt)
    logging.basicConfig()
