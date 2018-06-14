from mongoengine import *
from scrypt_user import scrypt_user
from betting_session import betting_session, odd_payout
import datetime

class better_info(Document):
    scrypt_user_id = ReferenceField(scrypt_user, required=True)
    amount_bet = DecimalField(required=True)
    betting_session_id = ReferenceField(betting_session, required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    payout = DecimalField(required=True)
    odd_payout_id = ReferenceField(odd_payout, required=True)