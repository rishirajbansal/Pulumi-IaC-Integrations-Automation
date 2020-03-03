## Project: GCP & GSuite Account Access from Okta SSO
Enabling SAML based Authentication SSO system for GCP & GSuite accounts using Okta as IdP.

The objective of the project is to allow users to securely login into the GCP & GSuite account (Console) from one-click login without using a password. This will make easier for users to access the application faster and avoiding the hassle to providing the login credentials everytime. 

These settings are based on Google account holder's admin SAML configuration. These SAML settings and certification created is handled automatically in this project and no user intervention is required to set SAML in google admin account or in cloud console.

#### Pulumi Project Setup

Prerequisites: Python v 3.6.x or later already installed.

Following steps are needed to install the Pulumi application successfully:

1.	Create project directory where the project artifacts of ‘Pulumi application’ will be copied

2.	Clone the code from GitHub repository to newly created project directory.

3.	CD to application root folder:
    ```
    $ cd gcpGSuiteSAMLAuthentication\src
    ```
    
 4.	Install Dependencies :
    ```
    $ pip install –r requirements.txt
    ```
    
5.	Update environment specific properties in configuration files. If default settings looks fine, then they can be left intact. 

#### Deployment Workflow

After setting up projects and setting up Pulumi as mentioned in the above section, this section is used to follow the steps to make application work in union with its all distinct components integrated and configured.

##### Step 1 (Create GCP and GSuite infrastructure)
 ```
$ pulumi up
 ```

##### Step 2 (Create SAML Settings and certificate in Google admin account)
 ```
$ python gAuth.py
 ```

This step will display URL to confirm the user consent for authenticating application to manage SAML settings. User will open this URL and confirms the approval, it will then generate the authorization code. User will then use this code to enter in the console to generate the OAuth tokens and in turn, these tokens will be further used to set the SAML settings and certification in admin.

#### Resource Diagram

![Resource Diagram](/gcpGSuiteSAMLAuthentication/documents/ResourceDiagram.png)

