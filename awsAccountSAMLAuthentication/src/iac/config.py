
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Change ARNs values after creating Stack 'FIRST' time and then run Pulumi again
# Get the values from the Pulumi output's console

# AWS_IAM_SAML_PROVIDER_ARN = 'arn:aws:iam::659051841213:saml-provider/NuageOkta001'
# AWS_IAM_SAML_ROLE_OKTA_ARN = 'arn:aws:iam::659051841213:role/OktaRoleForSAMLAccess'
AWS_IAM_SAML_PROVIDER_ARN = ''
AWS_IAM_SAML_ROLE_OKTA_ARN = ''
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OKTA_AWS_OIN_APP_RES_NAME = 'NuageAWSApp'
AWS_IAM_SAML_PROVIDER_RES_NAME = 'NuageOkta001'
AWS_IAM_SAML_ROLE_OKTA_RES_NAME = 'OktaRoleForSAMLAccess'
AWS_IAM_ADMIN_POLICY_RES_NAME = 'AWSAdminAccess'

OKTA_AWS_OIN_APP_NAME = 'Nuage AWS Administration'
AWS_IAM_SAML_PROVIDER_NAME = 'NuageOkta001'
AWS_IAM_SAML_ROLE_OKTA_NAME = 'OktaRoleForSAMLAccess'

# Enable admin access for Okta Role
# Format: Yes/No
ENABLE_ADMIN_ACCESS_ON_ROLE = True