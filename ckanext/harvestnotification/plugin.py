import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.harvestnotification.logic import action

class HarvestNotificationPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)

    # IActions
    def get_actions(self):
        return {
            'harvest_get_notifications_recipients': action.harvest_get_notifications_recipients
        }
