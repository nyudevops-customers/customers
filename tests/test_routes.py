"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import status  # HTTP Status Codes
from service.models import db
from service.routes import app, init_db
from .factories import CustomerFactory

# Disable all but ciritcal errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres")  
BASE_URL = "/customers"
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()


    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def _create_customers(self, count):
        """Factory method to create pets in bulk"""
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            resp = self.app.post(
                BASE_URL, json=test_customer.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test customer"
            )
            new_customer = resp.get_json()
            test_customer.customer_id = new_customer["customer_id"]
            customers.append(test_customer)
        return customers
    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_customer(self):
        """Create a new Customer"""
        test_customer = CustomerFactory()
        logging.debug(test_customer)
        resp = self.app.post(
            BASE_URL, json=test_customer.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_customer = resp.get_json()
        self.assertEqual(new_customer["firstname"], test_customer.firstname, "Firstname do not match")
        self.assertEqual(new_customer["lastname"], test_customer.lastname, "Lastname do not match")
        self.assertEqual(
            new_customer["email_id"], test_customer.email_id, "Email_id do not match"
        )
        self.assertEqual(
            new_customer["address"], test_customer.address, "Address does not match"
        )
        self.assertEqual(
            new_customer["phone_number"], test_customer.phone_number, "Phone_number does not match"
        )
        self.assertEqual(
            new_customer["card_number"], test_customer.card_number, "Card_number does not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_customer = resp.get_json()
        self.assertEqual(new_customer["firstname"], test_customer.firstname, "Firstnames do not match")
        self.assertEqual(new_customer["lastname"], test_customer.lastname, "Lastnames do not match")
        self.assertEqual(
            new_customer["email_id"], test_customer.email_id, "Email_id do not match"
        )
        self.assertEqual(
            new_customer["address"], test_customer.address, "Address does not match"
        )
        self.assertEqual(
            new_customer["phone_number"], test_customer.phone_number, "Phone_number does not match"
        )
        self.assertEqual(
            new_customer["card_number"], test_customer.card_number, "Card_number does not match"
        )

    def test_create_customer_no_data(self):
       """Create a Customer with missing data"""
       resp = self.app.post(BASE_URL, json={}, content_type=CONTENT_TYPE_JSON)
       self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_create_customer_no_content_type(self):
       """Create a Customer with no content type"""
       resp = self.app.post(BASE_URL)
       self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)