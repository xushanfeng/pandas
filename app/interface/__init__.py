from flask import Blueprint

inter = Blueprint('inter', __name__)

import app.interface.views
