from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import EmailChannel, PushChannel
from unittest.mock import patch, MagicMock

class ChannelsTestCase(TransactionTestCase):
	fixtures = ['users.json', 'environments.json']

	def setUp(self):
		pass

	def testChannelsCrud(self):
		with self.settings(ALLOWED_HOSTS=('example.com',)):
			self.client.force_login(get_user_model().objects.first())
			
			response = self.client.get(
				reverse('accounts:channel_list'),
				HTTP_HOST='example.com'
			)

			self.assertTemplateUsed(response, 'accounts/channel_list.html')
			self.assertNotContains(response, 'data-bs-target="#delete')
			
			self.assertContains(response, 'href="#form-add-emailchannel"')
			self.assertContains(response, 'href="#form-add-pushchannel"')

			
			self.assertRedirects(
				self.client.post(
					reverse('accounts:channel_create', kwargs={'type': 'emailchannel'}),
					{
						'host': 'example.com',
						'port': '465',
						'username': 'test',
						'password': 'password',
						'security': EmailChannel.SECURITY_TSL_SSL,
						'from_email': 'test@example.com',
						'enabled': True
					},
					HTTP_HOST='example.com'
				),
				reverse('accounts:channel_list')
			)
		

			PushChannel.get_firebase = lambda x: True
			self.assertRedirects(
				self.client.post(
					reverse('accounts:channel_create', kwargs={'type': 'pushchannel'}),
					{
						'firebase_credentials': '{"credentials":"yes please"}',
						'enabled': True
					},
					HTTP_HOST='example.com'
				),
				reverse('accounts:channel_list')
			)

			response = self.client.get(
				reverse('accounts:channel_list'),
				HTTP_HOST='example.com'
			)

			self.assertNotContains(response, 'href="#form-add-emailchannel"')
			self.assertNotContains(response, 'href="#form-add-pushchannel"')


			email_channel = EmailChannel.objects.get(site__domain='example.com')
			push_channel = PushChannel.objects.get(site__domain='example.com')


			self.assertRedirects(
				self.client.post(
					reverse('accounts:channel_update', kwargs={'pk': email_channel.pk }),
					{
						'host': 'example.com',
						'port': '465',
						'username': 'test',
						'password': 'password-updated',
						'security': EmailChannel.SECURITY_TSL_SSL,
						'from_email': 'test@example.com',
						'enabled': True
					},
					HTTP_HOST='example.com'
				),
				reverse('accounts:channel_list')
			)

			self.assertEquals('password-updated', EmailChannel.objects.first().password)


			self.assertRedirects(
				self.client.post(
					reverse('accounts:channel_update', kwargs={'pk': push_channel.pk }),
					{
						'firebase_credentials': '{"credentials":"updated-credentials"}',
						'enabled': True
					},
					HTTP_HOST='example.com'
				),
				reverse('accounts:channel_list')
			)

			self.assertEquals('updated-credentials', PushChannel.objects.first().firebase_credentials['credentials'])

			response = self.client.get(
				reverse('accounts:channel_list'),
				HTTP_HOST='example.com'
			)
			self.assertContains(response, f"Remove {push_channel}")
			self.assertContains(response, f"Remove {email_channel}")

			self.assertRedirects(
				self.client.post(
					reverse('accounts:channel_remove', kwargs={'pk': email_channel.pk}), HTTP_HOST='example.com'
				),
				reverse('accounts:channel_list')
			)

			self.assertRedirects(
				self.client.post(
					reverse('accounts:channel_remove', kwargs={'pk': push_channel.pk}), HTTP_HOST='example.com'
				),
				reverse('accounts:channel_list')
			)

			self.assertIsNone(EmailChannel.objects.first())
			self.assertIsNone(PushChannel.objects.first())
