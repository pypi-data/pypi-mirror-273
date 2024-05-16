# beats

![tests](https://github.com/elvijs/beats/workflows/main/badge.svg)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)

# What is it?

Determine the tempo of a song from its mp3. Designed for swing music. May work in other cases as well.

# Usage

## Non-Python dependencies

```console
$ sudo apt install ffmpeg
```

TODO: describe how to use the CLI

# Development

## Algorithm development

### Scoring new estimators

TODO: document how to score their songs.

### Streamlit apps

TODO

## Package development

### Install in dev mode

```console
$ make install
```

### Common dev tasks

* Auto-format: `make format`
* Run static checkers: `make statec_checks`
* Freeze the local env into `test_requirements` (say, after installing new deps):
  `make freeze_requirements`.

## Issues

Please raise [here](https://github.com/elvijs/beats/issues).

## Credits

This project was generated from [@elvijs](https://github.com/elvijs)'s
[Minimal Python Cookiecutter](https://github.com/elvijs/cookiecutter-minimal-python) template.
