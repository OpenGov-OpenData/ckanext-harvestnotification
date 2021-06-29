[![Tests](https://github.com/OpenGov/ckanext-harvestnotification/workflows/Tests/badge.svg?branch=main)](https://github.com/OpenGov/ckanext-harvestnotification/actions)

# ckanext-harvestnotification

This extension provides a plugin that adds configuration to specify the recipients of harvester email notifications.
Configuration for harvester email notifications from ckanext-harvest must be set to use this feature.
Users must also have email notifications enabled in their user settings.

## Requirements

This extension requires ckanext-harvest (https://github.com/ckan/ckanext-harvest) to be installed along with any of the following configuration options.

If you want to send an email when a Harvest Job fails, you can set the following configuration option in the ini file:

    ckan.harvest.status_mail.errored = True

If you want to send an email when completed Harvest Jobs finish (whether or not it failed), you can set the following configuration option in the ini file:

    ckan.harvest.status_mail.all = True


Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.7             | yes           |
| 2.8             | not tested    |
| 2.9             | not tested    |


## Installation

To install ckanext-harvestnotification:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Install ckanext-harvest (https://github.com/ckan/ckanext-harvest#installation)

3. Clone the source and install it on the virtualenv

    git clone https://github.com/OpenGov/ckanext-harvestnotification.git
    cd ckanext-harvestnotification
    pip install -e .
	pip install -r requirements.txt

4. Add `harvest_notification` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

If you want to send a harvest notifcation email to sysadmin users, you can set the following configuration option in the ini file. If you don't specify this setting, the default will be False.

    ckan.harvestnotification.notify_sysadmin = True


If the Harvest-Source of a Harvest-Job belongs to an organization, the error can also be sent to the organization admins if their email is configured. If you don't specify this setting, the default will be False.

    ckan.harvestnotification.notify_organization_admin = True

The following configuration option can be used to set a space-separated list of usernames that should be excluded from harvest emails, even if they are a sysadmin or org admin.

    ckan.harvestnotification.exclude_username_list = john_smith jane_doe


## Developer installation

To install ckanext-harvestnotification for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/OpenGov/ckanext-harvestnotification.git
    cd ckanext-harvestnotification
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-harvestnotification

If ckanext-harvestnotification should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags
