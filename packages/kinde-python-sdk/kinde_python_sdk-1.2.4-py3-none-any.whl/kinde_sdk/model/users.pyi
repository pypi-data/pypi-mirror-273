# coding: utf-8

"""
    Kinde Management API

    Provides endpoints to manage your Kinde Businesses  # noqa: E501

    The version of the OpenAPI document: 1
    Contact: support@kinde.com
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from kinde_sdk import schemas  # noqa: F401


class Users(
    schemas.ListSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Array of users.
    """


    class MetaOapg:
        
        @staticmethod
        def items() -> typing.Type['User']:
            return User

    def __new__(
        cls,
        _arg: typing.Union[typing.Tuple['User'], typing.List['User']],
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'Users':
        return super().__new__(
            cls,
            _arg,
            _configuration=_configuration,
        )

    def __getitem__(self, i: int) -> 'User':
        return super().__getitem__(i)

from kinde_sdk.model.user import User
