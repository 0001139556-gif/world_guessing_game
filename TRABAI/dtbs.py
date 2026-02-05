import sqlite3
from datetime import datetime


class BancoDados:
    def __init__(self):
        self.conexao = sqlite3.connect("ranking.db")
        self.criar_tabela()

    def criar_tabela(self):
        cursor = self.conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jogador TEXT,
                pontos INTEGER,
                data TEXT
            )
        """)

        #Pra coluna "pontos" existir
        try:
            cursor.execute("SELECT pontos FROM ranking LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE ranking ADD COLUMN pontos INTEGER")

        self.conexao.commit()

    def salvar_recorde(self, jogador, pontos):
        cursor = self.conexao.cursor()
        cursor.execute(
            "INSERT INTO ranking (jogador, pontos, data) VALUES (?, ?, ?)",
            (jogador, pontos, datetime.now().strftime("%d/%m/%Y %H:%M"))
        )
        self.conexao.commit()

    def buscar_top_5(self):
        cursor = self.conexao.cursor()
        cursor.execute(
            "SELECT jogador, pontos, data FROM ranking ORDER BY pontos DESC LIMIT 5"
        )
        return cursor.fetchall()
