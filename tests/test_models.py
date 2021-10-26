"""
Test cases for Customer Model

"""
import logging
import unittest
import os

from werkzeug.exceptions import NotFound
from service.models import Customer, DataValidationError, db
from service import app
from .factories import CustomerFactory
from flask import jsonify

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
        customer = Customer(firstname="Tom", lastname="Steven", email_id="123@gmail.com", address="102 XYZ St, Apt 98, Tx", phone_number="200988884", card_number="48097572893")
        self.assertTrue(customer != None)
        self.assertEqual(customer.customer_id, None)
        self.assertEqual(customer.firstname, "Tom")
        self.assertEqual(customer.lastname, "Steven")
        self.assertEqual(customer.email_id, "123@gmail.com")
        self.assertEqual(customer.address, "102 XYZ St, Apt 98, Tx")
        self.assertEqual(customer.phone_number, "200988884")
        self.assertEqual(customer.card_number, "48097572893")


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
            "address": "102 XYZ St, Apt 98, Tx",
            "phone_number": "200988884",
            "card_number": "48097572893",
        }
        customer = Customer()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.customer_id, None)
        self.assertEqual(customer.firstname, "Tom")
        self.assertEqual(customer.lastname, "Steven")
        self.assertEqual(customer.email_id, "123@gmail.com")
        self.assertEqual(customer.address, "102 XYZ St, Apt 98, Tx")
        self.assertEqual(customer.phone_number, "200988884")
        self.assertEqual(customer.card_number, "48097572893")

    def test_deserialize_with_type_error(self):
        """ Deserialize a Customer with a TypeError """
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, [])

    def test_deserialize_with_key_error(self):
        """ Deserialize a Customer with a KeyError """
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, {})

    def test_list_all(self):
        """Test case to list all customers"""
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        self.assertEqual(len(Customer.all()), 3)
        

    def test_find_customer(self):
        """ Find a customer by ID """
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        logging.debug(customers)
        # make sure they got updated
        self.assertEqual(len(Customer.all()), 3)
        # find the 2nd customer in the list
        customer = Customer.find(customers[1].customer_id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.customer_id, customers[1].customer_id)
        self.assertEqual(customer.firstname, customers[1].firstname)
        self.assertEqual(customer.lastname, customers[1].lastname)
        self.assertEqual(customer.email_id, customers[1].email_id)
        self.assertEqual(customer.address, customers[1].address)
        self.assertEqual(customer.phone_number, customers[1].phone_number)
        self.assertEqual(customer.card_number, customers[1].card_number)


    def test_find_by_firstname(self):
        """ Find a Customer by FirstName """
        Customer(firstname="John", lastname="Doe", email_id="jd@xyz.com",address="102 Mercer St, Apt 8, NY",phone_number="200987634",card_number="489372893").create()
        Customer(firstname="Jane", lastname="Doe", email_id="jnd@xyz.com",address="102 XYZ St, Apt 98, Tx",phone_number="200988884",card_number="48097572893").create()
        customers = Customer.find_by_firstname("Jane")
        self.assertEqual(customers[0].lastname,"Doe")
        self.assertEqual(customers[0].email_id,"jnd@xyz.com")
        self.assertEqual(customers[0].address,"102 XYZ St, Apt 98, Tx")
        self.assertEqual(customers[0].phone_number,"200988884")
        self.assertEqual(customers[0].card_number,"48097572893")

    def test_find_by_lastname(self):
        """ Find a Customer by LastName """
        Customer(firstname="John", lastname="Doe", email_id="jd@xyz.com",address="102 Mercer St, Apt 8, NY",phone_number="200987634",card_number="489372893").create()
        Customer(firstname="Jane", lastname="Doe", email_id="jnd@xyz.com",address="102 XYZ St, Apt 98, Tx",phone_number="200988884",card_number="48097572893").create()
        customers = Customer.find_by_lastname("Doe")
        self.assertEqual(customers[0].firstname,"John")
        self.assertEqual(customers[0].email_id,"jd@xyz.com")
        self.assertEqual(customers[0].address,"102 Mercer St, Apt 8, NY")
        self.assertEqual(customers[0].phone_number,"200987634")
        self.assertEqual(customers[0].card_number,"489372893")
        self.assertEqual(customers[1].firstname,"Jane")
        self.assertEqual(customers[1].email_id,"jnd@xyz.com")
        self.assertEqual(customers[1].address,"102 XYZ St, Apt 98, Tx")
        self.assertEqual(customers[1].phone_number,"200988884")
        self.assertEqual(customers[1].card_number,"48097572893")
    
    def test_find_by_email_id(self):
        """ Find a Customer by Email ID """
        Customer(firstname="John", lastname="Doe", email_id="jd@xyz.com",address="102 Mercer St, Apt 8, NY",phone_number="200987634",card_number="489372893").create()
        Customer(firstname="Jane", lastname="Doe", email_id="jnd@xyz.com",address="102 XYZ St, Apt 98, Tx",phone_number="200988884",card_number="48097572893").create()
        customers = Customer.find_by_emailID("jd@xyz.com")
        self.assertEqual(customers[0].firstname,"John")
        self.assertEqual(customers[0].lastname,"Doe")
        self.assertEqual(customers[0].address,"102 Mercer St, Apt 8, NY")
        self.assertEqual(customers[0].phone_number,"200987634")
        self.assertEqual(customers[0].card_number,"489372893")

    def test_find_by_phone_number(self):
        """ Find a Customer by Phone Number """
        Customer(firstname="John", lastname="Doe", email_id="jd@xyz.com",address="102 Mercer St, Apt 8, NY",phone_number="200987634",card_number="489372893").create()
        Customer(firstname="Jane", lastname="Doe", email_id="jnd@xyz.com",address="102 XYZ St, Apt 98, Tx",phone_number="200988884",card_number="48097572893").create()
        customers = Customer.find_by_phone_number("200987634")
        self.assertEqual(customers[0].firstname,"John")
        self.assertEqual(customers[0].lastname,"Doe")
        self.assertEqual(customers[0].email_id,"jd@xyz.com")
        self.assertEqual(customers[0].address,"102 Mercer St, Apt 8, NY")
        self.assertEqual(customers[0].card_number,"489372893")

    def test_find_or_404_found(self):
        """ Find or return 404 found """
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()

        customer = Customer.find_or_404_int(customers[1].customer_id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.customer_id, customers[1].customer_id)
        self.assertEqual(customer.firstname, customers[1].firstname)
        self.assertEqual(customer.lastname, customers[1].lastname)
        self.assertEqual(customer.email_id, customers[1].email_id)
        self.assertEqual(customer.address, customers[1].address)
        self.assertEqual(customer.phone_number, customers[1].phone_number)
        self.assertEqual(customer.card_number, customers[1].card_number)


    def test_find_or_404_not_found(self):
        """ Find or return 404 NOT found """
        self.assertRaises(NotFound, Customer.find_or_404_int, 0)


    def test_update_a_customer(self):
        """Update or return 404 NOT FOUND"""

        test_customer = Customer(firstname="Dev", lastname="Lincoln", email_id="dldl@xyz.com", address="22nd St. X Ave, N.Y.", phone_number="123456789", card_number="1615141312109988")
        test_customer.create()

        self.assertEqual(test_customer.customer_id, 1)

        test_customer.phone_number = "987654321"
        test_customer.update()

        cust = Customer.find(1)
        self.assertEqual(cust.phone_number, "987654321")

    def test_delete_customer(self):
        """ Delete a Customer """
        customer = CustomerFactory()
        customer.create()
        self.assertEqual(len(Customer.all()), 1)
        # delete the pet and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(Customer.all()), 0)
    
    def test_remove_all_customers(self):
        """ Remove all customers """
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        self.assertEqual(len(Customer.all()), 3) 
        customer.remove_all()
        all_customers = Customer.all()
        self.assertEquals(len(all_customers), 0)

    def test_repr_string(self):
        """"Test the _repr_ method"""

        customer = Customer(firstname="John", lastname="Doe", email_id="jd@xyz.com",address="102 Mercer St, Apt 8, NY",phone_number="200987634",card_number="489372893")
        customer.create()
        resp_string = repr(customer)
        test_string = "<customer_id=[{}] Firstname {} Lastname {} email_id {} address {} phone_number {} card_number {}>".format(customer.customer_id, customer.firstname, customer.lastname,
        customer.email_id, customer.address, customer.phone_number, customer.card_number)
        self.assertEqual(resp_string,test_string)
        
    def test_update_fail(self):
        """Test to see if update raises Data validation error"""

        cust = CustomerFactory()
        data = {
            "customer_id": None,
            "firstname": "Tom",
            "lastname": "Steven",
            "email_id": "123@gmail.com",
            "address": "102 Mercer St, Apt 8, NY",
            "phone_number": "200987634",
            "card_number": "489372893",
        }

        cust.deserialize(data)
        cust.customer_id = None

        self.assertRaises(DataValidationError, cust.update)
