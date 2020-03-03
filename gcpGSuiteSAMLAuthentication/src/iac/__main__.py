"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: March 2020
 *
"""

import pulumi

from config.config import *
from googleAdminSAMLConfigurator import GoogleAdminSAML, GoogleAdminSAMLProviderArgs
from oktaGCPSAML import GCPSAML, GCPSAMLArgs
from oktaGCPSAMLCertificate import GCPSAMLCertificate, GCPSAMLCertificateProviderArgs
from oktaGSuiteSAML import GSuiteSAMLArgs, GSuiteSAML


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IaC setup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create Okta GCP OIN App
okta_gcp_app = GCPSAML(OKTA_GCP_OIN_APP_RES_NAME,
                       GCPSAMLArgs())

# Create Okta GSuite OIN App
okta_gsuite_app = None
if ENABLE_GSUITE_APP_CREATION:
    okta_gsuite_app = GSuiteSAML(OKTA_GSUITE_OIN_APP_RES_NAME,
                                 GSuiteSAMLArgs())

# Generates X.509 certificate for application key credential usint Dynamic Provider
okta_gcp_app_validation = GCPSAMLCertificate("GCPSAMLCertificate",
                                            GCPSAMLCertificateProviderArgs(
                                                appid=okta_gcp_app.id
                                            ),
                                            opts=pulumi.ResourceOptions(
                                                depends_on=[
                                                    okta_gcp_app
                                                ]
                                            )
                                            )

# Configure SAML Settings in Google Admin console (admin.google.com)
# google_admin_saml_settings = GoogleAdminSAML("GoogleAdminSAML",
#                                              GoogleAdminSAMLProviderArgs(
#                                                  cert=okta_gcp_app_validation.cert
#                                              ),
#                                              opts=pulumi.ResourceOptions(
#                                                  depends_on=[
#                                                      okta_gcp_app_validation
#                                                  ]
#                                              )
#                                              )

# Details of Infrastructure Setup on GCP and Okta

pulumi.export('Okta GCP App Id                         => ', okta_gcp_app.id)
if ENABLE_GSUITE_APP_CREATION:
    pulumi.export('Okta GSuite App Id                  => ', okta_gsuite_app.id)
# pulumi.export('Okta GCP App Cert                       => ', okta_gcp_app_validation.cert)
