"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: March 2020
 *
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from http.client import HTTPSConnection
from base64 import b64encode
from config.config import *

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains the OAuth 2.0 information
CLIENT_SECRETS_FILE = "config/client_secret.json"

# SCOPE Definition for Admin SDK
SCOPES = ['https://apps-apis.google.com/a/feeds/domain/']

GOOGLE_API_ADMIN_ENDPOINT = "apps-apis.google.com"
GOOGLE_API_ADMIN_URI_PATH = "/a/feeds/domain/2.0/DOMAIN_NAME/sso/"
GOOGLE_API_ADMIN_URI_SAML_GENERAL = "general"
GOOGLE_API_ADMIN_URI_SAML_CERT = "signingkey"

API_REQUEST_TYPE_SAML_GENERAL = "general"
API_REQUEST_TYPE_SAML_SIGNKEY = "cert"


class GAuth:

    def generate_access_token_auto(self):
        """
        Autoamted handling of OAuth authentication by auto-generated authorization URL
        :return: token
        """

        try:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_console(authorization_prompt_message='Please open this URL in browser to authorize '
                                                                        'this action and copy generated code from '
                                                                        'there: {url}',
                                           authorization_code_message='Enter the authorization code here: ')
            token = credentials.token

            # print("Access Token : {0}".format(token))

            return token
        except Exception as ex:
            print("Invalid authorization code entered, please provide valid code: {0}".format(ex))

    def generate_access_token_custom(self):
        """
        Custom handling of OAuth authentication by customizing authorization URL based on needs
        :return: token

        """
        try:
            flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                                 SCOPES,
                                                 redirect_uri='urn:ietf:wg:oauth:2.0:oob')

            auth_url, state = flow.authorization_url(access_type='offline',
                                                     include_granted_scopes='true',
                                                     login_hint=USER_CONSENT_OFFICAL_EMAIL_ID)

            print("")
            print('Please open following URL in browser to authorize and copy generated code :')
            print('{0}'.format(auth_url))

            print("")
            auth_code = input('Enter the authorization code here : ')
            flow.fetch_token(code=auth_code)

            credentials = flow.credentials

            token = credentials.token

            # print("Access Token : {0}".format(token))

            return token

        except Exception as ex:
            print("Invalid authorization code entered, please provide valid code: {0}".format(ex))



    def validate_token(self, token):
        credentials = Credentials(token)
        return credentials.valid

    def post_endpoint_request(self, method, token, payload, request_type):
        """

       :param method: REST API Method type
       :param token: Access Token generated from OAuth authentication
       :param payload: Data to send in the Body of request
       :param request_type: Type of request ex. set SAML setting, set CERT
       :return: Response status, Data
       """

        endpoint = GOOGLE_API_ADMIN_ENDPOINT
        path = GOOGLE_API_ADMIN_URI_PATH.replace("DOMAIN_NAME", DOMAIN_NAME)

        if request_type == API_REQUEST_TYPE_SAML_GENERAL:
            path = path + GOOGLE_API_ADMIN_URI_SAML_GENERAL
        elif request_type == API_REQUEST_TYPE_SAML_SIGNKEY:
            path = path + GOOGLE_API_ADMIN_URI_SAML_CERT
        else:
            print("Invalid request type send in post endpoint request")
            return None, None

        headers = {
            "Accept": "application/atom+xml",
            "Content-type": "application/atom+xml",
            "Authorization": "Bearer {0}".format(token)
        }

        con = HTTPSConnection(endpoint)
        con.request("PUT", path, body=payload, headers=headers)
        response = con.getresponse()

        if response.status == 200 or response.status == 400:
            res_data = str(response.read().decode('utf-8'))
            # print(res_data)
            return response.status, res_data

        return None, None

    def prepare_atom_payload(self, request_type, cert=None):
        atom_xml_string = None

        if request_type == API_REQUEST_TYPE_SAML_GENERAL:
            atom_xml_string = self.file_to_string("config/samlSettingsAtomPub.xml")
            atom_xml_string = atom_xml_string.replace("{DOMAIN_NAME}", DOMAIN_NAME)
            atom_xml_string = atom_xml_string.replace("{PASSWORD_URL}", PASSWORD_URL)
            atom_xml_string = atom_xml_string.replace("{SIGNOUT_URL}", SIGNOUT_URL)
            atom_xml_string = atom_xml_string.replace("{SIGNIN_URL}", SIGNIN_URL)

        elif request_type == API_REQUEST_TYPE_SAML_SIGNKEY:
            atom_xml_string = self.file_to_string("config/samlCertAtomPub.xml")
            atom_xml_string = atom_xml_string.replace("{DOMAIN_NAME}", DOMAIN_NAME)

            encoded_cert = b64encode(bytes(cert, "utf-8")).decode("ascii")
            atom_xml_string = atom_xml_string.replace("{CERT}", encoded_cert)

        else:
            print("Invalid request type send for atom payload")

        return atom_xml_string

    def file_to_string(self, src_file):
        text = ''

        with open(src_file, 'r') as infile:
            for line in infile:
                text = text + line
            infile.close()

        return text


# def call_gauth():
if __name__ == '__main__':
    gauth = GAuth()
    token = gauth.generate_access_token_custom()
    is_token_valid = gauth.validate_token(token)

    if is_token_valid:
        # Add SAML Settings
        payload = gauth.prepare_atom_payload(API_REQUEST_TYPE_SAML_GENERAL)
        print("")
        # print("SAML Settings payload : {0}".format(payload))
        status_saml, data_saml = gauth.post_endpoint_request("PUT", token, payload, API_REQUEST_TYPE_SAML_GENERAL)

        # print("Response Status : {0}".format(status_saml))
        # print("Response Data : {0}".format(data_saml))

        # Add Cert
        okta_cert = gauth.file_to_string("config/okta.cert")
        payload = gauth.prepare_atom_payload(API_REQUEST_TYPE_SAML_SIGNKEY, okta_cert)
        # print("Cert payload : {0}".format(payload))

        status_cert, data_cert = gauth.post_endpoint_request("PUT", token, payload, API_REQUEST_TYPE_SAML_SIGNKEY)

        # print("Response Status : {0}".format(status_cert))
        # print("Response Data : {0}".format(data_cert))

        if status_saml in (200, 201) and status_saml in (200, 201):
            print("==> SAML Settings and certificate is set successfully in Google Admin")
        else:
            print("Failed to set SAML settings in Google Admin")

    else:
        print("Invalid Token, cannot continue.")
