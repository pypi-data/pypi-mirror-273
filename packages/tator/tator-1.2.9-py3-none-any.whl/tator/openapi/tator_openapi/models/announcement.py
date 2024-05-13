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


class Announcement(object):
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
        'created_datetime': 'str',
        'eol_datetime': 'str',
        'id': 'int',
        'markdown': 'str'
    }

    attribute_map = {
        'created_datetime': 'created_datetime',
        'eol_datetime': 'eol_datetime',
        'id': 'id',
        'markdown': 'markdown'
    }

    def __init__(self, created_datetime=None, eol_datetime=None, id=None, markdown=None, local_vars_configuration=None):  # noqa: E501
        """Announcement - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._created_datetime = None
        self._eol_datetime = None
        self._id = None
        self._markdown = None
        self.discriminator = None

        if created_datetime is not None:
            self.created_datetime = created_datetime
        if eol_datetime is not None:
            self.eol_datetime = eol_datetime
        if id is not None:
            self.id = id
        if markdown is not None:
            self.markdown = markdown

    @property
    def created_datetime(self):
        """
        When the announcement was made.

        :return: The created_datetime of this Announcement. 
        :rtype: str
        """
        return self._created_datetime

    @created_datetime.setter
    def created_datetime(self, created_datetime):
        """
        When the announcement was made.

        :param created_datetime: The created_datetime of this Announcement.
        :type: str
        """

        self._created_datetime = created_datetime

    @property
    def eol_datetime(self):
        """
        When the announcement will expire.

        :return: The eol_datetime of this Announcement. 
        :rtype: str
        """
        return self._eol_datetime

    @eol_datetime.setter
    def eol_datetime(self, eol_datetime):
        """
        When the announcement will expire.

        :param eol_datetime: The eol_datetime of this Announcement.
        :type: str
        """

        self._eol_datetime = eol_datetime

    @property
    def id(self):
        """
        Unique integer identifying an announcement.

        :return: The id of this Announcement. 
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Unique integer identifying an announcement.

        :param id: The id of this Announcement.
        :type: int
        """

        self._id = id

    @property
    def markdown(self):
        """
        Markdown formatted contents of the announcement.

        :return: The markdown of this Announcement. 
        :rtype: str
        """
        return self._markdown

    @markdown.setter
    def markdown(self, markdown):
        """
        Markdown formatted contents of the announcement.

        :param markdown: The markdown of this Announcement.
        :type: str
        """

        self._markdown = markdown

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
        if not isinstance(other, Announcement):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Announcement):
            return True

        return self.to_dict() != other.to_dict()
