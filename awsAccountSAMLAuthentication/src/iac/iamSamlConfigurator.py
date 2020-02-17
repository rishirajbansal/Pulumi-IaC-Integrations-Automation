"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: February 2020
 *
"""

import json
import os
import pulumi
import pulumi_aws as aws
from pulumi import ResourceOptions, ComponentResource


class IAMSamlConfiguratorArgs:
    def __init__(
            self,
            okta_saml_metadata: str
    ):
        self.okta_saml_metadata = okta_saml_metadata


class IAMSamlConfigurator(ComponentResource):
    def __init__(self, name: str, args: IAMSamlConfiguratorArgs, opts: ResourceOptions = None):
        super().__init__("custom:app:IAMSamlConfigurator", name, {}, opts)

        child_opts = ResourceOptions(parent=self, depends_on=opts.depends_on)

        iam_saml_provider = aws.iam.SamlProvider(os.getenv("AWS_IAM_SAML_PROVIDER_RES_NAME"),
                                                 name=os.getenv("AWS_IAM_SAML_PROVIDER_NAME"),
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

        iam_saml_role_okta = aws.iam.Role(os.getenv("AWS_IAM_SAML_ROLE_OKTA_RES_NAME"),
                                          name=os.getenv("AWS_IAM_SAML_ROLE_OKTA_NAME"),
                                          assume_role_policy=role_policy,
                                          force_detach_policies=True,
                                          opts=pulumi.ResourceOptions(
                                              depends_on=[
                                                  iam_saml_provider
                                              ]
                                          )
                                          )

        # Attach Admin access policy to IAM Role
        if os.getenv("ENABLE_ADMIN_ACCESS_ON_ROLE") == 'Yes':
            role_policy_attach = aws.iam.RolePolicyAttachment(os.getenv("AWS_IAM_ADMIN_POLICY_RES_NAME"),
                                                              policy_arn='arn:aws:iam::aws:policy/AdministratorAccess',
                                                              role=os.getenv("AWS_IAM_SAML_ROLE_OKTA_NAME"),
                                                              opts=pulumi.ResourceOptions(
                                                                  depends_on=[
                                                                      iam_saml_role_okta
                                                                  ]
                                                              )
                                                              )

        self.iam_saml_provider_arn = iam_saml_provider.arn.apply(lambda arn: arn)
        self.iam_role_urn = iam_saml_role_okta.arn.apply(lambda arn: arn)

        self.register_outputs({})
