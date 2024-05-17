# -- encoding: UTF-8 --
import re
import uuid

import pytest

from enumfields import IntegerEnumField

from .enums import Color, IntegerEnum, StateFlow, StateFlowAnyFirst, Taste, ZeroEnum
from .models import MyModel

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.urls('tests.urls')
def test_model_admin_post(admin_client):
    url = reverse("admin:tests_mymodel_add")
    secret_uuid = str(uuid.uuid4())
    post_data = {
        'color': Color.RED.value,
        'taste': Taste.UMAMI.value,
        'random_code': secret_uuid,
        'zero2': ZeroEnum.ZERO.value,
        'state': StateFlow.START.value,
        'any_first_state': StateFlowAnyFirst.START.value,
    }
    response = admin_client.post(url, follow=True, data=post_data)
    response.render()
    text = response.content

    assert b"This field is required" not in text
    assert b"Select a valid choice" not in text
    try:
        inst = MyModel.objects.get(random_code=secret_uuid)
    except MyModel.DoesNotExist:
        assert False, "Object wasn't created in the database"
    assert inst.color == Color.RED, "Redness not assured"
    assert inst.taste == Taste.UMAMI, "Umami not there"


@pytest.mark.django_db
@pytest.mark.urls('tests.urls')
@pytest.mark.parametrize('q_color', (None, Color.BLUE, Color.RED))
@pytest.mark.parametrize('q_taste', (None, Taste.SWEET, Taste.SOUR))
@pytest.mark.parametrize('q_int_enum', (None, IntegerEnum.A, IntegerEnum.B))
def test_model_admin_filter(admin_client, q_color, q_taste, q_int_enum):
    """
    Test that various combinations of ChoiceEnum filters seem to do the right thing in the change list.
    """

    # Create a bunch of objects...
    MyModel.objects.create(color=Color.RED)
    for taste in Taste:
        MyModel.objects.create(color=Color.BLUE, taste=taste)
    MyModel.objects.create(color=Color.BLUE, taste=Taste.UMAMI, int_enum=IntegerEnum.A)
    MyModel.objects.create(color=Color.GREEN, int_enum=IntegerEnum.B)

    # Build a Django lookup...
    lookup = dict((k, v) for (k, v) in {
        'color': q_color,
        'taste': q_taste,
        'int_enum': q_int_enum,
    }.items() if v is not None)
    # Build the query string (this is assuming things, sort of)
    qs = dict(('%s__exact' % k, v.value) for (k, v) in lookup.items())
    # Run the request!
    response = admin_client.get(reverse('admin:tests_mymodel_changelist'), data=qs)
    response.render()

    # Look for the paginator line that lists how many results we found...
    count = int(re.search(r'(\d+) my model', response.content.decode('utf8')).group(1))
    # and compare it to what we expect.
    assert count == MyModel.objects.filter(**lookup).count()


def test_django_admin_lookup_value_for_integer_enum_field():
    field = IntegerEnumField(Taste)

    assert field.get_prep_value(str(Taste.BITTER.value)) == 3, "get_prep_value should be able to convert from strings"
