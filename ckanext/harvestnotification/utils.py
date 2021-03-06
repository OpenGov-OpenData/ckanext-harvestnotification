import ckan.plugins.toolkit as toolkit


def gather_sysadmin_recipients(model, exclude_username_list):
    """
    Gather email recipients from an sysadmin users who
    have email notifications enabled and are not in the exclusion list.
    """
    sysadmin_recipients = []
    sysadmins = model.Session.query(model.User).filter(
        model.User.sysadmin == True
    ).all()
    for sysadmin in sysadmins:
        if (sysadmin.email
            and sysadmin.activity_streams_email_notifications
            and sysadmin.name not in exclude_username_list):
            sysadmin_recipients.append({
                'name': sysadmin.name,
                'email': sysadmin.email
            })
    return sysadmin_recipients

def gather_org_admin_recipients(organization, exclude_username_list):
    """
    Gather email recipients from an organnization's admin users who
    have email notifications enabled and are not in the exclusion list.
    """
    org_admin_recipients = []
    members = toolkit.get_action('member_list')({'ignore_auth': True}, {
        'id': organization.get('id'),
        'object_type': 'user',
        'capacity': 'admin'
    })
    context = {'ignore_auth': True, 'keep_email': True}
    for member in members:
        member_details = toolkit.get_action('user_show')(context, {
            'id': member[0]
        })
        if (member_details.get('email')
            and member_details.get('activity_streams_email_notifications')
            and member_details.get('name') not in exclude_username_list):
            org_admin_recipients.append({
                'name': member_details['name'],
                'email': member_details['email']
            })
    return org_admin_recipients
