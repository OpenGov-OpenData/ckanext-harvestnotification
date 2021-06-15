import pytest
from ckan import model
from ckan.tests import (
    helpers,
    factories
)
from ckanext.harvestnotification.utils import (
    gather_sysadmin_recipients,
    gather_org_admin_recipients
)

@pytest.mark.usefixtures("with_plugins")
@pytest.mark.ckan_config("ckan.plugins", "harvest harvestnotification")
class TestGatheringRecipients(object):

    @pytest.mark.usefixtures("clean_db")
    def test_gather_sysadmin_recipients(self):
        sysadmin1 = factories.Sysadmin(
            activity_streams_email_notifications = True,
            email = 'sysadmin1@example.com'
        )
        sysadmin2 = factories.Sysadmin(
            activity_streams_email_notifications = True,
            email = 'sysadmin2@example.com'
        )
        recipients = []
        exclude_username_list = []
        recipients = gather_sysadmin_recipients(model, recipients, exclude_username_list)
        assert len(recipients) == 2
        email_list = [i.get('email') for i in recipients]
        assert 'sysadmin1@example.com' in email_list
        assert 'sysadmin2@example.com' in email_list


    @pytest.mark.usefixtures("clean_db")
    def test_gather_sysadmin_recipients_with_exclusion(self):
        sysadmin3 = factories.Sysadmin(
            activity_streams_email_notifications = True,
            email = 'sysadmin3@example.com'
        )
        sysadmin4 = factories.Sysadmin(
            activity_streams_email_notifications = True,
            email = 'sysadmin4@example.com'
        )
        recipients = []
        exclude_username_list = [sysadmin3.get('name')]
        recipients = gather_sysadmin_recipients(model, recipients, exclude_username_list)
        assert len(recipients) == 1
        assert recipients[0]['email'] == 'sysadmin4@example.com'


    @pytest.mark.usefixtures("clean_db")
    def test_gather_sysadmin_recipients_with_disabled_notifications(self):
        sysadmin5 = factories.Sysadmin(
            activity_streams_email_notifications = True,
            email = 'sysadmin5@example.com'
        )
        sysadmin6 = factories.Sysadmin(
            activity_streams_email_notifications = False,
            email = 'sysadmin6@example.com'
        )
        recipients = []
        exclude_username_list = [sysadmin5.get('name')]
        recipients = gather_sysadmin_recipients(model, recipients, exclude_username_list)
        assert len(recipients) == 1
        assert recipients[0]['email'] == 'sysadmin6@example.com'


    @pytest.mark.usefixtures("clean_db", "with_request_context")
    def test_gather_org_admin_recipients(self):
        user1 = factories.User(
            activity_streams_email_notifications = True,
            email = 'user1@example.com'
        )
        user2 = factories.User(
            activity_streams_email_notifications = True,
            email = 'user2@example.com'
        )
        org = factories.Organization(users=[
            {'name': user1['id'], 'capacity': 'admin'},
            {'name': user2['id'], 'capacity': 'admin'}
        ])
        recipients = []
        exclude_username_list = []
        recipients = gather_org_admin_recipients(org, recipients, exclude_username_list)
        assert len(recipients) == 2
        email_list = [i.get('email') for i in recipients]
        assert 'user1@example.com' in email_list
        assert 'user2@example.com' in email_list


    @pytest.mark.usefixtures("clean_db", "with_request_context")
    def test_gather_org_admin_recipients_with_exclusion(self):
        user3 = factories.User(
            activity_streams_email_notifications = True,
            email = 'user3@example.com'
        )
        user4 = factories.User(
            activity_streams_email_notifications = True,
            email = 'user4@example.com'
        )
        org = factories.Organization(users=[
            {'name': user3['id'], 'capacity': 'admin'},
            {'name': user4['id'], 'capacity': 'admin'}
        ])
        recipients = []
        exclude_username_list = [user3.get("name")]
        recipients = gather_org_admin_recipients(org, recipients, exclude_username_list)
        assert len(recipients) == 1
        assert recipients[0]['email'] == 'user4@example.com'


    @pytest.mark.usefixtures("clean_db", "with_request_context")
    def test_gather_org_admin_recipients_with_disabled_notifications(self):
        user5 = factories.User(
            activity_streams_email_notifications = True,
            email = 'user5@example.com'
        )
        user6 = factories.User(
            activity_streams_email_notifications = False,
            email = 'user6@example.com'
        )
        org = factories.Organization(users=[
            {'name': user5['id'], 'capacity': 'admin'},
            {'name': user6['id'], 'capacity': 'admin'}
        ])
        recipients = []
        exclude_username_list = [user5.get("name")]
        recipients = gather_org_admin_recipients(org, recipients, exclude_username_list)
        assert len(recipients) == 1
        assert recipients[0]['email'] == 'user6@example.com'