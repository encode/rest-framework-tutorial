# Django REST Framework Tutorial

Source code for the [Django REST Framework tutorial][Tutorial].

You can get the final code for each tutorial part by either selecting its branch or following this index:

1. [Serialization][Part 1].
2. [Requests & Responses][Part 2].
3. [Class-based views][Part 3].
4. [Authentication & permissions][Part 4].
5. [Relationships & hyperlinked APIs][Part 5].
6. [Viewsets & routers][Part 6].
7. [Schemas & client libraries][Part 7].


## Heroku Example
The completed [implementation][Heroku Source] is also [online][Heroku Sandbox]! Try it yourself by logging in as one of these four users: **amy**, **max**,
**jose** or **aziz**.  The passwords are the same as the usernames.

If you want to try it —assuming you already installed the [heroku-cli][Heroku-CLI]—, run these commands to setup Heroku properly:

```shell
heroku create $APP_NAME --stack cedar --buildpack git://github.com/heroku/heroku-buildpack-python.git
heroku config:add BUILDPACK_URL=git@github.com:heroku/heroku-buildpack-python.git#purge --app=$APP_NAME
heroku config:set HEROKU=1 --app=$APP_NAME
```


[Tutorial]: http://www.django-rest-framework.org/tutorial/1-serialization
[Part 1]: https://github.com/luvejo/rest-framework-tutorial/tree/master
[Part 2]: https://github.com/luvejo/rest-framework-tutorial/tree/2-requests-and-responses
[Part 3]: https://github.com/luvejo/rest-framework-tutorial/tree/3-class-based-views
[Part 4]: https://github.com/luvejo/rest-framework-tutorial/tree/4-authentication-and-permissions
[Part 5]: https://github.com/luvejo/rest-framework-tutorial/tree/5-relationships-and-hyperlinked-apis
[Part 6]: https://github.com/luvejo/rest-framework-tutorial/tree/6-viewsets-and-routers
[Part 7]: https://github.com/luvejo/rest-framework-tutorial/tree/7-schemas-and-client-libraries
[Heroku Sandbox]: http://restframework.herokuapp.com/
[Heroku Source]: https://github.com/luvejo/rest-framework-tutorial/tree/heroku-example
[Heroku-CLI]: https://devcenter.heroku.com/articles/heroku-cli#download-and-install
