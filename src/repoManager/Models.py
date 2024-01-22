from pathlib import Path
from typing import List, Union
from decorators.decorators import auto_str


@auto_str
class ImagePromptDirectory(object):
    def __init__(self, prompt: str, repo: str, date: str, time: str, absPath: str = None):
        self.prompt = prompt
        self.repo = repo
        self.date = date
        self.time = time


@auto_str 
class NextToken(object):
    def __init__(self, prompt: str, repo: str, date: str, time: str):
        self.prompt = prompt
        self.repo = repo
        self.date = date
        self.time = time


@auto_str
class ImagePrompResult(object):
    def __init__(self, prompt: str, repo: str, date: str, time: str, num: int, pngPaths: List[Path]):
        self.prompt = prompt
        self.repo = repo
        self.date = date
        self.time = time
        self.num = num
        self.pngPaths = pngPaths


@auto_str
class GetImagePrompsResult(object):
    def __init__(self, results: List[ImagePrompResult] = [], nextToken: NextToken = None, errorMessage: Union[str, None] = None):
        self.results = results
        self.nextToken = nextToken
        self.errorMessage = errorMessage