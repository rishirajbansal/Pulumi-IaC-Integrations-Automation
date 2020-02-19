"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: February 2020
 *
"""
import os

import pulumi

from iamSamlConfigurator import IAMSamlConfigurator, IAMSamlConfiguratorArgs
from oktaIdp import OktaSetup, OktaSetupArgs
from config import *


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IaC setup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

okta_aws_app = OktaSetup("OktaSetup",
                         OktaSetupArgs(
                            iam_saml_provider_arn=AWS_IAM_SAML_PROVIDER_ARN,
                            iam_role_urn=AWS_IAM_SAML_ROLE_OKTA_ARN
                         )
                         )

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
