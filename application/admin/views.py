from application import app, login_required
from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user
#from flask_user import roles_required
from .helpers import adminHelper
from application.poll.models import Poll
from application.vote.models import Vote
from application.account.models import Account
from datetime import datetime

@app.route('/admin/', methods=['GET'])
@login_required(role="ADMIN")
def admin_index():
    top_polls = Poll.get_admin_top_polls()
    top_vote_polls = Vote.admin_top_polls_most_votes()
    active_polls = Poll.admin_active_vs_inactive_polls(datetime)
    account_count = Account.query.count()
    vote_count = Vote.query.count()
    return render_template("/admin/index.html", top_polls=top_polls, 
        top_vote_polls=top_vote_polls, active_polls=active_polls,
        account_count=account_count, vote_count=vote_count)

@app.route('/admin/order66', methods=['GET'])
@login_required(role="ADMIN")
def admin_order66():
    executed = False
    if 'executed' in request.args:
        executed = bool(request.args['executed'])
    return render_template('/admin/order66.html', executed=executed)

@app.route('/admin/execute_order66', methods=['POST'])
@login_required(role="ADMIN")
def admin_execute_order66():
    helper = adminHelper()
    helper.execute_order66()
    return redirect(url_for('admin_order66', executed=1))