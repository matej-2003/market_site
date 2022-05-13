from flask import render_template
from market_site import PHYSICAL_PERSON, app
from market_site.models import User
from flask_login import login_required

@app.route('/users', methods=['POST', 'GET'])
@login_required
def users():
	users = User.query.filter_by(type=PHYSICAL_PERSON).all()
	return render_template('users.html', title='Users', users=users)

@app.route('/user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def user(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user.html', title='User ' + user.username, user=user)