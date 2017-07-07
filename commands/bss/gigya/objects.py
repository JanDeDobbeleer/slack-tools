
class Profile(object):
    """
    Represents a user's profile from the identity system.
    """
    def __init__(self, email=None, first_name=None, last_name=None, birth_date=None, place_of_birth=None, gender=None, street=None,
                 house_number=None, box_number=None, postal_code=None, city=None):
        """
        :type birth_date: date or None
        :type gender: just a char 'm', 'f' and 'u' are supported in Gigya at this time.
        """

        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.place_of_birth = place_of_birth
        self.gender = gender
        self.street = street
        self.house_number = house_number
        self.box_number = box_number
        self.postal_code = postal_code
        self.city = city
