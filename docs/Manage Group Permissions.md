# Manage group Permissions

Each app should contain a folder named `auth` with these files:

* `groups.py` that defines all app groups into distinct variables
* `policy.py` that defines what permissions each group should have.

## Assign group Permission

### Step 1: Assign groups into `auth/groups.py`

For example:

```python
AUTHOR="author"
EDITOR="editor"
```

This file contains a list of variables representing a group.

### Step 2: Create/update `auth/policy.py`

Each app has a `policy.py` that defines which permissions a group should have.

For example:

```python
from .groups import AUTHOR, EDITOR

POLICY = {
    AUTHOR: {
        "is_staff":True,
        "permissions":{
            "add_article",
            "change_article",
            "delete_article",
            "view_article"
        }
    },
    EDITOR: {
        "is_staff":True,
        "is_superuser":True,
        "permissions":{
            "change_article",
            "view_article",
            "add_user",
            "change_user"
            "delete_user"
        },
        "manage_groups":{
            AUTHOR
        }
    },
}
```

The policy is a dict containing:

* `is_staff`: An indication whether this group can have access on Django Admin
* `is_admin`: An indication whether this group can have access on Django Admin as admi user
* `permissions`: a list of permissions a user can have
* `manage_groups`: a list of allowed users belonging to the groups is allowed. 
  In order to manage user also should have one of the following permissions:
  * `add_user`
  * `change_user`
  * `delete_user`

Permissions are strings and can contain the default that django creates and stored upon `auth_permission`.
If you are creating your own place place them as meta upon the model for example:

```python

class Article(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    content=models.TextField()
    slug=models.SlugField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    class Meta:
        permissions = [
            ("create_article","Can create article"),
            ("update_article","Can update article"),
        ]
```

And run:

```commandline
python manage.py makemigration
python manage.py migrate
```

#### Step 3: Create groups and assign permission into each group:

Every time you create or update policy please run

```commandline
python manage.py sync_group_policies
```

# Availabvle Services

## Policy service

The command:

```commandline
python manage.py sync_group_policies
```

Uses the library `app_auth.services.PolicyService`, this is an injectable service that iterates all available policies and aggregates them into a single dict.
In order to use it you can injects them into your service:

```python

from injector import inject
from app_auth.services.policy_service import PolicyService


class Myservice:

    @inject
    def __init__(self, policy_service:PolicyService ):
        self.__policy_service = policy_service

    # Get the policy
    def my_function(self):
        policy = self.__policy_service.get_current_policy_aggregated()
        # Do stuff here
```

Keep in mind that upon admin you need to fetch the service from service container for example:

```python
from django.contrib import admin
from django.apps import apps
from django.http.response import Http404
from app_auth.models import User
from app_auth.services.policy_service import PolicyService

@admin.register(User)
class AdminUser(admin.ModelAdmin):

    @property
    def __policy_service(self) -> PolicyService:
        injector = apps.get_app_config("django_injector").injector
        return injector.get(PolicyService)

```

# Group service

Using `PolicyService` in order to manage groups though id kinda tedious. Common utilities regarding the  django groups and what are cappable of exist into `GroupService`.

You can use it by injecting into your service:

```python

from injector import inject
from app_auth.services.group_service import GroupService


class Myservice:

    @inject
    def __init__(self, group_service:GroupService ):
        self.__group_service = group_service

    # Get the policy
    def my_function(self):
        groups = self.__group_service.get_managed_groups(["ADMIN"])
        # Do stuff here
```

Keep in mind that upon admin you need to fetch the service from service container for example:

```python
from django.contrib import admin
from django.apps import apps
from django.http.response import Http404
from app_auth.models import User
from app_auth.services.group_service import GroupService

@admin.register(User)
class AdminUser(admin.ModelAdmin):

    @property
    def __group_service(self) -> GroupService:
        injector = apps.get_app_config("django_injector").injector
        return injector.get(GroupService)
```
