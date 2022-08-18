# encoding: utf-8
import logging
import ckan.plugins as plugins
from ckan.lib.plugins import DefaultTranslation
from ckanext.useraffiliation import actions

log = logging.getLogger(__name__)


class UserAffiliationPlugin(
    plugins.SingletonPlugin, DefaultTranslation
):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config):
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
