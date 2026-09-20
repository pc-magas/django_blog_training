# Manage group Permissions

Each app should contain a folder named `auth` with these files:

* `permissions.py` that defines all app permission into a deistinct variables
* `groups.py` that defines all app groups into distinct variables
* `policy.py` that defines what permissions each group should have.


## Assign group Permission


### Step 1: Assign groups into `auth/groups.py`

For example:

```
AUTHOR="author"
EDITOR="editor"
```

This file contains a list of variables representing a group.

### Step 3: Create/update `auth/policy.py`

Each app has a `policy.py` that defines which permissions a group should have.

For example:

```
from .groups import AUTHOR, EDITOR


GROUP_PERMISSIONS = {
    AUTHOR: {
        ("add_article"),
        ("update_article")
    },
    EDITOR: {
        ("update_article"),
    },
}
```


### Step 4: Assign Policies upon models:

Then upon model you can assign your permissions:

```

class Article(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    content=models.TextField()
    slug=models.SlugField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    class Meta:
        permissions = [
            blog.auth.permissions.CREATE_ARTICLE,
            blog.auth.permissions.UPDATE_ARTICLE,
        ]
```

#### Step 5: Save permissions into db:

```
python manage.py makemigration
python manage.py migrate
python manage.py sync_group_policies
```

## Update Model permissions

Once you add a new permission upon a model run:

```
python manage.py makemigration
python manage.py migrate
python manage.py sync_group_policies
```


## Miscelanmous Notes:
1. The `sync_group_policies` would assign a permission upon group only if:
   1. A permission is assigned into a model as well.
   2. A permission is assigned ionto a group upon `auth/policy.py`
2. The django framework itself generates default permissions for each model. These permissions are not defined at `auth/permissions.py` unless you define them.
