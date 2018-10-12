from application import app
from flask import request
from flask_login import current_user
from application.poll.models import Poll

def hasvoted(poll_id):
    if not request.cookies.get("vt"):
        return False

    cookies = map(int, request.cookies.get("vt").split("."))
    if poll_id in cookies:
        return True
    
    return False

def setcookie(template, poll):
    # Store the poll.id into a cookie to prevent multiple votes (in the same session) for anonymous users
    response = app.make_response(template)
    cookie = []
    if "vt" in request.cookies:
        cookie = request.cookies.get("vt").split(".")
    cookie.append(poll.id)
    response.set_cookie("vt", ".".join(map(str,cookie)))
    return response