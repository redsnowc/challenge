from flask import Blueprint, render_template
from flask import request, current_app
from simpledu.models import Course, User, Live 
from simpledu.decorators import admin_required
from flask import redirect, url_for, flash
from simpledu.forms import CourseForm, UserForm, EditUserForm, db, CreateLive


admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/courses')
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
            page=page,
            per_page=current_app.config['ADMIN_PER_PAGE'],
            error_out=False
        )
    return render_template('admin/courses.html', pagination=pagination)

@admin.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        form.create_course()
        flash('课程创建成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/create_course.html', form=form)

@admin.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('课程更新成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/edit_course.html', form=form, course=course)

@admin.route('/course/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('课程删除成功', 'success')
    return redirect(url_for('admin.courses'))

@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
            page=page,
            per_page=current_app.config['ADMIN_PER_PAGE'],
            error_out=False
        )
    return render_template('admin/users.html', pagination=pagination)

@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        form.create_user()
        flash('用户创建成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form=form)

@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('用户更新成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/users/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('用户删除成功', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/live')
@admin_required
def live():
    lives = Live.query.all()
    return render_template('admin/live.html', lives=lives)

@admin.route('/live/create', methods=['GET', 'POST'])
@admin_required
def create_live():
    form = CreateLive()
    if form.validate_on_submit():
        form.create_live()
        flash('直播创建成功', 'success')
        return redirect(url_for('admin.live'))
    return render_template('admin/create_live.html', form=form)
