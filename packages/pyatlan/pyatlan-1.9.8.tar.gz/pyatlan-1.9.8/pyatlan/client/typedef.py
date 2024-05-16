# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Union

from pydantic import validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    CREATE_TYPE_DEFS,
    DELETE_TYPE_DEF_BY_NAME,
    GET_ALL_TYPE_DEFS,
    UPDATE_TYPE_DEFS,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import (
    AtlanTagDef,
    CustomMetadataDef,
    EnumDef,
    TypeDef,
    TypeDefResponse,
)


def _build_typedef_request(typedef: TypeDef) -> TypeDefResponse:
    if isinstance(typedef, AtlanTagDef):
        # Set up the request payload...
        payload = TypeDefResponse(
            atlan_tag_defs=[typedef],
            enum_defs=[],
            struct_defs=[],
            entity_defs=[],
            relationship_defs=[],
            custom_metadata_defs=[],
        )
    elif isinstance(typedef, CustomMetadataDef):
        # Set up the request payload...
        payload = TypeDefResponse(
            atlan_tag_defs=[],
            enum_defs=[],
            struct_defs=[],
            entity_defs=[],
            relationship_defs=[],
            custom_metadata_defs=[typedef],
        )
    elif isinstance(typedef, EnumDef):
        # Set up the request payload...
        payload = TypeDefResponse(
            atlan_tag_defs=[],
            enum_defs=[typedef],
            struct_defs=[],
            entity_defs=[],
            relationship_defs=[],
            custom_metadata_defs=[],
        )
    else:
        raise ErrorCode.UNABLE_TO_UPDATE_TYPEDEF_CATEGORY.exception_with_parameters(
            typedef.category.value
        )
    return payload


def _refresh_caches(typedef: TypeDef) -> None:
    if isinstance(typedef, AtlanTagDef):
        from pyatlan.cache.atlan_tag_cache import AtlanTagCache

        AtlanTagCache.refresh_cache()
    if isinstance(typedef, CustomMetadataDef):
        from pyatlan.cache.custom_metadata_cache import CustomMetadataCache

        CustomMetadataCache.refresh_cache()
    if isinstance(typedef, EnumDef):
        from pyatlan.cache.enum_cache import EnumCache

        EnumCache.refresh_cache()


class TypeDefClient:
    """
    This class can be used to retrieve information pertaining to TypeDefs. This class does not need to be instantiated
    directly but can be obtained through the typedef property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    def get_all(self) -> TypeDefResponse:
        """
        Retrieves a TypeDefResponse object that contains a list of all the type definitions in Atlan.

        :returns: TypeDefResponse object that contains  a list of all the type definitions in Atlan
        :raises AtlanError: on any API communication issue
        """
        raw_json = self._client._call_api(GET_ALL_TYPE_DEFS)
        return TypeDefResponse(**raw_json)

    @validate_arguments
    def get(
        self, type_category: Union[AtlanTypeCategory, list[AtlanTypeCategory]]
    ) -> TypeDefResponse:
        """
        Retrieves  a TypeDefResponse object that contain a list of the specified category type definitions in Atlan.

        :param type_category: category of type definitions to retrieve
        :returns: TypeDefResponse object that contain a list that contains the requested list of type definitions
        :raises AtlanError: on any API communication issue
        """
        categories: list[str] = []
        if isinstance(type_category, list):
            categories.extend(map(lambda x: x.value, type_category))
        else:
            categories.append(type_category.value)
        query_params = {"type": categories}
        raw_json = self._client._call_api(
            GET_ALL_TYPE_DEFS.format_path_with_params(),
            query_params,
        )
        return TypeDefResponse(**raw_json)

    @validate_arguments
    def create(self, typedef: TypeDef) -> TypeDefResponse:
        """
        Create a new type definition in Atlan.
        Note: only custom metadata, enumerations, and Atlan tag type definitions are currently
        supported. Furthermore, if any of these are created their respective cache will be
        force-refreshed.

        :param typedef: type definition to create
        :returns: the resulting type definition that was created
        :raises InvalidRequestError: if the typedef you are trying to create is not one of the allowed types
        :raises AtlanError: on any API communication issue
        """
        payload = _build_typedef_request(typedef)
        raw_json = self._client._call_api(
            CREATE_TYPE_DEFS, request_obj=payload, exclude_unset=True
        )
        _refresh_caches(typedef)
        return TypeDefResponse(**raw_json)

    @validate_arguments
    def update(self, typedef: TypeDef) -> TypeDefResponse:
        """
        Update an existing type definition in Atlan.
        Note: only custom metadata and Atlan tag type definitions are currently supported.
        Furthermore, if any of these are updated their respective cache will be force-refreshed.

        :param typedef: type definition to update
        :returns: the resulting type definition that was updated
        :raises InvalidRequestError: if the typedef you are trying to create is not one of the allowed types
        :raises AtlanError: on any API communication issue
        """
        payload = _build_typedef_request(typedef)
        raw_json = self._client._call_api(
            UPDATE_TYPE_DEFS, request_obj=payload, exclude_unset=True
        )
        _refresh_caches(typedef)
        return TypeDefResponse(**raw_json)

    @validate_arguments
    def purge(self, name: str, typedef_type: type) -> None:
        """
        Delete the type definition.
        Furthermore, if an Atlan tag, enumeration or custom metadata is deleted their
        respective cache will be force-refreshed.

        :param name: internal hashed-string name of the type definition
        :param typedef_type: type of the type definition that is being deleted
        :raises InvalidRequestError: if the typedef you are trying to delete is not one of the allowed types
        :raises NotFoundError: if the typedef you are trying to delete cannot be found
        :raises AtlanError: on any API communication issue
        """
        if typedef_type == CustomMetadataDef:
            from pyatlan.cache.custom_metadata_cache import CustomMetadataCache

            internal_name = CustomMetadataCache.get_id_for_name(name)
        elif typedef_type == EnumDef:
            internal_name = name
        elif typedef_type == AtlanTagDef:
            from pyatlan.cache.atlan_tag_cache import AtlanTagCache

            internal_name = str(AtlanTagCache.get_id_for_name(name))
        else:
            raise ErrorCode.UNABLE_TO_PURGE_TYPEDEF_OF_TYPE.exception_with_parameters(
                typedef_type
            )
        if internal_name:
            self._client._call_api(
                DELETE_TYPE_DEF_BY_NAME.format_path_with_params(internal_name)
            )
        else:
            raise ErrorCode.TYPEDEF_NOT_FOUND_BY_NAME.exception_with_parameters(name)

        if typedef_type == CustomMetadataDef:
            from pyatlan.cache.custom_metadata_cache import CustomMetadataCache

            CustomMetadataCache.refresh_cache()
        elif typedef_type == EnumDef:
            from pyatlan.cache.enum_cache import EnumCache

            EnumCache.refresh_cache()
        elif typedef_type == AtlanTagDef:
            from pyatlan.cache.atlan_tag_cache import AtlanTagCache

            AtlanTagCache.refresh_cache()
