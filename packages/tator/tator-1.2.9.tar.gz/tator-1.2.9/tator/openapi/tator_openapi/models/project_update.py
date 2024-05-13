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


class ProjectUpdate(object):
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
        'backup_bucket': 'int',
        'bucket': 'int',
        'elemental_id': 'str',
        'enable_downloads': 'bool',
        'name': 'str',
        'summary': 'str',
        'thumb': 'str',
        'upload_bucket': 'int'
    }

    attribute_map = {
        'backup_bucket': 'backup_bucket',
        'bucket': 'bucket',
        'elemental_id': 'elemental_id',
        'enable_downloads': 'enable_downloads',
        'name': 'name',
        'summary': 'summary',
        'thumb': 'thumb',
        'upload_bucket': 'upload_bucket'
    }

    def __init__(self, backup_bucket=None, bucket=None, elemental_id=None, enable_downloads=None, name=None, summary=None, thumb=None, upload_bucket=None, local_vars_configuration=None):  # noqa: E501
        """ProjectUpdate - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._backup_bucket = None
        self._bucket = None
        self._elemental_id = None
        self._enable_downloads = None
        self._name = None
        self._summary = None
        self._thumb = None
        self._upload_bucket = None
        self.discriminator = None

        if backup_bucket is not None:
            self.backup_bucket = backup_bucket
        if bucket is not None:
            self.bucket = bucket
        self.elemental_id = elemental_id
        if enable_downloads is not None:
            self.enable_downloads = enable_downloads
        if name is not None:
            self.name = name
        if summary is not None:
            self.summary = summary
        if thumb is not None:
            self.thumb = thumb
        if upload_bucket is not None:
            self.upload_bucket = upload_bucket

    @property
    def backup_bucket(self):
        """
        Unique integer identifying a bucket for backups.

        :return: The backup_bucket of this ProjectUpdate. 
        :rtype: int
        """
        return self._backup_bucket

    @backup_bucket.setter
    def backup_bucket(self, backup_bucket):
        """
        Unique integer identifying a bucket for backups.

        :param backup_bucket: The backup_bucket of this ProjectUpdate.
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                backup_bucket is not None and backup_bucket < 1):  # noqa: E501
            raise ValueError("Invalid value for `backup_bucket`, must be a value greater than or equal to `1`")  # noqa: E501

        self._backup_bucket = backup_bucket

    @property
    def bucket(self):
        """
        Unique integer identifying a bucket.

        :return: The bucket of this ProjectUpdate. 
        :rtype: int
        """
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """
        Unique integer identifying a bucket.

        :param bucket: The bucket of this ProjectUpdate.
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                bucket is not None and bucket < 1):  # noqa: E501
            raise ValueError("Invalid value for `bucket`, must be a value greater than or equal to `1`")  # noqa: E501

        self._bucket = bucket

    @property
    def elemental_id(self):
        """
        The elemental ID of the object.

        :return: The elemental_id of this ProjectUpdate. 
        :rtype: str
        """
        return self._elemental_id

    @elemental_id.setter
    def elemental_id(self, elemental_id):
        """
        The elemental ID of the object.

        :param elemental_id: The elemental_id of this ProjectUpdate.
        :type: str
        """

        self._elemental_id = elemental_id

    @property
    def enable_downloads(self):
        """
        Whether the UI should allow downloads for this project.

        :return: The enable_downloads of this ProjectUpdate. 
        :rtype: bool
        """
        return self._enable_downloads

    @enable_downloads.setter
    def enable_downloads(self, enable_downloads):
        """
        Whether the UI should allow downloads for this project.

        :param enable_downloads: The enable_downloads of this ProjectUpdate.
        :type: bool
        """

        self._enable_downloads = enable_downloads

    @property
    def name(self):
        """
        Name of the project.

        :return: The name of this ProjectUpdate. 
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Name of the project.

        :param name: The name of this ProjectUpdate.
        :type: str
        """

        self._name = name

    @property
    def summary(self):
        """
        Summary of the project.

        :return: The summary of this ProjectUpdate. 
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """
        Summary of the project.

        :param summary: The summary of this ProjectUpdate.
        :type: str
        """

        self._summary = summary

    @property
    def thumb(self):
        """
        S3 key of thumbnail used to represent the project.

        :return: The thumb of this ProjectUpdate. 
        :rtype: str
        """
        return self._thumb

    @thumb.setter
    def thumb(self, thumb):
        """
        S3 key of thumbnail used to represent the project.

        :param thumb: The thumb of this ProjectUpdate.
        :type: str
        """

        self._thumb = thumb

    @property
    def upload_bucket(self):
        """
        Unique integer identifying a bucket for uploads.

        :return: The upload_bucket of this ProjectUpdate. 
        :rtype: int
        """
        return self._upload_bucket

    @upload_bucket.setter
    def upload_bucket(self, upload_bucket):
        """
        Unique integer identifying a bucket for uploads.

        :param upload_bucket: The upload_bucket of this ProjectUpdate.
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                upload_bucket is not None and upload_bucket < 1):  # noqa: E501
            raise ValueError("Invalid value for `upload_bucket`, must be a value greater than or equal to `1`")  # noqa: E501

        self._upload_bucket = upload_bucket

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
        if not isinstance(other, ProjectUpdate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ProjectUpdate):
            return True

        return self.to_dict() != other.to_dict()
