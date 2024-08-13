import os
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for

from flaskr.auth import login_required
from flaskr.db import get_db

from werkzeug.utils import secure_filename


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



#-------------------News form & News Page-----------------------------------------------------


@bp.route('/create/news_form', methods=('GET', 'POST'))
def create_news_form():
    if request.method == 'POST':
        headline = request.form['headline']
        sub_headline = request.form['sub_headline']
        author = request.form['author']
        introduction = request.form['introduction']
        paragraph_one = request.form['paragraph_one']
        paragraph_two = request.form['paragraph_two']
        paragraph_three = request.form['paragraph_three']
        paragraph_four = request.form['paragraph_four']
        quotes = request.form['quotes']
        tags = request.form['tags']
        file = request.files.get('file')
        
        error = None
        
        if not headline:
            errors = 'Headline is required.'

        elif not sub_headline:
            errors = 'Last Name is required.'

        elif not author:
            errors = 'ID Number is required.'

        elif not introduction:
            errors = 'Date of Birth is required.'

        elif not paragraph_one:
            errors = 'Phone Number is required.'
        elif not paragraph_two:
            errors = 'Phone Number is required.'
        elif not paragraph_three:
            errors = 'Phone Number is required.'
        elif not paragraph_four:
            errors = 'Phone Number is required.'

        elif not quotes:
            errors = 'Email Address is required.'

        elif not tags:
            errors = 'Address / Street is required.'
            
        elif not file:
            errors = 'File upload is required.'
        
        filename = None
        
        if file and file.filename:
            # Ensure the uploads directory exists
            uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            file_path = os.path.join(uploads_dir, filename)
            file.save(file_path)
        # Save the file path in the database
        db = get_db()
        db.execute(
            'INSERT INTO news_posts (headline, sub_headline, author, introduction, paragraph_one,paragraph_two,paragraph_three, paragraph_four, quotes, tags, file)'
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?,?)',
            (headline, sub_headline, author, introduction,paragraph_one,paragraph_two,paragraph_three, paragraph_four, quotes, tags, filename)
        )
        db.commit()

        return redirect(url_for('university.news'))
        
    return render_template('university/dashboard/news_form.html')


@bp.route('/news')
def news():
    db = get_db()
    
    # Fetch distinct tags for the filter buttons
    tags = db.execute('SELECT DISTINCT tags FROM news_posts').fetchall()
    
    # Get the selected tag from query parameters
    selected_tag = request.args.get('tags')
    
    if selected_tag:
        # Fetch posts filtered by the selected tag
        news_posts = db.execute(
            'SELECT id, headline, sub_headline, author, introduction, paragraph_one,paragraph_two,paragraph_three, paragraph_four, quotes, tags, file, created_at FROM news_posts WHERE tags LIKE ?',
            ('%' + selected_tag + '%',)
        ).fetchall()
    else:
        # Fetch all posts if no tag is selected
        news_posts = db.execute(
            'SELECT id, headline, sub_headline, author, introduction, paragraph_one,paragraph_two,paragraph_three, paragraph_four, quotes, tags,  file, created_at FROM news_posts'
        ).fetchall()
    
    return render_template('university/news.html', news_posts=news_posts, tags=tags)

@bp.route('/news/<int:post_id>')
def news_post_details(post_id):
    db = get_db()
    post = db.execute(
        'SELECT id, headline, sub_headline, author, introduction, paragraph_one,paragraph_two,paragraph_three, paragraph_four, quotes, tags, file, created_at '
        'FROM news_posts WHERE id = ?',
        (post_id,)
    ).fetchone()

    if post is None:
        abort(404, f"News post id {post_id} doesn't exist.")

    return render_template('university/news_post.html', post=post)