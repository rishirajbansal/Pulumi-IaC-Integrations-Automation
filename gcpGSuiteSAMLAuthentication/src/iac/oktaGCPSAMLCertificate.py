"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: March 2020
 *
"""
import os
from http.client import HTTPSConnection
import json
from config.config import *
from pulumi import ResourceOptions, Output
from pulumi.dynamic import ResourceProvider, CreateResult, Resource, UpdateResult


class GCPSAMLCertificateProviderArgs(object):
    """
    Class for providing arguments to Custom Provider

    """

    def __init__(
            self,
            appid: Output[str],
    ):
        """
        The constructor for GCPSAMLValidationProviderArgs class
        :param appid: Okta App id generated by Pulumi
        """

        self.appid = appid


class GCPSAMLCertificateProvider(ResourceProvider):
    """
    Custom Provider for Okta
    """

    def create(self, props):

        status, data = self.get_endpoint_request(props["appid"])

        format_cert = self.format_cert(data[0]["x5c"][0])

        return CreateResult(id_="GCPSAMLValidation", outs={'cert': format_cert})

    def update(self, id, _olds, props):

        status, data = self.get_endpoint_request(props["appid"])

        format_cert = self.format_cert(data[0]["x5c"][0])

        return UpdateResult(outs={'cert': format_cert})

    def get_endpoint_request(self, appid):
        """

        :param appid: App id of Okta GCP App
        :return: Response status, Data
        """

        token_endpoint = "{0}".format(OKTA_DEV_URL)
        token_path = "/api/v1/apps/{0}/credentials/keys".format(appid)

        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": "SSWS {0}".format(OKTA_TOKEN_KEY)
        }

        con = HTTPSConnection(token_endpoint)
        con.request("GET", token_path, body="", headers=headers)
        response = con.getresponse()

        if response.status in (200, 201, 400):
            res_data = str(response.read().decode('utf-8'))
            data = json.loads(res_data)
            # print(data)
            return response.status, data

        return None, None

    def format_cert(self, cert_data):
        formatted_cert = ''
        with open('config/okta.cert', 'w+') as outfile:
            outfile.write("-----BEGIN CERTIFICATE-----")
            outfile.write(os.linesep)
            outfile.write(cert_data)
            outfile.write(os.linesep)
            outfile.write("-----END CERTIFICATE-----")
            outfile.close()

        with open('config/okta.cert', 'r') as infile:
            for line in infile:
                formatted_cert = formatted_cert + line
            infile.close()

        return formatted_cert


class GCPSAMLCertificate(Resource):
    """
    Custom Resource for Okta OIN GCP X.509 Certification generation.

    This class generates authentication certificate from Okta to integrate in Google admin.
    """

    cert: Output[str]

    def __init__(self, name: str, args: GCPSAMLCertificateProviderArgs, opts: ResourceOptions = None):
        """

        :param name: Unique name for the Component Resource Class
        :param args: Information passed to [initialize] method
        :param opts: Options that control this resource's behavior
        """

        full_args = {'cert': None, **vars(args)}

        super().__init__(GCPSAMLCertificateProvider(), name, full_args, opts)
