from datetime import datetime
from faker import Faker
from .gigya import Profile

class Helper(object):
    """Helper class to assist in creating users"""

    def create_mock_gigya_user(self):
        """Create a simple mocked Gigya user"""
        fake = Faker()
        profile = Profile()
        profile.first_name = fake.first_name_female()
        profile.last_name = fake.last_name()
        profile.street = 'Medialaan'
        profile.house_number = '1'
        profile.box_number = ''
        profile.postal_code = '1800'
        profile.city = 'Vilvoorde'
        profile.birth_date = datetime(1990, 5, 20)
        profile.place_of_birth = 'Vilvoorde'
        email = '{}.{}@veryrealemail.com'.format(profile.first_name, profile.last_name)
        password = 'stievie'
        return {
            'profile': profile,
            'username': email,
            'password': password
        }
