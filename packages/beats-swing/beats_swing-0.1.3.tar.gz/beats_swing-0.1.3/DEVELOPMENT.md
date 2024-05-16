# Algorithm development

It should be easy to adapt this package to work for other genres.
In order evaluate new implementations of the `Estimator` interface,
we've set up a simple evaluation script, see `scripts/score.py`.
See its docstring for detailed instructions.

# Package development

## Install in dev mode

```console
$ make install
```

Note that this sets up MLflow as well as other packages relevant for algorithm development.

## Common dev tasks

* Auto-format: `make format`
* Run static checkers: `make statec_checks`
* Freeze the local env into `test_requirements` (say, after installing new deps):
  `make freeze_requirements`.
