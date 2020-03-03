"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: March 2020
 *
"""
import json

import pulumi_okta as okta
from pulumi import ResourceOptions, ComponentResource
from config.config import *


class GCPSAMLArgs:
    """
    Class for providing arguements to Compoment resource

    """

    def __init__(
            self
    ):
        """
        The constructor for IAMSamlConfiguratorArgs class
        """


class GCPSAML(ComponentResource):
    """
    Component Resource for Okta OIN GCP App Configuration.

    This class creates Okta OIN based GCP Application with SAML authentication.
    """

    def __init__(self, name: str, args: GCPSAMLArgs, opts: ResourceOptions = None):
        """

        :param name: Unique name for the Component Resource Class
        :param args: Information passed to [initialize] method
        :param opts: Options that control this resource's behavior
        """
        super().__init__("custom:app:gcpSaml", name, {}, opts)

        child_opts = ResourceOptions(parent=self)

        app_settings_json = json.dumps({
            "domain": DOMAIN_NAME
        })

        okta_gcp_app = okta.app.Saml(OKTA_GCP_OIN_APP_RES_NAME,
                                     label=OKTA_GCP_OIN_APP_NAME,
                                     preconfigured_app='cloudconsole',
                                     app_settings_json=app_settings_json,
                                     subject_name_id_format='urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress',
                                     user_name_template='${source.email}',
                                     user_name_template_type='BUILT_IN',
                                     default_relay_state='https://console.cloud.google.com/'
                                     )

        self.id = okta_gcp_app.id.apply(lambda id: id)

        self.register_outputs({})
