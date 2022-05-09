### Episode Title Suffix

Python script that automatically appends the episode name to a video file for a television show.

For instance, it would convert
` Game of Thrones S01E01.mkv`
to
` Game of Thrones S01E01 Winter Is Coming.mkv`

## Getting Started

- run

## Prerequisites

TV show folder and file structure has to follow a specific format.
The folder structure must be

─ Show Name
└── Season X
    ├── Show Name S01E01.mkv
    ├── Show Name S01E02.mkv
    ├── Show Name S01E03.mkv
    ├── Show Name S01E04.mkv
    ├── Show Name S01E05.mkv
    ├── Show Name S01E06.mkv
    ├── Show Name S01E07.mkv
    ├── Show Name S01E08.mkv
    └── Show Name S01E09.mkv

Where X is the Season Number. Also, the extension does not have to be ```.mkv```
Read the Plex documentation [https://support.plex.tv/articles/naming-and-organizing-your-tv-show-files/](here) for more information

- Python
- pip
- Internet

## Installation

1. Clone the repo

```sh
git clone https://github.com/nolanwinsman/episode-title-suffix.git
```

2. Install Python modules

```sh
pip install -r requirements.txt
```

# Contact

Nolan Winsman - [@Github](https://github.com/nolanwinsman) - nolanwinsman@gmail.com

Project Link: [https://github.com/nolanwinsman/episode-title-suffix](https://github.com/nolanwinsman/episode-title-suffix)

# Contributers

- nolanwinsman

## Files

├── createSeries.py : file to generate mock data for testing
├── eSuffix.py : main script
├── IMDB.ico : icon used for when the tv show poster displays
├── README.md : this file
└── requirements.txt : python modules
