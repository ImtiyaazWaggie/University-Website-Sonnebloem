from flask import Blueprint, render_template


bp = Blueprint('university', __name__)

@bp.route('/')
def index():
    return render_template('university/index.html')