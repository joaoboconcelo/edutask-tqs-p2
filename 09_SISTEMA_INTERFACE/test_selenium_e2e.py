"""Quatro fluxos reais de navegador com banco isolado e capturas verificáveis."""

import json
import os
import sys
import tempfile
import threading
import unittest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from werkzeug.serving import make_server

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "01_SISTEMA_ALVO"))
from edutask.app import create_app


class TestEduTaskSeleniumE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.app = create_app(
            {"TESTING": True, "SECRET_KEY": "e2e-only", "DATABASE": str(Path(cls.tempdir.name) / "e2e.db")}
        )
        cls.server = make_server("127.0.0.1", 0, cls.app)
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1366,900")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        if os.environ.get("CHROME_BINARY"):
            options.binary_location = os.environ["CHROME_BINARY"]
        service = (
            Service(executable_path=os.environ["CHROMEDRIVER"])
            if os.environ.get("CHROMEDRIVER")
            else Service()
        )
        try:
            cls.driver = webdriver.Chrome(service=service, options=options)
        except Exception:
            cls.server.shutdown()
            cls.tempdir.cleanup()
            raise
        cls.driver.set_page_load_timeout(30)
        cls.wait = WebDriverWait(cls.driver, 12)
        cls.evidence = ROOT / "09_SISTEMA_INTERFACE" / "evidencias"
        cls.evidence.mkdir(exist_ok=True)
        (cls.evidence / "navegador.json").write_text(
            json.dumps(cls.driver.capabilities, indent=2), encoding="utf-8"
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server.shutdown()
        cls.thread.join(timeout=5)
        cls.tempdir.cleanup()

    def login(self):
        self.driver.get(self.base_url + "/logout")
        self.driver.get(self.base_url + "/login")
        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        email.clear()
        password.clear()
        email.send_keys("aluno@unisagrado.edu.br")
        password.send_keys("Senha@123")
        self.driver.execute_script("arguments[0].value = arguments[1]", email, "aluno@unisagrado.edu.br")
        self.driver.execute_script("arguments[0].value = arguments[1]", password, "Senha@123")
        self.driver.execute_script('arguments[0].closest("form").requestSubmit()', password)
        self.wait.until(EC.presence_of_element_located((By.ID, "card-total-tasks")))

    def capture(self, name):
        self.driver.save_screenshot(str(self.evidence / f"{name}.png"))
        (self.evidence / f"{name}.html").write_text(self.driver.page_source, encoding="utf-8")

    def test_01_rf02_login_and_logout(self):
        self.login()
        self.assertIn("Dashboard", self.driver.find_element(By.ID, "nav-dashboard").text)
        self.assertTrue(self.driver.find_element(By.ID, "card-total-tasks").is_displayed())
        self.capture("E2E-01-login")
        self.driver.get(self.base_url + "/logout")
        self.driver.get(self.base_url + "/tarefas")
        self.assertIn("/login", self.driver.current_url)

    def test_02_rf03_create_discipline(self):
        self.login()
        self.driver.get(self.base_url + "/disciplinas/nova")
        for field, value in [
            ("code", "CC-E2E01"),
            ("name", "Disciplina E2E"),
            ("teacher", "Professor Teste"),
            ("workload_hours", "80"),
        ]:
            element = self.driver.find_element(By.ID, field)
            element.clear()
            element.send_keys(value)
            self.driver.execute_script('arguments[0].value = arguments[1]', element, value)
            self.assertEqual(element.get_attribute('value'), value)
        self.driver.execute_script('document.getElementById("form-discipline").requestSubmit()')
        table = self.wait.until(EC.presence_of_element_located((By.ID, "table-disciplines")))
        self.assertIn("CC-E2E01", table.text)
        self.assertIn("Disciplina E2E", table.text)
        self.capture("E2E-02-disciplina")

    def test_03_rf04_create_task(self):
        self.login()
        self.driver.get(self.base_url + "/tarefas/nova")
        self.driver.execute_script('document.getElementById("title").value = arguments[0]', 'Atividade E2E verificável')
        self.driver.execute_script(
            "arguments[0].value = '2026-11-30'", self.driver.find_element(By.ID, "due_date")
        )
        Select(self.driver.find_element(By.ID, "priority")).select_by_visible_text("Alta")
        Select(self.driver.find_element(By.ID, "discipline_id")).select_by_index(1)
        self.driver.execute_script('document.getElementById("form-task").requestSubmit()')
        table = self.wait.until(EC.presence_of_element_located((By.ID, "table-tasks")))
        self.assertIn("Atividade E2E verificável", table.text)
        self.capture("E2E-03-tarefa")

    def test_04_rf05_transition_and_exact_dashboard_rate(self):
        self.login()
        with self.app.test_client() as client:
            client.post("/api/auth/login", json={"email": "aluno@unisagrado.edu.br", "password": "Senha@123"})
            before = client.get("/api/metricas").json
        self.driver.get(self.base_url + "/tarefas")
        dropdowns = self.driver.find_elements(By.CSS_SELECTOR, "select[id*='select-status']")
        target = next(d for d in dropdowns if Select(d).first_selected_option.text != "Concluída")
        Select(target).select_by_visible_text("Concluída")
        self.driver.execute_script("arguments[0].closest('form').submit()", target)
        self.wait.until(EC.presence_of_element_located((By.ID, "flash-alert")))
        self.driver.get(self.base_url + "/")
        bar = self.wait.until(EC.presence_of_element_located((By.ID, "progress-bar-completion")))
        expected = round((before["completed_tasks"] + 1) / before["total_tasks"] * 100, 2)
        self.assertEqual(float(bar.get_attribute("aria-valuenow")), expected)
        self.assertIn(f"{expected}", bar.text)
        self.capture("E2E-04-dashboard")


if __name__ == "__main__":
    unittest.main()
