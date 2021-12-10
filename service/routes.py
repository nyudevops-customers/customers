"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
import secrets
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_restx import Api, Resource, fields, reqparse, inputs
from . import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Customer, DataValidationError, DatabaseConnectionError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    # return (
    #     jsonify(name="Customer API Service",version="1.0"),
    #     status.HTTP_200_OK,
    # )
    """ Index page """
    return app.send_static_file('index.html')

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Customer REST API Service',
          description='This is a Customer server',
          default='customers',
          default_label='Customer operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
          prefix='/api'
         )

# Define the model so that the docs reflect what can be sent
create_model = api.model('Customer', {
    'firstname': fields.String(required=True,
                          description='The first name of the Customer'),
    'lastname': fields.String(required=True,
                          description='The last name of the Customer'),
    'email_id': fields.String(required=True,
                              description='The email id of the Customer'),
    'phone_number': fields.String(required=True,
                                description='The phone number of the Customer'),
    'active' : fields.Boolean(required=True,
                                description='Is the Customer activated'),
    'address' : fields.String(required=True,
                          description='The address of the Customer'),
    'card_number' : fields.String(required=True,
                          description='The card number of the Customer'),
})

customer_model = api.inherit(
    'CustomerModel', 
    create_model,
    {
        'customer_id': fields.Integer(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)


customer_args = reqparse.RequestParser()
customer_args.add_argument('firstname', type=str, required=False, location='args', help='List Customers by first name')
customer_args.add_argument('lastname', type=str, required=False, location='args', help='List Customers by last name')
customer_args.add_argument('email_id', type=str, required=False, location='args', help='List Customers by email id')
customer_args.add_argument('phone_number', type=str, required=False, location='args', help='List Customers by state')
customer_args.add_argument('active', type=inputs.boolean, required=False, location='args', help='List active Customers')

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@api.errorhandler(DatabaseConnectionError)
def database_connection_error(error):
    """ Handles Database Errors from connection attempts """
    message = str(error)
    app.logger.critical(message)
    return {
        'status_code': status.HTTP_503_SERVICE_UNAVAILABLE,
        'error': 'Service Unavailable',
        'message': message
    }, status.HTTP_503_SERVICE_UNAVAILABLE


######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
    """ Helper function used when testing API keys """
    return secrets.token_hex(16)



######################################################################
#  PATH: /customers
######################################################################
@api.route("/customers", strict_slashes=False)
class CustomerCollection(Resource):
    """ Handles all interactions with collections of Customers """
    #------------------------------------------------------------------
    # LIST ALL PETS
    #------------------------------------------------------------------
    @api.doc('list_customers')
    @api.expect(customer_args, validate=True)
    @api.marshal_list_with(customer_model)

    def get(self):
        """
        Retrieve a single Customer with the requested values
        """
        app.logger.info('Request to list Pets...')
        args = customer_args.parse_args()

        if args['email_id']:
            app.logger.info("Request for Customer with id: %s", args['email_id'])
            customer = Customer.find_by_emailID(args['email_id'])
            customer_list = [x.serialize() for x in customer]
            return customer_list, status.HTTP_200_OK
        
        elif args['firstname']:
            app.logger.info("Request for Customer with firstname: %s", args['firstname'])
            customer = Customer.find_by_firstname(args['firstname'])
            customer_list = [x.serialize() for x in customer]
            return customer_list, status.HTTP_200_OK
            
        elif args['lastname']:
            app.logger.info("Request for Customer with lastname: %s", args['lastname'])
            customer = Customer.find_by_lastname(args['lastname'])
            customer_list = [x.serialize() for x in customer]
            return customer_list, status.HTTP_200_OK
        
        elif args['phone_number']:
            app.logger.info("Request for Customer with phone_number: %s", args['phone_number'])
            customer = Customer.find_by_phone_number(args['phone_number'])
            customer_list = [x.serialize() for x in customer]
            return customer_list, status.HTTP_200_OK

        elif args['active']:
            app.logger.info("Request for Customer with active status: %s", args['active'])
            customer = Customer.find_by_boolean(args['active'])
            customer_list = [x.serialize() for x in customer]
            return customer_list, status.HTTP_200_OK

        else:
            app.logger.info("Request for all customers")
            customer = Customer.all()
            customer_list = [x.serialize() for x in customer]
            return customer_list, status.HTTP_200_OK

    #------------------------------------------------------------------
    # ADD A NEW CUSTOMER
    #------------------------------------------------------------------

    @api.doc('create_customers')
    @api.response(400, 'The posted data was not valid')
    @api.response(201, 'Customer created successfully')
    @api.expect(create_model)
    @api.marshal_with(customer_model, code=201)
    def post(self):
        """
        Creates a Customer
        This endpoint will create a Customer based the data in the body that is posted
        """
        app.logger.info("Request to create a customer")
        check_content_type("application/json")
        customer = Customer()
        app.logger.debug('Payload = %s', api.payload)
        customer.deserialize(api.payload)
        customer.create()
        message = customer.serialize()
        location_url = url_for("get_customers_byid", customer_id=customer.customer_id, _external=True)

        app.logger.info("Customer with ID [%s] created.", customer.customer_id)
        return message, status.HTTP_201_CREATED, {"Location": location_url}




@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers_byid(customer_id):
    """
    Retrieve a single Customer
    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for Customer with id: %s", customer_id)
    customer = Customer.find_or_404_int(customer_id)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)
    

# @app.route("/customers", methods=["POST"])
# def create_customers():
#     """
#     Creates a Customer
#     This endpoint will create a Customer based the data in the body that is posted
#     """
#     app.logger.info("Request to create a customer")
#     check_content_type("application/json")
#     customer = Customer()
#     customer.deserialize(request.get_json())
#     customer.create()
#     message = customer.serialize()
#     location_url = url_for("get_customers_byid", customer_id=customer.customer_id, _external=True)

#     app.logger.info("Customer with ID [%s] created.", customer.customer_id)
#     return make_response(
#         jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
#     )




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
@app.route('/customers/<int:customer_id>/deactivate',  methods = ["PUT"])
#@app.param('customer_id', 'Customer identifier')
def deactivate_customer(customer_id):
    """
    Deactivate a Customer
    This endpoint will deactivate a Customer
    """
    app.logger.info('Request to deactivate customer with id: %s', customer_id)
    customer = Customer.find(customer_id)
    if customer == None:
        app.abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found".format(customer_id))

    
    customer.active = False
    customer.update()
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)
        

######################################################################
# PATH: /customers/{user_id}/activate
######################################################################
@app.route('/customers/<int:customer_id>/activate', methods = ["PUT"])
#@app.param('customer_id', 'Customer identifier')
def activate_customer(customer_id):
    """
    Activate a Customer
    This endpoint will deactivate a Customer
    """
    app.logger.info('Request to activate customer with id: %s', customer_id)
    customer = Customer.find(customer_id)
    if customer == None:
        app.abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found".format(customer_id))
    customer.active = True
    customer.update()
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


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