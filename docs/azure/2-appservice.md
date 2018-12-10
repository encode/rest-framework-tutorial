# Deploying Django to the Azure App Service

Here we´re going to walk through deploying your Django application to the Azure App Service.

----

**Setup**

Extensions Needed:

* Azure Account
* Azure App Service
* Azure Storage

Open the Extensions activity bar and search for Azure. There are a whole load of extensions. Find these three, install them and then reload.

Once the Extensions are loaded, you´ll need to log into Azure. The Azure Account extension will handle this for you. It´ll open your browser. You log in and are authorenticated in VS Code.

You need an account, plus a subscription. Azure has a 30-day trial. If you don´t have an account you can create one online or via the extension´s `Azure: Create an Account` command.

You´ll also want to [install the Azure CLI][azure-cli-install]

[azure-cli-install]: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest

----

## Create the App Service Application.

In the Command Palette, bring up the `Azure App Service: Create New Web App...` command.

* You´ll need to give your app a unique name.
* Select `Linux` for the platform.
* Select `Python 3.7` for the runtime.

VS Code will create your new application, and offer to deploy it. Select `No` -- we need to configure a few things first!

## Configuring the Deploy

As with all Django deployments there´s three parts we need to configure:

1. The production database.
2. Serving the static files. (Images/CSS/Javascript.)
3. Production settings to tell Django about these.

Open the `env-example` file. The top section here includes placeholders for all the values we´re going to need to configure all these parts.

Make a copy of `env-example`, e.g. `.azure-env` and add the appropriate values for your application.

Then when you´re ready load the values into your environment like this:

    $ export $(grep -v '^#' .azure-env | xargs)

This uses `grep` to go through your `.azure-env` file excluding any lines that are comments, passing any values into `xargs` so they will be formatted to be interpreted by the shell. We then `export` these so they´re passed as environment variables to the commands we envoke.

### The production database

We´re going to use a hosted Azure PostgreSQL server for the deployment.

There´s a script in `bin/createdb.py` that will:

1. Create the Azure PostgreSQL server for you.
2. Add firewall rules to allow access to the PostgreSQL server from Azure IP addresses and your local IP.
3. Create the actual application database for your Django app.

You´re given a `y/n` choice at each step, and just skip steps that you already ran.

The only value you can´t provide here is the final `POSTGRES_HOST`, which is the URL of the created PostgreSQL server. This will be provided in the output when you run `bin/createdb.py`.

Once you´ve run `createdb.py` you can interact with your new database.

Run `./manage.py showmigrations` to test the connection and see the new empty database.

Run `./manage.py migrate` to run the migrations for the application.

Run `./restore.sh` to load the fixture data for the application.

### Serving the static files.

We´ll serve the static files from Azure Storages. We´ll use the Azure CLI to quickly configure this:

* Create a Storage Account

    ```bash
    az storage account create \
    --account-name $AZ_STORAGE_ACCOUNT_NAME \
    --resource-group $AZ_GROUP \
    --location $AZ_LOCATION
    ```

* Retrieve an access key

    ```bash
    az storage account keys list \
    --account-name $AZ_STORAGE_ACCOUNT_NAME \
    --resource-group $AZ_GROUP
    ```

    And the primary key returned here to you env file (and shell environment).

* Create a storage container

    ```bash
    az storage container create \
    --container-name $AZ_STORAGE_CONTAINER \
    --account-name $AZ_STORAGE_ACCOUNT_NAME \
    --account-key $AZ_STORAGE_KEY \
    --public-access blob
    ```

    This will configure a public container that will serve our static files.

With that in place you can run `collectstatic` to have your static files uploaded to Azure.

```bash
$ ./manage.py collectstatic
```

Note that you can browse your static files straight from the Azure Storage extension, an even download, edit and re-upload directly in place.

### Production settings for Django

The `env-example` files provides a value for the production settings module:

```python
DJANGO_SETTINGS_MODULE='tutorial.azure'
```

`tutorial/azure.py` is a simple settings file:

```python
from .settings import *

DEBUG = False
STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = os.getenv('AZ_STORAGE_ACCOUNT_NAME')
AZURE_CONTAINER = os.getenv('AZ_STORAGE_CONTAINER')
AZURE_ACCOUNT_KEY = os.getenv('AZ_STORAGE_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('APP_DB_NAME'),
        'USER': '{}@{}'.format(os.getenv('POSTGRES_ADMIN_USER'), os.getenv('POSTGRES_SERVER_NAME')),
        'PASSWORD': os.getenv('POSTGRES_ADMIN_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'},
    }
}
```

we just import the default settings and then define the production values from the environment variables we´ve been using so far.

For the deployment though we need to tell the Azure App Service to make these values available to our application.

For this we can use the `bin/as_settings.py` script, which will set the application settings in Azure, which will then be available as environment variables when we run Django.

```bash
./as_settings.py
```

With that in place we´re ready to go.

## Deploying

First time only, we need to set configure the deployment source for our app.

In the Azure App Service extension, right-click on our app name and select `Configure Deployment Source...`. Select `LocalGit` from the options.

When we deploy the app, VS Code will push our latest commit directly to the App Service. The App Service will then build our virtual environment and run our app.

That´s it. We´re ready.

Right-click on the app and hit `Deploy to Web App...`. Select your folder and VS Code will deploy you app.

Go to View > Output to see the deploy in progress. Once it´s finished you can right-click on the app name and select `Browse Website` to see your app live.
