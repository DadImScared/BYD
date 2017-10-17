from marshmallow import Schema, fields, validate, pre_load, ValidationError
import datetime


def validate_time(time_str):
    """Validates a time str is in the format of hh:mm am/pm

    :param time_str: Time string in the format of hh:mm am/pm
    :raises ValidationError:
    """
    try:
        valid_time = datetime.datetime.strptime(time_str, "%I:%M %p")
    except ValueError:
        raise ValidationError("Invalid time please format time like hh:mm am/pm")


class PersonSchema(Schema):
    """JSON schema for a person or doctor"""
    firstName = fields.String(
        attribute="first_name",
        required=True, error_messages={"required": "Name required"},
        validate=validate.Regexp(r'^[-a-zA-Z]+$', error="First name is not valid")
    )
    lastName = fields.String(
        attribute="last_name",
        required=True, error_messages={"required": "Last name required"},
        validate=validate.Regexp(r'^[-a-zA-Z]+$', error="Last name is not valid")
    )
    address = fields.String(validate=validate.Length(min=1, error="Address required"), required=True)
    city = fields.String(validate=validate.Regexp(r"^[a-zA-Z]+$", error="Not a valid city"), required=True)
    state = fields.String(validate=validate.Regexp(r"^[a-zA-Z]{2,}$", error="Not a valid state"), required=True)
    zipcode = fields.String(
        validate=validate.Regexp(r"^\d{5}$", error="Not a valid zip code"),
        required=True,
        attribute="zip_code"
    )
    email = fields.String(validate=validate.Email(error="Not a valid email address"), required=True)
    phone = fields.String(
        validate=validate.Regexp("^\\(?[0-9]{3}\\)?-?\\s?[0-9]{3}-[0-9]{4}$", error="Not a valid phone"), required=True
    )
    salary = fields.String(required=True)

    @pre_load
    def process_input(self, data):
        for key in data.keys():
            data[key] = data[key].lower().strip()
        return data


class AppointmentSchema(Schema):
    appointmentDate = fields.Date(error="Not a valid date.", attribute="appointment_date", required=True)
    appointmentTime = fields.String(error="Not a valid time", validate=validate_time,
                                    attribute='appointment_time', required=True)
    meetTime = fields.String(error="Not a valid time", validate=validate_time, attribute="meet_time", required=True)
    status = fields.String(default="unresolved")


class PostRequestSchema(Schema):
    person = fields.Nested(PersonSchema, required=True)
    doctor = fields.Nested(PersonSchema, exclude=('salary',), required=True)
    appointment = fields.Nested(AppointmentSchema, required=True)
    token = fields.String(required=True, error="Token required")
