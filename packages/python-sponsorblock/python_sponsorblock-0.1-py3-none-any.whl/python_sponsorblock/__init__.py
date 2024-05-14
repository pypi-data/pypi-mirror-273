import requests
import logging
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import re
from typing import Optional, List, Dict, Union, Any, Callable, Set
import json
from functools import wraps

from .exceptions import SponsorBlockError, SponsorBlockIdNotFoundError, ReturnDefault
from .constants import Segment, Category


def error_handling(default: Any) -> Callable:
    def _decorator(func: Callable) -> Callable:
        @wraps(func)
        def _wrapper(self, *args, **kwargs) -> Any:
            nonlocal default

            try:
                return func(self, *args, **kwargs)
            except SponsorBlockError as e:
                if isinstance(e, ReturnDefault):
                    return default

                if not self.silent:
                    raise e

                if self._requests_logging_exists and isinstance(e, SponsorBlockConnectionError):
                    return default

                self.logger.error(repr(e))

                return default

        return _wrapper

    return _decorator


class SponsorBlock:
    def __init__(self, session: requests.Session = None, base_url: str = "https://sponsor.ajay.app", silent: bool = False, _requests_logging_exists: bool = False):
        self.base_url: str = base_url
        self.session: requests.Session = session or requests.Session()

        self.silent: bool = silent
        self._requests_logging_exists: bool = _requests_logging_exists

        self.logger: logging.Logger = logging.Logger("SponsorBlock")

    def _get_video_id(self, video: str) -> str:
        if re.match(r"^[a-zA-Z0-9_-]{11}$", video):
            return video.strip()

        url = urlparse(url=video)

        if url.netloc == "youtu.be":
            return url.path[1:]

        type_frag_list = url.path.split("/")
                
        query_stuff = parse_qs(url.query)
        if "v" not in query_stuff:
            raise SponsorBlockIdNotFoundError("No video id found in the url")
        else:
            return query_stuff["v"][0]

    def _request(self, method: str, endpoint: str, return_default_at_response: List[str] = None) -> Union[List, Dict]:
        valid_responses: Set[str] = set([
            "Not Found",
        ])
        valid_responses.update(return_default_at_response or [])

        error_message = ""
        url = self.base_url + endpoint

        r: requests.Response = None
        try:
            r = self.session.request(method=method, url=url)
        except requests.exceptions.Timeout:
            error_message = f"Request timed out at \"{url}\""
        except requests.exceptions.ConnectionError:
            error_message = f"Couldn't connect to \"{url}\""

        if error_message != "":
            raise exceptions.SponsorBlockConnectionError(error_message)

        if r.status_code == 400:
            self.logger.warning(f"{url} returned 400, meaning I did something wrong.")

        if r.text in valid_responses:
            raise exceptions.ReturnDefault()

        data = {}
        try:
            data = r.json()
        except json.JSONDecodeError:
            raise exceptions.SponsorBlockConnectionError(f"{r.text} is invalid json.")
        
        return data
        
    @error_handling(default=[])
    def get_segments(self, video: str, categories: List[Category] = None) -> List[Segment]:
        """
        Retrieves the skip segments for a given video.

        Args:
            video (str): The video identifier.
            categories (List[Category], optional): A list of categories to filter the skip segments. Defaults to all categories.

        Returns:
            List[Segment]: A list of skip segments for the given video.
        """
        video_id = self._get_video_id(video)
        categories = categories or [c for c in Category]
        
        # build query parameters
        query = {
            "videoID": video_id,
            "categories": json.dumps([c.value for c in categories])
        }

        r = self._request(method="GET", endpoint="/api/skipSegments?" + urlencode(query))
        return [constants.Segment(**d) for d in r] 
