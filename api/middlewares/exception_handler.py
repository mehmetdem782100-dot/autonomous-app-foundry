from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from core.logger import get_logger
from core.exceptions import CognitaBaseException

logger = get_logger("GLOBAL_EXC_HANDLER")

async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, CognitaBaseException):
        logger.warning(f"Cognita Ozel Hatasi: {exc.message} - Detaylar: {exc.details}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "BusinessLogicError", "message": exc.message, "details": exc.details}
        )
        
    elif isinstance(exc, SQLAlchemyError):
        logger.error(f"Kritik Veritabani Hatasi: {str(exc)} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "DatabaseError", "message": "Veritabani isleminde kritik bir hata olustu."}
        )
        
    elif isinstance(exc, ValidationError):
        logger.error(f"Veri Dogrulama Hatasi: {exc.errors()} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "ValidationError", "details": exc.errors()}
        )
        
    else:
        logger.exception(f"Beklenmeyen Sistem Hatasi: {str(exc)} | Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "InternalServerError", "message": "Sistemde beklenmeyen bir hata olustu."}
        )
