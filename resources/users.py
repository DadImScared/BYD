import datetime
import json
import config
from flask import jsonify, Blueprint, abort, make_response, g, request
from resources.schemas import PostRequestSchema
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
        appointment, _ = models.Appointment.get_or_create(
            person=person,
            doctor=doctor,
            **data["appointment"]
        )
        charge = stripe.Charge.create(
            amount=200,
            currency="usd",
            source=data["token"],
            description="Fee for BillYourDoctor.com"
        )
        models.Fee.get_or_create(appointment=appointment, defaults={"charge_info": charge})
        # send payment confirmation to person email
        return 200


user_api = Blueprint('resources.users', __name__)
api = Api(user_api)
api.add_resource(
    CreateAppointment,
    '/add',
    endpoint="create_appointment"
)
