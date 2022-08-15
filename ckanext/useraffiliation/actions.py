import copy
import datetime
import logging
from ckan import model, logic
from ckan.plugins import toolkit

log = logging.getLogger(__name__)


def _get_user_obj(context):
    if "user_obj" in context:
        return context["user_obj"]
    user = context.get("user")
    m = context.get("model", model)
    user_obj = m.User.get(user)
    if not user_obj:
        raise toolkit.ObjectNotFound("User not found")
    return user_obj


@toolkit.chained_action
def user_show(up_func, context, data_dict):
    user = up_func(context, data_dict)
    user_obj = _get_user_obj(context)

    extras = _init_plugin_extras(user_obj.plugin_extras)
    extras = _validate_plugin_extras(extras["useraffiliation"])

    user["job_title"] = extras["job_title"]
    user["affiliation"] = extras["affiliation"]

    return user


@toolkit.chained_action
def user_create(up_func, context, data_dict):
    user = up_func(context, data_dict)
    user_obj = _get_user_obj(context)

    if not data_dict.get("job_title"):
        raise toolkit.ValidationError({"job_title": ["A job title must be provided."]})

    if not data_dict.get("affiliation"):
        raise toolkit.ValidationError(
            {"affiliation": ["An affiliation must be provided."]}
        )

    plugin_extras = _init_plugin_extras(user_obj.plugin_extras)
    plugin_extras["useraffiliation"]["affiliation"] = data_dict["affiliation"]
    plugin_extras["useraffiliation"]["job_title"] = data_dict["job_title"]
    user_obj.plugin_extras = plugin_extras

    if not context.get("defer_commit"):
        m = context.get("model", model)
        model.Session.commit()

    user["affiliation"] = plugin_extras["useraffiliation"]["affiliation"]
    user["job_title"] = plugin_extras["useraffiliation"]["job_title"]
    return user


@toolkit.chained_action
def user_update(up_func, context, data_dict):
    toolkit.check_access("user_update", context, data_dict)
    user = up_func(context, data_dict)
    user_obj = _get_user_obj(context)

    if not data_dict.get("job_title"):
        raise toolkit.ValidationError({"job_title": ["A job title must be provided."]})

    if not data_dict.get("affiliation"):
        raise toolkit.ValidationError(
            {"affiliation": ["An affiliation must be provided."]}
        )

    plugin_extras = _init_plugin_extras(user_obj.plugin_extras)
    plugin_extras["useraffiliation"]["affiliation"] = data_dict["affiliation"]
    plugin_extras["useraffiliation"]["job_title"] = data_dict["job_title"]
    user_obj.plugin_extras = plugin_extras

    if not context.get("defer_commit"):
        m = context.get("model", model)
        model.Session.commit()

    user["affiliation"] = plugin_extras["useraffiliation"]["affiliation"]
    user["job_title"] = plugin_extras["useraffiliation"]["job_title"]
    return user


def _init_plugin_extras(plugin_extras):
    out_dict = copy.deepcopy(plugin_extras)
    if not out_dict:
        out_dict = {}
    if "useraffiliation" not in out_dict:
        out_dict["useraffiliation"] = {}
    return out_dict


def _validate_plugin_extras(extras):
    CUSTOM_FIELDS = [
        {"name": "job_title", "default": ""},
        {"name": "affiliation", "default": None},
    ]
    if not extras:
        extras = {}
    out_dict = {}
    for field in CUSTOM_FIELDS:
        out_dict[field["name"]] = extras.get(field["name"], field["default"])
    return out_dict
