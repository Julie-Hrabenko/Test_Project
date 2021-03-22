from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import HomePagesView, AboutPagesView, ServicesPagesView


class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'home')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_homepgage_url_resolves_homepagesview(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePagesView.as_view().__name__)


class AboutPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('about')
        self.response = self.client.get(url)

    def test_aboutpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_aboutpage_template(self):
        self.assertTemplateUsed(self.response, 'about.html')

    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, 'about')

    def test_aboutpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_aboutpage_url_resolves_aboutpagesview(self):
        view = resolve('/about/')
        self.assertEqual(view.func.__name__, AboutPagesView.as_view().__name__)


class ServicesPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('services')
        self.response = self.client.get(url)

    def test_servicespage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_servicespage_template(self):
        self.assertTemplateUsed(self.response, 'services.html')

    def test_servicespage_contains_correct_html(self):
        self.assertContains(self.response, 'services')

    def test_servicespage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_servicespgage_url_resolves_servicespagesview(self):
        view = resolve('/services/')
        self.assertEqual(view.func.__name__, ServicesPagesView.as_view().__name__)
