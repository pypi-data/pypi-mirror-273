from setuptools import setup

name = "types-pyflakes"
description = "Typing stubs for pyflakes"
long_description = '''
## Typing stubs for pyflakes

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pyflakes`](https://github.com/PyCQA/pyflakes) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pyflakes`.

This version of `types-pyflakes` aims to provide accurate annotations
for `pyflakes==3.2.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pyflakes. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `a86115a19ddf2ca57645fea5fb6287fafa1cc1a0` and was tested
with mypy 1.10.0, pyright 1.1.362, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="3.2.0.20240515",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyflakes.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pyflakes-stubs'],
      package_data={'pyflakes-stubs': ['__init__.pyi', 'api.pyi', 'checker.pyi', 'messages.pyi', 'reporter.pyi', 'scripts/__init__.pyi', 'scripts/pyflakes.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
