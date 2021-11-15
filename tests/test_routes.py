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

from flask.json import jsonify
from werkzeug.datastructures import ContentRange
from service import status  # HTTP Status Codes
from service.models import Customer, db
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
class TestCustomerServer(TestCase):
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


    def test_get_all(self):
        """Get all customers"""
        self._create_customers(3)
        res = self.app.get(BASE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.get_json()
        self.assertEqual(len(res_data),3)


    def test_get_customer_byid(self):
        """ Get a single Customer by id """
        # get the id of a customer
        test_customer = self._create_customers(1)[0]
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_customer.customer_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["firstname"], test_customer.firstname)
        self.assertEqual(data["lastname"], test_customer.lastname)
        self.assertEqual(data["email_id"], test_customer.email_id)
        self.assertEqual(data["address"], test_customer.address)
        self.assertEqual(data["phone_number"], test_customer.phone_number)
        self.assertEqual(data["card_number"], test_customer.card_number)

    def test_get_customer_by_email(self):
        """ Get a single Customer by email """
        # get the id of a customer
        test_customer = self._create_customers(1)[0]
        resp = self.app.get(
            "{0}?email_id={1}".format(BASE_URL, test_customer.email_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["customer_id"], test_customer.customer_id)
        self.assertEqual(data["firstname"], test_customer.firstname)
        self.assertEqual(data["lastname"], test_customer.lastname)
        self.assertEqual(data["address"], test_customer.address)
        self.assertEqual(data["phone_number"], test_customer.phone_number)
        self.assertEqual(data["card_number"], test_customer.card_number)

    def test_get_customer_by_firstname(self):
        """ Get a single Customer firstname"""
        # get the id of a customer
        test_customer = self._create_customers(1)[0]
        resp = self.app.get(
            "{0}?firstname={1}".format(BASE_URL, test_customer.firstname), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["customer_id"], test_customer.customer_id)
        self.assertEqual(data["email_id"], test_customer.email_id)
        self.assertEqual(data["lastname"], test_customer.lastname)
        self.assertEqual(data["address"], test_customer.address)
        self.assertEqual(data["phone_number"], test_customer.phone_number)
        self.assertEqual(data["card_number"], test_customer.card_number)

    def test_get_customer_by_lastname(self):
        """ Get a single Customer lastname"""
        # get the id of a customer
        test_customer = self._create_customers(1)[0]
        resp = self.app.get(
            "{0}?lastname={1}".format(BASE_URL, test_customer.lastname), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["customer_id"], test_customer.customer_id)
        self.assertEqual(data["firstname"], test_customer.firstname)
        self.assertEqual(data["email_id"], test_customer.email_id)
        self.assertEqual(data["address"], test_customer.address)
        self.assertEqual(data["phone_number"], test_customer.phone_number)
        self.assertEqual(data["card_number"], test_customer.card_number)
    

    def test_get_customer_by_phone_number(self):
        """ Get a single Customer phone number"""
        # get the id of a customer
        test_customer = self._create_customers(1)[0]
        resp = self.app.get(
            "{0}?phone_number={1}".format(BASE_URL, test_customer.phone_number), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["customer_id"], test_customer.customer_id)
        self.assertEqual(data["firstname"], test_customer.firstname)
        self.assertEqual(data["lastname"], test_customer.lastname)
        self.assertEqual(data["address"], test_customer.address)
        self.assertEqual(data["email_id"], test_customer.email_id)
        self.assertEqual(data["card_number"], test_customer.card_number)
    


    def test_get_customer_not_found(self):
        """ Get a Customers thats not found """
        resp = self.app.get("{}/0".format(BASE_URL))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    def test_update(self):
        """Update a customer's phone number"""

        random_customers = CustomerFactory()
        resp = self.app.post(
            BASE_URL, json=random_customers.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        new_customer = resp.get_json()
        new_customer["phone_number"] = "5555511111"

        resp = self.app.put("/customers/{}".format(new_customer["customer_id"]), json = new_customer, content_type = CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        updated_customer  = resp.get_json()
        self.assertEqual(new_customer["customer_id"],updated_customer["customer_id"])
        self.assertEqual(new_customer["phone_number"], updated_customer["phone_number"])

    def test_delete_customer(self):
        """ Delete a Customer """
        test_customer = self._create_customers(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, test_customer.customer_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "{}/{}".format(BASE_URL, test_customer.customer_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_deactivate_customer(self):
        """ Deactivate an existing Customer """
        test_customer = self._create_customers(1)[0]
        resp = self.app.put(
            "/customers/{0}/deactivate".format(test_customer.customer_id)
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()['active'], False)

    def test_activate_customer(self):
        """ Activate an existing customer """
        # create a customer to activate
        test_customer = self._create_customers(1)[0]
        #deactivate a customer
        resp = self.app.put(
            "/customers/{0}/deactivate".format(test_customer.customer_id)
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()['active'], False)
        # activate the customer
        resp_activate = self.app.put(
            "/customers/{0}/activate".format(test_customer.customer_id)
        )
        self.assertEqual(resp_activate.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_activate.get_json()['active'], True)







        
        