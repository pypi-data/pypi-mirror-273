
import coloredlogs, logging, verboselogs, json

class EndpointFilter(logging.Filter):
    """
    A custom logging filter that ignores log messages containing specified endpoints.
    
    Attributes:
        endpoints (list of str): A list of endpoint substrings that, if found in a log message, will prevent the message from being logged.

    Example:
        # Create a filter to ignore log messages containing "/health" or "Press CTRL+C to quit" for filtering out Werkzeug server logs.
        logger.addFilter(EndpointFilter(["/health", "Press CTRL+C to quit"]))
    """
    def __init__(self, endpoints):
        """
        Initializes the EndpointFilter with a list of endpoints to ignore.

        Parameters:
            endpoints (list of str): Endpoints that should be filtered out from the logs.
        """
        super().__init__()
        self.endpoints = endpoints

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Determine if the specified log record should be logged or ignored.

        Parameters:
            record (logging.LogRecord): The log record to filter.

        Returns:
            bool: False if the log record contains any of the specified endpoints, True otherwise.
        """
        message = record.getMessage()
        return not any(endpoint in message for endpoint in self.endpoints)

def flexible_json_serializer(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif hasattr(obj, 'tolist'):
        return obj.tolist()
    elif hasattr(obj, 'to_json'):
        return json.loads(obj.to_json())
    return repr(obj)

class AutoFormatAdapter(logging.LoggerAdapter):
    """
    A logging adapter that automatically formats log messages based on their type.
    """
    def process(self, msg, kwargs):
        if isinstance(msg, (dict, list, tuple, set)) or hasattr(msg, '__dict__'):
            try:
                msg = json.dumps(msg, indent=4, default=flexible_json_serializer)
            except TypeError:
                msg = repr(msg)
        return msg, kwargs
    
    def __getattr__(self, name):
        verboselogs_methods = {
            'verbose': logging.VERBOSE,
            'success': logging.SUCCESS,
            'spam': logging.SPAM,
            'notice': logging.NOTICE
        }
        if name in verboselogs_methods:
            level = verboselogs_methods[name]
            def log_method(message, *args, **kwargs):
                if self.isEnabledFor(level):
                    self.log(level, message, *args, **kwargs)

            return log_method

        raise AttributeError(f"{name} not found in LoggerAdapter or logger")


class CustomLogger:
    """
    A factory for creating pre-configured logger instances with enhanced capabilities such as verbose logging levels and colored output, ignoring specified endpoints.
    
    Example:
        # Create a logger instance ignoring logs containing "/health" and "Press CTRL+C to quit"
        logger = CustomLogger(ignore=["/health", "Press CTRL+C to quit"])
    """
    def __new__(cls, level="INFO", name='werkzeug', ignore=None, include_date=True, include_level=True, date_color='yellow'):
        """
        Creates and returns a new logger instance with specified configurations.

        Parameters:
            name (str): The name of the logger. Default is 'werkzeug'.
            ignore (list of str, optional): A list of message substrings to ignore in the logs.
            include_date (bool, optional): Whether to include the date in the log messages. Default is True.
            include_level (bool, optional): Whether to include the log level in the log messages. Default is True.

        Returns:
            logging.Logger: A configured logger instance with colored logs and endpoint filtering.
        """
        if ignore is None:
            ignore = []
        verboselogs.install()
        logging.VERBOSE = verboselogs.VERBOSE
        logging.SPAM = verboselogs.SPAM
        logging.NOTICE = verboselogs.NOTICE
        logging.SUCCESS = verboselogs.SUCCESS

        logger = logging.getLogger(name)
        logger.addFilter(EndpointFilter(ignore))

        format_elements = []
        if include_date:
            format_elements.append('%(asctime)s')
        if include_level:
            format_elements.append('%(levelname)s')
        format_elements.append('%(message)s')
        log_format = ' '.join(format_elements)
        field_styles = {'asctime': {'color': date_color, 'bold': False}}

        coloredlogs.install(logger=logger, isatty=True, fmt=log_format, level=level.upper(), field_styles=field_styles)
        return AutoFormatAdapter(logger)
    
