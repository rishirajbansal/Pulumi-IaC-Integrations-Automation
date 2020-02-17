"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: February 2020
 *
"""
import os

import pulumi

from aws import IAMSetup
from generic.init.initConfigurator import InitConfigurator
from iamSamlConfigurator import IAMSamlConfigurator, IAMSamlConfiguratorArgs
from oktaIdp import OktaSetup


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Intialize basic configuration of project
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

init_config = InitConfigurator()
flag = init_config.initialize()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IaC setup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

oktaSetup = OktaSetup()
awsSetup = IAMSetup()

okta_aws_app = None
iam_saml_provider = None
iam_saml_role_okta = None
is_okta_app_exists = None

# Check if Okta App is already existed
if os.getenv("AWS_IAM_SAML_PROVIDER_ARN") == 'NONE' or os.getenv("AWS_IAM_SAML_ROLE_OKTA_ARN") == 'NONE':
    is_okta_app_exists = False
else:
    is_okta_app_exists = True

if is_okta_app_exists:
    # Update previously created Okta OIN AWS App with IAM settings
    okta_aws_app = oktaSetup.update_aws_app(os.getenv("AWS_IAM_SAML_PROVIDER_ARN"), os.getenv("AWS_IAM_SAML_ROLE_OKTA_ARN"))
else:
    # Create Okta AWS OIN App
    okta_aws_app = oktaSetup.create_aws_app()

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

# Details of Infrastructure Setup on AWS and Okta

pulumi.export('AWS IAM SAML Provider ARN        => ', iam_saml_configurator.iam_saml_provider_arn)
pulumi.export('AWS IAM Okta Role ARN            => ', iam_saml_configurator.iam_role_urn)


