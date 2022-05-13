from flask import Response
from market_site import PHYSICAL_PERSON, app
from market_site.models import User
from flask_login import login_required
import json



@app.route('/api/user/<int:user_id>/hard_assets')
@login_required
def api_user_hard_assets(user_id):
	user = User.query.get_or_404(user_id)
	data = []
	for hard_asset in user.hard_assets:
		data.append(hard_asset.objectify())
	return Response(json.dumps(data), mimetype='text/json')