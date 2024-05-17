from fhir.resources.R4B.fhirtypes import Id, IdentifierType

from kt2.models import (
    KT2ActivityDefinition,
    KT2AuditEvent,
    KT2CareTeam,
    KT2Device,
    KT2Endpoint,
    KT2Organization,
    KT2Patient,
    KT2Practitioner,
    KT2Subscription,
    KT2Task,
)

KT2AuditEventList = list[KT2AuditEvent]
KT2ActivityDefinitionList = list[KT2ActivityDefinition]
KT2CareTeamList = list[KT2CareTeam]
KT2DeviceList = list[KT2Device]
KT2EndpointList = list[KT2Endpoint]
KT2OrganizationList = list[KT2Organization]
KT2PatientList = list[KT2Patient]
KT2PracticionerList = list[KT2Practitioner]
KT2TaskList = list[KT2Task]
KT2SubscriptionList = list[KT2Subscription]
KT2Id = Id
KT2IdentifierType = IdentifierType
