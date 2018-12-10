# REST framework tutorial

[![Build Status](https://dev.azure.com/noumenal/rest-framework-tutorial/_apis/build/status/rest-framework-tutorial-CI)](https://dev.azure.com/noumenal/rest-framework-tutorial/_build/latest?definitionId=4)

The is my fork of the example code from the [Django REST Tramework tutorial][drf-tutorial]. It´s a base to discuss further topics, such as testing and deployment.

_Why the DRF Tutorial?_:

+ Assuming you´re using Django, it´s likely you´re using Django REST Framework, so hopefully it should be familiar to you.
+ It´s fully featured enough to be realistic, but...
+ ...not so big as to get in the way.


----

**Need Help?**

If the steps here don´t work for you, [Open a _New Issue_][new-issue] to discuss.

----

## Preparation

1. Clone this tutorial repo.
2. Create a virtual environment.
3. Install requirements.

    `pip install -r requirements.txt`
4. Set up the local SQLite database:

    1. Migrate: `./manage.py migrate`.
    2. Load fixtures: `./restore.sh`

        This script flushes the databases and then reloads initial fixture data.
    3. Create your own admin user: `./manage.py createsuperuser`.

That´s it. You´re ready to go.

## Guides

### Using Django with Visual Studio Code & Azure

1. [Using Django with VS Code][azure-vscode].
2. [Deploying Django to the Azure App Service][azure-appservice].
3. [Adding CI & CD with Azure Pipelines][azure-pipelines].
4. [Serverless Django with Azure Functions][azure-functions].

<!-- Links -->
[drf-tutorial]: http://www.django-rest-framework.org/tutorial/1-serialization
[new-issue]: https://github.com/carltongibson/rest-framework-tutorial/issues/new

[azure-vscode]: ./docs/azure/1-vscode.md
[azure-appservice]: ./docs/azure/2-appservice.md
[azure-pipelines]: ./docs/azure/3-pipelines.md
[azure-functions]: ./docs/azure/4-functions.md
