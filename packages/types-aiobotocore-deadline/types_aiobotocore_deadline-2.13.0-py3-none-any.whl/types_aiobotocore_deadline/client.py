"""
Type annotations for deadline service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_deadline.client import DeadlineCloudClient

    session = get_session()
    async with session.create_client("deadline") as client:
        client: DeadlineCloudClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    BudgetStatusType,
    CreateJobTargetTaskRunStatusType,
    DefaultQueueBudgetActionType,
    EnvironmentTemplateTypeType,
    FleetStatusType,
    JobTargetTaskRunStatusType,
    JobTemplateTypeType,
    MembershipLevelType,
    PeriodType,
    PrincipalTypeType,
    QueueStatusType,
    StepTargetTaskRunStatusType,
    StorageProfileOperatingSystemFamilyType,
    TaskTargetRunStatusType,
    UpdatedWorkerStatusType,
    UpdateQueueFleetAssociationStatusType,
    UsageGroupByFieldType,
    UsageStatisticType,
)
from .paginator import (
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
    ListSessionsForWorkerPaginator,
    ListSessionsPaginator,
    ListStepConsumersPaginator,
    ListStepDependenciesPaginator,
    ListStepsPaginator,
    ListStorageProfilesForQueuePaginator,
    ListStorageProfilesPaginator,
    ListTasksPaginator,
    ListWorkersPaginator,
)
from .type_defs import (
    AssumeFleetRoleForReadResponseTypeDef,
    AssumeFleetRoleForWorkerResponseTypeDef,
    AssumeQueueRoleForReadResponseTypeDef,
    AssumeQueueRoleForUserResponseTypeDef,
    AssumeQueueRoleForWorkerResponseTypeDef,
    AttachmentsUnionTypeDef,
    BatchGetJobEntityResponseTypeDef,
    BudgetActionToAddTypeDef,
    BudgetActionToRemoveTypeDef,
    BudgetScheduleUnionTypeDef,
    CopyJobTemplateResponseTypeDef,
    CreateBudgetResponseTypeDef,
    CreateFarmResponseTypeDef,
    CreateFleetResponseTypeDef,
    CreateJobResponseTypeDef,
    CreateLicenseEndpointResponseTypeDef,
    CreateMonitorResponseTypeDef,
    CreateQueueEnvironmentResponseTypeDef,
    CreateQueueResponseTypeDef,
    CreateStorageProfileResponseTypeDef,
    CreateWorkerResponseTypeDef,
    FileSystemLocationTypeDef,
    FleetConfigurationUnionTypeDef,
    GetBudgetResponseTypeDef,
    GetFarmResponseTypeDef,
    GetFleetResponseTypeDef,
    GetJobResponseTypeDef,
    GetLicenseEndpointResponseTypeDef,
    GetMonitorResponseTypeDef,
    GetQueueEnvironmentResponseTypeDef,
    GetQueueFleetAssociationResponseTypeDef,
    GetQueueResponseTypeDef,
    GetSessionActionResponseTypeDef,
    GetSessionResponseTypeDef,
    GetSessionsStatisticsAggregationResponseTypeDef,
    GetStepResponseTypeDef,
    GetStorageProfileForQueueResponseTypeDef,
    GetStorageProfileResponseTypeDef,
    GetTaskResponseTypeDef,
    GetWorkerResponseTypeDef,
    HostPropertiesRequestTypeDef,
    JobAttachmentSettingsTypeDef,
    JobEntityIdentifiersUnionTypeDef,
    JobParameterTypeDef,
    JobRunAsUserTypeDef,
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
    ListTagsForResourceResponseTypeDef,
    ListTasksResponseTypeDef,
    ListWorkersResponseTypeDef,
    S3LocationTypeDef,
    SearchGroupedFilterExpressionsTypeDef,
    SearchJobsResponseTypeDef,
    SearchSortExpressionTypeDef,
    SearchStepsResponseTypeDef,
    SearchTasksResponseTypeDef,
    SearchWorkersResponseTypeDef,
    SessionsStatisticsResourcesTypeDef,
    StartSessionsStatisticsAggregationResponseTypeDef,
    TimestampTypeDef,
    UpdatedSessionActionInfoTypeDef,
    UpdateWorkerResponseTypeDef,
    UpdateWorkerScheduleResponseTypeDef,
    UsageTrackingResourceTypeDef,
    WorkerCapabilitiesTypeDef,
)
from .waiter import (
    FleetActiveWaiter,
    JobCreateCompleteWaiter,
    LicenseEndpointDeletedWaiter,
    LicenseEndpointValidWaiter,
    QueueFleetAssociationStoppedWaiter,
    QueueSchedulingBlockedWaiter,
    QueueSchedulingWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("DeadlineCloudClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class DeadlineCloudClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DeadlineCloudClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#exceptions)
        """

    async def associate_member_to_farm(
        self,
        *,
        farmId: str,
        identityStoreId: str,
        membershipLevel: MembershipLevelType,
        principalId: str,
        principalType: PrincipalTypeType,
    ) -> Dict[str, Any]:
        """
        Assigns a farm membership level to a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.associate_member_to_farm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#associate_member_to_farm)
        """

    async def associate_member_to_fleet(
        self,
        *,
        farmId: str,
        fleetId: str,
        identityStoreId: str,
        membershipLevel: MembershipLevelType,
        principalId: str,
        principalType: PrincipalTypeType,
    ) -> Dict[str, Any]:
        """
        Assigns a fleet membership level to a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.associate_member_to_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#associate_member_to_fleet)
        """

    async def associate_member_to_job(
        self,
        *,
        farmId: str,
        identityStoreId: str,
        jobId: str,
        membershipLevel: MembershipLevelType,
        principalId: str,
        principalType: PrincipalTypeType,
        queueId: str,
    ) -> Dict[str, Any]:
        """
        Assigns a job membership level to a member See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/deadline-2023-10-12/AssociateMemberToJob).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.associate_member_to_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#associate_member_to_job)
        """

    async def associate_member_to_queue(
        self,
        *,
        farmId: str,
        identityStoreId: str,
        membershipLevel: MembershipLevelType,
        principalId: str,
        principalType: PrincipalTypeType,
        queueId: str,
    ) -> Dict[str, Any]:
        """
        Assigns a queue membership level to a member See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/deadline-2023-10-12/AssociateMemberToQueue).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.associate_member_to_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#associate_member_to_queue)
        """

    async def assume_fleet_role_for_read(
        self, *, farmId: str, fleetId: str
    ) -> AssumeFleetRoleForReadResponseTypeDef:
        """
        Get Amazon Web Services credentials from the fleet role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.assume_fleet_role_for_read)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#assume_fleet_role_for_read)
        """

    async def assume_fleet_role_for_worker(
        self, *, farmId: str, fleetId: str, workerId: str
    ) -> AssumeFleetRoleForWorkerResponseTypeDef:
        """
        Get credentials from the fleet role for a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.assume_fleet_role_for_worker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#assume_fleet_role_for_worker)
        """

    async def assume_queue_role_for_read(
        self, *, farmId: str, queueId: str
    ) -> AssumeQueueRoleForReadResponseTypeDef:
        """
        Gets Amazon Web Services credentials from the queue role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.assume_queue_role_for_read)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#assume_queue_role_for_read)
        """

    async def assume_queue_role_for_user(
        self, *, farmId: str, queueId: str
    ) -> AssumeQueueRoleForUserResponseTypeDef:
        """
        Allows a user to assume a role for a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.assume_queue_role_for_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#assume_queue_role_for_user)
        """

    async def assume_queue_role_for_worker(
        self, *, farmId: str, fleetId: str, queueId: str, workerId: str
    ) -> AssumeQueueRoleForWorkerResponseTypeDef:
        """
        Allows a worker to assume a queue role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.assume_queue_role_for_worker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#assume_queue_role_for_worker)
        """

    async def batch_get_job_entity(
        self,
        *,
        farmId: str,
        fleetId: str,
        identifiers: Sequence[JobEntityIdentifiersUnionTypeDef],
        workerId: str,
    ) -> BatchGetJobEntityResponseTypeDef:
        """
        Get batched job details for a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.batch_get_job_entity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#batch_get_job_entity)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#close)
        """

    async def copy_job_template(
        self, *, farmId: str, jobId: str, queueId: str, targetS3Location: S3LocationTypeDef
    ) -> CopyJobTemplateResponseTypeDef:
        """
        Copies a job template to an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.copy_job_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#copy_job_template)
        """

    async def create_budget(
        self,
        *,
        actions: Sequence[BudgetActionToAddTypeDef],
        approximateDollarLimit: float,
        displayName: str,
        farmId: str,
        schedule: BudgetScheduleUnionTypeDef,
        usageTrackingResource: UsageTrackingResourceTypeDef,
        clientToken: str = ...,
        description: str = ...,
    ) -> CreateBudgetResponseTypeDef:
        """
        Creates a budget to set spending thresholds for your rendering activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_budget)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#create_budget)
        """

    async def create_farm(
        self,
        *,
        displayName: str,
        clientToken: str = ...,
        description: str = ...,
        kmsKeyArn: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateFarmResponseTypeDef:
        """
        Creates a farm to allow space for queues and fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_farm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#create_farm)
        """

    async def create_fleet(
        self,
        *,
        configuration: FleetConfigurationUnionTypeDef,
        displayName: str,
        farmId: str,
        maxWorkerCount: int,
        roleArn: str,
        clientToken: str = ...,
        description: str = ...,
        minWorkerCount: int = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateFleetResponseTypeDef:
        """
        Creates a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#create_fleet)
        """

    async def create_job(
        self,
        *,
        farmId: str,
        priority: int,
        queueId: str,
        template: str,
        templateType: JobTemplateTypeType,
        attachments: AttachmentsUnionTypeDef = ...,
        clientToken: str = ...,
        maxFailedTasksCount: int = ...,
        maxRetriesPerTask: int = ...,
        parameters: Mapping[str, JobParameterTypeDef] = ...,
        storageProfileId: str = ...,
        targetTaskRunStatus: CreateJobTargetTaskRunStatusType = ...,
    ) -> CreateJobResponseTypeDef:
        """
        Creates a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#create_job)
        """

    async def create_license_endpoint(
        self,
        *,
        securityGroupIds: Sequence[str],
        subnetIds: Sequence[str],
        vpcId: str,
        clientToken: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateLicenseEndpointResponseTypeDef:
        """
        Creates a license endpoint to integrate your various licensed software used for
        rendering on Deadline
        Cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_license_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#create_license_endpoint)
        """

    async def create_monitor(
        self,
        *,
        displayName: str,
        identityCenterInstanceArn: str,
        roleArn: str,
        subdomain: str,
        clientToken: str = ...,
    ) -> CreateMonitorResponseTypeDef:
        """
        Creates an Amazon Web Services Deadline Cloud monitor that you can use to view
        your farms, queues, and
        fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#create_monitor)
        """

    async def create_queue(
        self,
        *,
        displayName: str,
        farmId: str,
        allowedStorageProfileIds: Sequence[str] = ...,
        clientToken: str = ...,
        defaultBudgetAction: DefaultQueueBudgetActionType = ...,
        description: str = ...,
        jobAttachmentSettings: JobAttachmentSettingsTypeDef = ...,
        jobRunAsUser: JobRunAsUserTypeDef = ...,
        requiredFileSystemLocationNames: Sequence[str] = ...,
        roleArn: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateQueueResponseTypeDef:
        """
        Creates a queue to coordinate the order in which jobs run on a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#create_queue)
        """

    async def create_queue_environment(
        self,
        *,
        farmId: str,
        priority: int,
        queueId: str,
        template: str,
        templateType: EnvironmentTemplateTypeType,
        clientToken: str = ...,
    ) -> CreateQueueEnvironmentResponseTypeDef:
        """
        Creates an environment for a queue that defines how jobs in the queue run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_queue_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#create_queue_environment)
        """

    async def create_queue_fleet_association(
        self, *, farmId: str, fleetId: str, queueId: str
    ) -> Dict[str, Any]:
        """
        Creates an association between a queue and a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_queue_fleet_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#create_queue_fleet_association)
        """

    async def create_storage_profile(
        self,
        *,
        displayName: str,
        farmId: str,
        osFamily: StorageProfileOperatingSystemFamilyType,
        clientToken: str = ...,
        fileSystemLocations: Sequence[FileSystemLocationTypeDef] = ...,
    ) -> CreateStorageProfileResponseTypeDef:
        """
        Creates a storage profile that specifies the operating system, file type, and
        file location of resources used on a
        farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_storage_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#create_storage_profile)
        """

    async def create_worker(
        self,
        *,
        farmId: str,
        fleetId: str,
        clientToken: str = ...,
        hostProperties: HostPropertiesRequestTypeDef = ...,
    ) -> CreateWorkerResponseTypeDef:
        """
        Creates a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_worker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#create_worker)
        """

    async def delete_budget(self, *, budgetId: str, farmId: str) -> Dict[str, Any]:
        """
        Deletes a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_budget)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#delete_budget)
        """

    async def delete_farm(self, *, farmId: str) -> Dict[str, Any]:
        """
        Deletes a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_farm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#delete_farm)
        """

    async def delete_fleet(
        self, *, farmId: str, fleetId: str, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#delete_fleet)
        """

    async def delete_license_endpoint(self, *, licenseEndpointId: str) -> Dict[str, Any]:
        """
        Deletes a license endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_license_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#delete_license_endpoint)
        """

    async def delete_metered_product(
        self, *, licenseEndpointId: str, productId: str
    ) -> Dict[str, Any]:
        """
        Deletes a metered product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_metered_product)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#delete_metered_product)
        """

    async def delete_monitor(self, *, monitorId: str) -> Dict[str, Any]:
        """
        Removes a Deadline Cloud monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#delete_monitor)
        """

    async def delete_queue(self, *, farmId: str, queueId: str) -> Dict[str, Any]:
        """
        Deletes a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#delete_queue)
        """

    async def delete_queue_environment(
        self, *, farmId: str, queueEnvironmentId: str, queueId: str
    ) -> Dict[str, Any]:
        """
        Deletes a queue environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_queue_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#delete_queue_environment)
        """

    async def delete_queue_fleet_association(
        self, *, farmId: str, fleetId: str, queueId: str
    ) -> Dict[str, Any]:
        """
        Deletes a queue-fleet association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_queue_fleet_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#delete_queue_fleet_association)
        """

    async def delete_storage_profile(self, *, farmId: str, storageProfileId: str) -> Dict[str, Any]:
        """
        Deletes a storage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_storage_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#delete_storage_profile)
        """

    async def delete_worker(self, *, farmId: str, fleetId: str, workerId: str) -> Dict[str, Any]:
        """
        Deletes a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_worker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#delete_worker)
        """

    async def disassociate_member_from_farm(
        self, *, farmId: str, principalId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a member from a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.disassociate_member_from_farm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#disassociate_member_from_farm)
        """

    async def disassociate_member_from_fleet(
        self, *, farmId: str, fleetId: str, principalId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a member from a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.disassociate_member_from_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#disassociate_member_from_fleet)
        """

    async def disassociate_member_from_job(
        self, *, farmId: str, jobId: str, principalId: str, queueId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a member from a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.disassociate_member_from_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#disassociate_member_from_job)
        """

    async def disassociate_member_from_queue(
        self, *, farmId: str, principalId: str, queueId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a member from a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.disassociate_member_from_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#disassociate_member_from_queue)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#generate_presigned_url)
        """

    async def get_budget(self, *, budgetId: str, farmId: str) -> GetBudgetResponseTypeDef:
        """
        Get a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_budget)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_budget)
        """

    async def get_farm(self, *, farmId: str) -> GetFarmResponseTypeDef:
        """
        Get a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_farm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_farm)
        """

    async def get_fleet(self, *, farmId: str, fleetId: str) -> GetFleetResponseTypeDef:
        """
        Get a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_fleet)
        """

    async def get_job(self, *, farmId: str, jobId: str, queueId: str) -> GetJobResponseTypeDef:
        """
        Gets a Deadline Cloud job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_job)
        """

    async def get_license_endpoint(
        self, *, licenseEndpointId: str
    ) -> GetLicenseEndpointResponseTypeDef:
        """
        Gets a licence endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_license_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_license_endpoint)
        """

    async def get_monitor(self, *, monitorId: str) -> GetMonitorResponseTypeDef:
        """
        Gets information about the specified monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_monitor)
        """

    async def get_queue(self, *, farmId: str, queueId: str) -> GetQueueResponseTypeDef:
        """
        Gets a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_queue)
        """

    async def get_queue_environment(
        self, *, farmId: str, queueEnvironmentId: str, queueId: str
    ) -> GetQueueEnvironmentResponseTypeDef:
        """
        Gets a queue environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_queue_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_queue_environment)
        """

    async def get_queue_fleet_association(
        self, *, farmId: str, fleetId: str, queueId: str
    ) -> GetQueueFleetAssociationResponseTypeDef:
        """
        Gets a queue-fleet association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_queue_fleet_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_queue_fleet_association)
        """

    async def get_session(
        self, *, farmId: str, jobId: str, queueId: str, sessionId: str
    ) -> GetSessionResponseTypeDef:
        """
        Gets a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_session)
        """

    async def get_session_action(
        self, *, farmId: str, jobId: str, queueId: str, sessionActionId: str
    ) -> GetSessionActionResponseTypeDef:
        """
        Gets a session action for the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_session_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_session_action)
        """

    async def get_sessions_statistics_aggregation(
        self, *, aggregationId: str, farmId: str, maxResults: int = ..., nextToken: str = ...
    ) -> GetSessionsStatisticsAggregationResponseTypeDef:
        """
        Gets a set of statistics for queues or farms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_sessions_statistics_aggregation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_sessions_statistics_aggregation)
        """

    async def get_step(
        self, *, farmId: str, jobId: str, queueId: str, stepId: str
    ) -> GetStepResponseTypeDef:
        """
        Gets a step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_step)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_step)
        """

    async def get_storage_profile(
        self, *, farmId: str, storageProfileId: str
    ) -> GetStorageProfileResponseTypeDef:
        """
        Gets a storage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_storage_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_storage_profile)
        """

    async def get_storage_profile_for_queue(
        self, *, farmId: str, queueId: str, storageProfileId: str
    ) -> GetStorageProfileForQueueResponseTypeDef:
        """
        Gets a storage profile for a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_storage_profile_for_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_storage_profile_for_queue)
        """

    async def get_task(
        self, *, farmId: str, jobId: str, queueId: str, stepId: str, taskId: str
    ) -> GetTaskResponseTypeDef:
        """
        Gets a task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_task)
        """

    async def get_worker(
        self, *, farmId: str, fleetId: str, workerId: str
    ) -> GetWorkerResponseTypeDef:
        """
        Gets a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_worker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_worker)
        """

    async def list_available_metered_products(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListAvailableMeteredProductsResponseTypeDef:
        """
        A list of the available metered products.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_available_metered_products)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_available_metered_products)
        """

    async def list_budgets(
        self,
        *,
        farmId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        status: BudgetStatusType = ...,
    ) -> ListBudgetsResponseTypeDef:
        """
        A list of budgets in a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_budgets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_budgets)
        """

    async def list_farm_members(
        self, *, farmId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListFarmMembersResponseTypeDef:
        """
        Lists the members of a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_farm_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_farm_members)
        """

    async def list_farms(
        self, *, maxResults: int = ..., nextToken: str = ..., principalId: str = ...
    ) -> ListFarmsResponseTypeDef:
        """
        Lists farms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_farms)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_farms)
        """

    async def list_fleet_members(
        self, *, farmId: str, fleetId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListFleetMembersResponseTypeDef:
        """
        Lists fleet members.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_fleet_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_fleet_members)
        """

    async def list_fleets(
        self,
        *,
        farmId: str,
        displayName: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        principalId: str = ...,
        status: FleetStatusType = ...,
    ) -> ListFleetsResponseTypeDef:
        """
        Lists fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_fleets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_fleets)
        """

    async def list_job_members(
        self, *, farmId: str, jobId: str, queueId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListJobMembersResponseTypeDef:
        """
        Lists members on a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_job_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_job_members)
        """

    async def list_jobs(
        self,
        *,
        farmId: str,
        queueId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        principalId: str = ...,
    ) -> ListJobsResponseTypeDef:
        """
        Lists jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_jobs)
        """

    async def list_license_endpoints(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListLicenseEndpointsResponseTypeDef:
        """
        Lists license endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_license_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_license_endpoints)
        """

    async def list_metered_products(
        self, *, licenseEndpointId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListMeteredProductsResponseTypeDef:
        """
        Lists metered products.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_metered_products)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_metered_products)
        """

    async def list_monitors(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListMonitorsResponseTypeDef:
        """
        Gets a list of your monitors in Deadline Cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_monitors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_monitors)
        """

    async def list_queue_environments(
        self, *, farmId: str, queueId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListQueueEnvironmentsResponseTypeDef:
        """
        Lists queue environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_queue_environments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_queue_environments)
        """

    async def list_queue_fleet_associations(
        self,
        *,
        farmId: str,
        fleetId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        queueId: str = ...,
    ) -> ListQueueFleetAssociationsResponseTypeDef:
        """
        Lists queue-fleet associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_queue_fleet_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_queue_fleet_associations)
        """

    async def list_queue_members(
        self, *, farmId: str, queueId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListQueueMembersResponseTypeDef:
        """
        Lists the members in a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_queue_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_queue_members)
        """

    async def list_queues(
        self,
        *,
        farmId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        principalId: str = ...,
        status: QueueStatusType = ...,
    ) -> ListQueuesResponseTypeDef:
        """
        Lists queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_queues)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_queues)
        """

    async def list_session_actions(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        sessionId: str = ...,
        taskId: str = ...,
    ) -> ListSessionActionsResponseTypeDef:
        """
        Lists session actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_session_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_session_actions)
        """

    async def list_sessions(
        self, *, farmId: str, jobId: str, queueId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListSessionsResponseTypeDef:
        """
        Lists sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_sessions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_sessions)
        """

    async def list_sessions_for_worker(
        self,
        *,
        farmId: str,
        fleetId: str,
        workerId: str,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListSessionsForWorkerResponseTypeDef:
        """
        Lists sessions for a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_sessions_for_worker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_sessions_for_worker)
        """

    async def list_step_consumers(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListStepConsumersResponseTypeDef:
        """
        Lists step consumers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_step_consumers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_step_consumers)
        """

    async def list_step_dependencies(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListStepDependenciesResponseTypeDef:
        """
        Lists the dependencies for a step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_step_dependencies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_step_dependencies)
        """

    async def list_steps(
        self, *, farmId: str, jobId: str, queueId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListStepsResponseTypeDef:
        """
        Lists steps for a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_steps)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_steps)
        """

    async def list_storage_profiles(
        self, *, farmId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListStorageProfilesResponseTypeDef:
        """
        Lists storage profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_storage_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_storage_profiles)
        """

    async def list_storage_profiles_for_queue(
        self, *, farmId: str, queueId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListStorageProfilesForQueueResponseTypeDef:
        """
        Lists storage profiles for a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_storage_profiles_for_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_storage_profiles_for_queue)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_tags_for_resource)
        """

    async def list_tasks(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListTasksResponseTypeDef:
        """
        Lists tasks for a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_tasks)
        """

    async def list_workers(
        self, *, farmId: str, fleetId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListWorkersResponseTypeDef:
        """
        Lists workers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_workers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#list_workers)
        """

    async def put_metered_product(
        self, *, licenseEndpointId: str, productId: str
    ) -> Dict[str, Any]:
        """
        Adds a metered product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.put_metered_product)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#put_metered_product)
        """

    async def search_jobs(
        self,
        *,
        farmId: str,
        itemOffset: int,
        queueIds: Sequence[str],
        filterExpressions: "SearchGroupedFilterExpressionsTypeDef" = ...,
        pageSize: int = ...,
        sortExpressions: Sequence[SearchSortExpressionTypeDef] = ...,
    ) -> SearchJobsResponseTypeDef:
        """
        Searches for jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.search_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#search_jobs)
        """

    async def search_steps(
        self,
        *,
        farmId: str,
        itemOffset: int,
        queueIds: Sequence[str],
        filterExpressions: "SearchGroupedFilterExpressionsTypeDef" = ...,
        jobId: str = ...,
        pageSize: int = ...,
        sortExpressions: Sequence[SearchSortExpressionTypeDef] = ...,
    ) -> SearchStepsResponseTypeDef:
        """
        Searches for steps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.search_steps)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#search_steps)
        """

    async def search_tasks(
        self,
        *,
        farmId: str,
        itemOffset: int,
        queueIds: Sequence[str],
        filterExpressions: "SearchGroupedFilterExpressionsTypeDef" = ...,
        jobId: str = ...,
        pageSize: int = ...,
        sortExpressions: Sequence[SearchSortExpressionTypeDef] = ...,
    ) -> SearchTasksResponseTypeDef:
        """
        Searches for tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.search_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#search_tasks)
        """

    async def search_workers(
        self,
        *,
        farmId: str,
        fleetIds: Sequence[str],
        itemOffset: int,
        filterExpressions: "SearchGroupedFilterExpressionsTypeDef" = ...,
        pageSize: int = ...,
        sortExpressions: Sequence[SearchSortExpressionTypeDef] = ...,
    ) -> SearchWorkersResponseTypeDef:
        """
        Searches for workers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.search_workers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#search_workers)
        """

    async def start_sessions_statistics_aggregation(
        self,
        *,
        endTime: TimestampTypeDef,
        farmId: str,
        groupBy: Sequence[UsageGroupByFieldType],
        resourceIds: SessionsStatisticsResourcesTypeDef,
        startTime: TimestampTypeDef,
        statistics: Sequence[UsageStatisticType],
        period: PeriodType = ...,
        timezone: str = ...,
    ) -> StartSessionsStatisticsAggregationResponseTypeDef:
        """
        Starts an asynchronous request for getting aggregated statistics about queues
        and
        farms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.start_sessions_statistics_aggregation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#start_sessions_statistics_aggregation)
        """

    async def tag_resource(
        self, *, resourceArn: str, tags: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Tags a resource using the resource's ARN and desired tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from a resource using the resource's ARN and tag to remove.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#untag_resource)
        """

    async def update_budget(
        self,
        *,
        budgetId: str,
        farmId: str,
        actionsToAdd: Sequence[BudgetActionToAddTypeDef] = ...,
        actionsToRemove: Sequence[BudgetActionToRemoveTypeDef] = ...,
        approximateDollarLimit: float = ...,
        clientToken: str = ...,
        description: str = ...,
        displayName: str = ...,
        schedule: BudgetScheduleUnionTypeDef = ...,
        status: BudgetStatusType = ...,
    ) -> Dict[str, Any]:
        """
        Updates a budget that sets spending thresholds for rendering activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_budget)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_budget)
        """

    async def update_farm(
        self, *, farmId: str, description: str = ..., displayName: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_farm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_farm)
        """

    async def update_fleet(
        self,
        *,
        farmId: str,
        fleetId: str,
        clientToken: str = ...,
        configuration: FleetConfigurationUnionTypeDef = ...,
        description: str = ...,
        displayName: str = ...,
        maxWorkerCount: int = ...,
        minWorkerCount: int = ...,
        roleArn: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_fleet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_fleet)
        """

    async def update_job(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        clientToken: str = ...,
        lifecycleStatus: Literal["ARCHIVED"] = ...,
        maxFailedTasksCount: int = ...,
        maxRetriesPerTask: int = ...,
        priority: int = ...,
        targetTaskRunStatus: JobTargetTaskRunStatusType = ...,
    ) -> Dict[str, Any]:
        """
        Updates a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_job)
        """

    async def update_monitor(
        self, *, monitorId: str, displayName: str = ..., roleArn: str = ..., subdomain: str = ...
    ) -> Dict[str, Any]:
        """
        Modifies the settings for a Deadline Cloud monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_monitor)
        """

    async def update_queue(
        self,
        *,
        farmId: str,
        queueId: str,
        allowedStorageProfileIdsToAdd: Sequence[str] = ...,
        allowedStorageProfileIdsToRemove: Sequence[str] = ...,
        clientToken: str = ...,
        defaultBudgetAction: DefaultQueueBudgetActionType = ...,
        description: str = ...,
        displayName: str = ...,
        jobAttachmentSettings: JobAttachmentSettingsTypeDef = ...,
        jobRunAsUser: JobRunAsUserTypeDef = ...,
        requiredFileSystemLocationNamesToAdd: Sequence[str] = ...,
        requiredFileSystemLocationNamesToRemove: Sequence[str] = ...,
        roleArn: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_queue)
        """

    async def update_queue_environment(
        self,
        *,
        farmId: str,
        queueEnvironmentId: str,
        queueId: str,
        clientToken: str = ...,
        priority: int = ...,
        template: str = ...,
        templateType: EnvironmentTemplateTypeType = ...,
    ) -> Dict[str, Any]:
        """
        Updates the queue environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_queue_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_queue_environment)
        """

    async def update_queue_fleet_association(
        self,
        *,
        farmId: str,
        fleetId: str,
        queueId: str,
        status: UpdateQueueFleetAssociationStatusType,
    ) -> Dict[str, Any]:
        """
        Updates a queue-fleet association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_queue_fleet_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_queue_fleet_association)
        """

    async def update_session(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        sessionId: str,
        targetLifecycleStatus: Literal["ENDED"],
        clientToken: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_session)
        """

    async def update_step(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        targetTaskRunStatus: StepTargetTaskRunStatusType,
        clientToken: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates a step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_step)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_step)
        """

    async def update_storage_profile(
        self,
        *,
        farmId: str,
        storageProfileId: str,
        clientToken: str = ...,
        displayName: str = ...,
        fileSystemLocationsToAdd: Sequence[FileSystemLocationTypeDef] = ...,
        fileSystemLocationsToRemove: Sequence[FileSystemLocationTypeDef] = ...,
        osFamily: StorageProfileOperatingSystemFamilyType = ...,
    ) -> Dict[str, Any]:
        """
        Updates a storage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_storage_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_storage_profile)
        """

    async def update_task(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        targetRunStatus: TaskTargetRunStatusType,
        taskId: str,
        clientToken: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates a task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_task)
        """

    async def update_worker(
        self,
        *,
        farmId: str,
        fleetId: str,
        workerId: str,
        capabilities: WorkerCapabilitiesTypeDef = ...,
        hostProperties: HostPropertiesRequestTypeDef = ...,
        status: UpdatedWorkerStatusType = ...,
    ) -> UpdateWorkerResponseTypeDef:
        """
        Updates a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_worker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_worker)
        """

    async def update_worker_schedule(
        self,
        *,
        farmId: str,
        fleetId: str,
        workerId: str,
        updatedSessionActions: Mapping[str, UpdatedSessionActionInfoTypeDef] = ...,
    ) -> UpdateWorkerScheduleResponseTypeDef:
        """
        Updates the schedule for a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_worker_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#update_worker_schedule)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_sessions_statistics_aggregation"]
    ) -> GetSessionsStatisticsAggregationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_available_metered_products"]
    ) -> ListAvailableMeteredProductsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_budgets"]) -> ListBudgetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_farm_members"]
    ) -> ListFarmMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_farms"]) -> ListFarmsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_fleet_members"]
    ) -> ListFleetMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_fleets"]) -> ListFleetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_job_members"]) -> ListJobMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_license_endpoints"]
    ) -> ListLicenseEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_metered_products"]
    ) -> ListMeteredProductsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_monitors"]) -> ListMonitorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_queue_environments"]
    ) -> ListQueueEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_queue_fleet_associations"]
    ) -> ListQueueFleetAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_queue_members"]
    ) -> ListQueueMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_queues"]) -> ListQueuesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_session_actions"]
    ) -> ListSessionActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_sessions"]) -> ListSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sessions_for_worker"]
    ) -> ListSessionsForWorkerPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_step_consumers"]
    ) -> ListStepConsumersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_step_dependencies"]
    ) -> ListStepDependenciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_steps"]) -> ListStepsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_storage_profiles"]
    ) -> ListStorageProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_storage_profiles_for_queue"]
    ) -> ListStorageProfilesForQueuePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tasks"]) -> ListTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workers"]) -> ListWorkersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["fleet_active"]) -> FleetActiveWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["job_create_complete"]) -> JobCreateCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["license_endpoint_deleted"]
    ) -> LicenseEndpointDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["license_endpoint_valid"]
    ) -> LicenseEndpointValidWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["queue_fleet_association_stopped"]
    ) -> QueueFleetAssociationStoppedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["queue_scheduling"]) -> QueueSchedulingWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["queue_scheduling_blocked"]
    ) -> QueueSchedulingBlockedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/#get_waiter)
        """

    async def __aenter__(self) -> "DeadlineCloudClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/client/)
        """
