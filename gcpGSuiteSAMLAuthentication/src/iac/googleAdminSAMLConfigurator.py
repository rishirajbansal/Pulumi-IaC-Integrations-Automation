"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: March 2020
 *
"""

from pulumi import ResourceOptions, Output
from pulumi.dynamic import ResourceProvider, CreateResult, Resource, UpdateResult

from gAuth import *


class GoogleAdminSAMLProviderArgs(object):
    """
    Class for providing arguments to Custom Provider

    """

    def __init__(
            self,
            cert: Output[str]
    ):
        """
        The constructor for GCPSAMLValidationProviderArgs class
        :param cert: Okta App X.509 Certificate generated for the app
        """

        self.appid = cert


class GoogleAdminSAMLProvider(ResourceProvider):
    """
    Custom Provider for Google Admin SAML Configuration
    """

    def create(self, props):
        gauth = GAuth()

        # Generate Access token after getting the user consent and passing the generated authorized code
        token = gauth.generate_access_token_custom()

        # Check if the token is valid
        is_token_valid = gauth.validate_token(token)

        if is_token_valid:
            self.configure_saml_settings(gauth, token, props["cert"])

            return CreateResult(id_="GoogleAdminSAML", outs={})
        else:
            print("Invalid Token, cannot continue.")

            return None

    def update(self, id, _olds, props):
        gauth = GAuth()

        # Generate Access token after getting the user consent and passing the generated authorized code
        token = gauth.generate_access_token_custom()

        # Check if the token is valid
        is_token_valid = gauth.validate_token(token)

        if is_token_valid:
            self.configure_saml_settings(gauth, token, props["cert"])

            return UpdateResult(outs={})
        else:
            print("Invalid Token, cannot continue.")

            return None

    def configure_saml_settings(self, gauth, token, cert):
        # Add SAML Settings
        payload = gauth.prepare_atom_payload(API_REQUEST_TYPE_SAML_GENERAL)
        # print("\n SAML Settings payload : {0}".format(payload))
        status_saml, data_saml = gauth.post_endpoint_request("PUT", token, payload, API_REQUEST_TYPE_SAML_GENERAL)

        #  print("Response Status : {0}".format(status_saml))
        # print("Response Data : {0}".format(data_saml))

        # Add Cert
        payload = gauth.prepare_atom_payload(API_REQUEST_TYPE_SAML_SIGNKEY, cert)
        #  print("\n Cert payload : {0}".format(payload))
        status_cert, data_cer = gauth.post_endpoint_request("PUT", token, payload, API_REQUEST_TYPE_SAML_SIGNKEY)

        # print("Response Status : {0}".format(status_cert))
        # print("Response Data : {0}".format(data_cer))


class GoogleAdminSAML(Resource):
    """
    Custom Resource for Google Admin SAML Settings.

    This class configures SAML Settings for Okta app aling with the certificate uploading.
    """

    def __init__(self, name: str, args: GoogleAdminSAMLProviderArgs, opts: ResourceOptions = None):
        """

        :param name: Unique name for the Component Resource Class
        :param args: Information passed to [initialize] method
        :param opts: Options that control this resource's behavior
        """

        full_args = {**vars(args)}

        super().__init__(GoogleAdminSAMLProvider(), name, full_args, opts)