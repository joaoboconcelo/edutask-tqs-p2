"""
SUÍTE DE TESTES DE SISTEMA E INTERFACE PONTA A PONTA (SELENIUM WEBDRIVER)
Projeto: EduTask Web v1.0.0-p2
UNISAGRADO - Ciência da Computação - Testes e Qualidade de Software
Responsável: João Lucas de Antonio Boconcelo
Total: 4 testes ponta a ponta (E2E) com esperas explícitas (WebDriverWait) e asserções visuais.
"""
import sys
import os
import time
import threading
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# Inclui caminho da aplicação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '01_SISTEMA_ALVO')))
from edutask.app import create_app

PORT = 5005
BASE_URL = f"http://127.0.0.1:{PORT}"

def run_test_server():
    app = create_app({'TESTING': True, 'SECRET_KEY': 'selenium-secret-2026'})
    app.run(host='127.0.0.1', port=PORT, debug=False, use_reloader=False)

class TestEduTaskSeleniumE2E(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=run_test_server, daemon=True)
        cls.server_thread.start()
        time.sleep(1.5)

        try:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1366,768")
            cls.driver = webdriver.Chrome(options=chrome_options)
        except Exception:
            edge_options = EdgeOptions()
            edge_options.add_argument("--headless=new")
            edge_options.add_argument("--disable-gpu")
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--window-size=1366,768")
            cls.driver = webdriver.Edge(options=edge_options)

        cls.driver.implicitly_wait(4)
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()

    def ensure_logged_in(self):
        """Garante sessão ativa"""
        self.driver.get(f"{BASE_URL}/")
        if "/login" in self.driver.current_url:
            email_input = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            password_input = self.driver.find_element(By.ID, "password")
            login_btn = self.driver.find_element(By.ID, "btn-login")
            
            email_input.clear()
            email_input.send_keys("aluno@unisagrado.edu.br")
            password_input.clear()
            password_input.send_keys("Senha@123")
            login_btn.click()
            self.wait.until(EC.presence_of_element_located((By.ID, "nav-dashboard")))

    # 1. E2E-01: Fluxo Completo de Autenticação / Login
    def test_01_fluxo_autenticacao_login(self):
        self.driver.get(f"{BASE_URL}/auth/logout")
        self.driver.get(f"{BASE_URL}/login")
        
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        password_input = self.driver.find_element(By.ID, "password")
        login_btn = self.driver.find_element(By.ID, "btn-login")
        
        email_input.clear()
        email_input.send_keys("aluno@unisagrado.edu.br")
        password_input.clear()
        password_input.send_keys("Senha@123")
        login_btn.click()
        
        dashboard_nav = self.wait.until(EC.presence_of_element_located((By.ID, "nav-dashboard")))
        self.assertIn("Dashboard", dashboard_nav.text)
        self.assertTrue(self.driver.find_element(By.ID, "card-total-tasks").is_displayed())

    # 2. E2E-02: Fluxo Completo de Cadastro de Nova Disciplina
    def test_02_fluxo_cadastrar_disciplina(self):
        self.ensure_logged_in()
        self.driver.get(f"{BASE_URL}/disciplinas/nova")
        
        code_input = self.wait.until(EC.presence_of_element_located((By.ID, "code")))
        name_input = self.driver.find_element(By.ID, "name")
        teacher_input = self.driver.find_element(By.ID, "teacher")
        workload_input = self.driver.find_element(By.ID, "workload_hours")
        submit_btn = self.driver.find_element(By.ID, "btn-save-discipline")
        
        unique_code = f"CC-E{int(time.time()) % 10000:04d}"
        code_input.clear()
        code_input.send_keys(unique_code)
        name_input.clear()
        name_input.send_keys("Laboratório de Testes Automatizados")
        teacher_input.clear()
        teacher_input.send_keys("Prof. Dr. Elvio Gilberto da Silva")
        workload_input.clear()
        workload_input.send_keys("80")
        submit_btn.click()
        
        table = self.wait.until(EC.presence_of_element_located((By.ID, "table-disciplines")))
        self.assertIn(unique_code, table.text)

    # 3. E2E-03: Fluxo Completo de Criação de Tarefa Acadêmica
    def test_03_fluxo_criar_tarefa(self):
        self.ensure_logged_in()
        self.driver.get(f"{BASE_URL}/tarefas/nova")
        
        title_input = self.wait.until(EC.presence_of_element_located((By.ID, "title")))
        due_input = self.driver.find_element(By.ID, "due_date")
        priority_select = Select(self.driver.find_element(By.ID, "priority"))
        disc_select = Select(self.driver.find_element(By.ID, "discipline_id"))
        submit_btn = self.driver.find_element(By.ID, "btn-save-task")
        
        unique_title = f"Atividade Selenium {int(time.time()) % 10000}"
        title_input.clear()
        title_input.send_keys(unique_title)
        
        self.driver.execute_script("arguments[0].value = '2026-11-30';", due_input)
        priority_select.select_by_visible_text("Alta")
        disc_select.select_by_index(1)
        
        submit_btn.click()
        
        tasks_table = self.wait.until(EC.presence_of_element_located((By.ID, "table-tasks")))
        self.assertIn(unique_title, tasks_table.text)

    # 4. E2E-04: Fluxo de Transição de Status e Validação no Dashboard
    def test_04_fluxo_transicao_status_e_dashboard(self):
        self.ensure_logged_in()
        self.driver.get(f"{BASE_URL}/tarefas")
        
        status_dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id, 'select-status')]")))
        Select(status_dropdown).select_by_visible_text("Concluída")
        
        self.driver.execute_script("arguments[0].closest('form').submit();", status_dropdown)
        
        self.wait.until(EC.presence_of_element_located((By.ID, "flash-alert")))
        
        self.driver.get(f"{BASE_URL}/")
        progress_bar = self.wait.until(EC.presence_of_element_located((By.ID, "progress-bar-completion")))
        self.assertTrue(progress_bar.is_displayed())
        self.assertIn("%", progress_bar.text)

if __name__ == '__main__':
    unittest.main()
