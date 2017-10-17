import os
import uuid
import datetime
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase, JSONField
import config


dir_path = os.path.dirname(os.path.realpath(__file__))

DATABASE = SqliteDatabase('{}{}people.db'.format(dir_path, os.path.sep))

psql_db = PostgresqlExtDatabase('my_database',
                                user=config.PGU,
                                password=config.PGP,
                                register_hstore=False,
                                host=config.HOST,
                                port=config.PORT
                                )


class BasePost(Model):
    class Meta:
        database = psql_db


class Charge(BasePost):
    info = JSONField()


class BaseModel(Model):
    class Meta:
        database = psql_db


class BasePerson(BaseModel):
    """Base model for both User and Doctor"""
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = CharField(max_length=255)
    joined_at = DateTimeField(default=datetime.datetime.now)
    address = TextField()
    city = TextField()
    state = TextField()
    phone = TextField()
    zip_code = TextField()


class User(BasePerson):
    """User model for database"""

    #: Salary of user
    salary = TextField()


class Doctor(BasePerson):
    """Doctor model for database"""


class Appointment(BaseModel):
    """Appointment model for database"""
    person = ForeignKeyField(rel_model=User)
    doctor = ForeignKeyField(rel_model=Doctor)
    appointment_time = DateTimeField(formats="%Y-%m-%d %I:%M %p")
    meet_time = DateTimeField(formats="%Y-%m-%d %I:%M %p")
    appointment_id = UUIDField(unique=True, default=uuid.uuid4)

    #: Status default unresolved
    status = CharField(default='unresolved')


class Fee(BaseModel):
    """Fee model for database. Relates a payment to an Appointment"""
    appointment = ForeignKeyField(rel_model=Appointment, unique=True)
    charge_info = JSONField()


def initialize():
    psql_db.connect()
    psql_db.create_tables([User, Doctor, Appointment, Fee], safe=True)
    psql_db.close()
