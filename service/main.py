import os
import secrets
import tempfile
from datetime import datetime as dt

import textract
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

# Placeholder for the version - to be updated with the CI process
__version__ = '0.0.1'


class ConvertResult(BaseModel):
    result: str
    text: str
    text_length: int
    file_name: str
    messages: str


app = FastAPI()
security = HTTPBasic()
_start_time = dt.now()

if os.getenv('SERVICE_AUTH_USERNAME'):
    username = os.getenv('SERVICE_AUTH_USERNAME')
    password = os.getenv('SERVICE_AUTH_PASSWORD')
else:
    # Please note - this is a sample password for local debugging purposes only. 
    # The real credentials must be provided as a part of the runtime configuration
    username = '_username_Pfa_45rfregw#'
    password = '_password_@@#$WuDV^fds'


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get('/')
async def index():
    return {'version': __version__, "start-time": _start_time}


@app.post('/convert', response_model=ConvertResult)
async def convert_file(file: UploadFile = File("file_to_convert"),
                       encoding: str = "utf-8",
                       user_name: str = Depends(get_current_username)):
    _text = ""
    _result, _warning_message, _convert_start_time = "success", "", dt.now()

    _, file_extension = os.path.splitext(file.filename)

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as _file:
        _content = await file.read()
        _file.write(_content)
        _tmp_file_name = _file.name

    attempts = 1
    while attempts >= 0:
        try:
            _text = textract.process(_tmp_file_name).decode(encoding)
            break
        except Exception as e:
            print('Conversion issue:', _tmp_file_name, e)
            _warning_message += f"Conversion issue: {str(e)}\n"
            _result = "warning"

            if "Rich Text" in str(e):
                os.rename(_tmp_file_name, _tmp_file_name + '.rtf')
                _tmp_file_name = _tmp_file_name + '.rtf'
                attempts -= 1
            else:
                _result = "error"
                break

    os.remove(_tmp_file_name)

    return {'result': _result,
            'text': _text,
            'text_length': len(_text),
            'file_name': file.filename,
            'messages': _warning_message}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)
