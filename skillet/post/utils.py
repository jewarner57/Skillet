from flask_login import current_user
from datetime import datetime
from skillet import db


def update_user_activity(user):
    user.last_active = datetime.now()
    db.session.add(user)
    db.session.commit()
