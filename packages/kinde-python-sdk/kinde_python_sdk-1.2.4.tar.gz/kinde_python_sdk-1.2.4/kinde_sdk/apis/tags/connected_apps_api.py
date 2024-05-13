# coding: utf-8

"""
    Kinde Management API

    Provides endpoints to manage your Kinde Businesses  # noqa: E501

    The version of the OpenAPI document: 1
    Contact: support@kinde.com
    Generated by: https://openapi-generator.tech
"""

from kinde_sdk.paths.api_v1_connected_apps_auth_url.get import GetConnectedAppAuthUrl
from kinde_sdk.paths.api_v1_connected_apps_token.get import GetConnectedAppToken
from kinde_sdk.paths.api_v1_connected_apps_revoke.post import RevokeConnectedAppToken


class ConnectedAppsApi(
    GetConnectedAppAuthUrl,
    GetConnectedAppToken,
    RevokeConnectedAppToken,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
