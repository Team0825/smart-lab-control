from django.test import TestCase

from .models import LoginRecord, Session, Student


class StudentLoginTests(TestCase):
    def test_successful_login_renders_success_page(self):
        student = Student.objects.create(
            registration_number="REG001",
            name="Test Student",
            department="Computer Science",
            semester=1
        )
        session = Session.objects.create(
            title="Morning Lab",
            code="123456",
            duration=60
        )

        response = self.client.post("/", {
            "registration": student.registration_number,
            "session_code": session.code
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "success.html")
        self.assertContains(response, "Welcome Test Student")
        self.assertEqual(
            LoginRecord.objects.filter(student=student, session=session).count(),
            1
        )

    def test_existing_login_still_renders_success_page(self):
        student = Student.objects.create(
            registration_number="REG001",
            name="Test Student",
            department="Computer Science",
            semester=1
        )
        session = Session.objects.create(
            title="Morning Lab",
            code="123456",
            duration=60
        )
        LoginRecord.objects.create(
            student=student,
            session=session,
            pc_name="TEST-PC",
            ip_address="127.0.0.1"
        )

        response = self.client.post("/", {
            "registration": student.registration_number,
            "session_code": session.code
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "success.html")
        self.assertContains(response, "Welcome Test Student")
        self.assertEqual(
            LoginRecord.objects.filter(student=student, session=session).count(),
            1
        )
