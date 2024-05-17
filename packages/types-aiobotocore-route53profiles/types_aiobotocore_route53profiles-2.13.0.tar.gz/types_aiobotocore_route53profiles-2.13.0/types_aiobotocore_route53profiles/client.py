"""
Type annotations for route53profiles service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53profiles.client import Route53ProfilesClient

    session = get_session()
    async with session.create_client("route53profiles") as client:
        client: Route53ProfilesClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListProfileAssociationsPaginator,
    ListProfileResourceAssociationsPaginator,
    ListProfilesPaginator,
)
from .type_defs import (
    AssociateProfileResponseTypeDef,
    AssociateResourceToProfileResponseTypeDef,
    CreateProfileResponseTypeDef,
    DeleteProfileResponseTypeDef,
    DisassociateProfileResponseTypeDef,
    DisassociateResourceFromProfileResponseTypeDef,
    GetProfileAssociationResponseTypeDef,
    GetProfileResourceAssociationResponseTypeDef,
    GetProfileResponseTypeDef,
    ListProfileAssociationsResponseTypeDef,
    ListProfileResourceAssociationsResponseTypeDef,
    ListProfilesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagTypeDef,
    UpdateProfileResourceAssociationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("Route53ProfilesClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class Route53ProfilesClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53ProfilesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#exceptions)
        """

    async def associate_profile(
        self, *, Name: str, ProfileId: str, ResourceId: str, Tags: Sequence[TagTypeDef] = ...
    ) -> AssociateProfileResponseTypeDef:
        """
        Associates a Route 53 Profiles profile with a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.associate_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#associate_profile)
        """

    async def associate_resource_to_profile(
        self, *, Name: str, ProfileId: str, ResourceArn: str, ResourceProperties: str = ...
    ) -> AssociateResourceToProfileResponseTypeDef:
        """
        Associates a DNS reource configuration to a Route 53 Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.associate_resource_to_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#associate_resource_to_profile)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#close)
        """

    async def create_profile(
        self, *, ClientToken: str, Name: str, Tags: Sequence[TagTypeDef] = ...
    ) -> CreateProfileResponseTypeDef:
        """
        Creates an empty Route 53 Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.create_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#create_profile)
        """

    async def delete_profile(self, *, ProfileId: str) -> DeleteProfileResponseTypeDef:
        """
        Deletes the specified Route 53 Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.delete_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#delete_profile)
        """

    async def disassociate_profile(
        self, *, ProfileId: str, ResourceId: str
    ) -> DisassociateProfileResponseTypeDef:
        """
        Dissociates a specified Route 53 Profile from the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.disassociate_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#disassociate_profile)
        """

    async def disassociate_resource_from_profile(
        self, *, ProfileId: str, ResourceArn: str
    ) -> DisassociateResourceFromProfileResponseTypeDef:
        """
        Dissoaciated a specified resource, from the Route 53 Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.disassociate_resource_from_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#disassociate_resource_from_profile)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#generate_presigned_url)
        """

    async def get_profile(self, *, ProfileId: str) -> GetProfileResponseTypeDef:
        """
        Returns information about a specified Route 53 Profile, such as whether whether
        the Profile is shared, and the current status of the
        Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.get_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#get_profile)
        """

    async def get_profile_association(
        self, *, ProfileAssociationId: str
    ) -> GetProfileAssociationResponseTypeDef:
        """
        Retrieves a Route 53 Profile association for a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.get_profile_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#get_profile_association)
        """

    async def get_profile_resource_association(
        self, *, ProfileResourceAssociationId: str
    ) -> GetProfileResourceAssociationResponseTypeDef:
        """
        Returns information about a specified Route 53 Profile resource association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.get_profile_resource_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#get_profile_resource_association)
        """

    async def list_profile_associations(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        ProfileId: str = ...,
        ResourceId: str = ...,
    ) -> ListProfileAssociationsResponseTypeDef:
        """
        Lists all the VPCs that the specified Route 53 Profile is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.list_profile_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#list_profile_associations)
        """

    async def list_profile_resource_associations(
        self,
        *,
        ProfileId: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        ResourceType: str = ...,
    ) -> ListProfileResourceAssociationsResponseTypeDef:
        """
        Lists all the resource associations for the specified Route 53 Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.list_profile_resource_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#list_profile_resource_associations)
        """

    async def list_profiles(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListProfilesResponseTypeDef:
        """
        Lists all the Route 53 Profiles associated with your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.list_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#list_profiles)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that you associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#list_tags_for_resource)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds one or more tags to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#untag_resource)
        """

    async def update_profile_resource_association(
        self, *, ProfileResourceAssociationId: str, Name: str = ..., ResourceProperties: str = ...
    ) -> UpdateProfileResourceAssociationResponseTypeDef:
        """
        Updates the specified Route 53 Profile resourse association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.update_profile_resource_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#update_profile_resource_association)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_profile_associations"]
    ) -> ListProfileAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_profile_resource_associations"]
    ) -> ListProfileResourceAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_profiles"]) -> ListProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/#get_paginator)
        """

    async def __aenter__(self) -> "Route53ProfilesClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/client/)
        """
