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


class BucketS3Config(object):
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
        'aws_access_key_id': 'str',
        'aws_secret_access_key': 'str',
        'endpoint_url': 'str',
        'region_name': 'str'
    }

    attribute_map = {
        'aws_access_key_id': 'aws_access_key_id',
        'aws_secret_access_key': 'aws_secret_access_key',
        'endpoint_url': 'endpoint_url',
        'region_name': 'region_name'
    }

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, endpoint_url=None, region_name=None, local_vars_configuration=None):  # noqa: E501
        """BucketS3Config - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._aws_access_key_id = None
        self._aws_secret_access_key = None
        self._endpoint_url = None
        self._region_name = None
        self.discriminator = None

        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.region_name = region_name

    @property
    def aws_access_key_id(self):
        """
        Account access key.

        :return: The aws_access_key_id of this BucketS3Config. 
        :rtype: str
        """
        return self._aws_access_key_id

    @aws_access_key_id.setter
    def aws_access_key_id(self, aws_access_key_id):
        """
        Account access key.

        :param aws_access_key_id: The aws_access_key_id of this BucketS3Config.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and aws_access_key_id is None:  # noqa: E501
            raise ValueError("Invalid value for `aws_access_key_id`, must not be `None`")  # noqa: E501

        self._aws_access_key_id = aws_access_key_id

    @property
    def aws_secret_access_key(self):
        """
        Account secret key.

        :return: The aws_secret_access_key of this BucketS3Config. 
        :rtype: str
        """
        return self._aws_secret_access_key

    @aws_secret_access_key.setter
    def aws_secret_access_key(self, aws_secret_access_key):
        """
        Account secret key.

        :param aws_secret_access_key: The aws_secret_access_key of this BucketS3Config.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and aws_secret_access_key is None:  # noqa: E501
            raise ValueError("Invalid value for `aws_secret_access_key`, must not be `None`")  # noqa: E501

        self._aws_secret_access_key = aws_secret_access_key

    @property
    def endpoint_url(self):
        """
        Endpoint URL for bucket.

        :return: The endpoint_url of this BucketS3Config. 
        :rtype: str
        """
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, endpoint_url):
        """
        Endpoint URL for bucket.

        :param endpoint_url: The endpoint_url of this BucketS3Config.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and endpoint_url is None:  # noqa: E501
            raise ValueError("Invalid value for `endpoint_url`, must not be `None`")  # noqa: E501

        self._endpoint_url = endpoint_url

    @property
    def region_name(self):
        """
        Bucket region.

        :return: The region_name of this BucketS3Config. 
        :rtype: str
        """
        return self._region_name

    @region_name.setter
    def region_name(self, region_name):
        """
        Bucket region.

        :param region_name: The region_name of this BucketS3Config.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and region_name is None:  # noqa: E501
            raise ValueError("Invalid value for `region_name`, must not be `None`")  # noqa: E501

        self._region_name = region_name

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
        if not isinstance(other, BucketS3Config):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BucketS3Config):
            return True

        return self.to_dict() != other.to_dict()
