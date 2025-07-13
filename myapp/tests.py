from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import ItemList, Items, Feedback, BookTable
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime


# ================================
# ✅ MODEL TESTS
# ================================

class ItemListModelTest(TestCase):
    def test_category_creation(self):
        category = ItemList.objects.create(Category_name='Drinks')
        self.assertEqual(category.Category_name, 'Drinks')
        self.assertEqual(str(category), 'Drinks')


class ItemsModelTest(TestCase):
    def setUp(self):
        self.category = ItemList.objects.create(Category_name='Snacks')
        self.item = Items.objects.create(
            Item_name='Burger',
            description='Tasty Veg Burger',
            Price=120,
            Category=self.category,
            Image=SimpleUploadedFile("burger.jpg", b"file_content")
        )

    def test_item_fields(self):
        self.assertEqual(self.item.Item_name, 'Burger')
        self.assertEqual(self.item.Price, 120)
        self.assertEqual(str(self.item), 'Burger')


class FeedbackModelTest(TestCase):
    def test_feedback_creation(self):
        feedback = Feedback.objects.create(
            User_name='Ravi',
            Description='Nice service!',
            Rating=5
        )
        self.assertEqual(feedback.Rating, 5)
        self.assertEqual(str(feedback), 'Ravi')


class BookTableModelTest(TestCase):
    def test_booking_creation(self):
        booking = BookTable.objects.create(
            Name='Pallavi',
            Phone_number=9876543210,
            Email='pallu@example.com',
            Total_person=3,
            Booking_date=datetime.date.today()
        )
        self.assertEqual(booking.Total_person, 3)
        self.assertEqual(str(booking), 'Pallavi')


# ================================
# ✅ VIEW TESTS
# ================================

class StaticPageTests(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('Home'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = self.client.get(reverse('About'))
        self.assertEqual(response.status_code, 200)

    def test_menu_view(self):
        response = self.client.get(reverse('Menu'))
        self.assertEqual(response.status_code, 200)

    def test_feedback_view(self):
        response = self.client.get(reverse('Feedback_Form'))
        self.assertEqual(response.status_code, 200)


# ================================
# ✅ BOOKING FORM TESTS
# ================================

class BookingTests(TestCase):
    def test_book_table_valid_post(self):
        response = self.client.post(reverse('Book_Table'), {
            'user_name': 'Ravi',
            'phone_number': '9876543210',
            'user_email': 'ravi@example.com',
            'total_person': '2',
            'booking_data': '2025-08-01'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(BookTable.objects.filter(Name='Ravi').exists())

    def test_book_table_invalid_post(self):
        response = self.client.post(reverse('Book_Table'), {
            'user_name': '',
            'phone_number': '123',
            'user_email': '',
            'total_person': '0',
            'booking_data': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BookTable.objects.count(), 0)


# ================================
# ✅ AUTH TESTS (LOGIN, LOGOUT, REGISTER)
# ================================

class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_valid_user(self):
        response = self.client.post(reverse('login_page'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_login_invalid_user(self):
        response = self.client.post(reverse('login_page'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout_page'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'Pallavi',
            'last_name': 'Sharma',
            'username': 'pallu',
            'password': 'secure123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/register/')
        self.assertTrue(User.objects.filter(username='pallu').exists())

    def test_register_duplicate_username(self):
        User.objects.create_user(username='pallu', password='existing')
        response = self.client.post(reverse('register'), {
            'first_name': 'Pallavi',
            'last_name': 'Sharma',
            'username': 'pallu',
            'password': 'secure123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/register/')
        self.assertEqual(User.objects.filter(username='pallu').count(), 1)
