# Introduction 
The File-to-Text convert service introduce small isolated REST API service,
which converts file of various types (pdf, word, rtf, ppt) into plain text.

Service relies on following public libraries for file conversion:

- [textract](https://textract.readthedocs.io/en/stable/)

Service is implemented using FastAPI and backed with uvicorn server
