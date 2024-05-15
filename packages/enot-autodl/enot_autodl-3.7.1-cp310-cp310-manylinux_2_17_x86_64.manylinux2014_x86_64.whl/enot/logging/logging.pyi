from pathlib import Path

def set_log_level(loglevel: int) -> None:
    """
    Set loglevel for entire package.

    Parameters
    ----------
    loglevel : int
        Desired loglevel.

    """
def enable_logging(enable: bool = True) -> None:
    """
    Enables (or disables) logging for entire package.

    Parameters
    ----------
    enable : bool
        Enable or disable logging for package.

    """
def enable_console_log(enable: bool = True) -> None:
    """
    Enables (or disables) display log in console (stdout) for entire package.

    Parameters
    ----------
    enable : bool
        Enable (or disable) display log in console (stdout) for entire package.

    """
def add_file_handler(path: str | Path) -> None:
    """
    Add file handler to module logger. Use it for logging into file.

    Parameters
    ----------
    path : str, Path
        Path to log file.

    """
