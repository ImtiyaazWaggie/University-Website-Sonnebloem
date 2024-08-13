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
            error = 'Headline is required.'

        elif not sub_headline:
            error = 'Last Name is required.'

        elif not author:
            error = 'ID Number is required.'

        elif not introduction:
            error = 'Date of Birth is required.'

        elif not paragraph_one:
            error = 'Phone Number is required.'
        elif not paragraph_two:
            error = 'Phone Number is required.'
        elif not paragraph_three:
            error = 'Phone Number is required.'
        elif not paragraph_four:
            error = 'Phone Number is required.'

        elif not quotes:
            error = 'Email Address is required.'

        elif not tags:
            error = 'Address / Street is required.'
            
        elif not file:
            error = 'File upload is required.'
        
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




#-------------------Application form-----------------------------------------------------


@bp.route('/application_form', methods=('GET', 'POST'))
def create_application_form():
    if request.method == 'POST':
        full_name = request.form['full_name']
        last_name = request.form['last_name']
        id_number = request.form['id_number']
        dob = request.form['dob']
        phone_number = request.form['phone_number']
        email = request.form['email']
        home_address = request.form['home_address']
        city = request.form['city']
        country = request.form['country']
        home_state = request.form['home_state']
        zipcode = request.form['zipcode']

        subject_one = request.form['subject_one']
        grade_one = request.form['grade_one']
        subject_two = request.form['subject_two']
        grade_two = request.form['grade_two']
        subject_three = request.form['subject_three']
        grade_three = request.form['grade_three']
        subject_four = request.form['subject_four']
        grade_four = request.form['grade_four']
        subject_five = request.form['subject_five']
        grade_five = request.form['grade_five']
        subject_six = request.form['subject_six']
        grade_six = request.form['grade_six']
        subject_seven = request.form['subject_seven']
        grade_seven = request.form['grade_seven']

        first_choice = request.form['first_choice']
        second_choice = request.form['second_choice']

        # Handle file upload separately
        file = request.files.get('file')
        
        error = None
        
        
        if not full_name:
            error = 'Full Name is required.'

        elif not last_name:
            error = 'Last Name is required.'

        elif not id_number:
            error = 'ID Number is required.'

        elif not dob:
            error = 'Date of Birth is required.'

        elif not phone_number:
            error = 'Phone Number is required.'

        elif not email:
            error = 'Email Address is required.'

        elif not home_address:
            error = 'Address / Street is required.'

        elif not city:
            error = 'City is required.'

        elif not country:
            error = 'Country / Region is required.'

        elif not home_state:
            error = 'State / Province is required.'

        elif not zipcode:
            error = 'Zipcode is required.'

        # Academic Details (assuming at least one subject and grade is required)
        elif not subject_one or not grade_one:
            error = 'First subject and grade are required.'

        elif not subject_two or not grade_two:
            error = 'Second subject and grade are required.'
            
        elif not subject_three or not grade_three:
            error = 'Subject Three and its grade are required.'

        elif not subject_four or not grade_four:
            error = 'Subject Four and its grade are required.'

        elif not subject_five or not grade_five:
            error = 'Subject Five and its grade are required.'

        elif not subject_six or not grade_six:
            error = 'Subject Six and its grade are required.'

        elif not subject_seven or not grade_seven:
            error = 'Subject Seven and its grade are required.'

        # You can add similar checks for additional subjects if needed

        elif not first_choice:
            error = 'First Choice Programme is required.'

        elif not second_choice:
            error = 'Second Choice Programme is required.'

        # File validation (optional)
        elif not file:
            error = 'File upload is required.'


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
        
            
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO applications (full_name, last_name, id_number, dob, phone_number, email, home_address, city, country, home_state, zipcode, '
                'subject_one, grade_one, subject_two, grade_two, subject_three, grade_three, subject_four, grade_four, subject_five, grade_five, '
                'subject_six, grade_six, subject_seven, grade_seven, first_choice, second_choice, file) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (full_name, last_name, id_number, dob, phone_number, email, home_address, city, country, home_state, zipcode, 
                subject_one, grade_one, subject_two, grade_two, subject_three, grade_three, subject_four, grade_four, subject_five, grade_five,
                subject_six, grade_six, subject_seven, grade_seven, first_choice, second_choice, filename)
            )
            db.commit()
            return redirect(url_for('university.index'))
    
    return render_template('university/application_form.html')




@bp.route('/events')
def events():
    db = get_db()
    
    # Fetch distinct tags for the filter buttons
        # Fetch all posts if no tag is selected
    events_posts = db.execute(
        'SELECT event_id, event_name, event_date, start_time, end_time, event_location, event_description, max_attendees, event_type, organizer_name, organizer_email, organizer_phone, file FROM events'
    ).fetchall()
    
    return render_template('university/events.html', events_posts=events_posts)


@bp.route('/create/event_form',methods=('GET', 'POST'))
def event_form():
    
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        event_location = request.form['event_location']
        event_description = request.form['event_description']
        max_attendees = request.form['max_attendees']
        event_type = request.form['event_type']
        organizer_name = request.form['organizer_name']
        organizer_email = request.form['organizer_email']
        organizer_number = request.form['organizer_number']


        # Handle file upload separately
        file = request.files.get('file')
        
        error = None

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
        
            
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO events (event_name, event_date, start_time, end_time, event_location, event_description, max_attendees, event_type, organizer_name, organizer_email, organizer_phone, file) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (event_name, event_date, start_time, end_time, event_location, event_description, max_attendees, event_type, organizer_name, organizer_email, organizer_number, filename)
            )
            db.commit()
            return redirect(url_for('university.events'))
        
    return render_template('university/dashboard/events_form.html')
