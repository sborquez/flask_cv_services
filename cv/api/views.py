# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify
)
from flask_wtf.csrf import CSRFProtect
#from flask_login import login_required, login_user, logout_user
from cv.api.services import cv_services
from cv.api import services
from cv.api.forms import ImageForm
from cv.extensions import csrf_protect

blueprint = Blueprint("api", __name__,  url_prefix="/api", static_folder="../static")
DISABLE_RENDER = False #todo: use app configuration

@blueprint.route("/list", methods=["GET"])
def list_services():
    """List of services page."""
    json_format = request.args.get("json", False)
    if DISABLE_RENDER or json_format:
        return jsonify(cv_services)
    else:
        return render_template("api/list.html", cv_services=cv_services)

@csrf_protect.exempt
@blueprint.route("/gray", methods=["POST"])
def gray():
    """Convert image to gray scale."""
    form = ImageForm(meta={'csrf': False})
    current_app.logger.debug(f"request: {request.form}")
    if form.validate():
        service_info = cv_services["gray"]
        json_format = request.args.get("json", False)
        # Image Processing
        image = services.convert_to_image(request.files["image"].read())
        err, image = services.gray(image)
        current_app.logger.debug(f"respond: {image}")
        respond = services.convert_to_base64(image)
        # Respond
        respond = jsonify({"image": str(respond)}), 200
    else:
        respond = jsonify(message=form.errors), 404
    return respond
        

@blueprint.route("/service", methods=["GET"])
def service():
    error = ""
    service = request.args.get("cv", "gray")
    #TODO check cv is in services
    service_info = cv_services[service]
    json_format = request.args.get("json", False)        
    if DISABLE_RENDER or json_format:
        return jsonify(cv_services["gray"])
    else:
        form = ImageForm(meta={'csrf': False})
        return render_template("api/service.html", form=form, message=error,
                                respond=None, service=service_info)
