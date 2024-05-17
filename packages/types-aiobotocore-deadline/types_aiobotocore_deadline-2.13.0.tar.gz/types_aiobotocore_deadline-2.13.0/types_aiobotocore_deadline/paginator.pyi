"""
Type annotations for deadline service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_deadline.client import DeadlineCloudClient
    from types_aiobotocore_deadline.paginator import (
        GetSessionsStatisticsAggregationPaginator,
        ListAvailableMeteredProductsPaginator,
        ListBudgetsPaginator,
        ListFarmMembersPaginator,
        ListFarmsPaginator,
        ListFleetMembersPaginator,
        ListFleetsPaginator,
        ListJobMembersPaginator,
        ListJobsPaginator,
        ListLicenseEndpointsPaginator,
        ListMeteredProductsPaginator,
        ListMonitorsPaginator,
        ListQueueEnvironmentsPaginator,
        ListQueueFleetAssociationsPaginator,
        ListQueueMembersPaginator,
        ListQueuesPaginator,
        ListSessionActionsPaginator,
        ListSessionsPaginator,
        ListSessionsForWorkerPaginator,
        ListStepConsumersPaginator,
        ListStepDependenciesPaginator,
        ListStepsPaginator,
        ListStorageProfilesPaginator,
        ListStorageProfilesForQueuePaginator,
        ListTasksPaginator,
        ListWorkersPaginator,
    )

    session = get_session()
    with session.create_client("deadline") as client:
        client: DeadlineCloudClient

        get_sessions_statistics_aggregation_paginator: GetSessionsStatisticsAggregationPaginator = client.get_paginator("get_sessions_statistics_aggregation")
        list_available_metered_products_paginator: ListAvailableMeteredProductsPaginator = client.get_paginator("list_available_metered_products")
        list_budgets_paginator: ListBudgetsPaginator = client.get_paginator("list_budgets")
        list_farm_members_paginator: ListFarmMembersPaginator = client.get_paginator("list_farm_members")
        list_farms_paginator: ListFarmsPaginator = client.get_paginator("list_farms")
        list_fleet_members_paginator: ListFleetMembersPaginator = client.get_paginator("list_fleet_members")
        list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
        list_job_members_paginator: ListJobMembersPaginator = client.get_paginator("list_job_members")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_license_endpoints_paginator: ListLicenseEndpointsPaginator = client.get_paginator("list_license_endpoints")
        list_metered_products_paginator: ListMeteredProductsPaginator = client.get_paginator("list_metered_products")
        list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
        list_queue_environments_paginator: ListQueueEnvironmentsPaginator = client.get_paginator("list_queue_environments")
        list_queue_fleet_associations_paginator: ListQueueFleetAssociationsPaginator = client.get_paginator("list_queue_fleet_associations")
        list_queue_members_paginator: ListQueueMembersPaginator = client.get_paginator("list_queue_members")
        list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
        list_session_actions_paginator: ListSessionActionsPaginator = client.get_paginator("list_session_actions")
        list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
        list_sessions_for_worker_paginator: ListSessionsForWorkerPaginator = client.get_paginator("list_sessions_for_worker")
        list_step_consumers_paginator: ListStepConsumersPaginator = client.get_paginator("list_step_consumers")
        list_step_dependencies_paginator: ListStepDependenciesPaginator = client.get_paginator("list_step_dependencies")
        list_steps_paginator: ListStepsPaginator = client.get_paginator("list_steps")
        list_storage_profiles_paginator: ListStorageProfilesPaginator = client.get_paginator("list_storage_profiles")
        list_storage_profiles_for_queue_paginator: ListStorageProfilesForQueuePaginator = client.get_paginator("list_storage_profiles_for_queue")
        list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
        list_workers_paginator: ListWorkersPaginator = client.get_paginator("list_workers")
    ```
"""

from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import BudgetStatusType, FleetStatusType, QueueStatusType
from .type_defs import (
    GetSessionsStatisticsAggregationResponseTypeDef,
    ListAvailableMeteredProductsResponseTypeDef,
    ListBudgetsResponseTypeDef,
    ListFarmMembersResponseTypeDef,
    ListFarmsResponseTypeDef,
    ListFleetMembersResponseTypeDef,
    ListFleetsResponseTypeDef,
    ListJobMembersResponseTypeDef,
    ListJobsResponseTypeDef,
    ListLicenseEndpointsResponseTypeDef,
    ListMeteredProductsResponseTypeDef,
    ListMonitorsResponseTypeDef,
    ListQueueEnvironmentsResponseTypeDef,
    ListQueueFleetAssociationsResponseTypeDef,
    ListQueueMembersResponseTypeDef,
    ListQueuesResponseTypeDef,
    ListSessionActionsResponseTypeDef,
    ListSessionsForWorkerResponseTypeDef,
    ListSessionsResponseTypeDef,
    ListStepConsumersResponseTypeDef,
    ListStepDependenciesResponseTypeDef,
    ListStepsResponseTypeDef,
    ListStorageProfilesForQueueResponseTypeDef,
    ListStorageProfilesResponseTypeDef,
    ListTasksResponseTypeDef,
    ListWorkersResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetSessionsStatisticsAggregationPaginator",
    "ListAvailableMeteredProductsPaginator",
    "ListBudgetsPaginator",
    "ListFarmMembersPaginator",
    "ListFarmsPaginator",
    "ListFleetMembersPaginator",
    "ListFleetsPaginator",
    "ListJobMembersPaginator",
    "ListJobsPaginator",
    "ListLicenseEndpointsPaginator",
    "ListMeteredProductsPaginator",
    "ListMonitorsPaginator",
    "ListQueueEnvironmentsPaginator",
    "ListQueueFleetAssociationsPaginator",
    "ListQueueMembersPaginator",
    "ListQueuesPaginator",
    "ListSessionActionsPaginator",
    "ListSessionsPaginator",
    "ListSessionsForWorkerPaginator",
    "ListStepConsumersPaginator",
    "ListStepDependenciesPaginator",
    "ListStepsPaginator",
    "ListStorageProfilesPaginator",
    "ListStorageProfilesForQueuePaginator",
    "ListTasksPaginator",
    "ListWorkersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetSessionsStatisticsAggregationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.GetSessionsStatisticsAggregation)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#getsessionsstatisticsaggregationpaginator)
    """

    def paginate(
        self, *, aggregationId: str, farmId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[GetSessionsStatisticsAggregationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.GetSessionsStatisticsAggregation.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#getsessionsstatisticsaggregationpaginator)
        """

class ListAvailableMeteredProductsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListAvailableMeteredProducts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listavailablemeteredproductspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListAvailableMeteredProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListAvailableMeteredProducts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listavailablemeteredproductspaginator)
        """

class ListBudgetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListBudgets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listbudgetspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        status: BudgetStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListBudgetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListBudgets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listbudgetspaginator)
        """

class ListFarmMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFarmMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfarmmemberspaginator)
    """

    def paginate(
        self, *, farmId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListFarmMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFarmMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfarmmemberspaginator)
        """

class ListFarmsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFarms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfarmspaginator)
    """

    def paginate(
        self, *, principalId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListFarmsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFarms.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfarmspaginator)
        """

class ListFleetMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFleetMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfleetmemberspaginator)
    """

    def paginate(
        self, *, farmId: str, fleetId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListFleetMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFleetMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfleetmemberspaginator)
        """

class ListFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFleets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfleetspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        displayName: str = ...,
        principalId: str = ...,
        status: FleetStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFleets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfleetspaginator)
        """

class ListJobMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListJobMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobmemberspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListJobMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListJobMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobmemberspaginator)
        """

class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        queueId: str,
        principalId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobspaginator)
        """

class ListLicenseEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListLicenseEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listlicenseendpointspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListLicenseEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListLicenseEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listlicenseendpointspaginator)
        """

class ListMeteredProductsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListMeteredProducts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listmeteredproductspaginator)
    """

    def paginate(
        self, *, licenseEndpointId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListMeteredProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListMeteredProducts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listmeteredproductspaginator)
        """

class ListMonitorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListMonitors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listmonitorspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListMonitorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListMonitors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listmonitorspaginator)
        """

class ListQueueEnvironmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueueEnvironments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueueenvironmentspaginator)
    """

    def paginate(
        self, *, farmId: str, queueId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListQueueEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueueEnvironments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueueenvironmentspaginator)
        """

class ListQueueFleetAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueueFleetAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuefleetassociationspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        fleetId: str = ...,
        queueId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListQueueFleetAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueueFleetAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuefleetassociationspaginator)
        """

class ListQueueMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueueMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuememberspaginator)
    """

    def paginate(
        self, *, farmId: str, queueId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListQueueMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueueMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuememberspaginator)
        """

class ListQueuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuespaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        principalId: str = ...,
        status: QueueStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuespaginator)
        """

class ListSessionActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSessionActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionactionspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        sessionId: str = ...,
        taskId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListSessionActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSessionActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionactionspaginator)
        """

class ListSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionspaginator)
        """

class ListSessionsForWorkerPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSessionsForWorker)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionsforworkerpaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        fleetId: str,
        workerId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListSessionsForWorkerResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSessionsForWorker.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionsforworkerpaginator)
        """

class ListStepConsumersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStepConsumers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepconsumerspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListStepConsumersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStepConsumers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepconsumerspaginator)
        """

class ListStepDependenciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStepDependencies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepdependenciespaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListStepDependenciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStepDependencies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepdependenciespaginator)
        """

class ListStepsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSteps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSteps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepspaginator)
        """

class ListStorageProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStorageProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststorageprofilespaginator)
    """

    def paginate(
        self, *, farmId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListStorageProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStorageProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststorageprofilespaginator)
        """

class ListStorageProfilesForQueuePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStorageProfilesForQueue)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststorageprofilesforqueuepaginator)
    """

    def paginate(
        self, *, farmId: str, queueId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListStorageProfilesForQueueResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStorageProfilesForQueue.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststorageprofilesforqueuepaginator)
        """

class ListTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listtaskspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listtaskspaginator)
        """

class ListWorkersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListWorkers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listworkerspaginator)
    """

    def paginate(
        self, *, farmId: str, fleetId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListWorkersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListWorkers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listworkerspaginator)
        """
