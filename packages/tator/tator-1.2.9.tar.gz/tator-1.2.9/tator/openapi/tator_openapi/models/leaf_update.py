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


class LeafUpdate(object):
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
        'attributes': 'dict(str, object)',
        'name': 'str',
        'null_attributes': 'list[str]',
        'reset_attributes': 'list[str]'
    }

    attribute_map = {
        'attributes': 'attributes',
        'name': 'name',
        'null_attributes': 'null_attributes',
        'reset_attributes': 'reset_attributes'
    }

    def __init__(self, attributes=None, name=None, null_attributes=None, reset_attributes=None, local_vars_configuration=None):  # noqa: E501
        """LeafUpdate - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._attributes = None
        self._name = None
        self._null_attributes = None
        self._reset_attributes = None
        self.discriminator = None

        if attributes is not None:
            self.attributes = attributes
        if name is not None:
            self.name = name
        if null_attributes is not None:
            self.null_attributes = null_attributes
        if reset_attributes is not None:
            self.reset_attributes = reset_attributes

    @property
    def attributes(self):
        """
        Attribute values to update.

        :return: The attributes of this LeafUpdate. 
        :rtype: dict(str, object)
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        Attribute values to update.

        :param attributes: The attributes of this LeafUpdate.
        :type: dict(str, object)
        """

        self._attributes = attributes

    @property
    def name(self):
        """
        Name of the leaf.

        :return: The name of this LeafUpdate. 
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Name of the leaf.

        :param name: The name of this LeafUpdate.
        :type: str
        """

        self._name = name

    @property
    def null_attributes(self):
        """
        Null a value in the attributes body

        :return: The null_attributes of this LeafUpdate. 
        :rtype: list[str]
        """
        return self._null_attributes

    @null_attributes.setter
    def null_attributes(self, null_attributes):
        """
        Null a value in the attributes body

        :param null_attributes: The null_attributes of this LeafUpdate.
        :type: list[str]
        """

        self._null_attributes = null_attributes

    @property
    def reset_attributes(self):
        """
        Reset an attribute to the default value specified in the Type object

        :return: The reset_attributes of this LeafUpdate. 
        :rtype: list[str]
        """
        return self._reset_attributes

    @reset_attributes.setter
    def reset_attributes(self, reset_attributes):
        """
        Reset an attribute to the default value specified in the Type object

        :param reset_attributes: The reset_attributes of this LeafUpdate.
        :type: list[str]
        """

        self._reset_attributes = reset_attributes

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
        if not isinstance(other, LeafUpdate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LeafUpdate):
            return True

        return self.to_dict() != other.to_dict()
