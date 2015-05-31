from peewee import *
import datetime

db = SqliteDatabase('tracking.db', threadlocals=True)

class BaseModel(Model):
    class Meta:
        database = db


class Tracking(BaseModel):
    added_time = DateTimeField(default=datetime.datetime.now())
    remaining_data = FloatField()