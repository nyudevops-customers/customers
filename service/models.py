"""
Models for Customer

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass


class Customer(db.Model):
    """
    Class that represents a <your resource model name>
    """

    app = None

    # Table Schema
    customer_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(63))
    lastname = db.Column(db.String(63))
    email_id = db.Column(db.String(63))
    address = db.Column(db.String(63))
    phone_number = db.Column(db.String(32))
    card_number = db.Column(db.String(32), nullable=True)

    def __repr__(self):
        return "<customer_id=[%s] Firstname %r Lastname %r  email_id %r address %r phone_number %r card_number %r>" % (self.customer_id, self.firstname, self.lastname,
        self.email_id, self.address, self.phone_number, self.card_number)

    def create(self):
        """
        Creates a Customer to the database
        """
        logger.info("Creating %s %s", self.firstname, self.lastname)
        self.customer_id = None  #customer_id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):

        if not self.customer_id:
            raise DataValidationError("No fields provided to update")
        db.session.commit()

    def delete(self):
        """ Removes a Customer from the data store """
        logger.info("Deleting %s %s", self.firstname, self.lastname)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {"customer_id": self.customer_id, "firstname": self.firstname, "lastname": self.lastname,
        "email_id": self.email_id, "address": self.address, "phone_number": self.phone_number,"card_number":self.card_number}

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.firstname = data["firstname"]
            self.lastname = data["lastname"]
            self.address = data["address"]
            self.phone_number = data["phone_number"]
            self.card_number = data["card_number"]
            self.email_id = data["email_id"]
        except AttributeError as error:
            raise DataValidationError(
                "Invalid attribute: " + error.args[0]
            )
        except KeyError as error:
            raise DataValidationError(
                "Invalid Customer: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Customer: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Customers in the database """
        logger.info("Processing all Customers")
        return cls.query.all()

    @classmethod
    def find(cls, customer_id):
        """ Finds a Customer by it's customer_id """
        logger.info("Processing lookup for customer_id %s ...", customer_id)
        return cls.query.get(customer_id)

    @classmethod
    def find_or_404_int(cls, customer_id):
        """ Find a Customer by it's customer_id """
        logger.info("Processing lookup or 404 for customer_id %s ...", customer_id)
        return cls.query.get_or_404(customer_id)
        
    @classmethod
    def find_or_404_str(cls, id):
        """ Find a Customer by it's email_id """
        logger.info("Processing lookup or 404 for email_id  %s ...", id)
        return cls.query.get_or_404(id)

    @classmethod
    def find_by_firstname(cls, firstname):
        """Returns all Customers with the given firstname

        Args:
            name (string): the name of the Customers you want to match
        """
        logger.info("Processing first name query for %s  ...", firstname)
        return cls.query.filter(cls.firstname == firstname)

    @classmethod
    def find_by_lastname(cls, lastname):
        """Returns all Customers with the given lastname

        Args:
            name (string): the name of the Customers you want to match
        """
        logger.info("Processing last name query for %s  ...", lastname)
        return cls.query.filter(cls.lastname == lastname) 

    @classmethod
    def find_by_emailID(cls, email_id):
        """Returns all Customers with the given Email ID

        Args:
            name (string): the name of the Customers you want to match
        """
        logger.info("Processing name query for %s  ...", email_id)
        return cls.query.filter(cls.email_id == email_id) 
        
    @classmethod
    def find_by_phone_number(cls, phone_number):
        """Returns all Customers with the given phone number

        Args:
            name (string): the name of the Customers you want to match
        """
        logger.info("Processing name query for %s  ...", phone_number)
        return cls.query.filter(cls.phone_number == phone_number) 
