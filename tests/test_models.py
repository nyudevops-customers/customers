"""
Test cases for Customer Model

"""
import logging
import unittest
import os
from service.models import Customer, DataValidationError, db
from service import app
from .factories import CustomerFactory

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


    def test_serialize_a_customer(self):
        """Test serialization of a Customer"""
        customer = CustomerFactory()
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("customer_id", data)
        self.assertEqual(data["customer_id"], customer.customer_id)
        self.assertIn("firstname", data)
        self.assertEqual(data["firstname"], customer.firstname)
        self.assertIn("lastname", data)
        self.assertEqual(data["lastname"], customer.lastname)
        self.assertIn("email_id", data)
        self.assertEqual(data["email_id"], customer.email_id)
        self.assertIn("address", data)
        self.assertEqual(data["address"], customer.address)
        self.assertIn("phone_number", data)
        self.assertEqual(data["phone_number"], customer.phone_number)
        self.assertIn("card_number", data)
        self.assertEqual(data["card_number"], customer.card_number)

    
    def test_deserialize_a_customer(self):
        """Test deserialization of a Customer"""
        data = {
            "customer_id": 1,
            "firstname": "Tom",
            "lastname": "Steven",
            "email_id": "123@gmail.com",
            "address": "110 street",
            "phone_number": "123",
            "card_number": "456",
        }
        customer = Customer()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.customer_id, None)
        self.assertEqual(customer.firstname, "Tom")
        self.assertEqual(customer.lastname, "Steven")
        self.assertEqual(customer.email_id, "123@gmail.com")
        self.assertEqual(customer.address, "110 street")
        self.assertEqual(customer.phone_number, "123")
        self.assertEqual(customer.card_number, "456")


    def test_deserialize_missing_data(self):
        """Test deserialization of a Customer with missing data"""
        data = {"customer_id": 1, "firstname": "Tom"}
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    
    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

