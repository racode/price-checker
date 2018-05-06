import uuid

from src.common.database import Database
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants
from src.common.utils import Utils
from src.models.alerts.alert import Alert

__author__ = "esobolie"


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email,)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an email password combo as sent my the site forms is valid or not
        Checks the e-mail exists and that the password associated to that e-mail is correct
        :param email: The user's email
        :param password: A hashed sha512 password
        :return: True if valid, False othervise
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})  # Password in sha512 -> pbkdf2_sha512
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user does not exists.")
        if not Utils.check_hashed_password(password, user_data["password"]):
            raise UserErrors.IncorrectPasswordError("Your password is wrong")
        return True

    @staticmethod
    def register_user(email, password):
        """
        This method registers user using email and pass
        The password already comes hashed as sha512
        :param email: user email (might be invalid)
        :param password: sha-512 hashed password
        :return:True if registered successfully, or false otherwise (exceptions can be raised)
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegistered("Email already exists")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("Email does not have valid format")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)
