"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: February 2020
 *
"""
import json

import pulumi
import pulumi_okta as okta
from pulumi import ResourceOptions, ComponentResource

from config import *


class OktaSetupArgs:
    """
    Class for providing arguements to Compoment resource

    Attributes:
        okta_saml_metadata (str): Metadata xml received from Okta AWS App
    """

    def __init__(
            self,
            iam_saml_provider_arn: str,
            iam_role_urn: str
    ):
        """
        The constructor for IAMSamlConfiguratorArgs class
        :param iam_saml_provider_arn: ARN Value of IAM SAML Provider
        :param iam_role_urn: ARN Value of IAM Role
        """

        self.iam_saml_provider_arn = iam_saml_provider_arn
        self.iam_role_urn = iam_role_urn


class OktaSetup(ComponentResource):
    """
    Component Resource for Okta OIN AWS App Configuration.

    This class creates Okta OIN based AWS Application with SAML authentication.
    """

    def __init__(self, name: str, args: OktaSetupArgs, opts: ResourceOptions = None):
        """

        :param name: Unique name for the Component Resource Class
        :param args: Information passed to [initialize] method
        :param opts: Options that control this resource's behavior
        """
        super().__init__("custom:app:OktaSetup", name, {}, opts)

        child_opts = ResourceOptions(parent=self)

        identity_provider_arn = "{0},{1}".format(args.iam_role_urn, args.iam_saml_provider_arn)

        okta_aws_app = okta.app.Saml(OKTA_AWS_OIN_APP_RES_NAME,
                                     label=OKTA_AWS_OIN_APP_NAME,
                                     preconfigured_app='amazon_aws',
                                     app_settings_json=json.dumps({
                                         "identityProviderArn": identity_provider_arn,
                                         "awsEnvironmentType": "aws.amazon",
                                         "sessionDuration": 3600,
                                         "joinAllRoles": True
                                     }),
                                     subject_name_id_format='urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress'
                                     )

        self.metadata = okta_aws_app.metadata.apply(lambda metadata: metadata)

        self.register_outputs({})
