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


class TranscodeSpec(object):
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
        'attributes': 'object',
        'email_spec': 'JobSpecFailureEmailSpec',
        'gid': 'str',
        'md5': 'str',
        'media_id': 'int',
        'name': 'str',
        'section': 'str',
        'size': 'int',
        'type': 'int',
        'uid': 'str',
        'url': 'str'
    }

    attribute_map = {
        'attributes': 'attributes',
        'email_spec': 'email_spec',
        'gid': 'gid',
        'md5': 'md5',
        'media_id': 'media_id',
        'name': 'name',
        'section': 'section',
        'size': 'size',
        'type': 'type',
        'uid': 'uid',
        'url': 'url'
    }

    def __init__(self, attributes=None, email_spec=None, gid=None, md5=None, media_id=None, name=None, section=None, size=None, type=None, uid=None, url=None, local_vars_configuration=None):  # noqa: E501
        """TranscodeSpec - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._attributes = None
        self._email_spec = None
        self._gid = None
        self._md5 = None
        self._media_id = None
        self._name = None
        self._section = None
        self._size = None
        self._type = None
        self._uid = None
        self._url = None
        self.discriminator = None

        self.attributes = attributes
        self.email_spec = email_spec
        self.gid = gid
        if md5 is not None:
            self.md5 = md5
        self.media_id = media_id
        self.name = name
        self.section = section
        if size is not None:
            self.size = size
        self.type = type
        self.uid = uid
        self.url = url

    @property
    def attributes(self):
        """
        Attributes to apply upon upload

        :return: The attributes of this TranscodeSpec. 
        :rtype: object
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        Attributes to apply upon upload

        :param attributes: The attributes of this TranscodeSpec.
        :type: object
        """

        self._attributes = attributes

    @property
    def email_spec(self):
        """

        :return: The email_spec of this TranscodeSpec. 
        :rtype: JobSpecFailureEmailSpec
        """
        return self._email_spec

    @email_spec.setter
    def email_spec(self, email_spec):
        """

        :param email_spec: The email_spec of this TranscodeSpec.
        :type: JobSpecFailureEmailSpec
        """

        self._email_spec = email_spec

    @property
    def gid(self):
        """
        UUID generated for the job group. This value may be associated with messages generated during upload via the `Progress` endpoint, or it may be newly generated. The transcode workflow will use this value to generate progress messages.

        :return: The gid of this TranscodeSpec. 
        :rtype: str
        """
        return self._gid

    @gid.setter
    def gid(self, gid):
        """
        UUID generated for the job group. This value may be associated with messages generated during upload via the `Progress` endpoint, or it may be newly generated. The transcode workflow will use this value to generate progress messages.

        :param gid: The gid of this TranscodeSpec.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and gid is None:  # noqa: E501
            raise ValueError("Invalid value for `gid`, must not be `None`")  # noqa: E501

        self._gid = gid

    @property
    def md5(self):
        """
        MD5 sum of the media file.

        :return: The md5 of this TranscodeSpec. 
        :rtype: str
        """
        return self._md5

    @md5.setter
    def md5(self, md5):
        """
        MD5 sum of the media file.

        :param md5: The md5 of this TranscodeSpec.
        :type: str
        """

        self._md5 = md5

    @property
    def media_id(self):
        """
        ID of an existing media. If given, this media will be used for the transcode operation rather than creating a new object.

        :return: The media_id of this TranscodeSpec. 
        :rtype: int
        """
        return self._media_id

    @media_id.setter
    def media_id(self, media_id):
        """
        ID of an existing media. If given, this media will be used for the transcode operation rather than creating a new object.

        :param media_id: The media_id of this TranscodeSpec.
        :type: int
        """

        self._media_id = media_id

    @property
    def name(self):
        """
        Name of the file.

        :return: The name of this TranscodeSpec. 
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Name of the file.

        :param name: The name of this TranscodeSpec.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def section(self):
        """
        Media section name to upload to.

        :return: The section of this TranscodeSpec. 
        :rtype: str
        """
        return self._section

    @section.setter
    def section(self, section):
        """
        Media section name to upload to.

        :param section: The section of this TranscodeSpec.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and section is None:  # noqa: E501
            raise ValueError("Invalid value for `section`, must not be `None`")  # noqa: E501

        self._section = section

    @property
    def size(self):
        """
        Size of the file in bytes. This parameter is required if the supplied URL is external (not produced by `DownloadInfo` and cannot accept HEAD requests.

        :return: The size of this TranscodeSpec. 
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Size of the file in bytes. This parameter is required if the supplied URL is external (not produced by `DownloadInfo` and cannot accept HEAD requests.

        :param size: The size of this TranscodeSpec.
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                size is not None and size < 0):  # noqa: E501
            raise ValueError("Invalid value for `size`, must be a value greater than or equal to `0`")  # noqa: E501

        self._size = size

    @property
    def type(self):
        """
        Unique integer identifying a video type.

        :return: The type of this TranscodeSpec. 
        :rtype: int
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Unique integer identifying a video type.

        :param type: The type of this TranscodeSpec.
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def uid(self):
        """
        UUID generated for the individual job. This value may be associated with messages generated during upload via the `Progress` endpoint, or it may be newly generated. The transcode workflow will use this value to generate progress messages.

        :return: The uid of this TranscodeSpec. 
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """
        UUID generated for the individual job. This value may be associated with messages generated during upload via the `Progress` endpoint, or it may be newly generated. The transcode workflow will use this value to generate progress messages.

        :param uid: The uid of this TranscodeSpec.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and uid is None:  # noqa: E501
            raise ValueError("Invalid value for `uid`, must not be `None`")  # noqa: E501

        self._uid = uid

    @property
    def url(self):
        """
        Upload URL for the raw video.

        :return: The url of this TranscodeSpec. 
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Upload URL for the raw video.

        :param url: The url of this TranscodeSpec.
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
        if not isinstance(other, TranscodeSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TranscodeSpec):
            return True

        return self.to_dict() != other.to_dict()
