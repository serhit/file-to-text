# Introduction 
The File-to-Text convert service introduce small isolated REST API service,
which converts file of various types (pdf, word, rtf, ppt) into plain text.

Service relies on following public libraries for file conversion:

- [textract](https://textract.readthedocs.io/en/stable/)

Service is implemented using `FastAPI` and backed with `uvicorn` server

# Repository

| Folder    | Content                                                |
|-----------|--------------------------------------------------------|
| /service  | This folder contains the service sources + Docker file |
| /api      | API package to work with service from custom utils     |

# Build

Building the service is just standard Docker build command.
Context of the build is assumed under /service folder.

```bash
$ docker build . -t <your-tag-for-the-image>
```

Building the API package is performed using standard Python procedure of package build.
Example below implies that commands are executed under context of /api folder.

```bash
$ python setup.py sdist -d <output-folder-for-dist>
$ python setup.py bdist_wheel -d <output-folder-for-dist>
```