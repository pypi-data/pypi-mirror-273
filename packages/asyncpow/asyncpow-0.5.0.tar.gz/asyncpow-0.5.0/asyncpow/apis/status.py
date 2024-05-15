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


from aiohttp import ClientSession
from yarl import URL

from asyncpow.models.status import StatusAppDataModel, StatusModel
from asyncpow.utils.http import request


class Status:
    """
    Class to interact with status-related endpoints.

    Initialize the Status object with the base URL, API key, and session.
    """

    def __init__(
        self, base_url: URL, api_key: str, session: ClientSession, raw_response: bool
    ) -> None:
        """
        Initialize the Status object with the base URL, API key, and session.

        Args:
            base_url (str): The base URL for the user API.
            api_key (str): The API key for authentication.
            session (ClientSession): HTTP Session.
            raw_response (bool): Return json if True.

        Returns:
            None
        """

        self.base_url = base_url.joinpath("status")
        self.api_key = api_key
        self.session = session
        self.raw_response = raw_response

    async def async_get_status(
        self,
        raw_response: bool | None = None,
    ) -> dict | StatusModel:
        """
        Summary:
            Asynchronously retrieves the status from the server.

        Args:
            raw_response (bool, optional): return raw json. Defaults to None.

        Returns:
            dict | StatusModel: The status information as either a dictionary or a StatusModel object.
        """
        if raw_response is None:
            raw_response = self.raw_response

        response = await request(self.session, self.base_url)
        return response if raw_response else StatusModel(**response)

    async def async_get_appdata(self, raw_response: bool = None) -> dict | StatusAppDataModel:
        """Retrieves the appdata from the server

        Args:
            raw_response (bool, optional): return raw json. Defaults to None.

        Returns:
            dict | StatusAppDataModel: The model object containing appdata items.
        """
        if raw_response is None:
            raw_response = self.raw_response

        url = self.base_url.joinpath("appdata")
        response = await request(self.session, url)
        return response if raw_response else StatusAppDataModel(**response)
