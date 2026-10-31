import json
import unittest

from app import DATA_PATH, app, institute_slug


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with DATA_PATH.open(encoding="utf-8") as file:
            self.recruitments = json.load(file)

    def test_overview_renders_dashboard_and_navigation(self):
        response = self.client.get("/")
        html = response.get_data(as_text=True)
        open_count = sum(job["status"].lower() == "open" for job in self.recruitments)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Find where your", html)
        self.assertIn('href="/opportunities"', html)
        self.assertIn('href="/institutes"', html)
        self.assertIn(f">{open_count}</strong>", html)

    def test_opportunities_can_be_filtered(self):
        response = self.client.get("/opportunities?q=IIT+Delhi&status=open")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("IIT Delhi", html)
        self.assertNotIn("NIT Agartala", html)
        self.assertIn("1 result", html)

    def test_opportunities_show_empty_state_for_no_matches(self):
        response = self.client.get("/opportunities?q=not-a-real-institute")

        self.assertEqual(response.status_code, 200)
        self.assertIn("No matching opportunities", response.get_data(as_text=True))

    def test_institute_directory_and_detail(self):
        response = self.client.get("/institutes")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Indian Institutes of Technology", html)
        self.assertIn("National Institutes of Technology", html)
        self.assertEqual(html.count('class="institute-card"'), 32)

        detail = self.client.get("/institutes/iit-delhi")
        self.assertEqual(detail.status_code, 200)
        self.assertIn("IIT Delhi", detail.get_data(as_text=True))

    def test_every_listed_institute_has_a_detail_page(self):
        names = {job["institute"] for job in self.recruitments}
        for name in names:
            with self.subTest(institute=name):
                response = self.client.get(f"/institutes/{institute_slug(name)}")
                self.assertEqual(response.status_code, 200)

    def test_unknown_institute_returns_not_found(self):
        self.assertEqual(self.client.get("/institutes/not-an-institute").status_code, 404)

    def test_about_page_explains_refresh(self):
        response = self.client.get("/about")

        self.assertEqual(response.status_code, 200)
        self.assertIn("2:00 AM local machine time", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
