from datetime import datetime

"""
Módulo com funções para logging.
"""

def logger(log_path: str, logging_level: str, log_entry: str):
    """
    Função para logar informações em um arquivo. Formatação [datetime | logging_level] logging_entry
    log_path = Caminho de arquivo .log/.txt.
    logging_level = Níveis usados geralmente INFO, DEBUG, WARNING, ERROR, FATAL/SEVERE.
    logging_entry = Mensagem a ser adicionada.
    """
    with open(log_path, 'a', encoding = 'utf-8') as log:
        message = f"[{datetime.now()} | {logging_level.upper()}] {log_entry}\n"
        log.write(message) 