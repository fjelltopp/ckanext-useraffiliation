import copy
import logging
from ckan.plugins import toolkit

log = logging.getLogger(__name__)

CUSTOM_FIELDS = [
    {"name": "job_title", "default": None},
    {"name": "affiliation", "default": None},
]

def _get_user_obj(context):
    if "user_obj" in context:
        user_obj = context["user_obj"]
    elif "model" in context and "user" in context:
        user_obj = context['model'].User.get(context['user'])
        
    if not user_obj:
        raise toolkit.ObjectNotFound("No user object could be found")
        
    return user_obj


def _commit_plugin_extras(context):
    if not context.get("defer_commit"):
        context['model'].Session.commit()


def check_plugin_extras_provided(data_dict):
    for field in CUSTOM_FIELDS:
        if field["name"] not in data_dict or data_dict.get(field["name"]) == '':
            raise toolkit.ValidationError(
                {field["name"]: ["Missing value"]}
            )

def _init_plugin_extras(plugin_extras):
    out_dict = copy.deepcopy(plugin_extras)
    if not out_dict:
        out_dict = {}
    if "useraffiliation" not in out_dict:
        out_dict["useraffiliation"] = {}
    return out_dict


def _add_to_plugin_extras(plugin_extras, data_dict):
    out_dict = copy.deepcopy(plugin_extras)
    for field in CUSTOM_FIELDS:
        out_dict["useraffiliation"][field["name"]] = data_dict.get(field["name"], field["default"])
    return out_dict


def _format_plugin_extras(plugin_extras):
    if not plugin_extras:
        plugin_extras = {}
    out_dict = {}
    for field in CUSTOM_FIELDS:
        out_dict[field["name"]] = plugin_extras.get(field["name"], field["default"])
    return out_dict

@toolkit.chained_action
def user_show(original_action, context, data_dict):
    user = original_action(context, data_dict)
    user_obj = _get_user_obj(context)

    extras = _init_plugin_extras(user_obj.plugin_extras)
    extras = _format_plugin_extras(extras["useraffiliation"])

    user.update(extras)
    return user


@toolkit.chained_action
def user_create(original_action, context, data_dict):
    check_plugin_extras_provided(data_dict)

    user = original_action(context, data_dict)
    user_obj = _get_user_obj(context)

    plugin_extras = _init_plugin_extras(user_obj.plugin_extras)
    plugin_extras = _add_to_plugin_extras(plugin_extras, data_dict)
    user_obj.plugin_extras = plugin_extras

    _commit_plugin_extras(context)

    user.update(plugin_extras["useraffiliation"])
    return user


@toolkit.chained_action
def user_update(original_action, context, data_dict):
    toolkit.check_access("user_update", context, data_dict)
    check_plugin_extras_provided(data_dict)

    user = original_action(context, data_dict)
    user_obj = _get_user_obj(context)

    plugin_extras = _init_plugin_extras(user_obj.plugin_extras)
    plugin_extras = _add_to_plugin_extras(plugin_extras, data_dict)
    print(plugin_extras)
    user_obj.plugin_extras = plugin_extras

    _commit_plugin_extras(context)

    user.update(plugin_extras["useraffiliation"])
    return user
