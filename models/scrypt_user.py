from mongoengine import *
import datetime

class scrypt_streamer(EmbeddedDocument):
    twitch_id = StringField(required=True)
    summary = StringField(required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)

class bets_stats(EmbeddedDocument):
    game_id = StringField(required=True)
    bet_amount = StringField(required=True)
    payout = DecimalField(required=True)
    transaction_id = StringField(required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    streamer_id = ReferenceField('scrypt_user')
    session_id = StringField(required=True)

class scrypt_user(Document):
    user_name = StringField(required=True)
    user_email = StringField(required=True)
    picture_path = StringField(required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    stripe_id = StringField(required=False)
    paypal_id = StringField(required=False)
    password = BinaryField(required=True)
    scrypt_token = StringField(required=True)
    scrypt_streamer = EmbeddedDocumentField(scrypt_streamer, required=False)
    bets_stats = EmbeddedDocumentListField(bets_stats, required=False)