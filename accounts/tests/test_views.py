from unittest.mock import call
from unittest.mock import patch

from django.test import TestCase

import accounts.views


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'prorok29@vp.pl'
        })
        self.assertRedirects(response, '/')

    def test_sends_mail_to_address_from_post(self):
        self.send_mail_called = False

        def fake_send_mail(subject, body, from_email, to_list):
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list = to_list

        accounts.views.send_mail = fake_send_mail

        self.client.post('/accounts/send_login_email', data={
            'email': 'prorok29@vp.pl'
        })

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Your login link for Superlists')
        self.assertEqual(self.from_email, 'kontaktletsdoittom@gmail.com')
        self.assertEqual(self.to_list, ['prorok29@vp.pl'])

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email', data={
            'email': 'prorok29@vp.pl'
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'kontaktletsdoittom@gmail.com')
        self.assertEqual(to_list, ['prorok29@vp.pl'])

    def test_adds_success_message(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'prorok29@vp.pl'
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in."
        )
        self.assertEqual(message.tags, "success")

    @patch('accounts.views.messages')
    def test_adds_success_message_with_mocks(self, mock_messages):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'prorok29@vp.pl'
        })

        expected = "Check your email, we've sent you a link you can use to log in."
        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, expected),
        )


class LoginViewTest(TestCase):
    def test_redirects_to_home_page(self):
        respone = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(respone, '/')
