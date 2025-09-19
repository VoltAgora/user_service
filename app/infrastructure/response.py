from fastapi.responses import JSONResponse

class ResultHandler:
    @staticmethod
    def success(data=None, message="OK"):
        return {"success": True, "message": message, "data": data}

    @staticmethod
    def created(data=None, message="Created"):
        return {"success": True, "message": message, "data": data}

    @staticmethod
    def bad_request(message="Bad request"):
        return {"success": False, "message": message, "data": None}

    @staticmethod
    def unauthorized(message="Unauthorized"):
        return {"success": False, "message": message, "data": None}

    @staticmethod
    def internal_error(message="Internal error"):
        return {"success": False, "message": message, "data": None}
    
    @staticmethod
    def forbidden(message="Forbidden", data=None):
        """
        Respuesta HTTP 403 - Forbidden. Usado cuando el usuario está autenticado
        pero no tiene permisos suficientes.
        """
        return JSONResponse(status_code=403, content={"success": False, "message": message, "data": data})