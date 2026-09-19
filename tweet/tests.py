from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Tweet
from .storage import ImageKitStorage


class StorageTests(TestCase):
    def test_imagekit_storage_url(self):
        storage = ImageKitStorage()
        # When name is full URL
        self.assertEqual(storage.url("https://ik.imagekit.io/demo/img.jpg"), "https://ik.imagekit.io/demo/img.jpg")
        # When name is relative path
        self.assertTrue(len(storage.url("photos/test.jpg")) > 0)


class TweetViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.tweet = Tweet.objects.create(user=self.user, text='Hello Tweeter on MongoDB!')

    def test_tweet_list_view(self):
        response = self.client.get(reverse('tweet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tweeter')
        self.assertContains(response, 'Hello Tweeter on MongoDB!')
        self.assertContains(response, '@testuser')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome Back')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an Account')

    def test_tweet_model_photo_url_helper(self):
        self.assertIsNone(self.tweet.photo_url)
        self.assertEqual(str(self.tweet), 'testuser - Hello Tweeter on Mon')
