"""
Type annotations for qbusiness service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_qbusiness.client import QBusinessClient

    session = get_session()
    async with session.create_client("qbusiness") as client:
        client: QBusinessClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ChatModeType,
    DataSourceSyncJobStatusType,
    IndexTypeType,
    MembershipTypeType,
    PluginStateType,
    PluginTypeType,
    ResponseScopeType,
    RetrieverTypeType,
    WebExperienceSamplePromptsControlModeType,
)
from .paginator import (
    GetChatControlsConfigurationPaginator,
    ListApplicationsPaginator,
    ListConversationsPaginator,
    ListDataSourcesPaginator,
    ListDataSourceSyncJobsPaginator,
    ListDocumentsPaginator,
    ListGroupsPaginator,
    ListIndicesPaginator,
    ListMessagesPaginator,
    ListPluginsPaginator,
    ListRetrieversPaginator,
    ListWebExperiencesPaginator,
)
from .type_defs import (
    ActionExecutionUnionTypeDef,
    AttachmentInputTypeDef,
    AttachmentsConfigurationTypeDef,
    AttributeFilterTypeDef,
    AuthChallengeResponseTypeDef,
    BatchDeleteDocumentResponseTypeDef,
    BatchPutDocumentResponseTypeDef,
    BlockedPhrasesConfigurationUpdateTypeDef,
    ChatModeConfigurationTypeDef,
    ChatSyncOutputTypeDef,
    CreateApplicationResponseTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateIndexResponseTypeDef,
    CreatePluginResponseTypeDef,
    CreateRetrieverResponseTypeDef,
    CreateWebExperienceResponseTypeDef,
    CreatorModeConfigurationTypeDef,
    CustomPluginConfigurationTypeDef,
    DataSourceVpcConfigurationUnionTypeDef,
    DeleteDocumentTypeDef,
    DocumentAttributeConfigurationTypeDef,
    DocumentEnrichmentConfigurationUnionTypeDef,
    DocumentTypeDef,
    EmptyResponseMetadataTypeDef,
    EncryptionConfigurationTypeDef,
    GetApplicationResponseTypeDef,
    GetChatControlsConfigurationResponseTypeDef,
    GetDataSourceResponseTypeDef,
    GetGroupResponseTypeDef,
    GetIndexResponseTypeDef,
    GetPluginResponseTypeDef,
    GetRetrieverResponseTypeDef,
    GetUserResponseTypeDef,
    GetWebExperienceResponseTypeDef,
    GroupMembersTypeDef,
    IndexCapacityConfigurationTypeDef,
    ListApplicationsResponseTypeDef,
    ListConversationsResponseTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDataSourceSyncJobsResponseTypeDef,
    ListDocumentsResponseTypeDef,
    ListGroupsResponseTypeDef,
    ListIndicesResponseTypeDef,
    ListMessagesResponseTypeDef,
    ListPluginsResponseTypeDef,
    ListRetrieversResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWebExperiencesResponseTypeDef,
    MessageUsefulnessFeedbackTypeDef,
    PluginAuthConfigurationUnionTypeDef,
    RetrieverConfigurationUnionTypeDef,
    StartDataSourceSyncJobResponseTypeDef,
    TagTypeDef,
    TimestampTypeDef,
    TopicConfigurationUnionTypeDef,
    UpdateUserResponseTypeDef,
    UserAliasTypeDef,
    WebExperienceAuthConfigurationTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("QBusinessClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    LicenseNotFoundException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class QBusinessClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        QBusinessClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#exceptions)
        """

    async def batch_delete_document(
        self,
        *,
        applicationId: str,
        indexId: str,
        documents: Sequence[DeleteDocumentTypeDef],
        dataSourceSyncId: str = ...,
    ) -> BatchDeleteDocumentResponseTypeDef:
        """
        Asynchronously deletes one or more documents added using the `BatchPutDocument`
        API from an Amazon Q Business
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.batch_delete_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#batch_delete_document)
        """

    async def batch_put_document(
        self,
        *,
        applicationId: str,
        indexId: str,
        documents: Sequence[DocumentTypeDef],
        roleArn: str = ...,
        dataSourceSyncId: str = ...,
    ) -> BatchPutDocumentResponseTypeDef:
        """
        Adds one or more documents to an Amazon Q Business index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.batch_put_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#batch_put_document)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#can_paginate)
        """

    async def chat_sync(
        self,
        *,
        applicationId: str,
        userId: str = ...,
        userGroups: Sequence[str] = ...,
        userMessage: str = ...,
        attachments: Sequence[AttachmentInputTypeDef] = ...,
        actionExecution: ActionExecutionUnionTypeDef = ...,
        authChallengeResponse: AuthChallengeResponseTypeDef = ...,
        conversationId: str = ...,
        parentMessageId: str = ...,
        attributeFilter: "AttributeFilterTypeDef" = ...,
        chatMode: ChatModeType = ...,
        chatModeConfiguration: ChatModeConfigurationTypeDef = ...,
        clientToken: str = ...,
    ) -> ChatSyncOutputTypeDef:
        """
        Starts or continues a non-streaming Amazon Q Business conversation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.chat_sync)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#chat_sync)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#close)
        """

    async def create_application(
        self,
        *,
        displayName: str,
        roleArn: str = ...,
        identityCenterInstanceArn: str = ...,
        description: str = ...,
        encryptionConfiguration: EncryptionConfigurationTypeDef = ...,
        tags: Sequence[TagTypeDef] = ...,
        clientToken: str = ...,
        attachmentsConfiguration: AttachmentsConfigurationTypeDef = ...,
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates an Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.create_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#create_application)
        """

    async def create_data_source(
        self,
        *,
        applicationId: str,
        indexId: str,
        displayName: str,
        configuration: Mapping[str, Any],
        vpcConfiguration: DataSourceVpcConfigurationUnionTypeDef = ...,
        description: str = ...,
        tags: Sequence[TagTypeDef] = ...,
        syncSchedule: str = ...,
        roleArn: str = ...,
        clientToken: str = ...,
        documentEnrichmentConfiguration: DocumentEnrichmentConfigurationUnionTypeDef = ...,
    ) -> CreateDataSourceResponseTypeDef:
        """
        Creates a data source connector for an Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.create_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#create_data_source)
        """

    async def create_index(
        self,
        *,
        applicationId: str,
        displayName: str,
        type: IndexTypeType = ...,
        description: str = ...,
        tags: Sequence[TagTypeDef] = ...,
        capacityConfiguration: IndexCapacityConfigurationTypeDef = ...,
        clientToken: str = ...,
    ) -> CreateIndexResponseTypeDef:
        """
        Creates an Amazon Q Business index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.create_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#create_index)
        """

    async def create_plugin(
        self,
        *,
        applicationId: str,
        displayName: str,
        type: PluginTypeType,
        authConfiguration: PluginAuthConfigurationUnionTypeDef,
        serverUrl: str = ...,
        customPluginConfiguration: CustomPluginConfigurationTypeDef = ...,
        tags: Sequence[TagTypeDef] = ...,
        clientToken: str = ...,
    ) -> CreatePluginResponseTypeDef:
        """
        Creates an Amazon Q Business plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.create_plugin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#create_plugin)
        """

    async def create_retriever(
        self,
        *,
        applicationId: str,
        type: RetrieverTypeType,
        displayName: str,
        configuration: RetrieverConfigurationUnionTypeDef,
        roleArn: str = ...,
        clientToken: str = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> CreateRetrieverResponseTypeDef:
        """
        Adds a retriever to your Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.create_retriever)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#create_retriever)
        """

    async def create_user(
        self,
        *,
        applicationId: str,
        userId: str,
        userAliases: Sequence[UserAliasTypeDef] = ...,
        clientToken: str = ...,
    ) -> Dict[str, Any]:
        """
        Creates a universally unique identifier (UUID) mapped to a list of local user
        ids within an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#create_user)
        """

    async def create_web_experience(
        self,
        *,
        applicationId: str,
        title: str = ...,
        subtitle: str = ...,
        welcomeMessage: str = ...,
        samplePromptsControlMode: WebExperienceSamplePromptsControlModeType = ...,
        roleArn: str = ...,
        tags: Sequence[TagTypeDef] = ...,
        clientToken: str = ...,
    ) -> CreateWebExperienceResponseTypeDef:
        """
        Creates an Amazon Q Business web experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.create_web_experience)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#create_web_experience)
        """

    async def delete_application(self, *, applicationId: str) -> Dict[str, Any]:
        """
        Deletes an Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.delete_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#delete_application)
        """

    async def delete_chat_controls_configuration(self, *, applicationId: str) -> Dict[str, Any]:
        """
        Deletes chat controls configured for an existing Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.delete_chat_controls_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#delete_chat_controls_configuration)
        """

    async def delete_conversation(
        self, *, conversationId: str, applicationId: str, userId: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Q Business web experience conversation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.delete_conversation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#delete_conversation)
        """

    async def delete_data_source(
        self, *, applicationId: str, indexId: str, dataSourceId: str
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Q Business data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.delete_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#delete_data_source)
        """

    async def delete_group(
        self, *, applicationId: str, indexId: str, groupName: str, dataSourceId: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a group so that all users and sub groups that belong to the group can
        no longer access documents only available to that
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.delete_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#delete_group)
        """

    async def delete_index(self, *, applicationId: str, indexId: str) -> Dict[str, Any]:
        """
        Deletes an Amazon Q Business index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.delete_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#delete_index)
        """

    async def delete_plugin(self, *, applicationId: str, pluginId: str) -> Dict[str, Any]:
        """
        Deletes an Amazon Q Business plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.delete_plugin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#delete_plugin)
        """

    async def delete_retriever(self, *, applicationId: str, retrieverId: str) -> Dict[str, Any]:
        """
        Deletes the retriever used by an Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.delete_retriever)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#delete_retriever)
        """

    async def delete_user(self, *, applicationId: str, userId: str) -> Dict[str, Any]:
        """
        Deletes a user by email id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#delete_user)
        """

    async def delete_web_experience(
        self, *, applicationId: str, webExperienceId: str
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Q Business web experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.delete_web_experience)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#delete_web_experience)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#generate_presigned_url)
        """

    async def get_application(self, *, applicationId: str) -> GetApplicationResponseTypeDef:
        """
        Gets information about an existing Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_application)
        """

    async def get_chat_controls_configuration(
        self, *, applicationId: str, maxResults: int = ..., nextToken: str = ...
    ) -> GetChatControlsConfigurationResponseTypeDef:
        """
        Gets information about an chat controls configured for an existing Amazon Q
        Business
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_chat_controls_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_chat_controls_configuration)
        """

    async def get_data_source(
        self, *, applicationId: str, indexId: str, dataSourceId: str
    ) -> GetDataSourceResponseTypeDef:
        """
        Gets information about an existing Amazon Q Business data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_data_source)
        """

    async def get_group(
        self, *, applicationId: str, indexId: str, groupName: str, dataSourceId: str = ...
    ) -> GetGroupResponseTypeDef:
        """
        Describes a group by group name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_group)
        """

    async def get_index(self, *, applicationId: str, indexId: str) -> GetIndexResponseTypeDef:
        """
        Gets information about an existing Amazon Q Business index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_index)
        """

    async def get_plugin(self, *, applicationId: str, pluginId: str) -> GetPluginResponseTypeDef:
        """
        Gets information about an existing Amazon Q Business plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_plugin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_plugin)
        """

    async def get_retriever(
        self, *, applicationId: str, retrieverId: str
    ) -> GetRetrieverResponseTypeDef:
        """
        Gets information about an existing retriever used by an Amazon Q Business
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_retriever)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_retriever)
        """

    async def get_user(self, *, applicationId: str, userId: str) -> GetUserResponseTypeDef:
        """
        Describes the universally unique identifier (UUID) associated with a local user
        in a data
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_user)
        """

    async def get_web_experience(
        self, *, applicationId: str, webExperienceId: str
    ) -> GetWebExperienceResponseTypeDef:
        """
        Gets information about an existing Amazon Q Business web experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_web_experience)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_web_experience)
        """

    async def list_applications(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists Amazon Q Business applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.list_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#list_applications)
        """

    async def list_conversations(
        self, *, applicationId: str, userId: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> ListConversationsResponseTypeDef:
        """
        Lists one or more Amazon Q Business conversations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.list_conversations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#list_conversations)
        """

    async def list_data_source_sync_jobs(
        self,
        *,
        dataSourceId: str,
        applicationId: str,
        indexId: str,
        nextToken: str = ...,
        maxResults: int = ...,
        startTime: TimestampTypeDef = ...,
        endTime: TimestampTypeDef = ...,
        statusFilter: DataSourceSyncJobStatusType = ...,
    ) -> ListDataSourceSyncJobsResponseTypeDef:
        """
        Get information about an Amazon Q Business data source connector
        synchronization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.list_data_source_sync_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#list_data_source_sync_jobs)
        """

    async def list_data_sources(
        self, *, applicationId: str, indexId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListDataSourcesResponseTypeDef:
        """
        Lists the Amazon Q Business data source connectors that you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.list_data_sources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#list_data_sources)
        """

    async def list_documents(
        self,
        *,
        applicationId: str,
        indexId: str,
        dataSourceIds: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListDocumentsResponseTypeDef:
        """
        A list of documents attached to an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.list_documents)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#list_documents)
        """

    async def list_groups(
        self,
        *,
        applicationId: str,
        indexId: str,
        updatedEarlierThan: TimestampTypeDef,
        dataSourceId: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListGroupsResponseTypeDef:
        """
        Provides a list of groups that are mapped to users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.list_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#list_groups)
        """

    async def list_indices(
        self, *, applicationId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListIndicesResponseTypeDef:
        """
        Lists the Amazon Q Business indices you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.list_indices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#list_indices)
        """

    async def list_messages(
        self,
        *,
        conversationId: str,
        applicationId: str,
        userId: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListMessagesResponseTypeDef:
        """
        Gets a list of messages associated with an Amazon Q Business web experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.list_messages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#list_messages)
        """

    async def list_plugins(
        self, *, applicationId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListPluginsResponseTypeDef:
        """
        Lists configured Amazon Q Business plugins.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.list_plugins)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#list_plugins)
        """

    async def list_retrievers(
        self, *, applicationId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListRetrieversResponseTypeDef:
        """
        Lists the retriever used by an Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.list_retrievers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#list_retrievers)
        """

    async def list_tags_for_resource(
        self, *, resourceARN: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of tags associated with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#list_tags_for_resource)
        """

    async def list_web_experiences(
        self, *, applicationId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListWebExperiencesResponseTypeDef:
        """
        Lists one or more Amazon Q Business Web Experiences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.list_web_experiences)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#list_web_experiences)
        """

    async def put_feedback(
        self,
        *,
        applicationId: str,
        conversationId: str,
        messageId: str,
        userId: str = ...,
        messageCopiedAt: TimestampTypeDef = ...,
        messageUsefulness: MessageUsefulnessFeedbackTypeDef = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables your end user to provide feedback on their Amazon Q Business generated
        chat
        responses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.put_feedback)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#put_feedback)
        """

    async def put_group(
        self,
        *,
        applicationId: str,
        indexId: str,
        groupName: str,
        type: MembershipTypeType,
        groupMembers: GroupMembersTypeDef,
        dataSourceId: str = ...,
    ) -> Dict[str, Any]:
        """
        Create, or updates, a mapping of users—who have access to a document—to groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.put_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#put_group)
        """

    async def start_data_source_sync_job(
        self, *, dataSourceId: str, applicationId: str, indexId: str
    ) -> StartDataSourceSyncJobResponseTypeDef:
        """
        Starts a data source connector synchronization job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.start_data_source_sync_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#start_data_source_sync_job)
        """

    async def stop_data_source_sync_job(
        self, *, dataSourceId: str, applicationId: str, indexId: str
    ) -> Dict[str, Any]:
        """
        Stops an Amazon Q Business data source connector synchronization job already in
        progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.stop_data_source_sync_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#stop_data_source_sync_job)
        """

    async def tag_resource(self, *, resourceARN: str, tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tag to the specified Amazon Q Business application or data
        source
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceARN: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from an Amazon Q Business application or a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#untag_resource)
        """

    async def update_application(
        self,
        *,
        applicationId: str,
        identityCenterInstanceArn: str = ...,
        displayName: str = ...,
        description: str = ...,
        roleArn: str = ...,
        attachmentsConfiguration: AttachmentsConfigurationTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Updates an existing Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.update_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#update_application)
        """

    async def update_chat_controls_configuration(
        self,
        *,
        applicationId: str,
        clientToken: str = ...,
        responseScope: ResponseScopeType = ...,
        blockedPhrasesConfigurationUpdate: BlockedPhrasesConfigurationUpdateTypeDef = ...,
        topicConfigurationsToCreateOrUpdate: Sequence[TopicConfigurationUnionTypeDef] = ...,
        topicConfigurationsToDelete: Sequence[TopicConfigurationUnionTypeDef] = ...,
        creatorModeConfiguration: CreatorModeConfigurationTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Updates an set of chat controls configured for an existing Amazon Q Business
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.update_chat_controls_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#update_chat_controls_configuration)
        """

    async def update_data_source(
        self,
        *,
        applicationId: str,
        indexId: str,
        dataSourceId: str,
        displayName: str = ...,
        configuration: Mapping[str, Any] = ...,
        vpcConfiguration: DataSourceVpcConfigurationUnionTypeDef = ...,
        description: str = ...,
        syncSchedule: str = ...,
        roleArn: str = ...,
        documentEnrichmentConfiguration: DocumentEnrichmentConfigurationUnionTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Updates an existing Amazon Q Business data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.update_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#update_data_source)
        """

    async def update_index(
        self,
        *,
        applicationId: str,
        indexId: str,
        displayName: str = ...,
        description: str = ...,
        capacityConfiguration: IndexCapacityConfigurationTypeDef = ...,
        documentAttributeConfigurations: Sequence[DocumentAttributeConfigurationTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Updates an Amazon Q Business index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.update_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#update_index)
        """

    async def update_plugin(
        self,
        *,
        applicationId: str,
        pluginId: str,
        displayName: str = ...,
        state: PluginStateType = ...,
        serverUrl: str = ...,
        customPluginConfiguration: CustomPluginConfigurationTypeDef = ...,
        authConfiguration: PluginAuthConfigurationUnionTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Updates an Amazon Q Business plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.update_plugin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#update_plugin)
        """

    async def update_retriever(
        self,
        *,
        applicationId: str,
        retrieverId: str,
        configuration: RetrieverConfigurationUnionTypeDef = ...,
        displayName: str = ...,
        roleArn: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates the retriever used for your Amazon Q Business application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.update_retriever)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#update_retriever)
        """

    async def update_user(
        self,
        *,
        applicationId: str,
        userId: str,
        userAliasesToUpdate: Sequence[UserAliasTypeDef] = ...,
        userAliasesToDelete: Sequence[UserAliasTypeDef] = ...,
    ) -> UpdateUserResponseTypeDef:
        """
        Updates a information associated with a user id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.update_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#update_user)
        """

    async def update_web_experience(
        self,
        *,
        applicationId: str,
        webExperienceId: str,
        roleArn: str = ...,
        authenticationConfiguration: WebExperienceAuthConfigurationTypeDef = ...,
        title: str = ...,
        subtitle: str = ...,
        welcomeMessage: str = ...,
        samplePromptsControlMode: WebExperienceSamplePromptsControlModeType = ...,
    ) -> Dict[str, Any]:
        """
        Updates an Amazon Q Business web experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.update_web_experience)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#update_web_experience)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_chat_controls_configuration"]
    ) -> GetChatControlsConfigurationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_conversations"]
    ) -> ListConversationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_source_sync_jobs"]
    ) -> ListDataSourceSyncJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_sources"]
    ) -> ListDataSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_documents"]) -> ListDocumentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_indices"]) -> ListIndicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_messages"]) -> ListMessagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_plugins"]) -> ListPluginsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_retrievers"]) -> ListRetrieversPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_web_experiences"]
    ) -> ListWebExperiencesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/#get_paginator)
        """

    async def __aenter__(self) -> "QBusinessClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness.html#QBusiness.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/client/)
        """
