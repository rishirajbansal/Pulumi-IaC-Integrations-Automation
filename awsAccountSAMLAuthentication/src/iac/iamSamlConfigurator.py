"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: February 2020
 *
"""

import json

import pulumi
import pulumi_aws as aws
from pulumi import ResourceOptions, ComponentResource
from config import *


class IAMSamlConfiguratorArgs:
    """
    Class for providing arguements to Compoment resource

    Attributes:
        okta_saml_metadata (str): Metadata xml received from Okta AWS App
    """

    def __init__(
            self,
            okta_saml_metadata: str
    ):
        """
        The constructor for IAMSamlConfiguratorArgs class
        :param okta_saml_metadata: Metadata xml received from Okta AWS App
        """

        self.okta_saml_metadata = okta_saml_metadata


class IAMSamlConfigurator(ComponentResource):
    """
    Component Resource for IAM SAML Configuration.

    This class create IAML SAML Provider and IAM SAML Role for Okta.
    It defines its own output properties using register_outputs and generates IAM ARNs
    """

    def __init__(self, name: str, args: IAMSamlConfiguratorArgs, opts: ResourceOptions = None):
        """
        The constructor for IAMSamlConfigurator class

        :param name: Unique name for the Component Resource Class
        :param args: Information passed to [initialize] method
        :param opts: Options that control this resource's behavior
        """
        super().__init__("custom:app:IAMSamlConfigurator", name, {}, opts)

        child_opts = ResourceOptions(parent=self, depends_on=opts.depends_on)

        iam_saml_provider = aws.iam.SamlProvider(AWS_IAM_SAML_PROVIDER_RES_NAME,
                                                 name=AWS_IAM_SAML_PROVIDER_NAME,
                                                 saml_metadata_document=args.okta_saml_metadata,
                                                 opts=child_opts,
                                                 )

        role_policy = iam_saml_provider.arn.apply(lambda arn: json.dumps({
                                                        "Version": "2012-10-17",
                                                        "Statement": [
                                                            {
                                                                "Effect": "Allow",
                                                                "Principal": {
                                                                    "Federated": f"{arn}"
                                                                },
                                                                "Action": "sts:AssumeRoleWithSAML",
                                                                "Condition": {
                                                                    "StringEquals": {
                                                                        "SAML:aud": "https://signin.aws.amazon.com/saml"
                                                                    }
                                                                }
                                                            }
                                                        ]
                                                    })
                                                  )

        iam_saml_role_okta = aws.iam.Role(AWS_IAM_SAML_ROLE_OKTA_RES_NAME,
                                          name=AWS_IAM_SAML_ROLE_OKTA_NAME,
                                          assume_role_policy=role_policy,
                                          force_detach_policies=True,
                                          opts=pulumi.ResourceOptions(
                                              depends_on=[
                                                  iam_saml_provider
                                              ]
                                          )
                                          )

        # Attach Admin access policy to IAM Role
        if ENABLE_ADMIN_ACCESS_ON_ROLE:
            role_policy_attach = aws.iam.RolePolicyAttachment(AWS_IAM_ADMIN_POLICY_RES_NAME,
                                                              policy_arn='arn:aws:iam::aws:policy/AdministratorAccess',
                                                              role=AWS_IAM_SAML_ROLE_OKTA_NAME,
                                                              opts=pulumi.ResourceOptions(
                                                                  depends_on=[
                                                                      iam_saml_role_okta
                                                                  ]
                                                              )
                                                              )

        self.iam_saml_provider_arn = iam_saml_provider.arn.apply(lambda arn: arn)
        self.iam_role_urn = iam_saml_role_okta.arn.apply(lambda arn: arn)

        self.register_outputs({})
