# Supercollect
#### Install
`pip install supercollect`
or
`poetry add supercollect`

Add `supercollect` to INSTALLED_APPS before `django.contrib.staticfiles`
```py
INSTALLED_APPS = [
    ...
    "supercollect",
    "django.contrib.staticfiles",
    ...
]
```
Set `STATIC_ROOT` setting

#### Usage
```py
python manage.py collectstatic --turbo
```

#### How
This package is built around a very simple idea. Perform collectstatic in a temporary local storage and upload all files in parallel after it's finished. Out of the box this should support any remote storage as well as manifest storages.  

```py
def collect(self):
    if collect_super_fast:
        self.storage = use_temporary_file_system_storage() # super.simple

    files_collected = super().collect() # super.collect
    
    if not collect_super_fast:
        return files_collected # super.pluggable

    self.storage = real_s3_storage
    multithreaded_upload() # super.fast
```
