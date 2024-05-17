"""
Type annotations for controlcatalog service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_controlcatalog.client import ControlCatalogClient
    from types_aiobotocore_controlcatalog.paginator import (
        ListCommonControlsPaginator,
        ListDomainsPaginator,
        ListObjectivesPaginator,
    )

    session = get_session()
    with session.create_client("controlcatalog") as client:
        client: ControlCatalogClient

        list_common_controls_paginator: ListCommonControlsPaginator = client.get_paginator("list_common_controls")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_objectives_paginator: ListObjectivesPaginator = client.get_paginator("list_objectives")
    ```
"""

from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    CommonControlFilterTypeDef,
    ListCommonControlsResponseTypeDef,
    ListDomainsResponseTypeDef,
    ListObjectivesResponseTypeDef,
    ObjectiveFilterTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListCommonControlsPaginator", "ListDomainsPaginator", "ListObjectivesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListCommonControlsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog.html#ControlCatalog.Paginator.ListCommonControls)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listcommoncontrolspaginator)
    """

    def paginate(
        self,
        *,
        CommonControlFilter: CommonControlFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListCommonControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog.html#ControlCatalog.Paginator.ListCommonControls.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listcommoncontrolspaginator)
        """


class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog.html#ControlCatalog.Paginator.ListDomains)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listdomainspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog.html#ControlCatalog.Paginator.ListDomains.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listdomainspaginator)
        """


class ListObjectivesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog.html#ControlCatalog.Paginator.ListObjectives)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listobjectivespaginator)
    """

    def paginate(
        self,
        *,
        ObjectiveFilter: ObjectiveFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListObjectivesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog.html#ControlCatalog.Paginator.ListObjectives.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controlcatalog/paginators/#listobjectivespaginator)
        """
