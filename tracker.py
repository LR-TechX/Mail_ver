from flask import Blueprint, send_file
from datetime import datetime
from models import db, EmailRecord

tracker_bp = Blueprint('tracker', __name__)

@tracker_bp.route('/tracker/<int:sender_id>/<int:receiver_id>')
def pixel(sender_id, receiver_id):
    record = EmailRecord.query.filter_by(sender_id=sender_id, receiver_id=receiver_id, opened=False).first()
    if record:
        record.opened = True
        record.opened_at = datetime.utcnow()
        db.session.commit()
    return send_file('static/images/pixel.png', mimetype='image/png')
