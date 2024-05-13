# coding: utf-8

"""
    Tator REST API

    Interface to the Tator backend.  # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from ..configuration import Configuration


class Favorite(object):
    """
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'entity_type_name': 'str',
        'id': 'int',
        'name': 'str',
        'page': 'int',
        'type': 'int',
        'user': 'int',
        'values': 'dict(str, object)'
    }

    attribute_map = {
        'entity_type_name': 'entity_type_name',
        'id': 'id',
        'name': 'name',
        'page': 'page',
        'type': 'type',
        'user': 'user',
        'values': 'values'
    }

    def __init__(self, entity_type_name=None, id=None, name=None, page=1, type=None, user=None, values=None, local_vars_configuration=None):  # noqa: E501
        """Favorite - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._entity_type_name = None
        self._id = None
        self._name = None
        self._page = None
        self._type = None
        self._user = None
        self._values = None
        self.discriminator = None

        if entity_type_name is not None:
            self.entity_type_name = entity_type_name
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if page is not None:
            self.page = page
        if type is not None:
            self.type = type
        if user is not None:
            self.user = user
        if values is not None:
            self.values = values

    @property
    def entity_type_name(self):
        """
        Name of entity type associated with the favorite

        :return: The entity_type_name of this Favorite. 
        :rtype: str
        """
        return self._entity_type_name

    @entity_type_name.setter
    def entity_type_name(self, entity_type_name):
        """
        Name of entity type associated with the favorite

        :param entity_type_name: The entity_type_name of this Favorite.
        :type: str
        """
        allowed_values = ["Localization", "State"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and entity_type_name not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `entity_type_name` ({0}), must be one of {1}"  # noqa: E501
                .format(entity_type_name, allowed_values)
            )

        self._entity_type_name = entity_type_name

    @property
    def id(self):
        """
        Unique integer identifying a favorite.

        :return: The id of this Favorite. 
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Unique integer identifying a favorite.

        :param id: The id of this Favorite.
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """
        Name of the favorite.

        :return: The name of this Favorite. 
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Name of the favorite.

        :param name: The name of this Favorite.
        :type: str
        """

        self._name = name

    @property
    def page(self):
        """
        Integer specifying page to display on. Should be 1-10.

        :return: The page of this Favorite. 
        :rtype: int
        """
        return self._page

    @page.setter
    def page(self, page):
        """
        Integer specifying page to display on. Should be 1-10.

        :param page: The page of this Favorite.
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                page is not None and page > 10):  # noqa: E501
            raise ValueError("Invalid value for `page`, must be a value less than or equal to `10`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                page is not None and page < 1):  # noqa: E501
            raise ValueError("Invalid value for `page`, must be a value greater than or equal to `1`")  # noqa: E501

        self._page = page

    @property
    def type(self):
        """
        Unique integer identifying entity type of this entry.

        :return: The type of this Favorite. 
        :rtype: int
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Unique integer identifying entity type of this entry.

        :param type: The type of this Favorite.
        :type: int
        """

        self._type = type

    @property
    def user(self):
        """
        Unique integer identifying a user.

        :return: The user of this Favorite. 
        :rtype: int
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Unique integer identifying a user.

        :param user: The user of this Favorite.
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                user is not None and user < 1):  # noqa: E501
            raise ValueError("Invalid value for `user`, must be a value greater than or equal to `1`")  # noqa: E501

        self._user = user

    @property
    def values(self):
        """
        Attribute name/value pairs.

        :return: The values of this Favorite. 
        :rtype: dict(str, object)
        """
        return self._values

    @values.setter
    def values(self, values):
        """
        Attribute name/value pairs.

        :param values: The values of this Favorite.
        :type: dict(str, object)
        """

        self._values = values

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Favorite):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Favorite):
            return True

        return self.to_dict() != other.to_dict()
