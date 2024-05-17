import asyncio
from fastapi import Request, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Union, List, Dict, Optional
from io import BytesIO
import zipfile
import json
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class Route(object):
    pass

class CommonModels(object):
    class OKResponseModel(BaseModel):
        message: str = "OK"
        status: str = "success"
        
    class DataResponseModel(BaseModel):
        data: Union[list, dict]
        status: str = "success"

    class ZipResponseModel(BaseModel):
        class Element(BaseModel):
            file: bytes
            path: str
            filename: str
            json: dict
        
        elements: List[Element]
        paths: Optional[List[str]] = None
        filename: Optional[str] = None
        status: str = "success"
        
        def get(self) -> FileResponse:
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for element in self.elements: 
                    file_name = f"{element.path}/{element.filename}"
                    zip_file.writestr(file_name, element.file)
                    json_name = f"{element.path}/{element.filename}.dict"
                    zip_file.writestr(json_name, json.dumps(element.json, indent=4))
                for path in self.paths:
                    zip_file.writestr(path, '')
                zip_file.writestr('response.dict', json.dumps({'status': self.status}, indent=4))
            zip_buffer.seek(0)
            return FileResponse(zip_buffer, media_type='application/zip', filename=self.filename)

    class UploadOSFile(UploadFile):
        def __init__(self):
            raise NotImplementedError()

class DefaultErrorRoute(Route):
    error_responses = {
        500: {
            "description": "Generic Server Error",
            "content": {
                "application/json": {
                    "example": {"message": "Something unexpected went wrong!", "status": "error"}
                }
            }
        },
        501: {
            "description": "Not Implemented",
            "content": {
                "application/json": {
                    "example": {"message": "This method (with these parameters) is not implemented!", "status": "error"}
                }
            }
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {"message": "These two lists must have the same length!", "status": "error"}
                }
            }            
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {"message": "Validation error on 0 -> filename!", "status": "error"}
                }
            }            
        },        
    }
    
    async def handle_error(request: Request, exc: Exception):
        '''Generic Error Handler'''
        status_code = 500
        if isinstance(exc, NotImplementedError):
            status_code = 501
        elif isinstance(exc, AssertionError):
            status_code = 400
        elif isinstance(exc, ValidationError) or isinstance(exc, RequestValidationError):
            status_code = 422
        try:
            message = exc.message
        except:
            message = str(exc)
        return JSONResponse(
            status_code=status_code,
            content={"message": message, 'status': 'error'}
        )
    
    def add_default_exception_handlers(fs_app):
        fs_app.add_exception_handler(RequestValidationError, DefaultErrorRoute.handle_error)
        fs_app.add_exception_handler(StarletteHTTPException, DefaultErrorRoute.handle_error)
        fs_app.add_exception_handler(Exception, DefaultErrorRoute.handle_error)
    
class RequestCancelledMiddleware:
    def __init__(self, app):
        self.app = app
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        queue = asyncio.Queue()
        async def message_poller(sentinel, handler_task):
            nonlocal queue
            while True:
                message = await receive()
                if message["type"] == "http.disconnect":
                    handler_task.cancel()
                    return sentinel
                await queue.put(message)
        sentinel = object()
        handler_task = asyncio.create_task(self.app(scope, queue.get, send))
        asyncio.create_task(message_poller(sentinel, handler_task))
        try:
            return await handler_task
        except asyncio.CancelledError:
            print("Cancelling request due to disconnect")
