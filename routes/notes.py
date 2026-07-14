from flask import ( Blueprint,
                   session,
                   url_for,
                   redirect,
                   flash,
                   render_template,
                   request

)
from models import Note
from extensions import db
notes_bp=Blueprint(
    'notes',
    __name__,
)



@notes_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You must be logged in to view the page','warning')
        return redirect(url_for('auth.login'))
    

    notes=Note.query.filter_by(
        user_id=session['user_id']).all()
    return render_template('dashboard.html',notes=notes)

#----------------------------------------
#Add notes

@notes_bp.route('/add_note',methods=['GET','POST'])
def add_note():
    if "user_id" not in session:
        flash('You must be logged in to view this page','warning')
        return redirect(url_for('auth.login'))
    

    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        note=Note(title=title,
                  discription=description,
                  user_id=session['user_id'])
        db.session.add(note)
        db.session.commit()
        flash('Note added successfully','success')
        return redirect(url_for('notes.dashboard'))

    return render_template('add_note.html')


#-------------------------------------------
#Edit notes
#----------------------------------------------

@notes_bp.route('/edit_note/<int:id>',methods=['GET','POST'])
def edit_note(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    note=Note.query.get_or_404(id)
    #security check
    if note.user_id!=session['user_id']:
        flash('You cannot edit this note','danger')
        return redirect(url_for('notes.dashboard'))
    
    if request.method=='POST':
        note.title=request.form['title']
        note.description=request.form['description']
        db.session.commit()
        flash('Note updatewd successfully','success')
        return redirect(url_for('notes.dashboard'))
    
    return render_template('edit_notes.html',note=note)


#-----------------------------------
#Delete notes
#-------------------------------------

@notes_bp.route('/delete_note/<int:id>')
def delete_note(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    note=Note.query.get_or_404(id)
    #security check
    if note.user_id!=session['user_id']:
        flash('You cannot delete this note','danger')
        return redirect(url_for('notes.dashboard'))
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully','success')
    return redirect(url_for('notes.dashboard'))

    
    