import datetime
import json
import config
from flask import jsonify, Blueprint, abort, make_response, g, request, render_template
from resources.schemas import PostRequestSchema
from send_email.email import send_mail
import models
from flask_restful import (Resource, Api, reqparse,
                               inputs, fields, marshal,
                               marshal_with, url_for)
import stripe

stripe.api_key = config.SSK


class CreateAppointment(Resource):

    def post(self):
        """Post method of CreateAppointment class"""

        json_data = request.get_json()
        schema = PostRequestSchema()
        data, errors = schema.load(json_data)

        if errors:
            return make_response(jsonify({
                "errors": errors
            }), 422)
        try:
            charge = stripe.Charge.create(
                amount=200,
                currency="usd",
                source=data["token"],
                receipt_email=data['person']['email'],
                description="Fee for billyourdr.com"
            )
        except stripe.InvalidRequestError:
            return make_response(jsonify({"message": "Invalid stripe token"}), 400)
        else:
            person, person_created = models.User.get_or_create(
                first_name=data['person']['first_name'],
                last_name=data['person']['last_name'],
                email=data['person']['email'],
                defaults={**data["person"]}
            )
            doctor, doctor_created = models.Doctor.get_or_create(
                first_name=data["doctor"]["first_name"],
                last_name=data["doctor"]["last_name"],
                email=data["doctor"]["email"],
                defaults={**data["doctor"]}
            )
            apt_data = data["appointment"]
            meet_time = datetime.datetime.strptime("{} {}".format(apt_data["appointment_date"], apt_data["meet_time"]),
                                                   "%Y-%m-%d %I:%M %p")
            appointment_time = datetime.datetime.strptime("{} {}".format(
                apt_data["appointment_date"], apt_data["appointment_time"]), "%Y-%m-%d %I:%M %p"
            )
            appointment, _ = models.Appointment.get_or_create(
                person=person,
                doctor=doctor,
                meet_time=meet_time,
                appointment_time=appointment_time
            )
            models.Fee.get_or_create(appointment=appointment, defaults={"charge_info": charge})
        # send payment confirmation to person email
        # fix empty text body to render template
        send_mail(
            subject='Bill Your Doctor payment confirmation and additional information',
            recipients=[person.email],
            text_body=render_template('email.txt', entry_id=appointment.appointment_id)
        )
        return make_response(jsonify({"message": "success"}), 200)


class Entry(Resource):

    def get(self, appointment_id):
        """get entry by appointment_id"""
        try:
            appointment = models.Appointment.get(appointment_id=appointment_id)
        except models.DoesNotExist:
            return make_response(jsonify({"message": "appointment not found"}), 404)
        else:
            status = appointment.status
            return make_response(jsonify({"status": status}), 200)


user_api = Blueprint('resources.users', __name__)
api = Api(user_api)
api.add_resource(
    CreateAppointment,
    '/add',
    endpoint="create_appointment"
)
api.add_resource(
    Entry,
    '/api/v1/entry/<appointment_id>',
    endpoint='entry'
)
