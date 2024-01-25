import azure.functions as func
from FlaskApp import app
import logging

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    """Each request is redirected to the WSGI handler.
    """
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)
