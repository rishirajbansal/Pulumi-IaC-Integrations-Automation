"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: February 2020
 *
"""

import os

import pulumi
import pulumi_okta as okta


class OktaSetup:

    def create_aws_app(self):
        okta_aws_app = okta.app.Saml(os.getenv("OKTA_AWS_OIN_APP_RES_NAME"),
                                    label=os.getenv("OKTA_AWS_OIN_APP_NAME"),
                                    preconfigured_app='amazon_aws'
                                    )

        return okta_aws_app

    def update_aws_app(self, iam_saml_provider_arn, iam_saml_role_okta_arn):
        identity_provider_arn = "{0},{1}".format(iam_saml_role_okta_arn, iam_saml_provider_arn)

        app_settings_json = '{'\
                            '"identityProviderArn": "%s",'\
                            '"awsEnvironmentType":"aws.amazon",'\
                            '"sessionDuration":3600,'\
                            '"joinAllRoles":true'\
                            '}' % (identity_provider_arn)

        okta_aws_app = okta.app.Saml(os.getenv("OKTA_AWS_OIN_APP_RES_NAME"),
                                     label=os.getenv("OKTA_AWS_OIN_APP_NAME"),
                                     preconfigured_app='amazon_aws',
                                     app_settings_json=app_settings_json,
                                     subject_name_id_format='urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress'
                                     )

        return okta_aws_app

    def retrieve_aws_app(self):
        existing_okta_aws_app = okta.app.Saml.get(os.getenv("OKTA_AWS_OIN_APP_RES_NAME"),
                                                  os.getenv("OKTA_AWS_ID"))

        return existing_okta_aws_app
