import factory
from factory.fuzzy import FuzzyChoice
from service.models import Customer


class CustomerFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:
        model = Customer

    customer_id = factory.Sequence(lambda n: n)
    firstname = factory.Faker("first_name")
    lastname = factory.Faker("last_name")
    email_id = factory.Faker("email")
    address = factory.Faker("address")
    phone_number = factory.Faker("phone_number")
    card_number = factory.Faker("phone_number")
    active = FuzzyChoice(choices=[True])