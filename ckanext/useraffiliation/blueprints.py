# encoding: utf-8
from operator import index
import ckan.lib.helpers as h
from ckan.views.dashboard import index
from ckan.common import _, config, g
from flask import Blueprint
import logging

log = logging.getLogger(__name__)

useraffiliation = Blueprint(
    'useraffiliation',
    __name__,
)


def check_user_affiliation():
    """
    Check if user profile has affiliation and job title, as defined by this plugin.
    """
    try:
        # get user profile
        user_profile = g.userobj
    except:
        # assume if this fails that the user is not logged in?
        h.redirect_to(u'user.login')

    # does user profile have the required plugin extras item?
    hasUserAffiliationFields = 'useraffiliation' in user_profile.plugin_extras
    # does user have a job title and is it a string with content?
    hasJobTitle = 'job_title' in user_profile.plugin_extras.get('useraffiliation', {}) and user_profile.plugin_extras.get('useraffiliation', {}).get('job_title', '') != ''
    # does user have an affiliation and is it a string with content?
    hasAffiliation = 'affiliation' in user_profile.plugin_extras.get('useraffiliation', {}) and user_profile.plugin_extras.get('useraffiliation', {}).get('affiliation', '') != ''
    
    # if any of the above are false
    if not hasUserAffiliationFields or not hasJobTitle or not hasAffiliation:
        # redirect to user edit page
        return h.redirect_to(u'user.edit')
        
    # otherwise, carry on as normal (i.e. load the dashboard)
    # Note - this now ignores the ckan.route_after_login config setting, which is not ideal
    return index()


def get_route_to_intercept():
    """
    Get the route that should be intercepted
    """
    configured_route = config.get('ckan.route_after_login', 'dashboard.index')

    # the default is dashboard.index
    # however, and ".index"es will not get caught at, for example, "/dashboard/"
    # so we remove any ending ".index"
    if configured_route.endswith('.index'):
        configured_route = configured_route[:-6]
        
    # add the leading slash and convert and periods to slashes
    return '/' + configured_route.replace('.', '/')

useraffiliation.add_url_rule(
    get_route_to_intercept(),
    view_func=check_user_affiliation,
    methods=['GET']
)
