from flask import Blueprint, render_template

from flaskr.auth import login_required


bp = Blueprint('university', __name__)


@bp.route('/')
def index():
    return render_template('university/index.html')


@bp.route('/admin-dashboard')
@login_required
def admin_dashoard():
    return render_template('university/dashboard/dashboard.html')