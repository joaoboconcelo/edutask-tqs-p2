"""
Módulo de regras de negócio de EduTask.
Contém regras puras de validação, cálculos de prazos, taxas e urgência.
Utilizado para testes unitários, testes de integração e prática de TDD.
"""
import re
from datetime import datetime, date

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
DISCIPLINE_CODE_REGEX = re.compile(r'^[A-Z]{2,4}-[A-Z0-9]{2,6}$')

def validate_email(email: str) -> bool:
    """Valida formato de e-mail institucional ou comum."""
    if not email or not isinstance(email, str):
        return False
    email = email.strip()
    if len(email) > 120 or len(email) < 5:
        return False
    return bool(EMAIL_REGEX.match(email))

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Valida política de senhas:
    - Mínimo de 8 caracteres
    - Pelo menos uma letra maiúscula
    - Pelo menos um dígito
    - Pelo menos um caractere especial (@$!%*?&#)
    """
    if not password or not isinstance(password, str):
        return False, "Senha não informada."
    if len(password) < 8:
        return False, "A senha deve conter no mínimo 8 caracteres."
    if not any(c.isupper() for c in password):
        return False, "A senha deve conter pelo menos uma letra maiúscula."
    if not any(c.isdigit() for c in password):
        return False, "A senha deve conter pelo menos um número."
    if not any(c in "@$!%*?&#^_-+=." for c in password):
        return False, "A senha deve conter pelo menos um caractere especial (@$!%*?&#...)."
    return True, "Senha válida."

def validate_discipline_code(code: str) -> bool:
    """
    Valida formato de código de disciplina:
    Exemplo: CC-TQS01, ENG-101, MAT-01
    """
    if not code or not isinstance(code, str):
        return False
    code = code.strip().upper()
    return bool(DISCIPLINE_CODE_REGEX.match(code))

def validate_workload(hours) -> bool:
    """Valida carga horária da disciplina: deve ser entre 15h e 400h."""
    try:
        val = int(hours)
        return 15 <= val <= 400
    except (ValueError, TypeError):
        return False

def calculate_completion_rate(total_tasks: int, completed_tasks: int) -> float:
    """Calcula taxa percentual de tarefas concluídas."""
    if not isinstance(total_tasks, int) or not isinstance(completed_tasks, int):
        raise TypeError("Valores devem ser inteiros.")
    if total_tasks < 0 or completed_tasks < 0:
        raise ValueError("Valores não podem ser negativos.")
    if completed_tasks > total_tasks:
        raise ValueError("Tarefas concluídas não podem exceder total.")
    if total_tasks == 0:
        return 0.0
    return round((completed_tasks / total_tasks) * 100.0, 2)

def calculate_task_urgency(due_date_str: str, current_date: date = None) -> tuple[int, str]:
    """
    Calcula nível e pontuação de urgência de uma atividade com base na data limite.
    Retorna: (score: int, level: str)
    
    Regras:
    - Dias restantes <= 0: Score 100, Nível: 'Crítica / Em Atraso'
    - Dias restantes 1 a 2: Score 75, Nível: 'Alta Urgência'
    - Dias restantes 3 a 7: Score 50, Nível: 'Média Urgência'
    - Dias restantes > 7: Score 25, Nível: 'Normal'
    """
    if not due_date_str:
        return 0, "Sem Data"
    
    if current_date is None:
        current_date = date.today()
        
    try:
        due_d = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Formato de data inválido. Use AAAA-MM-DD.")
        
    days_left = (due_d - current_date).days
    
    if days_left <= 0:
        return 100, "Crítica / Em Atraso"
    elif 1 <= days_left <= 2:
        return 75, "Alta Urgência"
    elif 3 <= days_left <= 7:
        return 50, "Média Urgência"
    else:
        return 25, "Normal"

def filter_task_list(tasks: list[dict], status: str = None, priority: str = None, search_term: str = None) -> list[dict]:
    """Filtra lista de tarefas conforme critérios."""
    filtered = tasks
    if status and status != 'Todos':
        filtered = [t for t in filtered if t.get('status') == status]
    if priority and priority != 'Todas':
        filtered = [t for t in filtered if t.get('priority') == priority]
    if search_term:
        term = search_term.strip().lower()
        filtered = [
            t for t in filtered 
            if term in t.get('title', '').lower() or term in t.get('description', '').lower()
        ]
    return filtered
