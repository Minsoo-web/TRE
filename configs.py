"""Contains various settings to be used in this package"""


import base64

from typing import NoReturn


class __Config:
    """This is the base class for all settings"""

    pass


class GlobalConfig(__Config):
    """It has settings to be used system-wide"""

    pass


class JenkinsConfig(__Config):
    """Contains the data needed to call Jenkins API"""

    def __init__(self):
        self.__url = 'aHR0cDovLzE5Mi4xNjguMTAyLjExNDozMTYwMC8='
        self.__user = 'ZG9uZ2h5dW4=='
        self.__password = 'Z2hrZGVoZGd1czEh'

    def __encoder(self, text: str) -> str:
        """Encode user data by base64

        Args:
            text (str): Text to be encoded

        Returns:
            str: Encoded text
        """

        return base64.b64encode(text.encode('utf-8'))

    def __decoder(self, text: str) -> str:
        """Decode user data from base64

        Args:
            text (str): Text to be decoded

        Returns:
            str: Decoded text
        """

        return base64.b64decode(text).decode('utf-8')

    @property
    def url(self) -> str:
        """Return your jenkins url

        Returns:
            str: Decoded jenkins url
        """

        return self.__decoder(self.__url)

    @url.setter
    def url(self, new_url: str) -> NoReturn:
        """Set new jenkins url

        Args:
            new_url (str): You wanted new jenkins url
        """

        self.__url = self.__encoder(new_url)

    @property
    def user(self) -> str:
        """Return your jenkins username

        Returns:
            str: Decoded jenkins username
        """

        return self.__decoder(self.__user)

    @user.setter
    def user(self, new_user: str) -> NoReturn:
        """Set new jenkins user

        Args:
            new_user (str): You wanted new jenkins user
        """

        self.__user = self.__encoder(new_user)

    @property
    def password(self) -> str:
        """Return your jenkins password

        Returns:
            str: Decoded jenkins password
        """

        return self.__decoder(self.__password)

    @password.setter
    def password(self, new_password: str) -> NoReturn:
        """Set new jenkins password

        Args:
            new_password (str): You wanted new jenkins password
        """

        self.__password = self.__encoder(new_password)
