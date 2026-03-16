from flask import Blueprint

camera_bp = Blueprint("camera", __name__)

@camera_bp.route("/camera")
def camera_feed():

    return "Camera stream will appear here"