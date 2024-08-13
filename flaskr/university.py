from flask import Blueprint, flash, redirect, render_template, request, url_for

from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint('university', __name__)


@bp.route('/')
def index():
    return render_template('university/index.html')


@bp.route('/admin-dashboard')
@login_required
def admin_dashoard():
    return render_template('university/dashboard/dashboard.html')




#-------------------Programmes form & Programmes Page-----------------------------------------------------

@bp.route('/create/programmes_form', methods=('GET', 'POST'))
def programmes_form():
        if request.method == 'POST':
            # Retrieve form data
            programme_name = request.form['programme_name']
            programme_code = request.form['programme_code']
            programme_length = request.form['programme_length']
            programme_stream = request.form['programme_stream']
            programme_description = request.form['programme_description']
            qualification_type = request.form['qualification_type']
            graduate_type = request.form['graduate_type']
            study_type = request.form['study_type']
            programme_faculty = request.form['programme_faculty']
            
            # Initialize error variable
            error = None

            # Validate form data
            if not programme_name:
                error = 'Programme Name is required.'
            elif not programme_code:
                error = 'Programme Code is required.'
            elif not programme_length:
                error = 'Programme Length is required.'
            elif not programme_stream:
                error = 'Programme Stream is required.'
            elif not programme_description:
                error = 'Programme Description is required.'
            elif not qualification_type:
                error = 'Qualification Type is required.'
            elif not graduate_type:
                error = 'Graduate Type is required.'
            elif not study_type:
                error = 'Study Type is required.'
            elif not programme_faculty:
                error = 'Programme Faculty is required.'

            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute(
                    'INSERT INTO programmes (programme_name, programme_code, programme_length, programme_stream, programme_description, qualification_type, graduate_type, study_type, programme_faculty)'
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (programme_name, programme_code, programme_length, programme_stream, programme_description, qualification_type, graduate_type, study_type, programme_faculty)
                )
                db.commit()
                return redirect(url_for('university.programmes'))
        return render_template('university/dashboard/programmes_form.html')

@bp.route('/programmes')
def programmes():
    db = get_db()
    
    # Fetch distinct tags for the filter buttons
    programme_faculty = db.execute('SELECT DISTINCT programme_faculty FROM programmes').fetchall()
    
    # Get the selected tag from query parameters
    selected_faculty = request.args.get('programme_faculty')
    
    if selected_faculty:
        # Fetch posts filtered by the selected tag
        programmes = db.execute(
            'SELECT id, programme_name, programme_code, programme_length, programme_stream, programme_description, qualification_type, graduate_type, study_type, programme_faculty FROM programmes WHERE programme_faculty LIKE ?',
            ('%' + selected_faculty + '%',)
        ).fetchall()
    else:
        # Fetch all posts if no tag is selected
        programmes = db.execute(
            'SELECT id, programme_name, programme_code, programme_length, programme_stream, programme_description, qualification_type, graduate_type, study_type, programme_faculty FROM programmes'
        ).fetchall()
    
    return render_template('university/programmes.html', programme_faculty=programme_faculty,programmes=programmes)
