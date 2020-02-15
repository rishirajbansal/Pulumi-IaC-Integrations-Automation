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

# Create Identity Provider in AWS
iam_saml_provider = awsSetup.create_iam_saml_provider(okta_aws_app, okta_aws_app.metadata)

# Create IAM Role and associate Identity Provider
iam_saml_role_okta = awsSetup.create_iam_saml_role_okta(iam_saml_provider, iam_saml_provider.arn)

# Attach Admin access policy to IAM Role
if os.getenv("ENABLE_ADMIN_ACCESS_ON_ROLE") == 'Yes':
    role_policy_attach = awsSetup.attach_role_policy_adminaccess(iam_saml_role_okta)

# Details of Infrastructure Setup on AWS and Okta

# pulumi.export('AWS SAML APP ID     => ', okta_aws_app.id)
pulumi.export('AWS IAM SAML Provider ARN     => ', iam_saml_provider.arn)
pulumi.export('AWS IAM Okta Role ARN     => ', iam_saml_role_okta.arn)


