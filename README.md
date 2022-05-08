# Intro

Hello :wave:

This repo is a fork from the original creator [groovy-sky](https://github.com/groovy-sky/azure-office-ip)

The fork aims to add some functionality to the app, as well as integrate it with some CI/CD, terraform and other bits and bobes.

## What this Python Function App does

This repo hosts all the code and the mechanisms to deploy a Linux Azure Function App into the Libre DevOps tenant.

- Build function app and needed resources using terraform
- Debug locally with a simplified script
- Deploy code via Azure Pipelines

The function itself is a Timer function, which, every 5 hours will fetch a list of IPs and add them to a convenient format inside a storage account created with terraform.

There are 2 functions - `Get-ClientIps` and `Get-ClientUrls`.  These functions do what they say in the tin, one fetches a list of IPs object from the [Office365 API](https://endpoints.office.com/endpoints/worldwide) and the other does the exact same, except gets the `urls` property as well.


## Building the environment

At the time of writing, this project only supports Azure DevOps continuous integration and is setup to deploy using some expected items in the Libre DevOps Azure DevOps instance.

You can freely use the modules used to deploy these resources as well as the pipeline templates, but setting up the bits in between will be up to you.
