"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: February 2020
 *
"""

import os

import pulumi
import pulumi_aws as aws


class IAMSetup:

    def create_iam_saml_provider(self, okta_aws_app, okta_saml_metadata):
        iam_saml_provider = aws.iam.SamlProvider(os.getenv("AWS_IAM_SAML_PROVIDER_RES_NAME"),
                                                 name=os.getenv("AWS_IAM_SAML_PROVIDER_NAME"),
                                                 saml_metadata_document=okta_saml_metadata,
                                                 opts=pulumi.ResourceOptions(
                                                     depends_on=[
                                                         okta_aws_app
                                                     ]
                                                 )
                                                 )

        return iam_saml_provider

    def create_iam_saml_role_okta(self, iam_saml_provider, iam_saml_provider_arn):

        role_policy = iam_saml_provider_arn.apply(lambda arn: '{'\
                                                              '"Version": "2012-10-17",'\
                                                              '"Statement": ['\
                                                              '  {' 
                                                              '    "Effect": "Allow",'\
                                                              '    "Principal": {'\
                                                              '     "Federated": "%s"'\
                                                              '  },'\
                                                              '   "Action": "sts:AssumeRoleWithSAML",'\
                                                              '   "Condition": {' \
                                                              '      "StringEquals": {' \
                                                              '        "SAML:aud": "https://signin.aws.amazon.com/saml"'\
                                                              '      }'\
                                                              '    }'\
                                                              '  }'\
                                                              ']'\
                                                              '}' % (arn))

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

        return iam_saml_role_okta

    def attach_role_policy_adminaccess(self, iam_saml_role_okta):
        role_policy_attach = aws.iam.RolePolicyAttachment(os.getenv("AWS_IAM_ADMIN_POLICY_RES_NAME"),
                                                          policy_arn='arn:aws:iam::aws:policy/AdministratorAccess',
                                                          role=os.getenv("AWS_IAM_SAML_ROLE_OKTA_NAME"),
                                                          opts=pulumi.ResourceOptions(
                                                              depends_on=[
                                                                  iam_saml_role_okta
                                                              ]
                                                          )
                                                          )

        return role_policy_attach