from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from ..views import home
from .models import Category, Commodity, TimeSeries, APISource

# Create your tests here.
class CategoryTests(TestCase):
    def setUp(self):
        Category.objects.create(name='Energy')

    def test_category_view_success_status_code(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_category_view_not_found_status_code(self):
        url = reverse('category-detail', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)


class BaseTemplateTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Energy')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_categories_page(self):
        commodity_tracker_url = reverse('categories')
        self.assertContains(self.response, 'href="{0}"'.format(commodity_tracker_url))    