import json
import ckan.plugins.toolkit as toolkit
from ckan import model
from ckan.logic import check_access
from ckan.lib.base import config
from six import string_types
from ckanext.harvestnotification.utils import (
    gather_sysadmin_recipients,
    gather_org_admin_recipients
)

import logging
log = logging.getLogger(__name__)


@toolkit.chained_action
def harvest_get_notifications_recipients(original_action, context, data_dict):
    """
    Get all recipients for a harvest source
    Return a list of dicts like {'name': 'Jhon', 'email': 'jhon@source.com'}
    """
    check_access('harvest_get_notifications_recipients', context, data_dict)

    notify_sysadmin = config.get(
        'ckan.harvestnotification.notify_sysadmin', False
    )

    notify_organization_admin = config.get(
        'ckan.harvestnotification.notify_organization_admin', False
    )

    exclude_username_list = config.get(
        'ckan.harvestnotification.exclude_username_list', []
    )
    if exclude_username_list:
        if isinstance(exclude_username_list, string_types):
            try:
                exclude_username_list = json.loads(exclude_username_list)
            except ValueError:
                log.debug('exclude_username_list must be in JSON format')

    if not isinstance(exclude_username_list, list):
        log.debug('exclude_username_list must be a list of usernames')
        exclude_username_list = []

    source_id = data_dict['source_id']
    source = toolkit.get_action('harvest_source_show')({'ignore_auth': True}, {
        'id': source_id
    })
    recipients = []

    # gather sysadmins email recipients
    if notify_sysadmin:
        recipients = gather_sysadmin_recipients(
            context['model'],
            recipients,
            exclude_username_list
        )

    # gather the harvest source's organization admins email recipients
    if notify_organization_admin and source.get('organization'):
        recipients = gather_org_admin_recipients(
            source.get('organization'),
            recipients,
            exclude_username_list
        )

    return recipients
