# Django Development using VS Code

Here we show how you can use VS Code to develop with your existing Django project.

We assume you followed the _Preparation_ steps from the README, and have the example project cloned, virtual environment created, and development database setup.

----

**Setup**

We´ll add some code here to demonstrate VS Code in action. If you want to follow-along checkout the `azure-begin` tag:

    $ git checkout azure-begin

When you´ve finished remember to discard your changes and switch back to `master`:

    $ git checkout -- . && git checkout master

----

## Connecting VS Code to the project

Getting started is easy: just open the project folder in VS Code.

Next we want to enable VS Code´s Python integration by installing the Python Extension.

Once the Python extension is installed and activated it will detect our virtual environment and use that to power autocomplete plus the inbuilt terminal and debugger.

## Run Project in the Built-in Terminal

Having opened the project we can now see VS Code´s inbuilt Terminal.

Go to the Terminal > New Terminal command.

Notice that VS Code will pick-up your virtual environment and automatically
activate it when creating the shell.

### Run the application

Now we´re ready to run the application.

```
$ ./manage.py runserver
```

Alt-Click on the URL in the terminal output to open the application in your
browser.

> Explore. If you´re not familiar with it, the HTML UI here is the default _Browseable API_ provided by Django REST Framework.
Click the dropdown next to `GET` and select `JSON` or add `?format=json` to the query string
to request the raw JSON response.


## Editing in VS Code

With the development server still running in the terminal, we going to add some new code. Our API already exposes `snippets` and `users` endpoints, lets add `groups`.

### Install the example snippets

In the video I used a couple of VS Code Snippets to quickly define the model serializer and viewset classes in the example. These snippets are [available in a _Gist_][drf-gist].

* Click the settings cog in the bottom-left of the VS Code window.
* Click _User Snippets_
* Select _New Snippets file for ..._ the repo folder.
* Copy in [the example snippets from the Gist][drf-gist].

### Create a serializer:

* Use Go > Go to File... (or use the shortcut) to open `serializers.py`.
* Add the import for `contrib.auth.models.Group`.
* Begin to type `serializer` and allow the autocomplete to provide the snippet suggestion.
* Fill in `Group` in the placeholders.

### Create the viewset:

* Open `views.py`.
* Repeat the steps for creating the serializer but using the `viewset` snippet.
* Note that VS Code will provide inline warnings if you forget something, e.g.
  to import `Group` or `GroupSerializer`.

### Register the viewset with the router

* Open `snippets/urls.py`.
* Register the viewset with the router, add this line below the existing `register` calls:

    ```python
    router.register(r'groups', views.GroupsViewSet)
    ```

That´s it. Refresh in the browser to see the new groups endpoints.

## Debugging

* Make sure your terminal from the previous section is **not** still running the Django development server.
* Open the Debugging activity bar. (Little bug icon, View > Debug, or shortcut.)

### Create Launch configurations

* Select `Add configuration...` from the dropdown menu.

    This will create a collection of debug configurations for various Python enviroments.
* In `lauch.json`, navigate to the `"Python: Django"` configuration and add the following key:

    ```json
    "debugStdLib": true
    ```

    This allow us to debug into the `pip` installed packages inside the
    `site_packages` folder in our virtual environment, and so into Django itself.

### Run the debugger

* In the dropdown, make sure the Python Django configuration is selected and hit the green run button.

This will run the development server under the debugger so we can insert
breakpoints and examine the behaviour of our code.

* Log into the admin, using the superuser you created.
* Navigate to the Add Snippet view.
* Try to add a Snippet, leaving the `highlighted` field blank.
* Note the error.

The `Snippet` model sets the `highlighted` field on `save()`. We don´t want to have to provide it when submitting the form.

Now we´ll put a breakpoint into `django.contrib.admin` code to examine what´s going on in the debugger.

In `admin.py` look at the `SnippetAdmin` defintion.

* Right-click on `ModelAdmin` and select _Go to Defintion_.

This will open `django/contrib/admin/options.py` from within the virtual environment´s `site_packages` folder.

We want to open the `_changeview_form()` method, which is the Django view function that handles the submitted form.

* Use Go > Find symbol in file... to search for the `_changeview_form` method.

* Set a breakpoint at line 1482:

    `if form.is_valid():`

Here we´re going to examine the form at the point of validation.

Submit the invalid form data again in the browser. The breakpoint will be hit in VS Code.

In the debug console, examine the form:

```python
form
<SnippetForm bound=True, valid=Unknown, fields=(title;code;linenos;language;style;owner;highlighted)>
form.is_valid()
False
form.errors
{'highlighted': ['This field is required.']}
```

Whilst the `highlighted` field is set in `Snippet.save()`, the model form does not know this and is expecting the field to be provided. We correct this by adjusting our `SnippetAdmin` definition:

```python
class SnippetAdmin(admin.ModelAdmin):
    readonly_fields = ('highlighted',)
```

By setting `readonly_fields` we tell the form that the field will not be provided.

Disable breakpoints. Reload the admin. Observe the `highlighted` field is no-longer available to be submitted.

# Next Steps

Explore other features in the [Python for VS Code docs][vscode-python] and the [Visual Studio Code Django Tutorial][vscode-django-tutorial].

In the step we´ll [Deploy our Django Application to the Azure App Service](./2-appservice.md).

[drf-gist]: https://gist.github.com/carltongibson/6d2870c7958dafe5002686454605d8b0
[new-issue]: https://github.com/carltongibson/rest-framework-tutorial/issues/new
[vscode-python]: https://code.visualstudio.com/docs/python/python-tutorial

[vscode-django-tutorial]: https://aka.ms/AA3fvpi