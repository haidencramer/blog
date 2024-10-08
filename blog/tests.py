from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post
from django.urls import reverse
# Create your tests here.

class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"

        ) 

        cls.post = Post.objects.create(
            title = "A Good Title",
            body = "Nice Body Content",
            author=cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, "A Good Title")
        self.assertEqual(self.post.body, "Nice Body Content")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "A Good Title")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nice Body Content")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detailview(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk" : self.post.pk}))
        no_response = self.client.get("/post/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "A Good Title")
        self.assertTemplateUsed(response, "post_detail.html")
