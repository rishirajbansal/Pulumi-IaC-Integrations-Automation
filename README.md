# Pulumi-IaC-Integrations-Automation
Automation of various interfaces, tools, infrastructures using Pulumi by integrating all in IaC form.

## Project: AWS Account Access from Okta SSO
Enabling SAML based Authentication SSO system for AWS accounts using Okta as IdP.

The objective of the project is to allow users to securely login into the AWS account (Console) from one-click login without using a password. This will make easier for users to access the application faster and avoiding the hassle to providing the login credentials everytime. 

Certain IAM Role can be associated with the account access with the required privileges. These privileges can be controlled from IAM Policies. Multiple IAM Policies can be associated with single IAM Role, hence providing an isolated layers of access which can be turned on/off. Each policy can be centralized around one AWS service or multiple. 

#### Directory Structure
```
.
|   requirements.txt
|   
+---envs
|       .env.development
|       .env.production
|       
\---iac
    |   aws.py
    |   oktaIdp.py
    |   Pulumi.dev.yaml
    |   Pulumi.yaml
    |   __main__.py
    |   
    +---generic
    |   \---init
    |       |   initConfigurator.py
```

#### Pulumi Project Setup

Prerequisites: Python v 3.6.x or later already installed.

Following steps are needed to install the Pulumi application successfully:

1.	Create project directory where the project artifacts of ‘Pulumi application’ will be copied

2.	Clone the code from GitHub repository to newly created project directory.

3.	CD to application root folder:
    ```
    $ cd awsAccountSAMLAuthentication\src
    ```
    
 4.	Install Dependencies :
    ```
    $ pip install –r requirements.txt
    ```
    
5.	Update environment specific properties in configuration files. If default settings looks fine, then they can be left intact. 

#### Deployment Workflow

After setting up projects and setting up Pulumi as mentioned in the above section, this section is used to follow the steps to make application work in union with its all distinct components integrated and configured.

Following steps need to be executed to complete Deployment Workflow:

###### 1.	[Create Infrastructure Stack by Pulumi](awsAccountSAMLAuthentication/documents/Nuage%20-%20Pulumi%20IaC%20Integrations%20Automation%20-%20Technical%20Specification.pdf)

This will create Okta OIN AWS app with base properties and its other components. At this moment, Pulumi need Okta’s app metadata details to associate them with IAM Identity Provider and Role creations.

Copy down the AWS IAM SAML Provider ARN and AWS IAM Okta Role ARN generated as the output from the Pulumi template as this is required in next step.

###### 2.	Rerun the Pulumi template

Pulumi template need to execute again to update the Okta AWS App with the ARNs of IAM Identity Provider and Role generated in above step. 

In the Pulumi project, open the environment configuration file and  update property AWS_IAM_SAML_PROVIDER_ARN and AWS_IAM_SAML_ROLE_OKTA_ARN with the ARNs values copied in above step.

```
AWS_IAM_SAML_PROVIDER_ARN = arn:aws:iam::859051841213:saml-provider/NuageOkta001
AWS_IAM_SAML_ROLE_OKTA_ARN = arn:aws:iam::859051841213:role/OktaRoleForSAMLAccess
```

Run the pulumi template from the same terminal used in Step 1:

```
$ pulumi up -y
```

This will update the Okta AWS app’s Sign On settings with AWS IAM associations.

This completes Application Deployment Workflow.

