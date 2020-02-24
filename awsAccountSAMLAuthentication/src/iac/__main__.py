"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: February 2020
 *
"""

import pulumi

from iamSamlConfigurator import IAMSamlConfigurator, IAMSamlConfiguratorArgs
from oktaAwsSAML import AWSSAML, AWSSAMLArgs
from config import *
from oktaAwsSAMLValidation import AWSSAMLValidation, AWSSAMLValidationProviderArgs


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IaC setup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create Okta AWS OIN App
okta_aws_app = AWSSAML(OKTA_AWS_OIN_APP_RES_NAME,
                       AWSSAMLArgs())

# Create and Configure IAM Settings in AWS
iam_saml_configurator = IAMSamlConfigurator("Okta_IAMSAMLConfigurator",
                                            IAMSamlConfiguratorArgs(
                                                okta_saml_metadata=okta_aws_app.metadata
                                            ),
                                            opts=pulumi.ResourceOptions(
                                                 depends_on=[
                                                     okta_aws_app
                                                 ]
                                            )
                                            )

# Update Okta AWS OIN app with IAM Details
okta_aws_app_validation = AWSSAMLValidation("AWSSAMLValidation",
                                            AWSSAMLValidationProviderArgs(
                                                appid=okta_aws_app.id,
                                                iam_saml_provider_arn=iam_saml_configurator.iam_saml_provider_arn,
                                                iam_role_urn=iam_saml_configurator.iam_role_urn
                                            ),
                                            opts=pulumi.ResourceOptions(
                                                depends_on=[
                                                    okta_aws_app
                                                ]
                                            )
                                            )


# Details of Infrastructure Setup on AWS and Okta

pulumi.export('Okta App Id                      => ', okta_aws_app.id)
pulumi.export('AWS IAM SAML Provider ARN        => ', iam_saml_configurator.iam_saml_provider_arn)
pulumi.export('AWS IAM Okta Role ARN            => ', iam_saml_configurator.iam_role_urn)
