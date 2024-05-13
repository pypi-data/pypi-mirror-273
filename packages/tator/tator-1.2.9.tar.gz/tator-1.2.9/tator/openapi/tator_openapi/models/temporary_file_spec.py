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


class TemporaryFileSpec(object):
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
        'hours': 'int',
        'lookup': 'str',
        'name': 'str',
        'url': 'str'
    }

    attribute_map = {
        'hours': 'hours',
        'lookup': 'lookup',
        'name': 'name',
        'url': 'url'
    }

    def __init__(self, hours=24, lookup=None, name=None, url=None, local_vars_configuration=None):  # noqa: E501
        """TemporaryFileSpec - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._hours = None
        self._lookup = None
        self._name = None
        self._url = None
        self.discriminator = None

        if hours is not None:
            self.hours = hours
        self.lookup = lookup
        self.name = name
        self.url = url

    @property
    def hours(self):
        """
        Number of hours file is to be kept alive

        :return: The hours of this TemporaryFileSpec. 
        :rtype: int
        """
        return self._hours

    @hours.setter
    def hours(self, hours):
        """
        Number of hours file is to be kept alive

        :param hours: The hours of this TemporaryFileSpec.
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                hours is not None and hours > 24):  # noqa: E501
            raise ValueError("Invalid value for `hours`, must be a value less than or equal to `24`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                hours is not None and hours < 1):  # noqa: E501
            raise ValueError("Invalid value for `hours`, must be a value greater than or equal to `1`")  # noqa: E501

        self._hours = hours

    @property
    def lookup(self):
        """
        md5hash of lookup parameters

        :return: The lookup of this TemporaryFileSpec. 
        :rtype: str
        """
        return self._lookup

    @lookup.setter
    def lookup(self, lookup):
        """
        md5hash of lookup parameters

        :param lookup: The lookup of this TemporaryFileSpec.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and lookup is None:  # noqa: E501
            raise ValueError("Invalid value for `lookup`, must not be `None`")  # noqa: E501

        self._lookup = lookup

    @property
    def name(self):
        """
        Unique name for the temporary file

        :return: The name of this TemporaryFileSpec. 
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Unique name for the temporary file

        :param name: The name of this TemporaryFileSpec.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def url(self):
        """
        URL for the temporary file

        :return: The url of this TemporaryFileSpec. 
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        URL for the temporary file

        :param url: The url of this TemporaryFileSpec.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and url is None:  # noqa: E501
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

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
        if not isinstance(other, TemporaryFileSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TemporaryFileSpec):
            return True

        return self.to_dict() != other.to_dict()
