"""
Type annotations for deadline service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/type_defs/)

Usage::

    ```python
    from types_aiobotocore_deadline.type_defs import AcceleratorCountRangeTypeDef

    data: AcceleratorCountRangeTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AutoScalingModeType,
    AutoScalingStatusType,
    BudgetActionTypeType,
    BudgetStatusType,
    ComparisonOperatorType,
    CompletedStatusType,
    CpuArchitectureTypeType,
    CreateJobTargetTaskRunStatusType,
    CustomerManagedFleetOperatingSystemFamilyType,
    DefaultQueueBudgetActionType,
    DependencyConsumerResolutionStatusType,
    Ec2MarketTypeType,
    EnvironmentTemplateTypeType,
    FileSystemLocationTypeType,
    FleetStatusType,
    JobAttachmentsFileSystemType,
    JobEntityErrorCodeType,
    JobLifecycleStatusType,
    JobTargetTaskRunStatusType,
    JobTemplateTypeType,
    LicenseEndpointStatusType,
    LogicalOperatorType,
    MembershipLevelType,
    PathFormatType,
    PeriodType,
    PrincipalTypeType,
    QueueBlockedReasonType,
    QueueFleetAssociationStatusType,
    QueueStatusType,
    RunAsType,
    ServiceManagedFleetOperatingSystemFamilyType,
    SessionActionStatusType,
    SessionLifecycleStatusType,
    SessionsStatisticsAggregationStatusType,
    SortOrderType,
    StepLifecycleStatusType,
    StepParameterTypeType,
    StepTargetTaskRunStatusType,
    StorageProfileOperatingSystemFamilyType,
    TaskRunStatusType,
    TaskTargetRunStatusType,
    UpdatedWorkerStatusType,
    UpdateQueueFleetAssociationStatusType,
    UsageGroupByFieldType,
    UsageStatisticType,
    UsageTypeType,
    WorkerStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AcceleratorCountRangeTypeDef",
    "AcceleratorTotalMemoryMiBRangeTypeDef",
    "AssignedEnvironmentEnterSessionActionDefinitionTypeDef",
    "AssignedEnvironmentExitSessionActionDefinitionTypeDef",
    "AssignedSyncInputJobAttachmentsSessionActionDefinitionTypeDef",
    "LogConfigurationTypeDef",
    "TaskParameterValueTypeDef",
    "AssociateMemberToFarmRequestRequestTypeDef",
    "AssociateMemberToFleetRequestRequestTypeDef",
    "AssociateMemberToJobRequestRequestTypeDef",
    "AssociateMemberToQueueRequestRequestTypeDef",
    "AssumeFleetRoleForReadRequestRequestTypeDef",
    "AwsCredentialsTypeDef",
    "ResponseMetadataTypeDef",
    "AssumeFleetRoleForWorkerRequestRequestTypeDef",
    "AssumeQueueRoleForReadRequestRequestTypeDef",
    "AssumeQueueRoleForUserRequestRequestTypeDef",
    "AssumeQueueRoleForWorkerRequestRequestTypeDef",
    "ManifestPropertiesOutputTypeDef",
    "ManifestPropertiesTypeDef",
    "BudgetActionToAddTypeDef",
    "BudgetActionToRemoveTypeDef",
    "FixedBudgetScheduleOutputTypeDef",
    "ConsumedUsagesTypeDef",
    "UsageTrackingResourceTypeDef",
    "S3LocationTypeDef",
    "CreateFarmRequestRequestTypeDef",
    "JobParameterTypeDef",
    "CreateLicenseEndpointRequestRequestTypeDef",
    "CreateMonitorRequestRequestTypeDef",
    "CreateQueueEnvironmentRequestRequestTypeDef",
    "CreateQueueFleetAssociationRequestRequestTypeDef",
    "JobAttachmentSettingsTypeDef",
    "FileSystemLocationTypeDef",
    "FleetAmountCapabilityTypeDef",
    "FleetAttributeCapabilityExtraOutputTypeDef",
    "MemoryMiBRangeTypeDef",
    "VCpuCountRangeTypeDef",
    "FleetAttributeCapabilityOutputTypeDef",
    "FleetAttributeCapabilityTypeDef",
    "TimestampTypeDef",
    "DeleteBudgetRequestRequestTypeDef",
    "DeleteFarmRequestRequestTypeDef",
    "DeleteFleetRequestRequestTypeDef",
    "DeleteLicenseEndpointRequestRequestTypeDef",
    "DeleteMeteredProductRequestRequestTypeDef",
    "DeleteMonitorRequestRequestTypeDef",
    "DeleteQueueEnvironmentRequestRequestTypeDef",
    "DeleteQueueFleetAssociationRequestRequestTypeDef",
    "DeleteQueueRequestRequestTypeDef",
    "DeleteStorageProfileRequestRequestTypeDef",
    "DeleteWorkerRequestRequestTypeDef",
    "DependencyCountsTypeDef",
    "DisassociateMemberFromFarmRequestRequestTypeDef",
    "DisassociateMemberFromFleetRequestRequestTypeDef",
    "DisassociateMemberFromJobRequestRequestTypeDef",
    "DisassociateMemberFromQueueRequestRequestTypeDef",
    "Ec2EbsVolumeTypeDef",
    "EnvironmentDetailsEntityTypeDef",
    "EnvironmentDetailsErrorTypeDef",
    "EnvironmentDetailsIdentifiersTypeDef",
    "EnvironmentEnterSessionActionDefinitionSummaryTypeDef",
    "EnvironmentEnterSessionActionDefinitionTypeDef",
    "EnvironmentExitSessionActionDefinitionSummaryTypeDef",
    "EnvironmentExitSessionActionDefinitionTypeDef",
    "FarmMemberTypeDef",
    "FarmSummaryTypeDef",
    "FieldSortExpressionTypeDef",
    "FleetMemberTypeDef",
    "GetBudgetRequestRequestTypeDef",
    "ResponseBudgetActionTypeDef",
    "GetFarmRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "GetFleetRequestRequestTypeDef",
    "JobAttachmentDetailsErrorTypeDef",
    "JobDetailsErrorTypeDef",
    "StepDetailsErrorTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetLicenseEndpointRequestRequestTypeDef",
    "GetMonitorRequestRequestTypeDef",
    "GetQueueEnvironmentRequestRequestTypeDef",
    "GetQueueFleetAssociationRequestRequestTypeDef",
    "GetQueueRequestRequestTypeDef",
    "GetSessionActionRequestRequestTypeDef",
    "GetSessionRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "GetSessionsStatisticsAggregationRequestRequestTypeDef",
    "GetStepRequestRequestTypeDef",
    "GetStorageProfileForQueueRequestRequestTypeDef",
    "GetStorageProfileRequestRequestTypeDef",
    "GetTaskRequestRequestTypeDef",
    "GetWorkerRequestRequestTypeDef",
    "IpAddressesTypeDef",
    "IpAddressesOutputTypeDef",
    "JobAttachmentDetailsIdentifiersTypeDef",
    "PathMappingRuleTypeDef",
    "JobDetailsIdentifiersTypeDef",
    "StepDetailsIdentifiersTypeDef",
    "StepDetailsEntityTypeDef",
    "JobMemberTypeDef",
    "PosixUserTypeDef",
    "WindowsUserTypeDef",
    "JobSummaryTypeDef",
    "LicenseEndpointSummaryTypeDef",
    "ListAvailableMeteredProductsRequestRequestTypeDef",
    "MeteredProductSummaryTypeDef",
    "ListBudgetsRequestRequestTypeDef",
    "ListFarmMembersRequestRequestTypeDef",
    "ListFarmsRequestRequestTypeDef",
    "ListFleetMembersRequestRequestTypeDef",
    "ListFleetsRequestRequestTypeDef",
    "ListJobMembersRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListLicenseEndpointsRequestRequestTypeDef",
    "ListMeteredProductsRequestRequestTypeDef",
    "ListMonitorsRequestRequestTypeDef",
    "MonitorSummaryTypeDef",
    "ListQueueEnvironmentsRequestRequestTypeDef",
    "QueueEnvironmentSummaryTypeDef",
    "ListQueueFleetAssociationsRequestRequestTypeDef",
    "QueueFleetAssociationSummaryTypeDef",
    "ListQueueMembersRequestRequestTypeDef",
    "QueueMemberTypeDef",
    "ListQueuesRequestRequestTypeDef",
    "QueueSummaryTypeDef",
    "ListSessionActionsRequestRequestTypeDef",
    "ListSessionsForWorkerRequestRequestTypeDef",
    "WorkerSessionSummaryTypeDef",
    "ListSessionsRequestRequestTypeDef",
    "SessionSummaryTypeDef",
    "ListStepConsumersRequestRequestTypeDef",
    "StepConsumerTypeDef",
    "ListStepDependenciesRequestRequestTypeDef",
    "StepDependencyTypeDef",
    "ListStepsRequestRequestTypeDef",
    "ListStorageProfilesForQueueRequestRequestTypeDef",
    "StorageProfileSummaryTypeDef",
    "ListStorageProfilesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTasksRequestRequestTypeDef",
    "ListWorkersRequestRequestTypeDef",
    "ParameterFilterExpressionTypeDef",
    "ParameterSortExpressionTypeDef",
    "StepParameterTypeDef",
    "PutMeteredProductRequestRequestTypeDef",
    "SearchTermFilterExpressionTypeDef",
    "StringFilterExpressionTypeDef",
    "SearchGroupedFilterExpressionsTypeDef",
    "UserJobsFirstTypeDef",
    "ServiceManagedEc2InstanceMarketOptionsTypeDef",
    "SyncInputJobAttachmentsSessionActionDefinitionSummaryTypeDef",
    "TaskRunSessionActionDefinitionSummaryTypeDef",
    "SyncInputJobAttachmentsSessionActionDefinitionTypeDef",
    "SessionsStatisticsResourcesTypeDef",
    "StatsTypeDef",
    "StepAmountCapabilityTypeDef",
    "StepAttributeCapabilityTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFarmRequestRequestTypeDef",
    "UpdateJobRequestRequestTypeDef",
    "UpdateMonitorRequestRequestTypeDef",
    "UpdateQueueEnvironmentRequestRequestTypeDef",
    "UpdateQueueFleetAssociationRequestRequestTypeDef",
    "UpdateSessionRequestRequestTypeDef",
    "UpdateStepRequestRequestTypeDef",
    "UpdateTaskRequestRequestTypeDef",
    "WorkerAmountCapabilityTypeDef",
    "WorkerAttributeCapabilityTypeDef",
    "AssignedTaskRunSessionActionDefinitionTypeDef",
    "TaskRunSessionActionDefinitionTypeDef",
    "TaskSearchSummaryTypeDef",
    "TaskSummaryTypeDef",
    "AssumeFleetRoleForReadResponseTypeDef",
    "AssumeFleetRoleForWorkerResponseTypeDef",
    "AssumeQueueRoleForReadResponseTypeDef",
    "AssumeQueueRoleForUserResponseTypeDef",
    "AssumeQueueRoleForWorkerResponseTypeDef",
    "CopyJobTemplateResponseTypeDef",
    "CreateBudgetResponseTypeDef",
    "CreateFarmResponseTypeDef",
    "CreateFleetResponseTypeDef",
    "CreateJobResponseTypeDef",
    "CreateLicenseEndpointResponseTypeDef",
    "CreateMonitorResponseTypeDef",
    "CreateQueueEnvironmentResponseTypeDef",
    "CreateQueueResponseTypeDef",
    "CreateStorageProfileResponseTypeDef",
    "CreateWorkerResponseTypeDef",
    "GetFarmResponseTypeDef",
    "GetLicenseEndpointResponseTypeDef",
    "GetMonitorResponseTypeDef",
    "GetQueueEnvironmentResponseTypeDef",
    "GetQueueFleetAssociationResponseTypeDef",
    "GetTaskResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartSessionsStatisticsAggregationResponseTypeDef",
    "UpdateWorkerResponseTypeDef",
    "AttachmentsOutputTypeDef",
    "AttachmentsTypeDef",
    "BudgetScheduleOutputTypeDef",
    "BudgetSummaryTypeDef",
    "CopyJobTemplateRequestRequestTypeDef",
    "JobSearchSummaryTypeDef",
    "CreateStorageProfileRequestRequestTypeDef",
    "GetStorageProfileForQueueResponseTypeDef",
    "GetStorageProfileResponseTypeDef",
    "UpdateStorageProfileRequestRequestTypeDef",
    "CustomerManagedWorkerCapabilitiesExtraOutputTypeDef",
    "CustomerManagedWorkerCapabilitiesOutputTypeDef",
    "FleetCapabilitiesTypeDef",
    "CustomerManagedWorkerCapabilitiesTypeDef",
    "DateTimeFilterExpressionTypeDef",
    "FixedBudgetScheduleTypeDef",
    "UpdatedSessionActionInfoTypeDef",
    "StepSummaryTypeDef",
    "ServiceManagedEc2InstanceCapabilitiesExtraOutputTypeDef",
    "ServiceManagedEc2InstanceCapabilitiesOutputTypeDef",
    "ServiceManagedEc2InstanceCapabilitiesTypeDef",
    "ListFarmMembersResponseTypeDef",
    "ListFarmsResponseTypeDef",
    "ListFleetMembersResponseTypeDef",
    "GetFleetRequestFleetActiveWaitTypeDef",
    "GetJobRequestJobCreateCompleteWaitTypeDef",
    "GetLicenseEndpointRequestLicenseEndpointDeletedWaitTypeDef",
    "GetLicenseEndpointRequestLicenseEndpointValidWaitTypeDef",
    "GetQueueFleetAssociationRequestQueueFleetAssociationStoppedWaitTypeDef",
    "GetQueueRequestQueueSchedulingBlockedWaitTypeDef",
    "GetQueueRequestQueueSchedulingWaitTypeDef",
    "GetJobEntityErrorTypeDef",
    "GetSessionsStatisticsAggregationRequestGetSessionsStatisticsAggregationPaginateTypeDef",
    "ListAvailableMeteredProductsRequestListAvailableMeteredProductsPaginateTypeDef",
    "ListBudgetsRequestListBudgetsPaginateTypeDef",
    "ListFarmMembersRequestListFarmMembersPaginateTypeDef",
    "ListFarmsRequestListFarmsPaginateTypeDef",
    "ListFleetMembersRequestListFleetMembersPaginateTypeDef",
    "ListFleetsRequestListFleetsPaginateTypeDef",
    "ListJobMembersRequestListJobMembersPaginateTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "ListLicenseEndpointsRequestListLicenseEndpointsPaginateTypeDef",
    "ListMeteredProductsRequestListMeteredProductsPaginateTypeDef",
    "ListMonitorsRequestListMonitorsPaginateTypeDef",
    "ListQueueEnvironmentsRequestListQueueEnvironmentsPaginateTypeDef",
    "ListQueueFleetAssociationsRequestListQueueFleetAssociationsPaginateTypeDef",
    "ListQueueMembersRequestListQueueMembersPaginateTypeDef",
    "ListQueuesRequestListQueuesPaginateTypeDef",
    "ListSessionActionsRequestListSessionActionsPaginateTypeDef",
    "ListSessionsForWorkerRequestListSessionsForWorkerPaginateTypeDef",
    "ListSessionsRequestListSessionsPaginateTypeDef",
    "ListStepConsumersRequestListStepConsumersPaginateTypeDef",
    "ListStepDependenciesRequestListStepDependenciesPaginateTypeDef",
    "ListStepsRequestListStepsPaginateTypeDef",
    "ListStorageProfilesForQueueRequestListStorageProfilesForQueuePaginateTypeDef",
    "ListStorageProfilesRequestListStorageProfilesPaginateTypeDef",
    "ListTasksRequestListTasksPaginateTypeDef",
    "ListWorkersRequestListWorkersPaginateTypeDef",
    "HostPropertiesRequestTypeDef",
    "HostPropertiesResponseTypeDef",
    "JobEntityIdentifiersUnionTypeDef",
    "ListJobMembersResponseTypeDef",
    "JobRunAsUserTypeDef",
    "ListJobsResponseTypeDef",
    "ListLicenseEndpointsResponseTypeDef",
    "ListAvailableMeteredProductsResponseTypeDef",
    "ListMeteredProductsResponseTypeDef",
    "ListMonitorsResponseTypeDef",
    "ListQueueEnvironmentsResponseTypeDef",
    "ListQueueFleetAssociationsResponseTypeDef",
    "ListQueueMembersResponseTypeDef",
    "ListQueuesResponseTypeDef",
    "ListSessionsForWorkerResponseTypeDef",
    "ListSessionsResponseTypeDef",
    "ListStepConsumersResponseTypeDef",
    "ListStepDependenciesResponseTypeDef",
    "ListStorageProfilesForQueueResponseTypeDef",
    "ListStorageProfilesResponseTypeDef",
    "ParameterSpaceTypeDef",
    "SearchSortExpressionTypeDef",
    "SessionActionDefinitionSummaryTypeDef",
    "StartSessionsStatisticsAggregationRequestRequestTypeDef",
    "StatisticsTypeDef",
    "StepRequiredCapabilitiesTypeDef",
    "WorkerCapabilitiesTypeDef",
    "AssignedSessionActionDefinitionTypeDef",
    "SessionActionDefinitionTypeDef",
    "SearchTasksResponseTypeDef",
    "ListTasksResponseTypeDef",
    "GetJobResponseTypeDef",
    "JobAttachmentDetailsEntityTypeDef",
    "AttachmentsUnionTypeDef",
    "CreateJobRequestRequestTypeDef",
    "GetBudgetResponseTypeDef",
    "ListBudgetsResponseTypeDef",
    "SearchJobsResponseTypeDef",
    "CustomerManagedFleetConfigurationExtraOutputTypeDef",
    "CustomerManagedFleetConfigurationOutputTypeDef",
    "CustomerManagedFleetConfigurationTypeDef",
    "SearchFilterExpressionTypeDef",
    "BudgetScheduleTypeDef",
    "UpdateWorkerScheduleRequestRequestTypeDef",
    "ListStepsResponseTypeDef",
    "ServiceManagedEc2FleetConfigurationExtraOutputTypeDef",
    "ServiceManagedEc2FleetConfigurationOutputTypeDef",
    "ServiceManagedEc2FleetConfigurationTypeDef",
    "CreateWorkerRequestRequestTypeDef",
    "GetSessionResponseTypeDef",
    "GetWorkerResponseTypeDef",
    "WorkerSearchSummaryTypeDef",
    "WorkerSummaryTypeDef",
    "BatchGetJobEntityRequestRequestTypeDef",
    "CreateQueueRequestRequestTypeDef",
    "GetQueueResponseTypeDef",
    "JobDetailsEntityTypeDef",
    "UpdateQueueRequestRequestTypeDef",
    "StepSearchSummaryTypeDef",
    "SearchJobsRequestRequestTypeDef",
    "SearchStepsRequestRequestTypeDef",
    "SearchTasksRequestRequestTypeDef",
    "SearchWorkersRequestRequestTypeDef",
    "SessionActionSummaryTypeDef",
    "GetSessionsStatisticsAggregationResponseTypeDef",
    "GetStepResponseTypeDef",
    "UpdateWorkerRequestRequestTypeDef",
    "AssignedSessionActionTypeDef",
    "GetSessionActionResponseTypeDef",
    "BudgetScheduleUnionTypeDef",
    "CreateBudgetRequestRequestTypeDef",
    "UpdateBudgetRequestRequestTypeDef",
    "FleetConfigurationExtraOutputTypeDef",
    "FleetConfigurationOutputTypeDef",
    "FleetConfigurationTypeDef",
    "SearchWorkersResponseTypeDef",
    "ListWorkersResponseTypeDef",
    "JobEntityTypeDef",
    "SearchStepsResponseTypeDef",
    "ListSessionActionsResponseTypeDef",
    "AssignedSessionTypeDef",
    "FleetSummaryTypeDef",
    "GetFleetResponseTypeDef",
    "CreateFleetRequestRequestTypeDef",
    "FleetConfigurationUnionTypeDef",
    "UpdateFleetRequestRequestTypeDef",
    "BatchGetJobEntityResponseTypeDef",
    "UpdateWorkerScheduleResponseTypeDef",
    "ListFleetsResponseTypeDef",
)

AcceleratorCountRangeTypeDef = TypedDict(
    "AcceleratorCountRangeTypeDef",
    {
        "min": int,
        "max": NotRequired[int],
    },
)
AcceleratorTotalMemoryMiBRangeTypeDef = TypedDict(
    "AcceleratorTotalMemoryMiBRangeTypeDef",
    {
        "min": int,
        "max": NotRequired[int],
    },
)
AssignedEnvironmentEnterSessionActionDefinitionTypeDef = TypedDict(
    "AssignedEnvironmentEnterSessionActionDefinitionTypeDef",
    {
        "environmentId": str,
    },
)
AssignedEnvironmentExitSessionActionDefinitionTypeDef = TypedDict(
    "AssignedEnvironmentExitSessionActionDefinitionTypeDef",
    {
        "environmentId": str,
    },
)
AssignedSyncInputJobAttachmentsSessionActionDefinitionTypeDef = TypedDict(
    "AssignedSyncInputJobAttachmentsSessionActionDefinitionTypeDef",
    {
        "stepId": NotRequired[str],
    },
)
LogConfigurationTypeDef = TypedDict(
    "LogConfigurationTypeDef",
    {
        "logDriver": str,
        "error": NotRequired[str],
        "options": NotRequired[Dict[str, str]],
        "parameters": NotRequired[Dict[str, str]],
    },
)
TaskParameterValueTypeDef = TypedDict(
    "TaskParameterValueTypeDef",
    {
        "float": NotRequired[str],
        "int": NotRequired[str],
        "path": NotRequired[str],
        "string": NotRequired[str],
    },
)
AssociateMemberToFarmRequestRequestTypeDef = TypedDict(
    "AssociateMemberToFarmRequestRequestTypeDef",
    {
        "farmId": str,
        "identityStoreId": str,
        "membershipLevel": MembershipLevelType,
        "principalId": str,
        "principalType": PrincipalTypeType,
    },
)
AssociateMemberToFleetRequestRequestTypeDef = TypedDict(
    "AssociateMemberToFleetRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "identityStoreId": str,
        "membershipLevel": MembershipLevelType,
        "principalId": str,
        "principalType": PrincipalTypeType,
    },
)
AssociateMemberToJobRequestRequestTypeDef = TypedDict(
    "AssociateMemberToJobRequestRequestTypeDef",
    {
        "farmId": str,
        "identityStoreId": str,
        "jobId": str,
        "membershipLevel": MembershipLevelType,
        "principalId": str,
        "principalType": PrincipalTypeType,
        "queueId": str,
    },
)
AssociateMemberToQueueRequestRequestTypeDef = TypedDict(
    "AssociateMemberToQueueRequestRequestTypeDef",
    {
        "farmId": str,
        "identityStoreId": str,
        "membershipLevel": MembershipLevelType,
        "principalId": str,
        "principalType": PrincipalTypeType,
        "queueId": str,
    },
)
AssumeFleetRoleForReadRequestRequestTypeDef = TypedDict(
    "AssumeFleetRoleForReadRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
    },
)
AwsCredentialsTypeDef = TypedDict(
    "AwsCredentialsTypeDef",
    {
        "accessKeyId": str,
        "expiration": datetime,
        "secretAccessKey": str,
        "sessionToken": str,
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
AssumeFleetRoleForWorkerRequestRequestTypeDef = TypedDict(
    "AssumeFleetRoleForWorkerRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "workerId": str,
    },
)
AssumeQueueRoleForReadRequestRequestTypeDef = TypedDict(
    "AssumeQueueRoleForReadRequestRequestTypeDef",
    {
        "farmId": str,
        "queueId": str,
    },
)
AssumeQueueRoleForUserRequestRequestTypeDef = TypedDict(
    "AssumeQueueRoleForUserRequestRequestTypeDef",
    {
        "farmId": str,
        "queueId": str,
    },
)
AssumeQueueRoleForWorkerRequestRequestTypeDef = TypedDict(
    "AssumeQueueRoleForWorkerRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "queueId": str,
        "workerId": str,
    },
)
ManifestPropertiesOutputTypeDef = TypedDict(
    "ManifestPropertiesOutputTypeDef",
    {
        "rootPath": str,
        "rootPathFormat": PathFormatType,
        "fileSystemLocationName": NotRequired[str],
        "inputManifestHash": NotRequired[str],
        "inputManifestPath": NotRequired[str],
        "outputRelativeDirectories": NotRequired[List[str]],
    },
)
ManifestPropertiesTypeDef = TypedDict(
    "ManifestPropertiesTypeDef",
    {
        "rootPath": str,
        "rootPathFormat": PathFormatType,
        "fileSystemLocationName": NotRequired[str],
        "inputManifestHash": NotRequired[str],
        "inputManifestPath": NotRequired[str],
        "outputRelativeDirectories": NotRequired[Sequence[str]],
    },
)
BudgetActionToAddTypeDef = TypedDict(
    "BudgetActionToAddTypeDef",
    {
        "thresholdPercentage": float,
        "type": BudgetActionTypeType,
        "description": NotRequired[str],
    },
)
BudgetActionToRemoveTypeDef = TypedDict(
    "BudgetActionToRemoveTypeDef",
    {
        "thresholdPercentage": float,
        "type": BudgetActionTypeType,
    },
)
FixedBudgetScheduleOutputTypeDef = TypedDict(
    "FixedBudgetScheduleOutputTypeDef",
    {
        "endTime": datetime,
        "startTime": datetime,
    },
)
ConsumedUsagesTypeDef = TypedDict(
    "ConsumedUsagesTypeDef",
    {
        "approximateDollarUsage": float,
    },
)
UsageTrackingResourceTypeDef = TypedDict(
    "UsageTrackingResourceTypeDef",
    {
        "queueId": NotRequired[str],
    },
)
S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "bucketName": str,
        "key": str,
    },
)
CreateFarmRequestRequestTypeDef = TypedDict(
    "CreateFarmRequestRequestTypeDef",
    {
        "displayName": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "kmsKeyArn": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
JobParameterTypeDef = TypedDict(
    "JobParameterTypeDef",
    {
        "float": NotRequired[str],
        "int": NotRequired[str],
        "path": NotRequired[str],
        "string": NotRequired[str],
    },
)
CreateLicenseEndpointRequestRequestTypeDef = TypedDict(
    "CreateLicenseEndpointRequestRequestTypeDef",
    {
        "securityGroupIds": Sequence[str],
        "subnetIds": Sequence[str],
        "vpcId": str,
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
CreateMonitorRequestRequestTypeDef = TypedDict(
    "CreateMonitorRequestRequestTypeDef",
    {
        "displayName": str,
        "identityCenterInstanceArn": str,
        "roleArn": str,
        "subdomain": str,
        "clientToken": NotRequired[str],
    },
)
CreateQueueEnvironmentRequestRequestTypeDef = TypedDict(
    "CreateQueueEnvironmentRequestRequestTypeDef",
    {
        "farmId": str,
        "priority": int,
        "queueId": str,
        "template": str,
        "templateType": EnvironmentTemplateTypeType,
        "clientToken": NotRequired[str],
    },
)
CreateQueueFleetAssociationRequestRequestTypeDef = TypedDict(
    "CreateQueueFleetAssociationRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "queueId": str,
    },
)
JobAttachmentSettingsTypeDef = TypedDict(
    "JobAttachmentSettingsTypeDef",
    {
        "rootPrefix": str,
        "s3BucketName": str,
    },
)
FileSystemLocationTypeDef = TypedDict(
    "FileSystemLocationTypeDef",
    {
        "name": str,
        "path": str,
        "type": FileSystemLocationTypeType,
    },
)
FleetAmountCapabilityTypeDef = TypedDict(
    "FleetAmountCapabilityTypeDef",
    {
        "min": float,
        "name": str,
        "max": NotRequired[float],
    },
)
FleetAttributeCapabilityExtraOutputTypeDef = TypedDict(
    "FleetAttributeCapabilityExtraOutputTypeDef",
    {
        "name": str,
        "values": List[str],
    },
)
MemoryMiBRangeTypeDef = TypedDict(
    "MemoryMiBRangeTypeDef",
    {
        "min": int,
        "max": NotRequired[int],
    },
)
VCpuCountRangeTypeDef = TypedDict(
    "VCpuCountRangeTypeDef",
    {
        "min": int,
        "max": NotRequired[int],
    },
)
FleetAttributeCapabilityOutputTypeDef = TypedDict(
    "FleetAttributeCapabilityOutputTypeDef",
    {
        "name": str,
        "values": List[str],
    },
)
FleetAttributeCapabilityTypeDef = TypedDict(
    "FleetAttributeCapabilityTypeDef",
    {
        "name": str,
        "values": Sequence[str],
    },
)
TimestampTypeDef = Union[datetime, str]
DeleteBudgetRequestRequestTypeDef = TypedDict(
    "DeleteBudgetRequestRequestTypeDef",
    {
        "budgetId": str,
        "farmId": str,
    },
)
DeleteFarmRequestRequestTypeDef = TypedDict(
    "DeleteFarmRequestRequestTypeDef",
    {
        "farmId": str,
    },
)
DeleteFleetRequestRequestTypeDef = TypedDict(
    "DeleteFleetRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "clientToken": NotRequired[str],
    },
)
DeleteLicenseEndpointRequestRequestTypeDef = TypedDict(
    "DeleteLicenseEndpointRequestRequestTypeDef",
    {
        "licenseEndpointId": str,
    },
)
DeleteMeteredProductRequestRequestTypeDef = TypedDict(
    "DeleteMeteredProductRequestRequestTypeDef",
    {
        "licenseEndpointId": str,
        "productId": str,
    },
)
DeleteMonitorRequestRequestTypeDef = TypedDict(
    "DeleteMonitorRequestRequestTypeDef",
    {
        "monitorId": str,
    },
)
DeleteQueueEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteQueueEnvironmentRequestRequestTypeDef",
    {
        "farmId": str,
        "queueEnvironmentId": str,
        "queueId": str,
    },
)
DeleteQueueFleetAssociationRequestRequestTypeDef = TypedDict(
    "DeleteQueueFleetAssociationRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "queueId": str,
    },
)
DeleteQueueRequestRequestTypeDef = TypedDict(
    "DeleteQueueRequestRequestTypeDef",
    {
        "farmId": str,
        "queueId": str,
    },
)
DeleteStorageProfileRequestRequestTypeDef = TypedDict(
    "DeleteStorageProfileRequestRequestTypeDef",
    {
        "farmId": str,
        "storageProfileId": str,
    },
)
DeleteWorkerRequestRequestTypeDef = TypedDict(
    "DeleteWorkerRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "workerId": str,
    },
)
DependencyCountsTypeDef = TypedDict(
    "DependencyCountsTypeDef",
    {
        "consumersResolved": int,
        "consumersUnresolved": int,
        "dependenciesResolved": int,
        "dependenciesUnresolved": int,
    },
)
DisassociateMemberFromFarmRequestRequestTypeDef = TypedDict(
    "DisassociateMemberFromFarmRequestRequestTypeDef",
    {
        "farmId": str,
        "principalId": str,
    },
)
DisassociateMemberFromFleetRequestRequestTypeDef = TypedDict(
    "DisassociateMemberFromFleetRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "principalId": str,
    },
)
DisassociateMemberFromJobRequestRequestTypeDef = TypedDict(
    "DisassociateMemberFromJobRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "principalId": str,
        "queueId": str,
    },
)
DisassociateMemberFromQueueRequestRequestTypeDef = TypedDict(
    "DisassociateMemberFromQueueRequestRequestTypeDef",
    {
        "farmId": str,
        "principalId": str,
        "queueId": str,
    },
)
Ec2EbsVolumeTypeDef = TypedDict(
    "Ec2EbsVolumeTypeDef",
    {
        "iops": NotRequired[int],
        "sizeGiB": NotRequired[int],
        "throughputMiB": NotRequired[int],
    },
)
EnvironmentDetailsEntityTypeDef = TypedDict(
    "EnvironmentDetailsEntityTypeDef",
    {
        "environmentId": str,
        "jobId": str,
        "schemaVersion": str,
        "template": Dict[str, Any],
    },
)
EnvironmentDetailsErrorTypeDef = TypedDict(
    "EnvironmentDetailsErrorTypeDef",
    {
        "code": JobEntityErrorCodeType,
        "environmentId": str,
        "jobId": str,
        "message": str,
    },
)
EnvironmentDetailsIdentifiersTypeDef = TypedDict(
    "EnvironmentDetailsIdentifiersTypeDef",
    {
        "environmentId": str,
        "jobId": str,
    },
)
EnvironmentEnterSessionActionDefinitionSummaryTypeDef = TypedDict(
    "EnvironmentEnterSessionActionDefinitionSummaryTypeDef",
    {
        "environmentId": str,
    },
)
EnvironmentEnterSessionActionDefinitionTypeDef = TypedDict(
    "EnvironmentEnterSessionActionDefinitionTypeDef",
    {
        "environmentId": str,
    },
)
EnvironmentExitSessionActionDefinitionSummaryTypeDef = TypedDict(
    "EnvironmentExitSessionActionDefinitionSummaryTypeDef",
    {
        "environmentId": str,
    },
)
EnvironmentExitSessionActionDefinitionTypeDef = TypedDict(
    "EnvironmentExitSessionActionDefinitionTypeDef",
    {
        "environmentId": str,
    },
)
FarmMemberTypeDef = TypedDict(
    "FarmMemberTypeDef",
    {
        "farmId": str,
        "identityStoreId": str,
        "membershipLevel": MembershipLevelType,
        "principalId": str,
        "principalType": PrincipalTypeType,
    },
)
FarmSummaryTypeDef = TypedDict(
    "FarmSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "displayName": str,
        "farmId": str,
        "kmsKeyArn": NotRequired[str],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
FieldSortExpressionTypeDef = TypedDict(
    "FieldSortExpressionTypeDef",
    {
        "name": str,
        "sortOrder": SortOrderType,
    },
)
FleetMemberTypeDef = TypedDict(
    "FleetMemberTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "identityStoreId": str,
        "membershipLevel": MembershipLevelType,
        "principalId": str,
        "principalType": PrincipalTypeType,
    },
)
GetBudgetRequestRequestTypeDef = TypedDict(
    "GetBudgetRequestRequestTypeDef",
    {
        "budgetId": str,
        "farmId": str,
    },
)
ResponseBudgetActionTypeDef = TypedDict(
    "ResponseBudgetActionTypeDef",
    {
        "thresholdPercentage": float,
        "type": BudgetActionTypeType,
        "description": NotRequired[str],
    },
)
GetFarmRequestRequestTypeDef = TypedDict(
    "GetFarmRequestRequestTypeDef",
    {
        "farmId": str,
    },
)
WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": NotRequired[int],
        "MaxAttempts": NotRequired[int],
    },
)
GetFleetRequestRequestTypeDef = TypedDict(
    "GetFleetRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
    },
)
JobAttachmentDetailsErrorTypeDef = TypedDict(
    "JobAttachmentDetailsErrorTypeDef",
    {
        "code": JobEntityErrorCodeType,
        "jobId": str,
        "message": str,
    },
)
JobDetailsErrorTypeDef = TypedDict(
    "JobDetailsErrorTypeDef",
    {
        "code": JobEntityErrorCodeType,
        "jobId": str,
        "message": str,
    },
)
StepDetailsErrorTypeDef = TypedDict(
    "StepDetailsErrorTypeDef",
    {
        "code": JobEntityErrorCodeType,
        "jobId": str,
        "message": str,
        "stepId": str,
    },
)
GetJobRequestRequestTypeDef = TypedDict(
    "GetJobRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
    },
)
GetLicenseEndpointRequestRequestTypeDef = TypedDict(
    "GetLicenseEndpointRequestRequestTypeDef",
    {
        "licenseEndpointId": str,
    },
)
GetMonitorRequestRequestTypeDef = TypedDict(
    "GetMonitorRequestRequestTypeDef",
    {
        "monitorId": str,
    },
)
GetQueueEnvironmentRequestRequestTypeDef = TypedDict(
    "GetQueueEnvironmentRequestRequestTypeDef",
    {
        "farmId": str,
        "queueEnvironmentId": str,
        "queueId": str,
    },
)
GetQueueFleetAssociationRequestRequestTypeDef = TypedDict(
    "GetQueueFleetAssociationRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "queueId": str,
    },
)
GetQueueRequestRequestTypeDef = TypedDict(
    "GetQueueRequestRequestTypeDef",
    {
        "farmId": str,
        "queueId": str,
    },
)
GetSessionActionRequestRequestTypeDef = TypedDict(
    "GetSessionActionRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "sessionActionId": str,
    },
)
GetSessionRequestRequestTypeDef = TypedDict(
    "GetSessionRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "sessionId": str,
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
GetSessionsStatisticsAggregationRequestRequestTypeDef = TypedDict(
    "GetSessionsStatisticsAggregationRequestRequestTypeDef",
    {
        "aggregationId": str,
        "farmId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
GetStepRequestRequestTypeDef = TypedDict(
    "GetStepRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "stepId": str,
    },
)
GetStorageProfileForQueueRequestRequestTypeDef = TypedDict(
    "GetStorageProfileForQueueRequestRequestTypeDef",
    {
        "farmId": str,
        "queueId": str,
        "storageProfileId": str,
    },
)
GetStorageProfileRequestRequestTypeDef = TypedDict(
    "GetStorageProfileRequestRequestTypeDef",
    {
        "farmId": str,
        "storageProfileId": str,
    },
)
GetTaskRequestRequestTypeDef = TypedDict(
    "GetTaskRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "stepId": str,
        "taskId": str,
    },
)
GetWorkerRequestRequestTypeDef = TypedDict(
    "GetWorkerRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "workerId": str,
    },
)
IpAddressesTypeDef = TypedDict(
    "IpAddressesTypeDef",
    {
        "ipV4Addresses": NotRequired[Sequence[str]],
        "ipV6Addresses": NotRequired[Sequence[str]],
    },
)
IpAddressesOutputTypeDef = TypedDict(
    "IpAddressesOutputTypeDef",
    {
        "ipV4Addresses": NotRequired[List[str]],
        "ipV6Addresses": NotRequired[List[str]],
    },
)
JobAttachmentDetailsIdentifiersTypeDef = TypedDict(
    "JobAttachmentDetailsIdentifiersTypeDef",
    {
        "jobId": str,
    },
)
PathMappingRuleTypeDef = TypedDict(
    "PathMappingRuleTypeDef",
    {
        "destinationPath": str,
        "sourcePath": str,
        "sourcePathFormat": PathFormatType,
    },
)
JobDetailsIdentifiersTypeDef = TypedDict(
    "JobDetailsIdentifiersTypeDef",
    {
        "jobId": str,
    },
)
StepDetailsIdentifiersTypeDef = TypedDict(
    "StepDetailsIdentifiersTypeDef",
    {
        "jobId": str,
        "stepId": str,
    },
)
StepDetailsEntityTypeDef = TypedDict(
    "StepDetailsEntityTypeDef",
    {
        "dependencies": List[str],
        "jobId": str,
        "schemaVersion": str,
        "stepId": str,
        "template": Dict[str, Any],
    },
)
JobMemberTypeDef = TypedDict(
    "JobMemberTypeDef",
    {
        "farmId": str,
        "identityStoreId": str,
        "jobId": str,
        "membershipLevel": MembershipLevelType,
        "principalId": str,
        "principalType": PrincipalTypeType,
        "queueId": str,
    },
)
PosixUserTypeDef = TypedDict(
    "PosixUserTypeDef",
    {
        "group": str,
        "user": str,
    },
)
WindowsUserTypeDef = TypedDict(
    "WindowsUserTypeDef",
    {
        "passwordArn": str,
        "user": str,
    },
)
JobSummaryTypeDef = TypedDict(
    "JobSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "jobId": str,
        "lifecycleStatus": JobLifecycleStatusType,
        "lifecycleStatusMessage": str,
        "name": str,
        "priority": int,
        "endedAt": NotRequired[datetime],
        "maxFailedTasksCount": NotRequired[int],
        "maxRetriesPerTask": NotRequired[int],
        "startedAt": NotRequired[datetime],
        "targetTaskRunStatus": NotRequired[JobTargetTaskRunStatusType],
        "taskRunStatus": NotRequired[TaskRunStatusType],
        "taskRunStatusCounts": NotRequired[Dict[TaskRunStatusType, int]],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
LicenseEndpointSummaryTypeDef = TypedDict(
    "LicenseEndpointSummaryTypeDef",
    {
        "licenseEndpointId": NotRequired[str],
        "status": NotRequired[LicenseEndpointStatusType],
        "statusMessage": NotRequired[str],
        "vpcId": NotRequired[str],
    },
)
ListAvailableMeteredProductsRequestRequestTypeDef = TypedDict(
    "ListAvailableMeteredProductsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
MeteredProductSummaryTypeDef = TypedDict(
    "MeteredProductSummaryTypeDef",
    {
        "family": str,
        "port": int,
        "productId": str,
        "vendor": str,
    },
)
ListBudgetsRequestRequestTypeDef = TypedDict(
    "ListBudgetsRequestRequestTypeDef",
    {
        "farmId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "status": NotRequired[BudgetStatusType],
    },
)
ListFarmMembersRequestRequestTypeDef = TypedDict(
    "ListFarmMembersRequestRequestTypeDef",
    {
        "farmId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListFarmsRequestRequestTypeDef = TypedDict(
    "ListFarmsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "principalId": NotRequired[str],
    },
)
ListFleetMembersRequestRequestTypeDef = TypedDict(
    "ListFleetMembersRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListFleetsRequestRequestTypeDef = TypedDict(
    "ListFleetsRequestRequestTypeDef",
    {
        "farmId": str,
        "displayName": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "principalId": NotRequired[str],
        "status": NotRequired[FleetStatusType],
    },
)
ListJobMembersRequestRequestTypeDef = TypedDict(
    "ListJobMembersRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListJobsRequestRequestTypeDef = TypedDict(
    "ListJobsRequestRequestTypeDef",
    {
        "farmId": str,
        "queueId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "principalId": NotRequired[str],
    },
)
ListLicenseEndpointsRequestRequestTypeDef = TypedDict(
    "ListLicenseEndpointsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListMeteredProductsRequestRequestTypeDef = TypedDict(
    "ListMeteredProductsRequestRequestTypeDef",
    {
        "licenseEndpointId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListMonitorsRequestRequestTypeDef = TypedDict(
    "ListMonitorsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
MonitorSummaryTypeDef = TypedDict(
    "MonitorSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "displayName": str,
        "identityCenterApplicationArn": str,
        "identityCenterInstanceArn": str,
        "monitorId": str,
        "roleArn": str,
        "subdomain": str,
        "url": str,
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
ListQueueEnvironmentsRequestRequestTypeDef = TypedDict(
    "ListQueueEnvironmentsRequestRequestTypeDef",
    {
        "farmId": str,
        "queueId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
QueueEnvironmentSummaryTypeDef = TypedDict(
    "QueueEnvironmentSummaryTypeDef",
    {
        "name": str,
        "priority": int,
        "queueEnvironmentId": str,
    },
)
ListQueueFleetAssociationsRequestRequestTypeDef = TypedDict(
    "ListQueueFleetAssociationsRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "queueId": NotRequired[str],
    },
)
QueueFleetAssociationSummaryTypeDef = TypedDict(
    "QueueFleetAssociationSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "fleetId": str,
        "queueId": str,
        "status": QueueFleetAssociationStatusType,
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
ListQueueMembersRequestRequestTypeDef = TypedDict(
    "ListQueueMembersRequestRequestTypeDef",
    {
        "farmId": str,
        "queueId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
QueueMemberTypeDef = TypedDict(
    "QueueMemberTypeDef",
    {
        "farmId": str,
        "identityStoreId": str,
        "membershipLevel": MembershipLevelType,
        "principalId": str,
        "principalType": PrincipalTypeType,
        "queueId": str,
    },
)
ListQueuesRequestRequestTypeDef = TypedDict(
    "ListQueuesRequestRequestTypeDef",
    {
        "farmId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "principalId": NotRequired[str],
        "status": NotRequired[QueueStatusType],
    },
)
QueueSummaryTypeDef = TypedDict(
    "QueueSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "defaultBudgetAction": DefaultQueueBudgetActionType,
        "displayName": str,
        "farmId": str,
        "queueId": str,
        "status": QueueStatusType,
        "blockedReason": NotRequired[QueueBlockedReasonType],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
ListSessionActionsRequestRequestTypeDef = TypedDict(
    "ListSessionActionsRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "sessionId": NotRequired[str],
        "taskId": NotRequired[str],
    },
)
ListSessionsForWorkerRequestRequestTypeDef = TypedDict(
    "ListSessionsForWorkerRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "workerId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
WorkerSessionSummaryTypeDef = TypedDict(
    "WorkerSessionSummaryTypeDef",
    {
        "jobId": str,
        "lifecycleStatus": SessionLifecycleStatusType,
        "queueId": str,
        "sessionId": str,
        "startedAt": datetime,
        "endedAt": NotRequired[datetime],
        "targetLifecycleStatus": NotRequired[Literal["ENDED"]],
    },
)
ListSessionsRequestRequestTypeDef = TypedDict(
    "ListSessionsRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
SessionSummaryTypeDef = TypedDict(
    "SessionSummaryTypeDef",
    {
        "fleetId": str,
        "lifecycleStatus": SessionLifecycleStatusType,
        "sessionId": str,
        "startedAt": datetime,
        "workerId": str,
        "endedAt": NotRequired[datetime],
        "targetLifecycleStatus": NotRequired[Literal["ENDED"]],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
ListStepConsumersRequestRequestTypeDef = TypedDict(
    "ListStepConsumersRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "stepId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
StepConsumerTypeDef = TypedDict(
    "StepConsumerTypeDef",
    {
        "status": DependencyConsumerResolutionStatusType,
        "stepId": str,
    },
)
ListStepDependenciesRequestRequestTypeDef = TypedDict(
    "ListStepDependenciesRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "stepId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
StepDependencyTypeDef = TypedDict(
    "StepDependencyTypeDef",
    {
        "status": DependencyConsumerResolutionStatusType,
        "stepId": str,
    },
)
ListStepsRequestRequestTypeDef = TypedDict(
    "ListStepsRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListStorageProfilesForQueueRequestRequestTypeDef = TypedDict(
    "ListStorageProfilesForQueueRequestRequestTypeDef",
    {
        "farmId": str,
        "queueId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
StorageProfileSummaryTypeDef = TypedDict(
    "StorageProfileSummaryTypeDef",
    {
        "displayName": str,
        "osFamily": StorageProfileOperatingSystemFamilyType,
        "storageProfileId": str,
    },
)
ListStorageProfilesRequestRequestTypeDef = TypedDict(
    "ListStorageProfilesRequestRequestTypeDef",
    {
        "farmId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
ListTasksRequestRequestTypeDef = TypedDict(
    "ListTasksRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "stepId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListWorkersRequestRequestTypeDef = TypedDict(
    "ListWorkersRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ParameterFilterExpressionTypeDef = TypedDict(
    "ParameterFilterExpressionTypeDef",
    {
        "name": str,
        "operator": ComparisonOperatorType,
        "value": str,
    },
)
ParameterSortExpressionTypeDef = TypedDict(
    "ParameterSortExpressionTypeDef",
    {
        "name": str,
        "sortOrder": SortOrderType,
    },
)
StepParameterTypeDef = TypedDict(
    "StepParameterTypeDef",
    {
        "name": str,
        "type": StepParameterTypeType,
    },
)
PutMeteredProductRequestRequestTypeDef = TypedDict(
    "PutMeteredProductRequestRequestTypeDef",
    {
        "licenseEndpointId": str,
        "productId": str,
    },
)
SearchTermFilterExpressionTypeDef = TypedDict(
    "SearchTermFilterExpressionTypeDef",
    {
        "searchTerm": str,
    },
)
StringFilterExpressionTypeDef = TypedDict(
    "StringFilterExpressionTypeDef",
    {
        "name": str,
        "operator": ComparisonOperatorType,
        "value": str,
    },
)
SearchGroupedFilterExpressionsTypeDef = TypedDict(
    "SearchGroupedFilterExpressionsTypeDef",
    {
        "filters": Sequence["SearchFilterExpressionTypeDef"],
        "operator": LogicalOperatorType,
    },
)
UserJobsFirstTypeDef = TypedDict(
    "UserJobsFirstTypeDef",
    {
        "userIdentityId": str,
    },
)
ServiceManagedEc2InstanceMarketOptionsTypeDef = TypedDict(
    "ServiceManagedEc2InstanceMarketOptionsTypeDef",
    {
        "type": Ec2MarketTypeType,
    },
)
SyncInputJobAttachmentsSessionActionDefinitionSummaryTypeDef = TypedDict(
    "SyncInputJobAttachmentsSessionActionDefinitionSummaryTypeDef",
    {
        "stepId": NotRequired[str],
    },
)
TaskRunSessionActionDefinitionSummaryTypeDef = TypedDict(
    "TaskRunSessionActionDefinitionSummaryTypeDef",
    {
        "stepId": str,
        "taskId": str,
    },
)
SyncInputJobAttachmentsSessionActionDefinitionTypeDef = TypedDict(
    "SyncInputJobAttachmentsSessionActionDefinitionTypeDef",
    {
        "stepId": NotRequired[str],
    },
)
SessionsStatisticsResourcesTypeDef = TypedDict(
    "SessionsStatisticsResourcesTypeDef",
    {
        "fleetIds": NotRequired[Sequence[str]],
        "queueIds": NotRequired[Sequence[str]],
    },
)
StatsTypeDef = TypedDict(
    "StatsTypeDef",
    {
        "avg": NotRequired[float],
        "max": NotRequired[float],
        "min": NotRequired[float],
        "sum": NotRequired[float],
    },
)
StepAmountCapabilityTypeDef = TypedDict(
    "StepAmountCapabilityTypeDef",
    {
        "name": str,
        "max": NotRequired[float],
        "min": NotRequired[float],
        "value": NotRequired[float],
    },
)
StepAttributeCapabilityTypeDef = TypedDict(
    "StepAttributeCapabilityTypeDef",
    {
        "name": str,
        "allOf": NotRequired[List[str]],
        "anyOf": NotRequired[List[str]],
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": NotRequired[Mapping[str, str]],
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)
UpdateFarmRequestRequestTypeDef = TypedDict(
    "UpdateFarmRequestRequestTypeDef",
    {
        "farmId": str,
        "description": NotRequired[str],
        "displayName": NotRequired[str],
    },
)
UpdateJobRequestRequestTypeDef = TypedDict(
    "UpdateJobRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "clientToken": NotRequired[str],
        "lifecycleStatus": NotRequired[Literal["ARCHIVED"]],
        "maxFailedTasksCount": NotRequired[int],
        "maxRetriesPerTask": NotRequired[int],
        "priority": NotRequired[int],
        "targetTaskRunStatus": NotRequired[JobTargetTaskRunStatusType],
    },
)
UpdateMonitorRequestRequestTypeDef = TypedDict(
    "UpdateMonitorRequestRequestTypeDef",
    {
        "monitorId": str,
        "displayName": NotRequired[str],
        "roleArn": NotRequired[str],
        "subdomain": NotRequired[str],
    },
)
UpdateQueueEnvironmentRequestRequestTypeDef = TypedDict(
    "UpdateQueueEnvironmentRequestRequestTypeDef",
    {
        "farmId": str,
        "queueEnvironmentId": str,
        "queueId": str,
        "clientToken": NotRequired[str],
        "priority": NotRequired[int],
        "template": NotRequired[str],
        "templateType": NotRequired[EnvironmentTemplateTypeType],
    },
)
UpdateQueueFleetAssociationRequestRequestTypeDef = TypedDict(
    "UpdateQueueFleetAssociationRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "queueId": str,
        "status": UpdateQueueFleetAssociationStatusType,
    },
)
UpdateSessionRequestRequestTypeDef = TypedDict(
    "UpdateSessionRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "sessionId": str,
        "targetLifecycleStatus": Literal["ENDED"],
        "clientToken": NotRequired[str],
    },
)
UpdateStepRequestRequestTypeDef = TypedDict(
    "UpdateStepRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "stepId": str,
        "targetTaskRunStatus": StepTargetTaskRunStatusType,
        "clientToken": NotRequired[str],
    },
)
UpdateTaskRequestRequestTypeDef = TypedDict(
    "UpdateTaskRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "stepId": str,
        "targetRunStatus": TaskTargetRunStatusType,
        "taskId": str,
        "clientToken": NotRequired[str],
    },
)
WorkerAmountCapabilityTypeDef = TypedDict(
    "WorkerAmountCapabilityTypeDef",
    {
        "name": str,
        "value": float,
    },
)
WorkerAttributeCapabilityTypeDef = TypedDict(
    "WorkerAttributeCapabilityTypeDef",
    {
        "name": str,
        "values": Sequence[str],
    },
)
AssignedTaskRunSessionActionDefinitionTypeDef = TypedDict(
    "AssignedTaskRunSessionActionDefinitionTypeDef",
    {
        "parameters": Dict[str, TaskParameterValueTypeDef],
        "stepId": str,
        "taskId": str,
    },
)
TaskRunSessionActionDefinitionTypeDef = TypedDict(
    "TaskRunSessionActionDefinitionTypeDef",
    {
        "parameters": Dict[str, TaskParameterValueTypeDef],
        "stepId": str,
        "taskId": str,
    },
)
TaskSearchSummaryTypeDef = TypedDict(
    "TaskSearchSummaryTypeDef",
    {
        "endedAt": NotRequired[datetime],
        "failureRetryCount": NotRequired[int],
        "jobId": NotRequired[str],
        "parameters": NotRequired[Dict[str, TaskParameterValueTypeDef]],
        "queueId": NotRequired[str],
        "runStatus": NotRequired[TaskRunStatusType],
        "startedAt": NotRequired[datetime],
        "stepId": NotRequired[str],
        "targetRunStatus": NotRequired[TaskTargetRunStatusType],
        "taskId": NotRequired[str],
    },
)
TaskSummaryTypeDef = TypedDict(
    "TaskSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "runStatus": TaskRunStatusType,
        "taskId": str,
        "endedAt": NotRequired[datetime],
        "failureRetryCount": NotRequired[int],
        "latestSessionActionId": NotRequired[str],
        "parameters": NotRequired[Dict[str, TaskParameterValueTypeDef]],
        "startedAt": NotRequired[datetime],
        "targetRunStatus": NotRequired[TaskTargetRunStatusType],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
AssumeFleetRoleForReadResponseTypeDef = TypedDict(
    "AssumeFleetRoleForReadResponseTypeDef",
    {
        "credentials": AwsCredentialsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AssumeFleetRoleForWorkerResponseTypeDef = TypedDict(
    "AssumeFleetRoleForWorkerResponseTypeDef",
    {
        "credentials": AwsCredentialsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AssumeQueueRoleForReadResponseTypeDef = TypedDict(
    "AssumeQueueRoleForReadResponseTypeDef",
    {
        "credentials": AwsCredentialsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AssumeQueueRoleForUserResponseTypeDef = TypedDict(
    "AssumeQueueRoleForUserResponseTypeDef",
    {
        "credentials": AwsCredentialsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AssumeQueueRoleForWorkerResponseTypeDef = TypedDict(
    "AssumeQueueRoleForWorkerResponseTypeDef",
    {
        "credentials": AwsCredentialsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CopyJobTemplateResponseTypeDef = TypedDict(
    "CopyJobTemplateResponseTypeDef",
    {
        "templateType": JobTemplateTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateBudgetResponseTypeDef = TypedDict(
    "CreateBudgetResponseTypeDef",
    {
        "budgetId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateFarmResponseTypeDef = TypedDict(
    "CreateFarmResponseTypeDef",
    {
        "farmId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateFleetResponseTypeDef = TypedDict(
    "CreateFleetResponseTypeDef",
    {
        "fleetId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateJobResponseTypeDef = TypedDict(
    "CreateJobResponseTypeDef",
    {
        "jobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateLicenseEndpointResponseTypeDef = TypedDict(
    "CreateLicenseEndpointResponseTypeDef",
    {
        "licenseEndpointId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateMonitorResponseTypeDef = TypedDict(
    "CreateMonitorResponseTypeDef",
    {
        "identityCenterApplicationArn": str,
        "monitorId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateQueueEnvironmentResponseTypeDef = TypedDict(
    "CreateQueueEnvironmentResponseTypeDef",
    {
        "queueEnvironmentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateQueueResponseTypeDef = TypedDict(
    "CreateQueueResponseTypeDef",
    {
        "queueId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateStorageProfileResponseTypeDef = TypedDict(
    "CreateStorageProfileResponseTypeDef",
    {
        "storageProfileId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateWorkerResponseTypeDef = TypedDict(
    "CreateWorkerResponseTypeDef",
    {
        "workerId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetFarmResponseTypeDef = TypedDict(
    "GetFarmResponseTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "displayName": str,
        "farmId": str,
        "kmsKeyArn": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetLicenseEndpointResponseTypeDef = TypedDict(
    "GetLicenseEndpointResponseTypeDef",
    {
        "dnsName": str,
        "licenseEndpointId": str,
        "securityGroupIds": List[str],
        "status": LicenseEndpointStatusType,
        "statusMessage": str,
        "subnetIds": List[str],
        "vpcId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetMonitorResponseTypeDef = TypedDict(
    "GetMonitorResponseTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "displayName": str,
        "identityCenterApplicationArn": str,
        "identityCenterInstanceArn": str,
        "monitorId": str,
        "roleArn": str,
        "subdomain": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "url": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetQueueEnvironmentResponseTypeDef = TypedDict(
    "GetQueueEnvironmentResponseTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "name": str,
        "priority": int,
        "queueEnvironmentId": str,
        "template": str,
        "templateType": EnvironmentTemplateTypeType,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetQueueFleetAssociationResponseTypeDef = TypedDict(
    "GetQueueFleetAssociationResponseTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "fleetId": str,
        "queueId": str,
        "status": QueueFleetAssociationStatusType,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTaskResponseTypeDef = TypedDict(
    "GetTaskResponseTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "endedAt": datetime,
        "failureRetryCount": int,
        "latestSessionActionId": str,
        "parameters": Dict[str, TaskParameterValueTypeDef],
        "runStatus": TaskRunStatusType,
        "startedAt": datetime,
        "targetRunStatus": TaskTargetRunStatusType,
        "taskId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartSessionsStatisticsAggregationResponseTypeDef = TypedDict(
    "StartSessionsStatisticsAggregationResponseTypeDef",
    {
        "aggregationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateWorkerResponseTypeDef = TypedDict(
    "UpdateWorkerResponseTypeDef",
    {
        "log": LogConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AttachmentsOutputTypeDef = TypedDict(
    "AttachmentsOutputTypeDef",
    {
        "manifests": List[ManifestPropertiesOutputTypeDef],
        "fileSystem": NotRequired[JobAttachmentsFileSystemType],
    },
)
AttachmentsTypeDef = TypedDict(
    "AttachmentsTypeDef",
    {
        "manifests": Sequence[ManifestPropertiesTypeDef],
        "fileSystem": NotRequired[JobAttachmentsFileSystemType],
    },
)
BudgetScheduleOutputTypeDef = TypedDict(
    "BudgetScheduleOutputTypeDef",
    {
        "fixed": NotRequired[FixedBudgetScheduleOutputTypeDef],
    },
)
BudgetSummaryTypeDef = TypedDict(
    "BudgetSummaryTypeDef",
    {
        "approximateDollarLimit": float,
        "budgetId": str,
        "createdAt": datetime,
        "createdBy": str,
        "displayName": str,
        "status": BudgetStatusType,
        "usageTrackingResource": UsageTrackingResourceTypeDef,
        "usages": ConsumedUsagesTypeDef,
        "description": NotRequired[str],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
CopyJobTemplateRequestRequestTypeDef = TypedDict(
    "CopyJobTemplateRequestRequestTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "targetS3Location": S3LocationTypeDef,
    },
)
JobSearchSummaryTypeDef = TypedDict(
    "JobSearchSummaryTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "endedAt": NotRequired[datetime],
        "jobId": NotRequired[str],
        "jobParameters": NotRequired[Dict[str, JobParameterTypeDef]],
        "lifecycleStatus": NotRequired[JobLifecycleStatusType],
        "lifecycleStatusMessage": NotRequired[str],
        "maxFailedTasksCount": NotRequired[int],
        "maxRetriesPerTask": NotRequired[int],
        "name": NotRequired[str],
        "priority": NotRequired[int],
        "queueId": NotRequired[str],
        "startedAt": NotRequired[datetime],
        "targetTaskRunStatus": NotRequired[JobTargetTaskRunStatusType],
        "taskRunStatus": NotRequired[TaskRunStatusType],
        "taskRunStatusCounts": NotRequired[Dict[TaskRunStatusType, int]],
    },
)
CreateStorageProfileRequestRequestTypeDef = TypedDict(
    "CreateStorageProfileRequestRequestTypeDef",
    {
        "displayName": str,
        "farmId": str,
        "osFamily": StorageProfileOperatingSystemFamilyType,
        "clientToken": NotRequired[str],
        "fileSystemLocations": NotRequired[Sequence[FileSystemLocationTypeDef]],
    },
)
GetStorageProfileForQueueResponseTypeDef = TypedDict(
    "GetStorageProfileForQueueResponseTypeDef",
    {
        "displayName": str,
        "fileSystemLocations": List[FileSystemLocationTypeDef],
        "osFamily": StorageProfileOperatingSystemFamilyType,
        "storageProfileId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStorageProfileResponseTypeDef = TypedDict(
    "GetStorageProfileResponseTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "displayName": str,
        "fileSystemLocations": List[FileSystemLocationTypeDef],
        "osFamily": StorageProfileOperatingSystemFamilyType,
        "storageProfileId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateStorageProfileRequestRequestTypeDef = TypedDict(
    "UpdateStorageProfileRequestRequestTypeDef",
    {
        "farmId": str,
        "storageProfileId": str,
        "clientToken": NotRequired[str],
        "displayName": NotRequired[str],
        "fileSystemLocationsToAdd": NotRequired[Sequence[FileSystemLocationTypeDef]],
        "fileSystemLocationsToRemove": NotRequired[Sequence[FileSystemLocationTypeDef]],
        "osFamily": NotRequired[StorageProfileOperatingSystemFamilyType],
    },
)
CustomerManagedWorkerCapabilitiesExtraOutputTypeDef = TypedDict(
    "CustomerManagedWorkerCapabilitiesExtraOutputTypeDef",
    {
        "cpuArchitectureType": CpuArchitectureTypeType,
        "memoryMiB": MemoryMiBRangeTypeDef,
        "osFamily": CustomerManagedFleetOperatingSystemFamilyType,
        "vCpuCount": VCpuCountRangeTypeDef,
        "acceleratorCount": NotRequired[AcceleratorCountRangeTypeDef],
        "acceleratorTotalMemoryMiB": NotRequired[AcceleratorTotalMemoryMiBRangeTypeDef],
        "acceleratorTypes": NotRequired[List[Literal["gpu"]]],
        "customAmounts": NotRequired[List[FleetAmountCapabilityTypeDef]],
        "customAttributes": NotRequired[List[FleetAttributeCapabilityExtraOutputTypeDef]],
    },
)
CustomerManagedWorkerCapabilitiesOutputTypeDef = TypedDict(
    "CustomerManagedWorkerCapabilitiesOutputTypeDef",
    {
        "cpuArchitectureType": CpuArchitectureTypeType,
        "memoryMiB": MemoryMiBRangeTypeDef,
        "osFamily": CustomerManagedFleetOperatingSystemFamilyType,
        "vCpuCount": VCpuCountRangeTypeDef,
        "acceleratorCount": NotRequired[AcceleratorCountRangeTypeDef],
        "acceleratorTotalMemoryMiB": NotRequired[AcceleratorTotalMemoryMiBRangeTypeDef],
        "acceleratorTypes": NotRequired[List[Literal["gpu"]]],
        "customAmounts": NotRequired[List[FleetAmountCapabilityTypeDef]],
        "customAttributes": NotRequired[List[FleetAttributeCapabilityOutputTypeDef]],
    },
)
FleetCapabilitiesTypeDef = TypedDict(
    "FleetCapabilitiesTypeDef",
    {
        "amounts": NotRequired[List[FleetAmountCapabilityTypeDef]],
        "attributes": NotRequired[List[FleetAttributeCapabilityOutputTypeDef]],
    },
)
CustomerManagedWorkerCapabilitiesTypeDef = TypedDict(
    "CustomerManagedWorkerCapabilitiesTypeDef",
    {
        "cpuArchitectureType": CpuArchitectureTypeType,
        "memoryMiB": MemoryMiBRangeTypeDef,
        "osFamily": CustomerManagedFleetOperatingSystemFamilyType,
        "vCpuCount": VCpuCountRangeTypeDef,
        "acceleratorCount": NotRequired[AcceleratorCountRangeTypeDef],
        "acceleratorTotalMemoryMiB": NotRequired[AcceleratorTotalMemoryMiBRangeTypeDef],
        "acceleratorTypes": NotRequired[Sequence[Literal["gpu"]]],
        "customAmounts": NotRequired[Sequence[FleetAmountCapabilityTypeDef]],
        "customAttributes": NotRequired[Sequence[FleetAttributeCapabilityTypeDef]],
    },
)
DateTimeFilterExpressionTypeDef = TypedDict(
    "DateTimeFilterExpressionTypeDef",
    {
        "dateTime": TimestampTypeDef,
        "name": str,
        "operator": ComparisonOperatorType,
    },
)
FixedBudgetScheduleTypeDef = TypedDict(
    "FixedBudgetScheduleTypeDef",
    {
        "endTime": TimestampTypeDef,
        "startTime": TimestampTypeDef,
    },
)
UpdatedSessionActionInfoTypeDef = TypedDict(
    "UpdatedSessionActionInfoTypeDef",
    {
        "completedStatus": NotRequired[CompletedStatusType],
        "endedAt": NotRequired[TimestampTypeDef],
        "processExitCode": NotRequired[int],
        "progressMessage": NotRequired[str],
        "progressPercent": NotRequired[float],
        "startedAt": NotRequired[TimestampTypeDef],
        "updatedAt": NotRequired[TimestampTypeDef],
    },
)
StepSummaryTypeDef = TypedDict(
    "StepSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "lifecycleStatus": StepLifecycleStatusType,
        "name": str,
        "stepId": str,
        "taskRunStatus": TaskRunStatusType,
        "taskRunStatusCounts": Dict[TaskRunStatusType, int],
        "dependencyCounts": NotRequired[DependencyCountsTypeDef],
        "endedAt": NotRequired[datetime],
        "lifecycleStatusMessage": NotRequired[str],
        "startedAt": NotRequired[datetime],
        "targetTaskRunStatus": NotRequired[StepTargetTaskRunStatusType],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
ServiceManagedEc2InstanceCapabilitiesExtraOutputTypeDef = TypedDict(
    "ServiceManagedEc2InstanceCapabilitiesExtraOutputTypeDef",
    {
        "cpuArchitectureType": CpuArchitectureTypeType,
        "memoryMiB": MemoryMiBRangeTypeDef,
        "osFamily": ServiceManagedFleetOperatingSystemFamilyType,
        "vCpuCount": VCpuCountRangeTypeDef,
        "allowedInstanceTypes": NotRequired[List[str]],
        "customAmounts": NotRequired[List[FleetAmountCapabilityTypeDef]],
        "customAttributes": NotRequired[List[FleetAttributeCapabilityExtraOutputTypeDef]],
        "excludedInstanceTypes": NotRequired[List[str]],
        "rootEbsVolume": NotRequired[Ec2EbsVolumeTypeDef],
    },
)
ServiceManagedEc2InstanceCapabilitiesOutputTypeDef = TypedDict(
    "ServiceManagedEc2InstanceCapabilitiesOutputTypeDef",
    {
        "cpuArchitectureType": CpuArchitectureTypeType,
        "memoryMiB": MemoryMiBRangeTypeDef,
        "osFamily": ServiceManagedFleetOperatingSystemFamilyType,
        "vCpuCount": VCpuCountRangeTypeDef,
        "allowedInstanceTypes": NotRequired[List[str]],
        "customAmounts": NotRequired[List[FleetAmountCapabilityTypeDef]],
        "customAttributes": NotRequired[List[FleetAttributeCapabilityOutputTypeDef]],
        "excludedInstanceTypes": NotRequired[List[str]],
        "rootEbsVolume": NotRequired[Ec2EbsVolumeTypeDef],
    },
)
ServiceManagedEc2InstanceCapabilitiesTypeDef = TypedDict(
    "ServiceManagedEc2InstanceCapabilitiesTypeDef",
    {
        "cpuArchitectureType": CpuArchitectureTypeType,
        "memoryMiB": MemoryMiBRangeTypeDef,
        "osFamily": ServiceManagedFleetOperatingSystemFamilyType,
        "vCpuCount": VCpuCountRangeTypeDef,
        "allowedInstanceTypes": NotRequired[Sequence[str]],
        "customAmounts": NotRequired[Sequence[FleetAmountCapabilityTypeDef]],
        "customAttributes": NotRequired[Sequence[FleetAttributeCapabilityTypeDef]],
        "excludedInstanceTypes": NotRequired[Sequence[str]],
        "rootEbsVolume": NotRequired[Ec2EbsVolumeTypeDef],
    },
)
ListFarmMembersResponseTypeDef = TypedDict(
    "ListFarmMembersResponseTypeDef",
    {
        "members": List[FarmMemberTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFarmsResponseTypeDef = TypedDict(
    "ListFarmsResponseTypeDef",
    {
        "farms": List[FarmSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFleetMembersResponseTypeDef = TypedDict(
    "ListFleetMembersResponseTypeDef",
    {
        "members": List[FleetMemberTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetFleetRequestFleetActiveWaitTypeDef = TypedDict(
    "GetFleetRequestFleetActiveWaitTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetJobRequestJobCreateCompleteWaitTypeDef = TypedDict(
    "GetJobRequestJobCreateCompleteWaitTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetLicenseEndpointRequestLicenseEndpointDeletedWaitTypeDef = TypedDict(
    "GetLicenseEndpointRequestLicenseEndpointDeletedWaitTypeDef",
    {
        "licenseEndpointId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetLicenseEndpointRequestLicenseEndpointValidWaitTypeDef = TypedDict(
    "GetLicenseEndpointRequestLicenseEndpointValidWaitTypeDef",
    {
        "licenseEndpointId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetQueueFleetAssociationRequestQueueFleetAssociationStoppedWaitTypeDef = TypedDict(
    "GetQueueFleetAssociationRequestQueueFleetAssociationStoppedWaitTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "queueId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetQueueRequestQueueSchedulingBlockedWaitTypeDef = TypedDict(
    "GetQueueRequestQueueSchedulingBlockedWaitTypeDef",
    {
        "farmId": str,
        "queueId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetQueueRequestQueueSchedulingWaitTypeDef = TypedDict(
    "GetQueueRequestQueueSchedulingWaitTypeDef",
    {
        "farmId": str,
        "queueId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetJobEntityErrorTypeDef = TypedDict(
    "GetJobEntityErrorTypeDef",
    {
        "environmentDetails": NotRequired[EnvironmentDetailsErrorTypeDef],
        "jobAttachmentDetails": NotRequired[JobAttachmentDetailsErrorTypeDef],
        "jobDetails": NotRequired[JobDetailsErrorTypeDef],
        "stepDetails": NotRequired[StepDetailsErrorTypeDef],
    },
)
GetSessionsStatisticsAggregationRequestGetSessionsStatisticsAggregationPaginateTypeDef = TypedDict(
    "GetSessionsStatisticsAggregationRequestGetSessionsStatisticsAggregationPaginateTypeDef",
    {
        "aggregationId": str,
        "farmId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAvailableMeteredProductsRequestListAvailableMeteredProductsPaginateTypeDef = TypedDict(
    "ListAvailableMeteredProductsRequestListAvailableMeteredProductsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListBudgetsRequestListBudgetsPaginateTypeDef = TypedDict(
    "ListBudgetsRequestListBudgetsPaginateTypeDef",
    {
        "farmId": str,
        "status": NotRequired[BudgetStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListFarmMembersRequestListFarmMembersPaginateTypeDef = TypedDict(
    "ListFarmMembersRequestListFarmMembersPaginateTypeDef",
    {
        "farmId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListFarmsRequestListFarmsPaginateTypeDef = TypedDict(
    "ListFarmsRequestListFarmsPaginateTypeDef",
    {
        "principalId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListFleetMembersRequestListFleetMembersPaginateTypeDef = TypedDict(
    "ListFleetMembersRequestListFleetMembersPaginateTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListFleetsRequestListFleetsPaginateTypeDef = TypedDict(
    "ListFleetsRequestListFleetsPaginateTypeDef",
    {
        "farmId": str,
        "displayName": NotRequired[str],
        "principalId": NotRequired[str],
        "status": NotRequired[FleetStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListJobMembersRequestListJobMembersPaginateTypeDef = TypedDict(
    "ListJobMembersRequestListJobMembersPaginateTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "ListJobsRequestListJobsPaginateTypeDef",
    {
        "farmId": str,
        "queueId": str,
        "principalId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListLicenseEndpointsRequestListLicenseEndpointsPaginateTypeDef = TypedDict(
    "ListLicenseEndpointsRequestListLicenseEndpointsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListMeteredProductsRequestListMeteredProductsPaginateTypeDef = TypedDict(
    "ListMeteredProductsRequestListMeteredProductsPaginateTypeDef",
    {
        "licenseEndpointId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListMonitorsRequestListMonitorsPaginateTypeDef = TypedDict(
    "ListMonitorsRequestListMonitorsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListQueueEnvironmentsRequestListQueueEnvironmentsPaginateTypeDef = TypedDict(
    "ListQueueEnvironmentsRequestListQueueEnvironmentsPaginateTypeDef",
    {
        "farmId": str,
        "queueId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListQueueFleetAssociationsRequestListQueueFleetAssociationsPaginateTypeDef = TypedDict(
    "ListQueueFleetAssociationsRequestListQueueFleetAssociationsPaginateTypeDef",
    {
        "farmId": str,
        "fleetId": NotRequired[str],
        "queueId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListQueueMembersRequestListQueueMembersPaginateTypeDef = TypedDict(
    "ListQueueMembersRequestListQueueMembersPaginateTypeDef",
    {
        "farmId": str,
        "queueId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListQueuesRequestListQueuesPaginateTypeDef = TypedDict(
    "ListQueuesRequestListQueuesPaginateTypeDef",
    {
        "farmId": str,
        "principalId": NotRequired[str],
        "status": NotRequired[QueueStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSessionActionsRequestListSessionActionsPaginateTypeDef = TypedDict(
    "ListSessionActionsRequestListSessionActionsPaginateTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "sessionId": NotRequired[str],
        "taskId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSessionsForWorkerRequestListSessionsForWorkerPaginateTypeDef = TypedDict(
    "ListSessionsForWorkerRequestListSessionsForWorkerPaginateTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "workerId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSessionsRequestListSessionsPaginateTypeDef = TypedDict(
    "ListSessionsRequestListSessionsPaginateTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListStepConsumersRequestListStepConsumersPaginateTypeDef = TypedDict(
    "ListStepConsumersRequestListStepConsumersPaginateTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "stepId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListStepDependenciesRequestListStepDependenciesPaginateTypeDef = TypedDict(
    "ListStepDependenciesRequestListStepDependenciesPaginateTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "stepId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListStepsRequestListStepsPaginateTypeDef = TypedDict(
    "ListStepsRequestListStepsPaginateTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListStorageProfilesForQueueRequestListStorageProfilesForQueuePaginateTypeDef = TypedDict(
    "ListStorageProfilesForQueueRequestListStorageProfilesForQueuePaginateTypeDef",
    {
        "farmId": str,
        "queueId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListStorageProfilesRequestListStorageProfilesPaginateTypeDef = TypedDict(
    "ListStorageProfilesRequestListStorageProfilesPaginateTypeDef",
    {
        "farmId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTasksRequestListTasksPaginateTypeDef = TypedDict(
    "ListTasksRequestListTasksPaginateTypeDef",
    {
        "farmId": str,
        "jobId": str,
        "queueId": str,
        "stepId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListWorkersRequestListWorkersPaginateTypeDef = TypedDict(
    "ListWorkersRequestListWorkersPaginateTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
HostPropertiesRequestTypeDef = TypedDict(
    "HostPropertiesRequestTypeDef",
    {
        "hostName": NotRequired[str],
        "ipAddresses": NotRequired[IpAddressesTypeDef],
    },
)
HostPropertiesResponseTypeDef = TypedDict(
    "HostPropertiesResponseTypeDef",
    {
        "ec2InstanceArn": NotRequired[str],
        "ec2InstanceType": NotRequired[str],
        "hostName": NotRequired[str],
        "ipAddresses": NotRequired[IpAddressesOutputTypeDef],
    },
)
JobEntityIdentifiersUnionTypeDef = TypedDict(
    "JobEntityIdentifiersUnionTypeDef",
    {
        "environmentDetails": NotRequired[EnvironmentDetailsIdentifiersTypeDef],
        "jobAttachmentDetails": NotRequired[JobAttachmentDetailsIdentifiersTypeDef],
        "jobDetails": NotRequired[JobDetailsIdentifiersTypeDef],
        "stepDetails": NotRequired[StepDetailsIdentifiersTypeDef],
    },
)
ListJobMembersResponseTypeDef = TypedDict(
    "ListJobMembersResponseTypeDef",
    {
        "members": List[JobMemberTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
JobRunAsUserTypeDef = TypedDict(
    "JobRunAsUserTypeDef",
    {
        "runAs": RunAsType,
        "posix": NotRequired[PosixUserTypeDef],
        "windows": NotRequired[WindowsUserTypeDef],
    },
)
ListJobsResponseTypeDef = TypedDict(
    "ListJobsResponseTypeDef",
    {
        "jobs": List[JobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListLicenseEndpointsResponseTypeDef = TypedDict(
    "ListLicenseEndpointsResponseTypeDef",
    {
        "licenseEndpoints": List[LicenseEndpointSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListAvailableMeteredProductsResponseTypeDef = TypedDict(
    "ListAvailableMeteredProductsResponseTypeDef",
    {
        "meteredProducts": List[MeteredProductSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListMeteredProductsResponseTypeDef = TypedDict(
    "ListMeteredProductsResponseTypeDef",
    {
        "meteredProducts": List[MeteredProductSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListMonitorsResponseTypeDef = TypedDict(
    "ListMonitorsResponseTypeDef",
    {
        "monitors": List[MonitorSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListQueueEnvironmentsResponseTypeDef = TypedDict(
    "ListQueueEnvironmentsResponseTypeDef",
    {
        "environments": List[QueueEnvironmentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListQueueFleetAssociationsResponseTypeDef = TypedDict(
    "ListQueueFleetAssociationsResponseTypeDef",
    {
        "nextToken": str,
        "queueFleetAssociations": List[QueueFleetAssociationSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListQueueMembersResponseTypeDef = TypedDict(
    "ListQueueMembersResponseTypeDef",
    {
        "members": List[QueueMemberTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListQueuesResponseTypeDef = TypedDict(
    "ListQueuesResponseTypeDef",
    {
        "nextToken": str,
        "queues": List[QueueSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListSessionsForWorkerResponseTypeDef = TypedDict(
    "ListSessionsForWorkerResponseTypeDef",
    {
        "nextToken": str,
        "sessions": List[WorkerSessionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListSessionsResponseTypeDef = TypedDict(
    "ListSessionsResponseTypeDef",
    {
        "nextToken": str,
        "sessions": List[SessionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListStepConsumersResponseTypeDef = TypedDict(
    "ListStepConsumersResponseTypeDef",
    {
        "consumers": List[StepConsumerTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListStepDependenciesResponseTypeDef = TypedDict(
    "ListStepDependenciesResponseTypeDef",
    {
        "dependencies": List[StepDependencyTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListStorageProfilesForQueueResponseTypeDef = TypedDict(
    "ListStorageProfilesForQueueResponseTypeDef",
    {
        "nextToken": str,
        "storageProfiles": List[StorageProfileSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListStorageProfilesResponseTypeDef = TypedDict(
    "ListStorageProfilesResponseTypeDef",
    {
        "nextToken": str,
        "storageProfiles": List[StorageProfileSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ParameterSpaceTypeDef = TypedDict(
    "ParameterSpaceTypeDef",
    {
        "parameters": List[StepParameterTypeDef],
        "combination": NotRequired[str],
    },
)
SearchSortExpressionTypeDef = TypedDict(
    "SearchSortExpressionTypeDef",
    {
        "fieldSort": NotRequired[FieldSortExpressionTypeDef],
        "parameterSort": NotRequired[ParameterSortExpressionTypeDef],
        "userJobsFirst": NotRequired[UserJobsFirstTypeDef],
    },
)
SessionActionDefinitionSummaryTypeDef = TypedDict(
    "SessionActionDefinitionSummaryTypeDef",
    {
        "envEnter": NotRequired[EnvironmentEnterSessionActionDefinitionSummaryTypeDef],
        "envExit": NotRequired[EnvironmentExitSessionActionDefinitionSummaryTypeDef],
        "syncInputJobAttachments": NotRequired[
            SyncInputJobAttachmentsSessionActionDefinitionSummaryTypeDef
        ],
        "taskRun": NotRequired[TaskRunSessionActionDefinitionSummaryTypeDef],
    },
)
StartSessionsStatisticsAggregationRequestRequestTypeDef = TypedDict(
    "StartSessionsStatisticsAggregationRequestRequestTypeDef",
    {
        "endTime": TimestampTypeDef,
        "farmId": str,
        "groupBy": Sequence[UsageGroupByFieldType],
        "resourceIds": SessionsStatisticsResourcesTypeDef,
        "startTime": TimestampTypeDef,
        "statistics": Sequence[UsageStatisticType],
        "period": NotRequired[PeriodType],
        "timezone": NotRequired[str],
    },
)
StatisticsTypeDef = TypedDict(
    "StatisticsTypeDef",
    {
        "costInUsd": StatsTypeDef,
        "count": int,
        "runtimeInSeconds": StatsTypeDef,
        "aggregationEndTime": NotRequired[datetime],
        "aggregationStartTime": NotRequired[datetime],
        "fleetId": NotRequired[str],
        "instanceType": NotRequired[str],
        "jobId": NotRequired[str],
        "jobName": NotRequired[str],
        "licenseProduct": NotRequired[str],
        "queueId": NotRequired[str],
        "usageType": NotRequired[UsageTypeType],
        "userId": NotRequired[str],
    },
)
StepRequiredCapabilitiesTypeDef = TypedDict(
    "StepRequiredCapabilitiesTypeDef",
    {
        "amounts": List[StepAmountCapabilityTypeDef],
        "attributes": List[StepAttributeCapabilityTypeDef],
    },
)
WorkerCapabilitiesTypeDef = TypedDict(
    "WorkerCapabilitiesTypeDef",
    {
        "amounts": Sequence[WorkerAmountCapabilityTypeDef],
        "attributes": Sequence[WorkerAttributeCapabilityTypeDef],
    },
)
AssignedSessionActionDefinitionTypeDef = TypedDict(
    "AssignedSessionActionDefinitionTypeDef",
    {
        "envEnter": NotRequired[AssignedEnvironmentEnterSessionActionDefinitionTypeDef],
        "envExit": NotRequired[AssignedEnvironmentExitSessionActionDefinitionTypeDef],
        "syncInputJobAttachments": NotRequired[
            AssignedSyncInputJobAttachmentsSessionActionDefinitionTypeDef
        ],
        "taskRun": NotRequired[AssignedTaskRunSessionActionDefinitionTypeDef],
    },
)
SessionActionDefinitionTypeDef = TypedDict(
    "SessionActionDefinitionTypeDef",
    {
        "envEnter": NotRequired[EnvironmentEnterSessionActionDefinitionTypeDef],
        "envExit": NotRequired[EnvironmentExitSessionActionDefinitionTypeDef],
        "syncInputJobAttachments": NotRequired[
            SyncInputJobAttachmentsSessionActionDefinitionTypeDef
        ],
        "taskRun": NotRequired[TaskRunSessionActionDefinitionTypeDef],
    },
)
SearchTasksResponseTypeDef = TypedDict(
    "SearchTasksResponseTypeDef",
    {
        "nextItemOffset": int,
        "tasks": List[TaskSearchSummaryTypeDef],
        "totalResults": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTasksResponseTypeDef = TypedDict(
    "ListTasksResponseTypeDef",
    {
        "nextToken": str,
        "tasks": List[TaskSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetJobResponseTypeDef = TypedDict(
    "GetJobResponseTypeDef",
    {
        "attachments": AttachmentsOutputTypeDef,
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "endedAt": datetime,
        "jobId": str,
        "lifecycleStatus": JobLifecycleStatusType,
        "lifecycleStatusMessage": str,
        "maxFailedTasksCount": int,
        "maxRetriesPerTask": int,
        "name": str,
        "parameters": Dict[str, JobParameterTypeDef],
        "priority": int,
        "startedAt": datetime,
        "storageProfileId": str,
        "targetTaskRunStatus": JobTargetTaskRunStatusType,
        "taskRunStatus": TaskRunStatusType,
        "taskRunStatusCounts": Dict[TaskRunStatusType, int],
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
JobAttachmentDetailsEntityTypeDef = TypedDict(
    "JobAttachmentDetailsEntityTypeDef",
    {
        "attachments": AttachmentsOutputTypeDef,
        "jobId": str,
    },
)
AttachmentsUnionTypeDef = Union[AttachmentsTypeDef, AttachmentsOutputTypeDef]
CreateJobRequestRequestTypeDef = TypedDict(
    "CreateJobRequestRequestTypeDef",
    {
        "farmId": str,
        "priority": int,
        "queueId": str,
        "template": str,
        "templateType": JobTemplateTypeType,
        "attachments": NotRequired[AttachmentsTypeDef],
        "clientToken": NotRequired[str],
        "maxFailedTasksCount": NotRequired[int],
        "maxRetriesPerTask": NotRequired[int],
        "parameters": NotRequired[Mapping[str, JobParameterTypeDef]],
        "storageProfileId": NotRequired[str],
        "targetTaskRunStatus": NotRequired[CreateJobTargetTaskRunStatusType],
    },
)
GetBudgetResponseTypeDef = TypedDict(
    "GetBudgetResponseTypeDef",
    {
        "actions": List[ResponseBudgetActionTypeDef],
        "approximateDollarLimit": float,
        "budgetId": str,
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "displayName": str,
        "queueStoppedAt": datetime,
        "schedule": BudgetScheduleOutputTypeDef,
        "status": BudgetStatusType,
        "updatedAt": datetime,
        "updatedBy": str,
        "usageTrackingResource": UsageTrackingResourceTypeDef,
        "usages": ConsumedUsagesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListBudgetsResponseTypeDef = TypedDict(
    "ListBudgetsResponseTypeDef",
    {
        "budgets": List[BudgetSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SearchJobsResponseTypeDef = TypedDict(
    "SearchJobsResponseTypeDef",
    {
        "jobs": List[JobSearchSummaryTypeDef],
        "nextItemOffset": int,
        "totalResults": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CustomerManagedFleetConfigurationExtraOutputTypeDef = TypedDict(
    "CustomerManagedFleetConfigurationExtraOutputTypeDef",
    {
        "mode": AutoScalingModeType,
        "workerCapabilities": CustomerManagedWorkerCapabilitiesExtraOutputTypeDef,
        "storageProfileId": NotRequired[str],
    },
)
CustomerManagedFleetConfigurationOutputTypeDef = TypedDict(
    "CustomerManagedFleetConfigurationOutputTypeDef",
    {
        "mode": AutoScalingModeType,
        "workerCapabilities": CustomerManagedWorkerCapabilitiesOutputTypeDef,
        "storageProfileId": NotRequired[str],
    },
)
CustomerManagedFleetConfigurationTypeDef = TypedDict(
    "CustomerManagedFleetConfigurationTypeDef",
    {
        "mode": AutoScalingModeType,
        "workerCapabilities": CustomerManagedWorkerCapabilitiesTypeDef,
        "storageProfileId": NotRequired[str],
    },
)
SearchFilterExpressionTypeDef = TypedDict(
    "SearchFilterExpressionTypeDef",
    {
        "dateTimeFilter": NotRequired[DateTimeFilterExpressionTypeDef],
        "groupFilter": NotRequired[Dict[str, Any]],
        "parameterFilter": NotRequired[ParameterFilterExpressionTypeDef],
        "searchTermFilter": NotRequired[SearchTermFilterExpressionTypeDef],
        "stringFilter": NotRequired[StringFilterExpressionTypeDef],
    },
)
BudgetScheduleTypeDef = TypedDict(
    "BudgetScheduleTypeDef",
    {
        "fixed": NotRequired[FixedBudgetScheduleTypeDef],
    },
)
UpdateWorkerScheduleRequestRequestTypeDef = TypedDict(
    "UpdateWorkerScheduleRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "workerId": str,
        "updatedSessionActions": NotRequired[Mapping[str, UpdatedSessionActionInfoTypeDef]],
    },
)
ListStepsResponseTypeDef = TypedDict(
    "ListStepsResponseTypeDef",
    {
        "nextToken": str,
        "steps": List[StepSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ServiceManagedEc2FleetConfigurationExtraOutputTypeDef = TypedDict(
    "ServiceManagedEc2FleetConfigurationExtraOutputTypeDef",
    {
        "instanceCapabilities": ServiceManagedEc2InstanceCapabilitiesExtraOutputTypeDef,
        "instanceMarketOptions": ServiceManagedEc2InstanceMarketOptionsTypeDef,
    },
)
ServiceManagedEc2FleetConfigurationOutputTypeDef = TypedDict(
    "ServiceManagedEc2FleetConfigurationOutputTypeDef",
    {
        "instanceCapabilities": ServiceManagedEc2InstanceCapabilitiesOutputTypeDef,
        "instanceMarketOptions": ServiceManagedEc2InstanceMarketOptionsTypeDef,
    },
)
ServiceManagedEc2FleetConfigurationTypeDef = TypedDict(
    "ServiceManagedEc2FleetConfigurationTypeDef",
    {
        "instanceCapabilities": ServiceManagedEc2InstanceCapabilitiesTypeDef,
        "instanceMarketOptions": ServiceManagedEc2InstanceMarketOptionsTypeDef,
    },
)
CreateWorkerRequestRequestTypeDef = TypedDict(
    "CreateWorkerRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "clientToken": NotRequired[str],
        "hostProperties": NotRequired[HostPropertiesRequestTypeDef],
    },
)
GetSessionResponseTypeDef = TypedDict(
    "GetSessionResponseTypeDef",
    {
        "endedAt": datetime,
        "fleetId": str,
        "hostProperties": HostPropertiesResponseTypeDef,
        "lifecycleStatus": SessionLifecycleStatusType,
        "log": LogConfigurationTypeDef,
        "sessionId": str,
        "startedAt": datetime,
        "targetLifecycleStatus": Literal["ENDED"],
        "updatedAt": datetime,
        "updatedBy": str,
        "workerId": str,
        "workerLog": LogConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetWorkerResponseTypeDef = TypedDict(
    "GetWorkerResponseTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "farmId": str,
        "fleetId": str,
        "hostProperties": HostPropertiesResponseTypeDef,
        "log": LogConfigurationTypeDef,
        "status": WorkerStatusType,
        "updatedAt": datetime,
        "updatedBy": str,
        "workerId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
WorkerSearchSummaryTypeDef = TypedDict(
    "WorkerSearchSummaryTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "fleetId": NotRequired[str],
        "hostProperties": NotRequired[HostPropertiesResponseTypeDef],
        "status": NotRequired[WorkerStatusType],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
        "workerId": NotRequired[str],
    },
)
WorkerSummaryTypeDef = TypedDict(
    "WorkerSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "farmId": str,
        "fleetId": str,
        "status": WorkerStatusType,
        "workerId": str,
        "hostProperties": NotRequired[HostPropertiesResponseTypeDef],
        "log": NotRequired[LogConfigurationTypeDef],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
BatchGetJobEntityRequestRequestTypeDef = TypedDict(
    "BatchGetJobEntityRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "identifiers": Sequence[JobEntityIdentifiersUnionTypeDef],
        "workerId": str,
    },
)
CreateQueueRequestRequestTypeDef = TypedDict(
    "CreateQueueRequestRequestTypeDef",
    {
        "displayName": str,
        "farmId": str,
        "allowedStorageProfileIds": NotRequired[Sequence[str]],
        "clientToken": NotRequired[str],
        "defaultBudgetAction": NotRequired[DefaultQueueBudgetActionType],
        "description": NotRequired[str],
        "jobAttachmentSettings": NotRequired[JobAttachmentSettingsTypeDef],
        "jobRunAsUser": NotRequired[JobRunAsUserTypeDef],
        "requiredFileSystemLocationNames": NotRequired[Sequence[str]],
        "roleArn": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
GetQueueResponseTypeDef = TypedDict(
    "GetQueueResponseTypeDef",
    {
        "allowedStorageProfileIds": List[str],
        "blockedReason": QueueBlockedReasonType,
        "createdAt": datetime,
        "createdBy": str,
        "defaultBudgetAction": DefaultQueueBudgetActionType,
        "description": str,
        "displayName": str,
        "farmId": str,
        "jobAttachmentSettings": JobAttachmentSettingsTypeDef,
        "jobRunAsUser": JobRunAsUserTypeDef,
        "queueId": str,
        "requiredFileSystemLocationNames": List[str],
        "roleArn": str,
        "status": QueueStatusType,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
JobDetailsEntityTypeDef = TypedDict(
    "JobDetailsEntityTypeDef",
    {
        "jobId": str,
        "logGroupName": str,
        "schemaVersion": str,
        "jobAttachmentSettings": NotRequired[JobAttachmentSettingsTypeDef],
        "jobRunAsUser": NotRequired[JobRunAsUserTypeDef],
        "parameters": NotRequired[Dict[str, JobParameterTypeDef]],
        "pathMappingRules": NotRequired[List[PathMappingRuleTypeDef]],
        "queueRoleArn": NotRequired[str],
    },
)
UpdateQueueRequestRequestTypeDef = TypedDict(
    "UpdateQueueRequestRequestTypeDef",
    {
        "farmId": str,
        "queueId": str,
        "allowedStorageProfileIdsToAdd": NotRequired[Sequence[str]],
        "allowedStorageProfileIdsToRemove": NotRequired[Sequence[str]],
        "clientToken": NotRequired[str],
        "defaultBudgetAction": NotRequired[DefaultQueueBudgetActionType],
        "description": NotRequired[str],
        "displayName": NotRequired[str],
        "jobAttachmentSettings": NotRequired[JobAttachmentSettingsTypeDef],
        "jobRunAsUser": NotRequired[JobRunAsUserTypeDef],
        "requiredFileSystemLocationNamesToAdd": NotRequired[Sequence[str]],
        "requiredFileSystemLocationNamesToRemove": NotRequired[Sequence[str]],
        "roleArn": NotRequired[str],
    },
)
StepSearchSummaryTypeDef = TypedDict(
    "StepSearchSummaryTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "endedAt": NotRequired[datetime],
        "jobId": NotRequired[str],
        "lifecycleStatus": NotRequired[StepLifecycleStatusType],
        "lifecycleStatusMessage": NotRequired[str],
        "name": NotRequired[str],
        "parameterSpace": NotRequired[ParameterSpaceTypeDef],
        "queueId": NotRequired[str],
        "startedAt": NotRequired[datetime],
        "stepId": NotRequired[str],
        "targetTaskRunStatus": NotRequired[StepTargetTaskRunStatusType],
        "taskRunStatus": NotRequired[TaskRunStatusType],
        "taskRunStatusCounts": NotRequired[Dict[TaskRunStatusType, int]],
    },
)
SearchJobsRequestRequestTypeDef = TypedDict(
    "SearchJobsRequestRequestTypeDef",
    {
        "farmId": str,
        "itemOffset": int,
        "queueIds": Sequence[str],
        "filterExpressions": NotRequired["SearchGroupedFilterExpressionsTypeDef"],
        "pageSize": NotRequired[int],
        "sortExpressions": NotRequired[Sequence[SearchSortExpressionTypeDef]],
    },
)
SearchStepsRequestRequestTypeDef = TypedDict(
    "SearchStepsRequestRequestTypeDef",
    {
        "farmId": str,
        "itemOffset": int,
        "queueIds": Sequence[str],
        "filterExpressions": NotRequired["SearchGroupedFilterExpressionsTypeDef"],
        "jobId": NotRequired[str],
        "pageSize": NotRequired[int],
        "sortExpressions": NotRequired[Sequence[SearchSortExpressionTypeDef]],
    },
)
SearchTasksRequestRequestTypeDef = TypedDict(
    "SearchTasksRequestRequestTypeDef",
    {
        "farmId": str,
        "itemOffset": int,
        "queueIds": Sequence[str],
        "filterExpressions": NotRequired["SearchGroupedFilterExpressionsTypeDef"],
        "jobId": NotRequired[str],
        "pageSize": NotRequired[int],
        "sortExpressions": NotRequired[Sequence[SearchSortExpressionTypeDef]],
    },
)
SearchWorkersRequestRequestTypeDef = TypedDict(
    "SearchWorkersRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetIds": Sequence[str],
        "itemOffset": int,
        "filterExpressions": NotRequired["SearchGroupedFilterExpressionsTypeDef"],
        "pageSize": NotRequired[int],
        "sortExpressions": NotRequired[Sequence[SearchSortExpressionTypeDef]],
    },
)
SessionActionSummaryTypeDef = TypedDict(
    "SessionActionSummaryTypeDef",
    {
        "definition": SessionActionDefinitionSummaryTypeDef,
        "sessionActionId": str,
        "status": SessionActionStatusType,
        "endedAt": NotRequired[datetime],
        "progressPercent": NotRequired[float],
        "startedAt": NotRequired[datetime],
        "workerUpdatedAt": NotRequired[datetime],
    },
)
GetSessionsStatisticsAggregationResponseTypeDef = TypedDict(
    "GetSessionsStatisticsAggregationResponseTypeDef",
    {
        "nextToken": str,
        "statistics": List[StatisticsTypeDef],
        "status": SessionsStatisticsAggregationStatusType,
        "statusMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStepResponseTypeDef = TypedDict(
    "GetStepResponseTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "dependencyCounts": DependencyCountsTypeDef,
        "description": str,
        "endedAt": datetime,
        "lifecycleStatus": StepLifecycleStatusType,
        "lifecycleStatusMessage": str,
        "name": str,
        "parameterSpace": ParameterSpaceTypeDef,
        "requiredCapabilities": StepRequiredCapabilitiesTypeDef,
        "startedAt": datetime,
        "stepId": str,
        "targetTaskRunStatus": StepTargetTaskRunStatusType,
        "taskRunStatus": TaskRunStatusType,
        "taskRunStatusCounts": Dict[TaskRunStatusType, int],
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateWorkerRequestRequestTypeDef = TypedDict(
    "UpdateWorkerRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "workerId": str,
        "capabilities": NotRequired[WorkerCapabilitiesTypeDef],
        "hostProperties": NotRequired[HostPropertiesRequestTypeDef],
        "status": NotRequired[UpdatedWorkerStatusType],
    },
)
AssignedSessionActionTypeDef = TypedDict(
    "AssignedSessionActionTypeDef",
    {
        "definition": AssignedSessionActionDefinitionTypeDef,
        "sessionActionId": str,
    },
)
GetSessionActionResponseTypeDef = TypedDict(
    "GetSessionActionResponseTypeDef",
    {
        "definition": SessionActionDefinitionTypeDef,
        "endedAt": datetime,
        "processExitCode": int,
        "progressMessage": str,
        "progressPercent": float,
        "sessionActionId": str,
        "sessionId": str,
        "startedAt": datetime,
        "status": SessionActionStatusType,
        "workerUpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BudgetScheduleUnionTypeDef = Union[BudgetScheduleTypeDef, BudgetScheduleOutputTypeDef]
CreateBudgetRequestRequestTypeDef = TypedDict(
    "CreateBudgetRequestRequestTypeDef",
    {
        "actions": Sequence[BudgetActionToAddTypeDef],
        "approximateDollarLimit": float,
        "displayName": str,
        "farmId": str,
        "schedule": BudgetScheduleTypeDef,
        "usageTrackingResource": UsageTrackingResourceTypeDef,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
    },
)
UpdateBudgetRequestRequestTypeDef = TypedDict(
    "UpdateBudgetRequestRequestTypeDef",
    {
        "budgetId": str,
        "farmId": str,
        "actionsToAdd": NotRequired[Sequence[BudgetActionToAddTypeDef]],
        "actionsToRemove": NotRequired[Sequence[BudgetActionToRemoveTypeDef]],
        "approximateDollarLimit": NotRequired[float],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "displayName": NotRequired[str],
        "schedule": NotRequired[BudgetScheduleTypeDef],
        "status": NotRequired[BudgetStatusType],
    },
)
FleetConfigurationExtraOutputTypeDef = TypedDict(
    "FleetConfigurationExtraOutputTypeDef",
    {
        "customerManaged": NotRequired[CustomerManagedFleetConfigurationExtraOutputTypeDef],
        "serviceManagedEc2": NotRequired[ServiceManagedEc2FleetConfigurationExtraOutputTypeDef],
    },
)
FleetConfigurationOutputTypeDef = TypedDict(
    "FleetConfigurationOutputTypeDef",
    {
        "customerManaged": NotRequired[CustomerManagedFleetConfigurationOutputTypeDef],
        "serviceManagedEc2": NotRequired[ServiceManagedEc2FleetConfigurationOutputTypeDef],
    },
)
FleetConfigurationTypeDef = TypedDict(
    "FleetConfigurationTypeDef",
    {
        "customerManaged": NotRequired[CustomerManagedFleetConfigurationTypeDef],
        "serviceManagedEc2": NotRequired[ServiceManagedEc2FleetConfigurationTypeDef],
    },
)
SearchWorkersResponseTypeDef = TypedDict(
    "SearchWorkersResponseTypeDef",
    {
        "nextItemOffset": int,
        "totalResults": int,
        "workers": List[WorkerSearchSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListWorkersResponseTypeDef = TypedDict(
    "ListWorkersResponseTypeDef",
    {
        "nextToken": str,
        "workers": List[WorkerSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
JobEntityTypeDef = TypedDict(
    "JobEntityTypeDef",
    {
        "environmentDetails": NotRequired[EnvironmentDetailsEntityTypeDef],
        "jobAttachmentDetails": NotRequired[JobAttachmentDetailsEntityTypeDef],
        "jobDetails": NotRequired[JobDetailsEntityTypeDef],
        "stepDetails": NotRequired[StepDetailsEntityTypeDef],
    },
)
SearchStepsResponseTypeDef = TypedDict(
    "SearchStepsResponseTypeDef",
    {
        "nextItemOffset": int,
        "steps": List[StepSearchSummaryTypeDef],
        "totalResults": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListSessionActionsResponseTypeDef = TypedDict(
    "ListSessionActionsResponseTypeDef",
    {
        "nextToken": str,
        "sessionActions": List[SessionActionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AssignedSessionTypeDef = TypedDict(
    "AssignedSessionTypeDef",
    {
        "jobId": str,
        "logConfiguration": LogConfigurationTypeDef,
        "queueId": str,
        "sessionActions": List[AssignedSessionActionTypeDef],
    },
)
FleetSummaryTypeDef = TypedDict(
    "FleetSummaryTypeDef",
    {
        "configuration": FleetConfigurationOutputTypeDef,
        "createdAt": datetime,
        "createdBy": str,
        "displayName": str,
        "farmId": str,
        "fleetId": str,
        "maxWorkerCount": int,
        "minWorkerCount": int,
        "status": FleetStatusType,
        "workerCount": int,
        "autoScalingStatus": NotRequired[AutoScalingStatusType],
        "targetWorkerCount": NotRequired[int],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
GetFleetResponseTypeDef = TypedDict(
    "GetFleetResponseTypeDef",
    {
        "autoScalingStatus": AutoScalingStatusType,
        "capabilities": FleetCapabilitiesTypeDef,
        "configuration": FleetConfigurationOutputTypeDef,
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "displayName": str,
        "farmId": str,
        "fleetId": str,
        "maxWorkerCount": int,
        "minWorkerCount": int,
        "roleArn": str,
        "status": FleetStatusType,
        "targetWorkerCount": int,
        "updatedAt": datetime,
        "updatedBy": str,
        "workerCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateFleetRequestRequestTypeDef = TypedDict(
    "CreateFleetRequestRequestTypeDef",
    {
        "configuration": FleetConfigurationTypeDef,
        "displayName": str,
        "farmId": str,
        "maxWorkerCount": int,
        "roleArn": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "minWorkerCount": NotRequired[int],
        "tags": NotRequired[Mapping[str, str]],
    },
)
FleetConfigurationUnionTypeDef = Union[
    FleetConfigurationTypeDef, FleetConfigurationExtraOutputTypeDef
]
UpdateFleetRequestRequestTypeDef = TypedDict(
    "UpdateFleetRequestRequestTypeDef",
    {
        "farmId": str,
        "fleetId": str,
        "clientToken": NotRequired[str],
        "configuration": NotRequired[FleetConfigurationTypeDef],
        "description": NotRequired[str],
        "displayName": NotRequired[str],
        "maxWorkerCount": NotRequired[int],
        "minWorkerCount": NotRequired[int],
        "roleArn": NotRequired[str],
    },
)
BatchGetJobEntityResponseTypeDef = TypedDict(
    "BatchGetJobEntityResponseTypeDef",
    {
        "entities": List[JobEntityTypeDef],
        "errors": List[GetJobEntityErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateWorkerScheduleResponseTypeDef = TypedDict(
    "UpdateWorkerScheduleResponseTypeDef",
    {
        "assignedSessions": Dict[str, AssignedSessionTypeDef],
        "cancelSessionActions": Dict[str, List[str]],
        "desiredWorkerStatus": Literal["STOPPED"],
        "updateIntervalSeconds": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFleetsResponseTypeDef = TypedDict(
    "ListFleetsResponseTypeDef",
    {
        "fleets": List[FleetSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
