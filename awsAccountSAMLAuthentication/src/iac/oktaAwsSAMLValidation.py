"""
 * Licensed To: Nuage
 * Authored By: Rishi Raj Bansal
 * Developed in: February 2020
 *
"""
from http.client import HTTPSConnection
import json

from config import *
from pulumi import ResourceOptions, Output
from pulumi.dynamic import ResourceProvider, CreateResult, Resource, UpdateResult


class AWSSAMLValidationProviderArgs(object):
    """
    Class for providing arguments to Custom Provider

    """

    def __init__(
            self,
            appid: Output[str],
            iam_saml_provider_arn: str,
            iam_role_urn: str
    ):
        """
        The constructor for IAMSamlConfiguratorArgs class
        :param appid: Okta App id generated by Pulumi
        :param iam_saml_provider_arn: ARN Value of IAM SAML Provider
        :param iam_role_urn: ARN Value of IAM Role
        """

        self.appid = appid
        self.iam_saml_provider_arn = iam_saml_provider_arn
        self.iam_role_urn = iam_role_urn


class AWSSAMLValidationProvider(ResourceProvider):
    """
    Custom Provider for Okta
    """

    def create(self, props):

        identity_provider_arn = "{0},{1}".format(props["iam_role_urn"], props["iam_saml_provider_arn"])

        status, data = self.post_appupdate_endpoint_request(props["appid"], identity_provider_arn)

        return CreateResult(id_="AWSSAMLValidation", outs={})

    def update(self, id, _olds, props):
        identity_provider_arn = "{0},{1}".format(props["iam_role_urn"], props["iam_saml_provider_arn"])

        status, data = self.post_appupdate_endpoint_request(props["appid"], identity_provider_arn)

        return UpdateResult(outs={})

    def post_appupdate_endpoint_request(self, appid, identity_provider_arn):
        """

        :param appid: App id of Okta AWS App
        :param identity_provider_arn: Consolidated String combining IAM Role ARN and Identity Provider ARN
        :return: Response status, Data
        """

        token_endpoint = "{0}".format(OKTA_DEV_URL)
        token_path = "/api/v1/apps/{0}".format(appid)

        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": "SSWS {0}".format(OKTA_TOKEN_KEY)
        }

        app_settings_json = json.dumps({
            "name": "amazon_aws",
            "signOnMode": "SAML_2_0",
            "credentials": {
                "userNameTemplate": {
                    "template": "${source.email}",
                    "type": "BUILT_IN"
                },
            },
            "settings": {
                "app": {
                    "identityProviderArn": identity_provider_arn,
                    "awsEnvironmentType": "aws.amazon",
                    "sessionDuration": 3600,
                    "joinAllRoles": True
                }
            }
        })

        con = HTTPSConnection(token_endpoint)
        con.request("PUT", token_path, body=app_settings_json, headers=headers)
        response = con.getresponse()

        if response.status == 200 or response.status == 400:
            res_data = str(response.read().decode('utf-8'))
            data = json.loads(res_data)
            # print(data)
            return response.status, data

        return None, None


class AWSSAMLValidation(Resource):
    """
    Custom Resource for Okta OIN AWS App Configuration.

    This class creates Okta OIN based AWS Application with SAML authentication.
    """

    okta_metadata: str

    def __init__(self, name: str, args: AWSSAMLValidationProviderArgs, opts: ResourceOptions = None):
        """

        :param name: Unique name for the Component Resource Class
        :param args: Information passed to [initialize] method
        :param opts: Options that control this resource's behavior
        """

        full_args = {'okta_metadata': None, **vars(args)}

        super().__init__(AWSSAMLValidationProvider(), name, full_args, opts)

