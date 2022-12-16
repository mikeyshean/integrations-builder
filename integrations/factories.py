import factory
from faker import Factory as Fake
from integrations.models import Category, Integration

faker = Fake.create()

class CategoryFactory(factory.django.DjangoModelFactory):
    """
    Creates a Category factory model
    """

    class Meta:
        model = Category
    
    name = factory.Sequence(lambda n: "{word}_{n}".format(word=faker.word(), n=n))


class IntegrationFactory(factory.django.DjangoModelFactory):
    """
    Creates a Integration factory model
    """

    class Meta:
        model = Integration
    
    name = factory.Sequence(lambda n: "{word}_{n}".format(word=faker.word(), n=n))
    category = factory.SubFactory(CategoryFactory)
