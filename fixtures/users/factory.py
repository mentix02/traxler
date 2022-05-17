"""
factory.py

Contains helper functions to create fake users with populated info objects.
Does not actually generate data as fixtures/states/generate.py - we'd need
to use Django project settings to manually create hashed passwords via the
argon2 module but that seems like too much work - plus, we can make users
once via the Django shell, `manage.py dumpdata > fixtures/users/data.json`
and use those pre-created users. No more hashing, no more Django specific settings.
"""
import faker
import string
import random

from tax.models import State
from user.models import User, Info

DEFAULT_PASSWORD = 'abcd'

fake = faker.Faker()
states = State.objects.all()


def generate_fake_pan(last_name: str) -> str:
    """pan format - https://cleartax.in/g/terms/permanent-account-number-pan"""

    # generate the first 3 letters
    start_idx = random.randint(0, len(string.ascii_uppercase) - 3)
    first_three = string.ascii_uppercase[start_idx : start_idx + 3]

    # T - trust, F - firm, H - HUF, C - company, P - individual
    pan_status = random.choice(['T', 'F', 'H', 'P', 'C'])

    # generate the last 4 digits
    last_four = ''.join(sorted(str(random.randint(0, 9999)).zfill(4)))

    return (
        first_three
        + pan_status
        + last_name[0].upper()
        + last_four
        + random.choice(string.ascii_uppercase)
    )


def generate_fake_gst(state_code: str, pan: str) -> str:
    """gst format - https://groww.in/p/tax/gstin"""
    return state_code + pan + '1' + 'Z' + str(random.randint(0, 9))


def create_fake_info(user_id: int, last_name: str) -> Info:

    pan = generate_fake_pan(last_name)
    state: State = random.choice(states)
    gst = generate_fake_gst(state.code, pan)

    return Info.objects.create(
        pan=pan,
        gstin=gst,
        state=state,
        user_id=user_id,
        address=fake.address(),
        business_name=fake.company(),
    )


def create_fake_user(role: int = User.TAXPAYER) -> User:
    return User.objects.create_user(
        username=fake.user_name(),
        email=fake.email(),
        password=DEFAULT_PASSWORD,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        role=role,
    )
