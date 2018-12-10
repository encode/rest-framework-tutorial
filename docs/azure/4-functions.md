# Running Serverless Django on Azure Functions

Here we want to run our Django app _serverless_ on Azure Functions.

----

**Setup**

You need to install various dependencies for this video. Best bet is to walk through at least the local developement steps of the [Python in Azure Functions Quickstart](https://aka.ms/AA3fvpk).

Then install the VS Code Azure Functions extension.

----

If you checkout the `azure/4-functions` branch of the repo the project is already set up ready to run in functions.

* The project is already initialised.

    ```bash
    func init —worker-runtime=python
    ```

    The VS Code Azure Functions extension has a command that will guide you through this step.

* The `serverless` folder containing the function code is already in place and configured to use an _Http Trigger_, i.e. to respond to web requests.

    ```bash
    func new
    ```

    Again you can create a new function using the VS Code extension.

* In `serverless/function.json`, we configure the `route` to capture the entire path after the base URL:

    ```json
    "route": "serverless/{*path_info}",
    ```

    This gets passed to Django as the WSGI `PATH_INFO` value, which Django will use to route the request to the correct view function.

Then inside `serverless/__init__.py` we use the `wsgi_adapter` code to map Azure functions HTTP request and response objects to WSGI request and responses that Django can understand.

* We import our Django app´s WSGI handler and wrap it in the adapter:

    ```python
    from wsgi_adapter import AzureWSGIHandler
    from tutorial.wsgi import application
    azure_application = AzureWSGIHandler(application)
    ````
* Then in our function´s `main()`, we pass in the `func.HttpRequest` and get back a `func.HttpResponse`.

    ```python
    def main(req: func.HttpRequest) -> func.HttpResponse:
        response: func.HttpResponse = azure_application(req)
        return response
    ````

    The `AzureWSGIHandler` maps between the functions and the WSGI environments. The actual request handling is still performed by Django.

----

**Note**

Everything here is somewhat experimental. It is using wrapper code available in my [azure-functions-wsgi-adapter repository](https://github.com/carltongibson/azure-functions-wsgi-adapter), and via `pip install azure-functions-wsgi-adapter`.

 The WSGI Adapter is still work in progress: if you´re interested in this, do stop by to help me finish it!

----

