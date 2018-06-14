from mongoengine import *
from scrypt_user import scrypt_user
import datetime

class odd_payout(EmbeddedDocument):
    overview = StringField(required=True) #Description
    total_payout = DecimalField(required=True)
    probability = DecimalField(required=True)
    return_on_investment_ratio = DecimalField(required=True)

class betting_session(Document):
    game_id = StringField(required=True)
    streamer_id = ReferenceField(scrypt_user, required=True)
    total_amount_bet = DecimalField(required=True)
    streamer_payout = DecimalField(required=True)
    odds_payouts_table = EmbeddedDocumentListField(odd_payout, required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)    