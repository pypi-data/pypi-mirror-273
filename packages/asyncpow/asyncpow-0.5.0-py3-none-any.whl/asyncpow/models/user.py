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


from pydantic import BaseModel

from asyncpow.models.common import PaginatedResponseModel


class UserSettingsModel(BaseModel):
    """User Settings Model"""

    id: int
    user: "UserModel"
    locale: str | None
    region: str | None
    originalLanguage: str | None
    pgpKey: str | None
    discordId: str | None
    pushbulletAccessToken: str | None
    pushoverApplicationToken: str | None
    pushoverUserKey: str | None
    pushoverSound: str | None
    telegramChatId: str | None
    telegramSendSilently: bool | None
    watchlistSyncMovies: bool | None
    watchlistSyncTv: bool | None


class UserPushSubscriptionModel(BaseModel):
    """User push sucscription model"""

    id: int
    user: "UserModel"
    endpoint: str
    p256dh: str
    auth: str


class UserModel(BaseModel):
    """User Model"""

    displayName: str
    id: int
    email: str
    plexUsername: str | None = None
    username: str | None = None
    password: str | None = None
    resetPasswordGuid: str | None = None
    recoveryLinkExpirationDate: str | None = None
    userType: int
    plexId: int | None = None
    plexToken: str | None = None
    permissions: int
    avatar: str
    requestCount: int
    requests: list[dict] | None = None  # TODO: should be requests model, but circular imports
    movieQuotaLimit: int | None = None
    movieQuotaDays: int | None = None
    tvQuotaLimit: int | None = None
    tvQuotaDays: int | None = None
    settings: UserSettingsModel | None = None
    pushSubscriptions: list[UserPushSubscriptionModel] | None = None
    createdIssues: list[dict] | None = None  # TODO: should be issues model, but circular imports
    createdAt: str
    updatedAt: str


class UserResultsResponseModel(PaginatedResponseModel):
    """
    Data class representing a user model.
    """

    results: list[UserModel]
