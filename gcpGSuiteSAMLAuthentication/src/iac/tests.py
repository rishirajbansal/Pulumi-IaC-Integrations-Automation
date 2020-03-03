"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: March 2020
 *
"""

from gAuth import *


# Test method

if __name__ == '__main__':
    gauth = GAuth()
    token = gauth.generate_access_token_custom()
    is_token_valid = gauth.validate_token(token)

    if is_token_valid:
        # Add SAML Settings
        payload = gauth.prepare_atom_payload(API_REQUEST_TYPE_SAML_GENERAL)
        print("")
        print("SAML Settings payload : {0}".format(payload))
        status, data = gauth.post_endpoint_request("PUT", token, payload, API_REQUEST_TYPE_SAML_GENERAL)

        print("Response Status : {0}".format(status))
        print("Response Data : {0}".format(data))

        # Add Cert
        print("")
        okta_cert = gauth.file_to_string("config/okta.cert")
        payload = gauth.prepare_atom_payload(API_REQUEST_TYPE_SAML_SIGNKEY, okta_cert)
        print("Cert payload : {0}".format(payload))

        status, data = gauth.post_endpoint_request("PUT", token, payload, API_REQUEST_TYPE_SAML_SIGNKEY)

        print("Response Status : {0}".format(status))
        print("Response Data : {0}".format(data))

    else:
        print("Invalid Token, cannot continue.")
