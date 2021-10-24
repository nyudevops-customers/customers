"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Customer, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )

@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers_byid(customer_id):
    """
    Retrieve a single Customer
    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for Customer with id: %s", customer_id)
    customer = Customer.find_or_404_int(customer_id)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

@app.route("/customers/<string:email_id>", methods=["GET"])
def get_customers_byemail(email_id):
    """
    Retrieve a single Customer with the requested email ID
    This endpoint will return a Customer based on it's email_id
    """
    app.logger.info("Request for Customer with id: %s", email_id)
    customer = Customer.find_or_404_str(email_id)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


@app.route("/customers", methods=["POST"])
def create_customers():
    """
    Creates a Customer
    This endpoint will create a Customer based the data in the body that is posted
    """
    app.logger.info("Request to create a customer")
    check_content_type("application/json")
    customer = Customer()
    customer.deserialize(request.get_json())
    customer.create()
    message = customer.serialize()
    location_url = url_for("get_customers_byid", customer_id=customer.customer_id, _external=True)

    app.logger.info("Customer with ID [%s] created.", customer.customer_id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Customer.init_db(app)
