from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag
from recipe.serializers import TagSerializer

TAG_URL = reverse('recipe"list-tag')


def create_user(email='test@user.com', password='test123'):
    """Create and return user."""
    return get_user_model().objects.create_user(email, password)


class PublicTagApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_is_required(self):
        """Test auth is require"""
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):
    """Test authenticated api required"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()

        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Tets retrieve tags"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='dessert')
        res = self.client.get(TAG_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_tags_limited_to_user(self):
        user2 = create_user(email='test123@example.com', password='test123')
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort food')

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)
