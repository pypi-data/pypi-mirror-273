# AsyncPOW - https://github.com/totaldebug/asyncpow
#
# Copyright (c) 2024 Steven Marks, Total Debug
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from aiohttp import ClientSession, hdrs
from yarl import URL

from asyncpow.models.common import UserSortOptions
from asyncpow.models.user import UserModel, UserResultsResponseModel
from asyncpow.utils.http import request


class User:
    """
    Initialize the User object with the base URL and API key.
    """

    def __init__(
        self, base_url: URL, api_key: str, session: ClientSession, raw_response: bool
    ) -> None:
        """
        Initialize the UserAPI object with the base URL and API key.

        Args:
            base_url (str): The base URL for the user API.
            api_key (str): The API key for authentication.
            session (ClientSession): HTTP Session.
            raw_response (bool): Return json if True.

        Returns:
            None
        """
        self.user_url = base_url.joinpath("user")
        self.api_key = api_key
        self.session = session
        self.raw_response = raw_response

    async def async_get_user(
        self,
        take: int = 20,
        skip: int = 0,
        sort: UserSortOptions = "created",
        id: int = None,
        raw_response: bool | None = None,
    ) -> dict | UserModel | list[UserModel]:
        """Get a user record, or all user records

        Args:
            take (int): limit number of records
            skip (int): skip number of records
            sort (_type_): sort records
            id (int, optional): User ID if it is known. Defaults to None.
            raw_response (bool, optional): return raw json. Defaults to None.

        Returns:
            dict | UserModel: Returns json dictionary or UserModel
        """
        if raw_response is None:
            raw_response = self.raw_response

        url = self.user_url.joinpath(str(id)) if id else self.user_url
        params = {"take": take, "skip": skip, "sort": sort}

        headers = {"X-Api-Key": self.api_key}
        response = await request(self.session, url, params=params, headers=headers)
        if raw_response:
            return response
        else:
            return UserModel(**response) if id else UserResultsResponseModel(**response)

    async def async_create_user(
        self, email: str, username: str, permissions: int, raw_response: bool | None = None
    ) -> dict | UserModel:
        """Create a new user

        Args:
            email (str): user email address
            username (str): username
            permissions (int): ID for the required permission
            raw_response (bool, optional): return raw json. Defaults to None.

        Returns:
            dict | UserModel: Returns json dictionary or UserModel
        """
        if raw_response is None:
            raw_response = self.raw_response

        req_data = {"email": email, "username": username, "permissions": permissions}

        headers = {"X-Api-Key": self.api_key, "Content-Type": "application/json"}
        response = await request(
            self.session,
            self.user_url,
            method=hdrs.METH_POST,
            json_data=req_data,
            headers=headers,
        )
        return response if raw_response else UserModel(**response)

    async def async_bulk_update_user(
        self, ids: list[int], permissions: int, raw_response: bool | None = None
    ) -> dict | list[UserModel]:
        """Update a list of users

        Args:
            ids (list[int]): List of user IDs to update
            permissions (int): Permission ID to change to
            raw_response (bool, optional): return raw json. Defaults to None.

        Returns:
            dict | list[UserModel]: Returns json dictionary or list of UserModel
        """
        if raw_response is None:
            raw_response = self.raw_response

        req_data = {"ids": ids, "permissions": permissions}

        headers = {"X-Api-Key": self.api_key, "Content-Type": "application/json"}
        response = await request(
            self.session,
            self.user_url,
            method=hdrs.METH_POST,
            json_data=req_data,
            headers=headers,
        )
        return response if raw_response else list[UserModel(**response)]
