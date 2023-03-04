# Videotheque

Videotheque is a simple python command cli that can be use to:

- rename all files and directories in a given path with the following format `MOVIE_TITLE_LANGUAGE`
- search movies in a given path for given keywords and print the result in a table format:
  
  `python3 videotheque.py /share/Films/ search` will produce something like:

  | Title          | Duration       | Languages  |
  |----------------|----------------|------------|
  | The_Impossible | 1:53:31.904000 | ['French'] |
  | ...            | ...            | ...        |


## Installation
You need at least a python `3.9` functional env.

- Create a venv `python -m venv venv`
- Activate the venv `source venv/bin/activate`
- Run pip installation `pip install -r requirements.txt`

In order to perform searches, you need to have [ffprobe](https://ffmpeg.org/ffprobe.html) installed

### Configuration
Edit the `settings.ini` file:
- RUNNER: the path to ffprobe binary or simply `ffprobe` if already in your path 

## Usage

run `python3 videotheque.py -h` to get the list of availabe commands and their usages

