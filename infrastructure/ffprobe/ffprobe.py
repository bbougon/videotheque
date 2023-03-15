from __future__ import annotations

import json
import subprocess
from subprocess import CompletedProcess

from search.exceptions import RunnerException
from search.runner import VideoInformationRunner, VideoDetails
from settings import config


class FFProbeVideoDetailsDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs
        )

    def object_hook(self, dct):
        if "streams" in dct:
            languages = [
                stream["tags"]["language"] for stream in dct["streams"]
            ]
            duration = dct["format"]["duration"]
            return VideoDetails(languages, duration)
        if "format" in dct:
            return VideoDetails(
                languages=[], duration=dct["format"]["duration"]
            )
        return dct


class FFProbeRunner(VideoInformationRunner):
    def __init__(self) -> None:
        self.runner = config("VIDEO.RUNNER")

    def run(self, *args):
        command = f"{self.runner} -i {''.join(args)} -show_entries format=duration -v error -of json -sexagesimal -show_entries stream=index:stream_tags=language -select_streams a"
        completed_process: CompletedProcess = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        if completed_process.returncode != 0:
            raise RunnerException(
                "Impossible to run the command",
                completed_process.returncode,
                completed_process.stderr,
                args=completed_process.args,
            )
        return json.loads(
            completed_process.stdout.decode("utf-8"),
            cls=FFProbeVideoDetailsDecoder,
        )
