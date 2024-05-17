"""
Type annotations for resiliencehub service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_resiliencehub.client import ResilienceHubClient
    from types_aiobotocore_resiliencehub.paginator import (
        ListAppAssessmentResourceDriftsPaginator,
    )

    session = get_session()
    with session.create_client("resiliencehub") as client:
        client: ResilienceHubClient

        list_app_assessment_resource_drifts_paginator: ListAppAssessmentResourceDriftsPaginator = client.get_paginator("list_app_assessment_resource_drifts")
    ```
"""

from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListAppAssessmentResourceDriftsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListAppAssessmentResourceDriftsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAppAssessmentResourceDriftsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Paginator.ListAppAssessmentResourceDrifts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/#listappassessmentresourcedriftspaginator)
    """

    def paginate(
        self, *, assessmentArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListAppAssessmentResourceDriftsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Paginator.ListAppAssessmentResourceDrifts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/#listappassessmentresourcedriftspaginator)
        """
