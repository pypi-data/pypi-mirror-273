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


class MediaType(object):
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
        'archive_config': 'list[ArchiveConfig]',
        'attribute_types': 'list[AttributeType]',
        'default_box': 'int',
        'default_dot': 'int',
        'default_line': 'int',
        'default_volume': 'int',
        'description': 'str',
        'dtype': 'str',
        'elemental_id': 'str',
        'file_format': 'str',
        'id': 'int',
        'name': 'str',
        'overlay_config': 'dict(str, object)',
        'project': 'int',
        'streaming_config': 'list[ResolutionConfig]',
        'visible': 'bool'
    }

    attribute_map = {
        'archive_config': 'archive_config',
        'attribute_types': 'attribute_types',
        'default_box': 'default_box',
        'default_dot': 'default_dot',
        'default_line': 'default_line',
        'default_volume': 'default_volume',
        'description': 'description',
        'dtype': 'dtype',
        'elemental_id': 'elemental_id',
        'file_format': 'file_format',
        'id': 'id',
        'name': 'name',
        'overlay_config': 'overlay_config',
        'project': 'project',
        'streaming_config': 'streaming_config',
        'visible': 'visible'
    }

    def __init__(self, archive_config=None, attribute_types=None, default_box=None, default_dot=None, default_line=None, default_volume=None, description='', dtype=None, elemental_id=None, file_format=None, id=None, name=None, overlay_config=None, project=None, streaming_config=None, visible=None, local_vars_configuration=None):  # noqa: E501
        """MediaType - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._archive_config = None
        self._attribute_types = None
        self._default_box = None
        self._default_dot = None
        self._default_line = None
        self._default_volume = None
        self._description = None
        self._dtype = None
        self._elemental_id = None
        self._file_format = None
        self._id = None
        self._name = None
        self._overlay_config = None
        self._project = None
        self._streaming_config = None
        self._visible = None
        self.discriminator = None

        if archive_config is not None:
            self.archive_config = archive_config
        if attribute_types is not None:
            self.attribute_types = attribute_types
        if default_box is not None:
            self.default_box = default_box
        if default_dot is not None:
            self.default_dot = default_dot
        if default_line is not None:
            self.default_line = default_line
        if default_volume is not None:
            self.default_volume = default_volume
        if description is not None:
            self.description = description
        if dtype is not None:
            self.dtype = dtype
        self.elemental_id = elemental_id
        if file_format is not None:
            self.file_format = file_format
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if overlay_config is not None:
            self.overlay_config = overlay_config
        if project is not None:
            self.project = project
        if streaming_config is not None:
            self.streaming_config = streaming_config
        if visible is not None:
            self.visible = visible

    @property
    def archive_config(self):
        """
        Archive config definitions. If null, the raw file will be uploaded to Tator.

        :return: The archive_config of this MediaType. 
        :rtype: list[ArchiveConfig]
        """
        return self._archive_config

    @archive_config.setter
    def archive_config(self, archive_config):
        """
        Archive config definitions. If null, the raw file will be uploaded to Tator.

        :param archive_config: The archive_config of this MediaType.
        :type: list[ArchiveConfig]
        """

        self._archive_config = archive_config

    @property
    def attribute_types(self):
        """
        Attribute type definitions.

        :return: The attribute_types of this MediaType. 
        :rtype: list[AttributeType]
        """
        return self._attribute_types

    @attribute_types.setter
    def attribute_types(self, attribute_types):
        """
        Attribute type definitions.

        :param attribute_types: The attribute_types of this MediaType.
        :type: list[AttributeType]
        """

        self._attribute_types = attribute_types

    @property
    def default_box(self):
        """
        Unique integer identifying default box type for drawing.

        :return: The default_box of this MediaType. 
        :rtype: int
        """
        return self._default_box

    @default_box.setter
    def default_box(self, default_box):
        """
        Unique integer identifying default box type for drawing.

        :param default_box: The default_box of this MediaType.
        :type: int
        """

        self._default_box = default_box

    @property
    def default_dot(self):
        """
        Unique integer identifying default dot type for drawing.

        :return: The default_dot of this MediaType. 
        :rtype: int
        """
        return self._default_dot

    @default_dot.setter
    def default_dot(self, default_dot):
        """
        Unique integer identifying default dot type for drawing.

        :param default_dot: The default_dot of this MediaType.
        :type: int
        """

        self._default_dot = default_dot

    @property
    def default_line(self):
        """
        Unique integer identifying default line type for drawing.

        :return: The default_line of this MediaType. 
        :rtype: int
        """
        return self._default_line

    @default_line.setter
    def default_line(self, default_line):
        """
        Unique integer identifying default line type for drawing.

        :param default_line: The default_line of this MediaType.
        :type: int
        """

        self._default_line = default_line

    @property
    def default_volume(self):
        """
        Default audio volume for this media type.

        :return: The default_volume of this MediaType. 
        :rtype: int
        """
        return self._default_volume

    @default_volume.setter
    def default_volume(self, default_volume):
        """
        Default audio volume for this media type.

        :param default_volume: The default_volume of this MediaType.
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                default_volume is not None and default_volume > 100):  # noqa: E501
            raise ValueError("Invalid value for `default_volume`, must be a value less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                default_volume is not None and default_volume < 0):  # noqa: E501
            raise ValueError("Invalid value for `default_volume`, must be a value greater than or equal to `0`")  # noqa: E501

        self._default_volume = default_volume

    @property
    def description(self):
        """
        Description of the media type.

        :return: The description of this MediaType. 
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Description of the media type.

        :param description: The description of this MediaType.
        :type: str
        """

        self._description = description

    @property
    def dtype(self):
        """
        Type of the media, image or video.

        :return: The dtype of this MediaType. 
        :rtype: str
        """
        return self._dtype

    @dtype.setter
    def dtype(self, dtype):
        """
        Type of the media, image or video.

        :param dtype: The dtype of this MediaType.
        :type: str
        """
        allowed_values = ["image", "video", "multi", "live"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and dtype not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `dtype` ({0}), must be one of {1}"  # noqa: E501
                .format(dtype, allowed_values)
            )

        self._dtype = dtype

    @property
    def elemental_id(self):
        """
        The elemental ID of the object.

        :return: The elemental_id of this MediaType. 
        :rtype: str
        """
        return self._elemental_id

    @elemental_id.setter
    def elemental_id(self, elemental_id):
        """
        The elemental ID of the object.

        :param elemental_id: The elemental_id of this MediaType.
        :type: str
        """

        self._elemental_id = elemental_id

    @property
    def file_format(self):
        """
        File extension. If omitted, any recognized file extension for the given dtype is accepted for upload. Do not include a dot prefix.

        :return: The file_format of this MediaType. 
        :rtype: str
        """
        return self._file_format

    @file_format.setter
    def file_format(self, file_format):
        """
        File extension. If omitted, any recognized file extension for the given dtype is accepted for upload. Do not include a dot prefix.

        :param file_format: The file_format of this MediaType.
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                file_format is not None and len(file_format) > 4):
            raise ValueError("Invalid value for `file_format`, length must be less than or equal to `4`")  # noqa: E501

        self._file_format = file_format

    @property
    def id(self):
        """
        Unique integer identifying a media type.

        :return: The id of this MediaType. 
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Unique integer identifying a media type.

        :param id: The id of this MediaType.
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """
        Name of the media type.

        :return: The name of this MediaType. 
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Name of the media type.

        :param name: The name of this MediaType.
        :type: str
        """

        self._name = name

    @property
    def overlay_config(self):
        """
        Overlay configuration

        :return: The overlay_config of this MediaType. 
        :rtype: dict(str, object)
        """
        return self._overlay_config

    @overlay_config.setter
    def overlay_config(self, overlay_config):
        """
        Overlay configuration

        :param overlay_config: The overlay_config of this MediaType.
        :type: dict(str, object)
        """

        self._overlay_config = overlay_config

    @property
    def project(self):
        """
        Unique integer identifying project for this media type.

        :return: The project of this MediaType. 
        :rtype: int
        """
        return self._project

    @project.setter
    def project(self, project):
        """
        Unique integer identifying project for this media type.

        :param project: The project of this MediaType.
        :type: int
        """

        self._project = project

    @property
    def streaming_config(self):
        """
        Streaming config definition. If null, the default will be used.

        :return: The streaming_config of this MediaType. 
        :rtype: list[ResolutionConfig]
        """
        return self._streaming_config

    @streaming_config.setter
    def streaming_config(self, streaming_config):
        """
        Streaming config definition. If null, the default will be used.

        :param streaming_config: The streaming_config of this MediaType.
        :type: list[ResolutionConfig]
        """

        self._streaming_config = streaming_config

    @property
    def visible(self):
        """
        Visible configuration

        :return: The visible of this MediaType. 
        :rtype: bool
        """
        return self._visible

    @visible.setter
    def visible(self, visible):
        """
        Visible configuration

        :param visible: The visible of this MediaType.
        :type: bool
        """

        self._visible = visible

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
        if not isinstance(other, MediaType):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MediaType):
            return True

        return self.to_dict() != other.to_dict()
