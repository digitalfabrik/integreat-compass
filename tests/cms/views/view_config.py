"""
This modules contains the config for the view tests
"""

from integreat_compass.cms.constants import offer_group_types, offer_mode_types

from ...conftest import ALL_ROLES, OFFER_PROVIDER, ROOT

#: This list contains the config for all views
#: Each element is a tuple which consists of two elements: A list of view configs and the keyword arguments that are
#: identical for all views in this list. Each view config item consists of the name of the view, the list of roles that
#: are allowed to access that view and optionally post data that is sent with the request. The post data can either be
#: a dict to send form data or a string to send JSON.
VIEWS = [
    (
        [
            ("cms:public:login", ALL_ROLES),
            ("cms:public:index", ALL_ROLES),
            ("cms:protected:new_offer", [ROOT, OFFER_PROVIDER]),
            (
                "cms:protected:new_offer",
                [ROOT, OFFER_PROVIDER],
                {
                    "offer_version-title": "Title",
                    "offer_version-description": "Description",
                    "offer_version-language": 2,
                    "offer_version-is_free": True,
                    "tags": [1],
                    "offer-group_type": offer_group_types.PRIVATE,
                    "offer-mode_type": offer_mode_types.HYBRID,
                    "location-address": "Address",
                    "location-lat": 1.000000,
                    "location-long": 1.000000,
                    "contact-name": "Contact Name",
                    "contact-email": "contact@email.com",
                    "contact-phone": "",
                    "organization-name": "OrgName",
                    "organization-web_address": "https://org.site",
                },
            ),
        ],
        {},
    ),
    (
        [
            (
                "cms:protected:edit_offer",
                [ROOT, OFFER_PROVIDER],
                {
                    "offer_version-title": "Title",
                    "offer_version-description": "Description",
                    "offer_version-language": 2,
                    "offer_version-is_free": True,
                    "tags": [1],
                    "offer-group_type": offer_group_types.PRIVATE,
                    "offer-mode_type": offer_mode_types.HYBRID,
                    "location-address": "Address",
                    "location-lat": 1.000000,
                    "location-long": 1.000000,
                    "contact-name": "Contact Name",
                    "contact-email": "contact@email.com",
                    "contact-phone": "",
                    "organization-name": "OrgName",
                    "organization-web_address": "https://org.site",
                },
            )
        ],
        {"pk": "1"},
    ),
]

#: In order for these views to be used as parameters, we have to flatten the nested structure
PARAMETRIZED_VIEWS = [
    (view_name, kwargs, post_data[0] if post_data else {}, roles)
    for view_conf, kwargs in VIEWS
    for view_name, roles, *post_data in view_conf
]
