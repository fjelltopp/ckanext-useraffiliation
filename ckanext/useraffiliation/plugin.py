# encoding: utf-8
import logging

from ckan.common import CKANConfig
import ckan.plugins as plugins
from ckan.lib.plugins import DefaultTranslation
from ckan.lib.plugins import DefaultPermissionLabels

from ckanext.useraffiliation import actions

log = logging.getLogger(__name__)


ALLOWED_ACTIONS = [
    "user_show",
    "user_create",
    "user_update",
]


class UserAffiliationPlugin(
    plugins.SingletonPlugin, DefaultTranslation, DefaultPermissionLabels
):
    plugins.implements(plugins.IActions)
    # plugins.implements(plugins.interfaces.IBlueprint)
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config: CKANConfig):
        # Add extension templates directory
        plugins.toolkit.add_template_directory(config, "templates")

    # IActions
    def get_actions(self):
        functions = {
            "user_show": actions.user_show,
            "user_create": actions.user_create,
            "user_update": actions.user_update,
        }
        return functions

    # IBlueprint
    # def get_blueprint(self):
    #     return actions.user_affiliation_blueprint
