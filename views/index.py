from flask import Blueprint, redirect

index_pade = Blueprint('index_pade', __name__)


@index_pade.route("/", methods=['GET'])
def redirect_to_apidocs():
    return redirect("/docs")
