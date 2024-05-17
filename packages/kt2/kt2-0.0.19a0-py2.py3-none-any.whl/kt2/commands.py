import asyncio
import json

import click
from pydantic import BaseModel
from rich import print

from kt2 import __version__ as VERSION
from kt2.client import KoppeltaalSDK
from kt2.helpers import font
from kt2.settings import CommandLineArgs, ConfigFile, load_settings, merge_config
from kt2.types import (
    KT2ActivityDefinitionList,
    KT2AuditEventList,
    KT2CareTeamList,
    KT2EndpointList,
    KT2OrganizationList,
    KT2PatientList,
    KT2PracticionerList,
    KT2SubscriptionList,
    KT2TaskList,
)

# ----------------------------------------------------------------------------
# KoppeltaalAsyncRunner: runs KoppeltaalSDK in aysnc-mode
# ----------------------------------------------------------------------------


def print_json(data):
    print(data)


class JsonResponse(BaseModel):
    __root__: (
        KT2AuditEventList
        | KT2ActivityDefinitionList
        | KT2CareTeamList
        | KT2CareTeamList
        | KT2EndpointList
        | KT2OrganizationList
        | KT2PatientList
        | KT2PracticionerList
        | KT2TaskList
        | KT2SubscriptionList
    )


class KoppeltaalAsyncRunner:
    def __init__(self, config: ConfigFile, debug: bool):
        self.config: ConfigFile = config

        # build SDK
        self.client = KoppeltaalSDK(
            client_name=self.config.client_name,
            fhir_url=self.config.fhir_url,
            oauth_token_url=self.config.oauth_token_url,
            oauth_authorize_url=self.config.oauth_authorize_url,
            smart_config_url=self.config.smart_config_url,
            domain=self.config.domain,
            client_id=self.config.client_id,
            oauth_introspection_token_url=self.config.oauth_introspection_token_url,
            jwks_url=self.config.jwks_url,
            jwks_kid=self.config.jwks_kid,
            jwks_keys=self.config.jwks_keys,
            enable_logger=True,
        )

    async def get_patients(self) -> None:
        """Get all Patient resources from Koppeltaal"""
        response = await self.client.get_patients()
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_patient(self, id: str) -> None:
        """Get single Patient resource from Koppeltaal"""
        response = await self.client.get_patient(id=id)
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_practitioners(self) -> None:
        """Get all Practitioner resources from Koppeltaal"""
        response = await self.client.get_practitioners()
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_practitioner(self, id: str) -> None:
        """Get single Practitioner resource from Koppeltaal"""
        response = await self.client.get_practitioner(id=id)
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_careteams(self) -> None:
        """Get all CareTeam resources from Koppeltaal"""
        response = await self.client.get_careteams()
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_careteam(self, id: str) -> None:
        """Get single CareTeam resource from Koppeltaal"""
        response = await self.client.get_careteam(id=id)
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_audit_events(self) -> None:
        """Get all AuditEvent resources from Koppeltaal"""
        response = await self.client.get_audit_events()
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_devices(self) -> None:
        """Get all Device resources from Koppeltaal"""
        response = await self.client.get_devices()
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_endpoints(self) -> None:
        """Get all Endpoint resources from Koppeltaal"""
        response = await self.client.get_endpoints()
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_endpoint(self, id: str) -> None:
        """Get single Endpoint resource from Koppeltaal"""
        response = await self.client.get_endpoint(id=id)
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_activitydefinitions(self) -> None:
        """Get all ActivityDefinition resources from Koppeltaal"""
        response = await self.client.get_activitydefinitions()
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_activitydefinition(self, id: str) -> None:
        """Get single ActivityDefinition resource from Koppeltaal"""
        response = await self.client.get_activitydefinition(id=id)
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def delete_activitydefinition(self, id: str) -> None:
        """Get single ActivityDefinition resource from Koppeltaal"""
        response = await self.client.delete_activitydefinition(id=id)
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_tasks(self) -> None:
        """Get all Task resources from Koppeltaal"""
        response = await self.client.get_tasks()
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_task(self, id: str) -> None:
        """Get single Task resource from Koppeltaal"""
        response = await self.client.get_task(id=id)
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(
                exclude_unset=True, exclude_none=True, indent=4
            )
        )

    async def get_subscriptions(self) -> None:
        """Get all Subscription resources from Koppeltaal"""
        response = await self.client.get_subscriptions()
        print_json(
            JsonResponse.parse_obj([obj for obj in response]).json(exclude_none=True)
        )

    async def get_info(
        self,
    ) -> None:
        """Show information for Koppeltaal Api"""
        info = await self.client.get_info()
        print(info)


class KoppeltaalCli:
    """Koppeltaal Api Cli wrapper"""

    def __init__(self, **kwargs) -> None:
        # Get commandline arguments
        self.args = CommandLineArgs(**kwargs)
        # Get toml file settings
        self.toml_config = load_settings(self.args.config)
        # build config
        self.config = merge_config(self.toml_config, self.args.dict())
        # build runner
        self.runner = KoppeltaalAsyncRunner(self.config, self.args.debug)

    # ----------------------------------------------------------------------------#
    # FHIR Endpoints                                                              #
    # ----------------------------------------------------------------------------#

    def patients(self) -> None:
        asyncio.run(self.runner.get_patients())

    def patient(self, id: str) -> None:
        asyncio.run(self.runner.get_patient(id=id))

    def practitioners(self) -> None:
        asyncio.run(self.runner.get_practitioners())

    def practitioner(self, id: str) -> None:
        asyncio.run(self.runner.get_practitioner(id=id))

    def audit_events(self) -> None:
        asyncio.run(self.runner.get_audit_events())

    def devices(self) -> None:
        asyncio.run(self.runner.get_devices())

    def endpoints(self) -> None:
        asyncio.run(self.runner.get_endpoints())

    def endpoint(self, id: str) -> None:
        asyncio.run(self.runner.get_endpoint(id=id))

    def activitydefinitions(self) -> None:
        asyncio.run(self.runner.get_activitydefinitions())

    def activitydefinition(self, id: str) -> None:
        asyncio.run(self.runner.get_activitydefinition(id=id))

    def delete_activitydefinition(self, id: str) -> None:
        asyncio.run(self.runner.delete_activitydefinition(id=id))

    def tasks(self) -> None:
        asyncio.run(self.runner.get_tasks())

    def task(self, id: str) -> None:
        asyncio.run(self.runner.get_task(id=id))

    def subscriptions(self) -> None:
        asyncio.run(self.runner.get_subscriptions())

    # ----------------------------------------------------------------------------#
    # Function for info, version, config, and other usefull insights              #
    # ----------------------------------------------------------------------------#

    def info(self) -> None:
        asyncio.run(self.runner.get_info())

    def show_version(self) -> None:
        click.secho("Koppeltaal CLI tools")
        click.secho(font.renderText("Koppeltaal"), fg="blue")
        click.secho(f"Version {VERSION}")


pass_koppeltaal = click.make_pass_decorator(KoppeltaalCli, ensure=True)
