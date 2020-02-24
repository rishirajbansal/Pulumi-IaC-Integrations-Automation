# Pulumi-IaC-Integrations-Automation
Automation of various interfaces, tools, infrastructures using Pulumi by integrating all in IaC form.

## Project: AWS Account Access from Okta SSO
Enabling SAML based Authentication SSO system for AWS accounts using Okta as IdP.

The objective of the project is to allow users to securely login into the AWS account (Console) from one-click login without using a password. This will make easier for users to access the application faster and avoiding the hassle to providing the login credentials everytime. 

Certain IAM Role can be associated with the account access with the required privileges. These privileges can be controlled from IAM Policies. Multiple IAM Policies can be associated with single IAM Role, hence providing an isolated layers of access which can be turned on/off. Each policy can be centralized around one AWS service or multiple. 

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

Follow this document to create Okta OIN AWS app with base properties and its other component.

[Create Infrastructure Stack by Pulumi](awsAccountSAMLAuthentication/documents/Nuage%20-%20Pulumi%20IaC%20Integrations%20Automation%20-%20Technical%20Specification.pdf)

This completes Application Deployment Workflow.

#### Resource Diagram

[Resource Diagram](https://github.com/rishirajbansal/Pulumi-IaC-Integrations-Automation/blob/master/awsAccountSAMLAuthentication/documents/ResourceDiagram.png)
