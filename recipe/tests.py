from django.test import TestCase
from django.urls import reverse
from .models import Recipe, Category
from django.utils import timezone

class RecipeViewsTest(TestCase):
    def setUp(self):

        self.category = Category.objects.create(name='Soups')

        for i in range(12):
            Recipe.objects.create(
                title=f'Recipe {i}',
                description='Test description',
                instructions='Test instructions',
                ingredients='Test ingredients',
                category=self.category
            )

    def test_main_view_returns_200_and_renders_template(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

        self.assertTrue(len(response.context['recipes']) <= 10)

    def test_category_detail_view_returns_200_and_renders_template(self):
        response = self.client.get(reverse('category_detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_detail.html')

        self.assertEqual(len(response.context['recipes']), 12)

    def test_main_view_returns_different_recipes(self):
        first_response = self.client.get(reverse('main'))
        second_response = self.client.get(reverse('main'))

        titles_1 = set(r.title for r in first_response.context['recipes'])
        titles_2 = set(r.title for r in second_response.context['recipes'])

        self.assertNotEqual(titles_1, titles_2)

    def test_main_view_with_no_recipes(self):
        Recipe.objects.all().delete()
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes found.')

    def test_category_detail_with_no_recipes(self):
        Recipe.objects.all().delete()
        response = self.client.get(reverse('category_detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes found.')

