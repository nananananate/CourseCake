import logging

from flask import Blueprint
import markdown
import markdown.extensions.fenced_code

from ..limiter import limiter

logging.basicConfig(filename="home.log",level=logging.DEBUG)
home_blueprint = Blueprint("home_blueprint", __name__)


@home_blueprint.route("/")
@home_blueprint.route("/index")
@home_blueprint.route("/readme")
def homePage():
    readMe = open("README.md", "r")
    mdTemplateStr = markdown.markdown(
        readMe.read(),
        extensions = ["fenced_code"]
    )

    return mdTemplateStr