# Pulumi-IaC-Integrations-Automation
Automation of various interfaces, tools, infrastructures using Pulumi by integrating all in IaC form.

## Project: AWS Account Access from Okta SSO
Enabling SAML based Authentication SSO system for AWS accounts using Okta as IdP.

The objective of the project is to allow users to securely login into the AWS account (Console) from one-click login without using a password. This will make easier for users to access the application faster and avoiding the hassle to providing the login credentials everytime. 

Certain IAM Role can be associated with the account access with the required privileges. These privileges can be controlled from IAM Policies. Multiple IAM Policies can be associated with single IAM Role, hence providing an isolated layers of access which can be turned on/off. Each policy can be centralized around one AWS service or multiple. 

For more details, check [Documentation](awsAccountSAMLAuthentication/README.md)

#### Resource Diagram for Project: 

![Resource Diagram](/awsAccountSAMLAuthentication/documents/ResourceDiagram.png)

## Project: GCP & GSUite Account Access from Okta SSO
Enabling SAML based Authentication SSO system for GCP & GSuite accounts using Okta as IdP.

The objective of the project is to allow users to securely login into the GCP & GSuite account (Console) from one-click login without using a password. This will make easier for users to access the application faster and avoiding the hassle to providing the login credentials everytime. 

These settings are based on Google account holder's admin SAML configuration. These SAML settings and certification created is handled automatically in this project and no user intervention is required to set SAML in google admin account or in cloud console.

For more details, check [Documentation](gcpGSuiteSAMLAuthentication/README.md)

#### Resource Diagram for Project: 

![Resource Diagram](/gcpGSuiteSAMLAuthentication/documents/ResourceDiagram.png)

