# `ldm`: Loose Dependency Manager

[![PyPI version](https://badge.fury.io/py/loose-dependency-manager.svg)](https://pypi.org/project/loose-dependency-manager)
[![Testsuite](https://github.com/01Joseph-Hwang10/loose-dependency-manager/workflows/Test%20and%20Lint/badge.svg)](https://github.com/01Joseph-Hwang10/loose-dependency-manager/actions?query=workflow%3A"Test+and+Lint")
[![Python version](https://img.shields.io/pypi/pyversions/loose-dependency-manager.svg)](https://pypi.org/project/loose-dependency-manager)
[![Project Status](https://img.shields.io/pypi/status/loose-dependency-manager.svg)](https://pypi.org/project/loose-dependency-manager/)
[![Supported Interpreters](https://img.shields.io/pypi/implementation/loose-dependency-manager.svg)](https://pypi.org/project/loose-dependency-manager/)
[![License](https://img.shields.io/pypi/l/loose-dependency-manager.svg)](https://github.com/pawelzny/loose-dependency-manager/blob/master/LICENSE)


Loose Dependency Manager (or `ldm` in short) is a tool for managing code dependencies in a loosely-coupled way.

## Quick Start

First, install `loose-dependency-manager`:

```bash
pip install loose-dependency-manager
```

Then, create a `ldm.yml` file in the root of your project:

```yaml
schemes:
  lodash:
    uses: github
    with:
      url: https://github.com/lodash/lodash
      ref: main

dependencies:
  clamp: lodash:///src/clamp.ts -> src/utils/clamp.ts
  reset.css: |
    https://cdn.jsdelivr.net/npm/reset-css@5.0.2/reset.min.css
    -> src/styles/reset.css

config:
  parallel:
    workers: 8
  environment:
    from: .env
```

Finally, run `ldm install` to install the dependencies

```bash
ldm install
```

> [!NOTE]
> You can also run `ldm install [...dependencies]` to install specific dependencies.
>  
> ```bash
> ldm install clamp
> ```

## API Documentation

> TODO: description

## Contributing

Any contribution is welcome! Check out [CONTRIBUTING.md](https://github.com/01Joseph-Hwang10/loose-dependency-manager/blob/master/.github/CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](https://github.com/01Joseph-Hwang10/loose-dependency-manager/blob/master/.github/CODE_OF_CONDUCT.md) for more information on how to get started.

## License

`ldm` is licensed under a [MIT License](https://github.com/01Joseph-Hwang10/loose-dependency-manager/blob/master/LICENSE).