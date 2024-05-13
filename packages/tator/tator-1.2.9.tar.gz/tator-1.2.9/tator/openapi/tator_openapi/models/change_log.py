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


class ChangeLog(object):
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
        'description_of_change': 'ChangeLogDescriptionOfChange',
        'id': 'int',
        'modified_datetime': 'datetime',
        'project': 'int',
        'user': 'int'
    }

    attribute_map = {
        'description_of_change': 'description_of_change',
        'id': 'id',
        'modified_datetime': 'modified_datetime',
        'project': 'project',
        'user': 'user'
    }

    def __init__(self, description_of_change=None, id=None, modified_datetime=None, project=None, user=None, local_vars_configuration=None):  # noqa: E501
        """ChangeLog - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._description_of_change = None
        self._id = None
        self._modified_datetime = None
        self._project = None
        self._user = None
        self.discriminator = None

        if description_of_change is not None:
            self.description_of_change = description_of_change
        if id is not None:
            self.id = id
        if modified_datetime is not None:
            self.modified_datetime = modified_datetime
        if project is not None:
            self.project = project
        if user is not None:
            self.user = user

    @property
    def description_of_change(self):
        """

        :return: The description_of_change of this ChangeLog. 
        :rtype: ChangeLogDescriptionOfChange
        """
        return self._description_of_change

    @description_of_change.setter
    def description_of_change(self, description_of_change):
        """

        :param description_of_change: The description_of_change of this ChangeLog.
        :type: ChangeLogDescriptionOfChange
        """

        self._description_of_change = description_of_change

    @property
    def id(self):
        """
        Unique integer identifying this change log.

        :return: The id of this ChangeLog. 
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Unique integer identifying this change log.

        :param id: The id of this ChangeLog.
        :type: int
        """

        self._id = id

    @property
    def modified_datetime(self):
        """
        Datetime this change occurred.

        :return: The modified_datetime of this ChangeLog. 
        :rtype: datetime
        """
        return self._modified_datetime

    @modified_datetime.setter
    def modified_datetime(self, modified_datetime):
        """
        Datetime this change occurred.

        :param modified_datetime: The modified_datetime of this ChangeLog.
        :type: datetime
        """

        self._modified_datetime = modified_datetime

    @property
    def project(self):
        """
        Unique integer identifying project of this change log.

        :return: The project of this ChangeLog. 
        :rtype: int
        """
        return self._project

    @project.setter
    def project(self, project):
        """
        Unique integer identifying project of this change log.

        :param project: The project of this ChangeLog.
        :type: int
        """

        self._project = project

    @property
    def user(self):
        """
        Unique integer identifying the user whose changes created this change log.

        :return: The user of this ChangeLog. 
        :rtype: int
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Unique integer identifying the user whose changes created this change log.

        :param user: The user of this ChangeLog.
        :type: int
        """

        self._user = user

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
        if not isinstance(other, ChangeLog):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChangeLog):
            return True

        return self.to_dict() != other.to_dict()
