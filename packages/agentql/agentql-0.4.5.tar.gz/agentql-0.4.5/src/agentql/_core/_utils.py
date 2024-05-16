import os
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

import aiofiles


def ensure_url_scheme(url: str) -> str:
    """
    Ensure that the URL has a scheme.
    """
    if not url.startswith(("http://", "https://", "file://")):
        return "https://" + url
    return url


def minify_query(query: str) -> str:
    """
    Minify the query by removing all newlines and extra spaces.
    """
    return query.replace("\n", "\\").replace(" ", "")


def get_api_key() -> Optional[str]:
    """
    Get the AgentQL API key from a configuration file or an environment variable.

    Returns:
    -------
    Optional[str]: The API key if found, None otherwise.
    """
    try:
        config = ConfigParser()
        config_file_path = Path.home() / ".agentql" / "config" / "agentql_api_key.ini"
        config.read(config_file_path)
        api_key = config.get("DEFAULT", "AGENTQL_API_KEY", fallback=None)
        if api_key:
            return api_key
    except FileNotFoundError:
        pass

    # Fallback to environment variable if the key wasn't found in the file
    return os.getenv("AGENTQL_API_KEY")


async def get_api_key_async() -> Optional[str]:
    """
    Get the AgentQL API key from a configuration file or an environment variable asynchronously.

    Returns:
    -------
    Optional[str]: The API key if found, None otherwise.
    """
    try:
        config = ConfigParser()
        config_file_path = Path.home() / ".agentql" / "config" / "agentql_api_key.ini"
        async with aiofiles.open(config_file_path, mode="r") as file:
            content = await file.read()
        config.read_string(content)
        api_key = config.get("DEFAULT", "AGENTQL_API_KEY", fallback=None)
        if api_key:
            return api_key
    except FileNotFoundError:
        pass

    # Fallback to environment variable if the key wasn't found in the file
    return os.getenv("AGENTQL_API_KEY")
