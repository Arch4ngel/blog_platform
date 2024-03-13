from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.forms import PostForm
from blog.models import Post, Payment

User = get_user_model()


class BlogViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone='79991234567',
            nickname='tester',
            is_staff=True,
            is_active=True,
            is_superuser=False,
            is_subscribed=True
        )
        self.user.set_password('test')
        self.user.save()
        self.post_data = Post.objects.create(
            user=self.user,
            title='test_title',
            slug='test_slug',
            body='test_body')
        self.payment_data = Payment.objects.create(
            user=self.user,
            transaction_id='1',
            amount=100
        )
        self.client.force_login(self.user)

    def test_list_view(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post_data.title.encode('utf-8'), response.content)
        self.assertIn(self.post_data.user.nickname.encode('utf-8'), response.content)

    def test_detail_view(self):
        response = self.client.get(f'/view/{self.post_data.id}', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_view(self):
        data = {
            'pk': self.post_data.id,
            'user': self.user.id,
            'title': 'test_title',
            'body': 'test_body_updated',
            'image': None,
            'is_private': False
        }
        response = self.client.put(f'/edit/{self.post_data.id}', data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        form = PostForm(data=data, instance=self.post_data)
        form.save()
        self.assertEqual(self.post_data.body, 'test_body_updated')

    def test_delete_view(self):
        response = self.client.delete(f'/delete/{self.post_data.id}')
        self.assertEqual(response.status_code, 301)
