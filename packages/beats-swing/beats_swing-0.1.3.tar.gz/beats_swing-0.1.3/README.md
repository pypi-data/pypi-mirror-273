# beats

![tests](https://github.com/elvijs/beats/workflows/tests/badge.svg)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)

# What is it?

Determine the tempo of a song from its mp3. Designed for swing music. May work in other cases as well.

This is essentially a thin wrapper on top of the amazing [`librosa`](https://librosa.org/doc/latest/index.html) library.

# Estimating tempo of songs

## Install

Ensure you have the [`ffmpeg`](https://ffmpeg.org/) system-level package installed via e.g.
```console
$ sudo apt install ffmpeg
```

Then install the package (in a Python virtual environment) via
```console
$ pip install beats-swing
```

## Usage

The main entrypoint is the CLI script `beats`:
```console
(venv) user@computer:~$ beats -f data/sample.mp3
172
```

Alternatively, use the package directly in Python via the `Estimator` interface implementations.

## Caveats

* Supported formats: `mp3`, `m4a`.
* This package is the simplest possible solution to estimating the tempo of swing songs
  and has been tweaked against a small sample of songs.
  If you find cases where it does a particularly bad job,
  please raise [an issue](https://github.com/elvijs/beats/issues) and upload the relevant audio file.
  * If you want to extend it in any way, please read the algorithm development guidelines on `DEVELOPMENT.md`.

## Issues

Please raise [here](https://github.com/elvijs/beats/issues).

## Credits

This project was generated from [@elvijs](https://github.com/elvijs)'s
[Minimal Python Cookiecutter](https://github.com/elvijs/cookiecutter-minimal-python) template.
