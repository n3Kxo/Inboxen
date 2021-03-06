##
#    Copyright (C) 2020 Jessica Tallon & Matt Molyneaux
#
#    This file is part of Inboxen.
#
#    Inboxen is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Inboxen is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Inboxen.  If not, see <http://www.gnu.org/licenses/>.
##

from django.conf import settings
from django.urls import reverse

from inboxen.account.middleware import ReturningSuspendedUser
from inboxen.test import InboxenTestCase, MockRequest
from inboxen.tests import factories


class MiddlewareTestCase(InboxenTestCase):
    def setUp(self):
        self.middleware = ReturningSuspendedUser(lambda request: {})

    def test_normal_user(self):
        user = factories.UserFactory()
        request = MockRequest(user)

        response = self.middleware(request)
        self.assertEqual(response, {})

    def test_suspended_user(self):
        user = factories.UserFactory()
        user.inboxenprofile.receiving_emails = False
        user.inboxenprofile.save()
        request = MockRequest(user)
        request.path = "/blah/blah"

        response = self.middleware(request)
        self.assertNotEqual(response, {})
        self.assertRedirects(response, "{}?next={}".format(reverse("user-returned"), "/blah/blah"),
                             fetch_redirect_response=False)

    def test_suspended_user_has_session_variable_set(self):
        user = factories.UserFactory()
        user.inboxenprofile.receiving_emails = False
        user.inboxenprofile.save()
        request = MockRequest(user)
        request.path = "/nah/nah"

        response = self.middleware(request)
        self.assertNotEqual(response, {})
        self.assertRedirects(response, "{}?next={}".format(reverse("user-returned"), "/nah/nah"),
                             fetch_redirect_response=False)
        self.assertEqual(request.session[settings.USER_SUSPENDED_SESSION_KEY], True)

        response = self.middleware(request)
        self.assertEqual(response, {})
        self.assertEqual(request.session[settings.USER_SUSPENDED_SESSION_KEY], True)

    def test_ajax_user(self):
        user = factories.UserFactory()
        user.inboxenprofile.receiving_emails = False
        user.inboxenprofile.save()
        request = MockRequest(user)
        request.META["HTTP_X_REQUESTED_WITH"] = "jQuery"

        response = self.middleware(request)
        self.assertEqual(response, {})


class ViewTestCase(InboxenTestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        login = self.client.login(username=self.user.username, password="123456", request=MockRequest(self.user))
        assert login

    def test_redirect_good(self):
        response = self.client.get("{}?next={}".format(reverse("user-returned"), "/fake"))
        self.assertEqual(response.context_data["next"], "/fake")

    def test_rediect_bad(self):
        response = self.client.get("{}?next={}".format(reverse("user-returned"), "https://django.com"))
        self.assertEqual(response.context_data["next"], reverse("user-home"))

    def test_login_required(self):
        self.client.logout()
        url = "{}?next={}".format(reverse("user-returned"), "/fake")
        response = self.client.get(url)
        self.assertRedirects(response, "{}?next={}".format(reverse("user-login"), url), fetch_redirect_response=False)

    def test_set_things(self):
        self.user.inboxenprofile.receiving_emails = False
        self.client.session[settings.USER_SUSPENDED_SESSION_KEY] = True

        self.client.get(reverse("user-returned"))
        self.assertEqual(self.client.session[settings.USER_SUSPENDED_SESSION_KEY], False)

        self.user.inboxenprofile.refresh_from_db()
        self.assertEqual(self.client.session[settings.USER_SUSPENDED_SESSION_KEY], False)
