"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: February 2020
 *
"""

import pulumi_okta as okta
from pulumi import ResourceOptions, ComponentResource

from config import *


class AWSSAMLArgs:
    """
    Class for providing arguements to Compoment resource

    """

    def __init__(
            self,
            iam_saml_provider_arn: str = None,
            iam_role_urn: str = None
    ):
        """
        The constructor for IAMSamlConfiguratorArgs class
        :param iam_saml_provider_arn: ARN Value of IAM SAML Provider
        :param iam_role_urn: ARN Value of IAM Role
        """

        self.iam_saml_provider_arn = iam_saml_provider_arn
        self.iam_role_urn = iam_role_urn


class AWSSAML(ComponentResource):
    """
    Component Resource for Okta OIN AWS App Configuration.

    This class creates Okta OIN based AWS Application with SAML authentication.
    """

    def __init__(self, name: str, args: AWSSAMLArgs, opts: ResourceOptions = None):
        """

        :param name: Unique name for the Component Resource Class
        :param args: Information passed to [initialize] method
        :param opts: Options that control this resource's behavior
        """
        super().__init__("custom:app:awsSaml", name, {}, opts)

        child_opts = ResourceOptions(parent=self)

        okta_aws_app = okta.app.Saml(OKTA_AWS_OIN_APP_RES_NAME,
                                     label=OKTA_AWS_OIN_APP_NAME,
                                     preconfigured_app='amazon_aws',
                                     subject_name_id_format='urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress'
                                     )

        self.metadata = okta_aws_app.metadata.apply(lambda metadata: metadata)
        self.id = okta_aws_app.id.apply(lambda id: id)

        self.register_outputs({})
