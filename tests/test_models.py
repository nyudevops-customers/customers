"""
Test cases for Customer Model

"""
import logging
import unittest
import os
from service.models import Customer, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres")

######################################################################
#  <Customer>   M O D E L   T E S T   C A S E S
######################################################################
class TestCustomer(unittest.TestCase):
    """ Test Cases for Customer Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Customer.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_customer(self):
        """ Test something """
        customer = Customer(firstname="Tom", lastname="Steven", email_id="123@gmail.com", address="110 street", phone_number="123", card_number="456")
        self.assertTrue(customer != None)
        self.assertEqual(customer.customer_id, None)
        self.assertEqual(customer.firstname, "Tom")
        self.assertEqual(customer.lastname, "Steven")
        self.assertEqual(customer.email_id, "123@gmail.com")
        self.assertEqual(customer.address, "110 street")
        self.assertEqual(customer.phone_number, "123")
        self.assertEqual(customer.card_number, "456")
