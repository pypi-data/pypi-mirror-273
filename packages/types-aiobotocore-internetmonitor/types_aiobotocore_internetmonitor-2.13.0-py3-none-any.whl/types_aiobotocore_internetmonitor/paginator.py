"""
Type annotations for internetmonitor service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_internetmonitor.client import CloudWatchInternetMonitorClient
    from types_aiobotocore_internetmonitor.paginator import (
        ListHealthEventsPaginator,
        ListInternetEventsPaginator,
        ListMonitorsPaginator,
    )

    session = get_session()
    with session.create_client("internetmonitor") as client:
        client: CloudWatchInternetMonitorClient

        list_health_events_paginator: ListHealthEventsPaginator = client.get_paginator("list_health_events")
        list_internet_events_paginator: ListInternetEventsPaginator = client.get_paginator("list_internet_events")
        list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    ```
"""

from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import HealthEventStatusType
from .type_defs import (
    ListHealthEventsOutputTypeDef,
    ListInternetEventsOutputTypeDef,
    ListMonitorsOutputTypeDef,
    PaginatorConfigTypeDef,
    TimestampTypeDef,
)

__all__ = ("ListHealthEventsPaginator", "ListInternetEventsPaginator", "ListMonitorsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListHealthEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor.html#CloudWatchInternetMonitor.Paginator.ListHealthEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/#listhealtheventspaginator)
    """

    def paginate(
        self,
        *,
        MonitorName: str,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        EventStatus: HealthEventStatusType = ...,
        LinkedAccountId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListHealthEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor.html#CloudWatchInternetMonitor.Paginator.ListHealthEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/#listhealtheventspaginator)
        """


class ListInternetEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor.html#CloudWatchInternetMonitor.Paginator.ListInternetEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/#listinterneteventspaginator)
    """

    def paginate(
        self,
        *,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        EventStatus: str = ...,
        EventType: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListInternetEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor.html#CloudWatchInternetMonitor.Paginator.ListInternetEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/#listinterneteventspaginator)
        """


class ListMonitorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor.html#CloudWatchInternetMonitor.Paginator.ListMonitors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/#listmonitorspaginator)
    """

    def paginate(
        self,
        *,
        MonitorStatus: str = ...,
        IncludeLinkedAccounts: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListMonitorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor.html#CloudWatchInternetMonitor.Paginator.ListMonitors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/#listmonitorspaginator)
        """
