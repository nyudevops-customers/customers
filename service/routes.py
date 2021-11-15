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



@app.route("/customers", methods=["GET"])
def get_customers_by_values():
    """
    Retrieve a single Customer with the requested values
    """

    args= request.args.to_dict()

    if "email_id" in args:
        app.logger.info("Request for Customer with id: %s", ["email_id"])
        customer = Customer.find_by_emailID(args["email_id"]).first()
        return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)
    
    elif "firstname" in args:
        app.logger.info("Request for Customer with firstname: %s", args["firstname"])
        customer = Customer.find_by_firstname(args["firstname"]).first()
        return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)
        
    elif "lastname" in args:
        app.logger.info("Request for Customer with lastname: %s", args["lastname"])
        customer = Customer.find_by_lastname(args["lastname"]).first()
        return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)
    
    elif "phone_number" in args:
        app.logger.info("Request for Customer with phone_number: %s", args["phone_number"])
        customer = Customer.find_by_phone_number(args["phone_number"]).first()
        return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)
    
    else:
        app.logger.info("Request for all customers")
        customer = Customer.all()
        customer_list = [x.serialize() for x in customer]
        return make_response(jsonify(customer_list), status.HTTP_200_OK)

@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers_byid(customer_id):
    """
    Retrieve a single Customer
    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for Customer with id: %s", customer_id)
    customer = Customer.find_or_404_int(customer_id)
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




#######################
# UPDATE Customer
####################### 
@app.route("/customers/<int:customer_id>", methods = ["PUT"])
def update_customers(customer_id):

    app.logger.info("Requesting to update a customer")
    check_content_type("application/json")
    customer = Customer.find_or_404_int(customer_id)
    
    customer.deserialize(request.get_json())
    customer.customer_id = customer_id
    customer.update()
    app.logger.info("Updated customer with id %s", customer.customer_id)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    """
    Delete a Customer

    This endpoint will delete a Customer based on the id specified in the path
    """
    app.logger.info("Request to delete pet with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if customer:
        customer.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# PATH: /customers/{user_id}/deactivate
######################################################################
# @app.route('/customers/<int:customer_id>/deactivate',  methods = ["PUT"])
# @app.param('customer_id', 'Customer identifier')
# def deactivate_customer(self, customer_id):
#     """
#     Deactivate a Customer
#     This endpoint will deactivate a Customer
#     """
#     app.logger.info('Request to deactivate customer with id: %s', customer_id)
#     customers = Customer.find(customer_id)
#     if customers.count() == 0:
#         app.abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found".format(customer_id))

#     customer = customers[0]
#     customer.customer_id = customer_id
#     customer.active = False
#     customer.update()
#     return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)
        

######################################################################
# PATH: /customers/{user_id}/activate
######################################################################
# @app.route('/customers/<int:customer_id>/activate')
# @app.param('customer_id', 'Customer identifier')
# def deactivate_customer(self, customer_id):
#     """
#     Activate a Customer
#     This endpoint will deactivate a Customer
#     """
#     app.logger.info('Request to activate customer with id: %s', customer_id)
#     customers = Customer.find(customer_id)
#     if customers.count() == 0:
#         app.abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found".format(customer_id))

#     customer = customers[0]
#     customer.customer_id = customer_id
#     customer.active = True
#     customer.update()
#     return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


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
