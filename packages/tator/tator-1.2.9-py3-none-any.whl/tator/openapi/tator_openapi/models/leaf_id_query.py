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


class LeafIdQuery(object):
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
        'float_array': 'list[FloatArrayQuery]',
        'ids': 'list[int]',
        'object_search': 'AttributeOperationSpec'
    }

    attribute_map = {
        'float_array': 'float_array',
        'ids': 'ids',
        'object_search': 'object_search'
    }

    def __init__(self, float_array=None, ids=None, object_search=None, local_vars_configuration=None):  # noqa: E501
        """LeafIdQuery - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._float_array = None
        self._ids = None
        self._object_search = None
        self.discriminator = None

        if float_array is not None:
            self.float_array = float_array
        if ids is not None:
            self.ids = ids
        if object_search is not None:
            self.object_search = object_search

    @property
    def float_array(self):
        """
        Searches on `float_array` attributes.

        :return: The float_array of this LeafIdQuery. 
        :rtype: list[FloatArrayQuery]
        """
        return self._float_array

    @float_array.setter
    def float_array(self, float_array):
        """
        Searches on `float_array` attributes.

        :param float_array: The float_array of this LeafIdQuery.
        :type: list[FloatArrayQuery]
        """

        self._float_array = float_array

    @property
    def ids(self):
        """
        Array of leaf IDs to retrieve.

        :return: The ids of this LeafIdQuery. 
        :rtype: list[int]
        """
        return self._ids

    @ids.setter
    def ids(self, ids):
        """
        Array of leaf IDs to retrieve.

        :param ids: The ids of this LeafIdQuery.
        :type: list[int]
        """

        self._ids = ids

    @property
    def object_search(self):
        """

        :return: The object_search of this LeafIdQuery. 
        :rtype: AttributeOperationSpec
        """
        return self._object_search

    @object_search.setter
    def object_search(self, object_search):
        """

        :param object_search: The object_search of this LeafIdQuery.
        :type: AttributeOperationSpec
        """

        self._object_search = object_search

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
        if not isinstance(other, LeafIdQuery):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LeafIdQuery):
            return True

        return self.to_dict() != other.to_dict()
