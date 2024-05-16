import os

from python_grains.profiles.profiles import Profile
from python_grains.profiles.stitches import Stitch, StitchPool
from python_grains.profiles.audiences import Audiences
from python_grains.profiles.profile_properties import (PROFILE_VALUE_CREATED_POSTFIX,
                                                       PROFILE_VALUE_UPDATED_POSTFIX,
                                                       PROFILE_VALUE_EXPIRE_AT_POSTFIX,
                                                       PROFILE_VALUE_POSTFIX)
from python_grains.profiles.lua import LuaScripts

def attach_profile_lua_scripts(redis_client,
                               user_ttl,
                               user_data_ttl_margin,
                               profile_ttl,
                               profile_ttl_margin,
                               new_user_detection_ttl):

    if not hasattr(redis_client, 'get_user_profile'):

        redis_client.get_user_profile = redis_client.register_script(
            LuaScripts.get_user_profile(
                value_postfix=PROFILE_VALUE_POSTFIX,
                updated_postfix=PROFILE_VALUE_UPDATED_POSTFIX,
                created_postfix=PROFILE_VALUE_CREATED_POSTFIX,
                expire_postfix=PROFILE_VALUE_EXPIRE_AT_POSTFIX))

    if not hasattr(redis_client, 'update_profile') and \
            not any(x is None for x in (user_ttl, user_data_ttl_margin)):

        redis_client.update_profile = redis_client.register_script(
            LuaScripts.update_profile(
                user_ttl=user_ttl,
                user_ttl_margin=user_data_ttl_margin,
                profile_ttl=profile_ttl,
                profile_ttl_margin=profile_ttl_margin,
                value_postfix=PROFILE_VALUE_POSTFIX,
                updated_postfix=PROFILE_VALUE_UPDATED_POSTFIX,
                created_postfix=PROFILE_VALUE_CREATED_POSTFIX,
                expire_postfix=PROFILE_VALUE_EXPIRE_AT_POSTFIX,
                new_user_detection_ttl=new_user_detection_ttl))

    if not hasattr(redis_client, 'get_all_user_pointers') and \
            not any(x is None for x in (user_ttl, user_data_ttl_margin)):

        redis_client.get_all_user_pointers = redis_client.register_script(
            LuaScripts.get_all_user_pointers(
                user_ttl=user_ttl,
                user_ttl_margin=user_data_ttl_margin
            ))

    if not hasattr(redis_client, 'set_profile_if_new_user') and \
            not any(x is None for x in (user_ttl, user_data_ttl_margin, new_user_detection_ttl)):

        redis_client.set_profile_if_new_user = redis_client.register_script(
            LuaScripts.set_profile_if_new_user(
                user_ttl=user_ttl,
                user_ttl_margin=user_data_ttl_margin,
                profile_ttl=profile_ttl,
                profile_ttl_margin=profile_ttl_margin,
                new_user_detection_ttl=new_user_detection_ttl
            ))

    if not hasattr(redis_client, 'completely_remove_from_cache'):

        redis_client.completely_remove_from_cache = redis_client.register_script(
            LuaScripts.completely_remove_from_cache())

    if not hasattr(redis_client, 'get_multiple_stitches'):

        redis_client.get_multiple_stitches = redis_client.register_script(
            LuaScripts.get_multiple_stitches())

    if not hasattr(redis_client, 'get_stitched_user_profile'):

        redis_client.get_stitched_user_profile = redis_client.register_script(
            LuaScripts.get_stitched_user_profile(
                value_postfix=PROFILE_VALUE_POSTFIX,
                updated_postfix=PROFILE_VALUE_UPDATED_POSTFIX,
                created_postfix=PROFILE_VALUE_CREATED_POSTFIX,
                expire_postfix=PROFILE_VALUE_EXPIRE_AT_POSTFIX
            ))

    if not hasattr(redis_client, 'switch_profiles') and \
            not any(x is None for x in (user_ttl, user_data_ttl_margin)):

        redis_client.switch_profiles = redis_client.register_script(
            LuaScripts.switch_profiles(
                user_ttl=user_ttl,
                user_ttl_margin=user_data_ttl_margin
            ))

    if not hasattr(redis_client, 'finalize_profile'):

        redis_client.finalize_profile = redis_client.register_script(
            LuaScripts.finalize_profile(local=bool(os.getenv('DJANGO_DEVELOPMENT'))))

    if not hasattr(redis_client, 'delete_in_cache'):

        redis_client.delete_in_cache = redis_client.register_script(
            LuaScripts.delete_in_cache())

    if not hasattr(redis_client, 'get_all_user_pointers_if_main_profile'):

        redis_client.get_all_user_pointers_if_main_profile = redis_client.register_script(
            LuaScripts.get_all_user_pointers_if_main_profile())

    return redis_client

def attach_stitch_lua_scripts(redis_client):

    if not hasattr(redis_client, 'get_multiple_stitches'):

        redis_client.get_multiple_stitches = redis_client.register_script(
            LuaScripts.get_multiple_stitches())

    if not hasattr(redis_client, 'get_stitched_user_profile'):

        redis_client.get_stitched_user_profile = redis_client.register_script(
            LuaScripts.get_stitched_user_profile(
                value_postfix=PROFILE_VALUE_POSTFIX,
                updated_postfix=PROFILE_VALUE_UPDATED_POSTFIX,
                created_postfix=PROFILE_VALUE_CREATED_POSTFIX,
                expire_postfix=PROFILE_VALUE_EXPIRE_AT_POSTFIX
            ))

    if not hasattr(redis_client, 'delete_stitched_user_profile'):

        redis_client.delete_stitched_user_profile = redis_client.register_script(
            LuaScripts.delete_stitched_user_profile()
        )

    if not hasattr(redis_client, 'remove_stitch_keys_from_pool'):

        redis_client.remove_stitch_keys_from_pool = redis_client.register_script(
            LuaScripts.remove_stitch_keys_from_pool()
        )

    if not hasattr(redis_client, 'remove_user_ids_from_stitch'):

        redis_client.remove_user_ids_from_stitch = redis_client.register_script(
            LuaScripts.remove_user_ids_from_stitch()
        )

    return redis_client

def getProfileClass(
        domain,
        fast_clean_threshold,
        redis_client,
        django_profile_model,
        django_pointer_model,
        django_connection_tuple,  # should contain (connection, connections) from django.db
        django_count_func,
        django_max_func,
        profile_ttl,
        profile_ttl_margin,
        user_ttl=None,
        user_data_ttl_margin=None,
        clean_queue_ttl=None,
        new_user_detection_ttl=None,
        max_stitch_keys=None):

    cls = Profile
    cls.domain = domain
    cls.fast_clean_threshold = fast_clean_threshold
    cls.redis_client = attach_profile_lua_scripts(redis_client=redis_client,
                                                  user_ttl=user_ttl,
                                                  user_data_ttl_margin=user_data_ttl_margin,
                                                  profile_ttl=profile_ttl,
                                                  profile_ttl_margin=profile_ttl_margin,
                                                  new_user_detection_ttl=new_user_detection_ttl)
    cls.django_profile_model = django_profile_model
    cls.django_pointer_model = django_pointer_model
    cls.django_connection_tuple = django_connection_tuple
    cls.django_count_func = django_count_func
    cls.django_max_func = django_max_func
    cls.profile_ttl = profile_ttl
    cls.profile_ttl_margin = profile_ttl_margin
    cls.user_ttl = user_ttl
    cls.user_data_ttl_margin = user_data_ttl_margin
    cls.clean_queue_ttl = clean_queue_ttl
    cls.max_stitch_keys = max_stitch_keys

    return cls

def getStitchClass(
        domain,
        redis_client,
        django_stitch_model,
        django_connection_tuple,
        user_ttl=None,
        user_data_ttl_margin=None,
        max_stitch_keys=None):

    cls = Stitch
    cls.domain = domain
    cls.redis_client = attach_stitch_lua_scripts(redis_client=redis_client)
    cls.django_stitch_model = django_stitch_model
    cls.django_connection_tuple = django_connection_tuple
    cls.user_ttl = user_ttl
    cls.user_data_ttl_margin = user_data_ttl_margin
    cls.max_stitch_keys = max_stitch_keys

    return cls


def getStitchPoolClass(
        domain,
        redis_client,
        django_stitch_pool_model,
        django_connection_tuple,
        user_ttl=None,
        user_data_ttl_margin=None):

    cls = StitchPool
    cls.domain = domain
    cls.redis_client = attach_stitch_lua_scripts(redis_client=redis_client)
    cls.django_stitch_pool_model = django_stitch_pool_model
    cls.django_connection_tuple = django_connection_tuple
    cls.user_ttl = user_ttl
    cls.user_data_ttl_margin = user_data_ttl_margin

    return cls

def getAudiencesClass(
        domain,
        redis_client,
        django_audience_model,
        django_connection_tuple,
        django_max_func,
        audience_ttl,
        audience_domains,
        default_audience_id_prefix,
        allowed_audience_fields):

    cls = Audiences
    cls.domain = domain
    cls.redis_client = redis_client
    cls.django_audience_model = django_audience_model
    cls.django_connection_tuple = django_connection_tuple
    cls.audience_ttl = audience_ttl
    cls.audience_domains = audience_domains
    cls.default_audience_id_prefix = default_audience_id_prefix
    cls.django_max_func = django_max_func
    cls.allowed_audience_fields = allowed_audience_fields

    return cls