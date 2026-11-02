# Superuser and access controll


## Business rules
1. If a user has `is_superuser` flag `True` then is should be able tyo perform any action. Otherwise is should be allowed to perform the actions according to the policy.

2. Furthgermore, if a user is `is_superuser` it automatically is staff as well.

3. A user without a group having `is_superuser` as `True` it belongs to group `ADMIN`

## ModelAdmin permissions

Upon `ModelAdmin` you should always allow to perform any action if a user has `is_superuser` into `True`. That includes the methods:

* `has_add_permission`
* `has_change_permission`
* `has_delete_permission`
