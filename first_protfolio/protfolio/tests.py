from django.test import TestCase, Client
from protfolio.models import Skill, Project, ContactMessage
from django.urls import reverse
from protfolio.forms import ContactForm  # Assuming you have this
# Create your tests here.


class ModelTests(TestCase):
    def test_skill_creation(self):
        skill = Skill.objects.create(
            name="Python",
            proficiency=90,
            category="webdev",
            icon="fa-python"
        )
        self.assertEqual(str(skill), "Python")  # Tests __str__
        self.assertTrue(skill.showcase)  # Tests default value

    def test_project_creation(self):
        project = Project.objects.create(
            title="My Portfolio Project",  # Explicitly include "Portfolio"
            description="Test description",
            start_date="2023-01-01"
        )
        self.assertEqual(str(project), "My Portfolio Project")  # Exact match
        # OR if you want partial matching:
        self.assertIn("Portfolio", project.title)
        self.assertEqual(project.project_type, "personal")  # Tests default
        self.assertIn("Portfolio", str(project))  # Tests __str__

    def test_contact_message(self):
        msg = ContactMessage.objects.create(
            name="John",
            email="john@test.com",
            message="Hello!"
        )
        self.assertEqual(msg.phone, "")  # Tests blank field
        self.assertTrue(msg.created_at)  # Tests auto_now_add


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(
            title="Test Project",
            description="Test",
            start_date="2023-01-01"
        )

    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portfolio")  # Check template

    def test_project_detail(self):
        url = reverse('project_detail', args=[self.project.id])
        response = self.client.get(url)
        self.assertContains(response, "Test Project")

    def test_contact_form_submission(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Alice',
            'email': 'alice@test.com',
            'message': "Hello! This is long enough.",
            'phone': ''  # Add this
        })
        self.assertEqual(response.status_code, 302)  # Should redirect

class FormTests(TestCase):
    def test_valid_contact_form(self):
        form = ContactForm(data={
            'name': "Bob",
            'email': "bob@test.com",
            'message': "Hello!"
        })
        self.assertTrue(form.is_valid())

    def test_valid_contact_form(self):
        form_data = {
            'name': "John Doe",  # Minimum 3 chars
            'email': "john@example.com",  # Valid email format
            'message': "This message is definitely long enough for validation.",  # 10+ chars
            'phone': "+1234567890"  # If required
        }
        form = ContactForm(data=form_data)
        if not form.is_valid():
            print("Form errors:", form.errors)  # Debug output
        self.assertTrue(form.is_valid())