import math
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from api import ServicoAPI
from dtbs import BancoDados


class JogoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("World Guessing Game")

        # Integração da API e Banco
        self.api = ServicoAPI()
        self.db = BancoDados()

        self.configurar_gui()
        self.nova_rodada()

    def configurar_gui(self):
        # Dica
        tk.Label(self.root, text="Dica: Capital do País").pack()
        self.lbl_capital = tk.Label(self.root, text="", font=("Arial", 14, "bold"))
        self.lbl_capital.pack(pady=5)

        # Nome do jogador
        tk.Label(self.root, text="Seu nome:").pack()
        self.ent_nome = tk.Entry(self.root)
        self.ent_nome.pack()

        # Palpite
        tk.Label(self.root, text="Qual é o país?").pack()
        self.ent_palpite = tk.Entry(self.root)
        self.ent_palpite.pack()

        # Botão
        self.btn_chutar = tk.Button(
            self.root,
            text="CHUTAR!",
            command=self.verificar_chute,
            bg="pink",
            fg="white"
        )
        self.btn_chutar.pack(pady=5)

        # Ranking 
        self.tree = ttk.Treeview(
            self.root,
            columns=("Jogador", "Pontuação", "Data"),
            show="headings"
        )
        self.tree.heading("Jogador", text="Jogador")
        self.tree.heading("Pontuação", text="Pontuação")
        self.tree.heading("Data", text="Data/Hora")
        self.tree.pack(pady=10)

        self.atualizar_tabela_visual()

    def nova_rodada(self):
        self.pais_atual = self.api.buscar_pais_aleatorio()

        if self.pais_atual:
            self.lbl_capital.config(text=self.pais_atual["capital"])
            self.inicio_tempo = datetime.now()
            self.ent_palpite.delete(0, tk.END)

    def verificar_chute(self):
        palpite = self.ent_palpite.get().strip()
        nome_jogador = self.ent_nome.get().strip()

        if not palpite or not nome_jogador:
            messagebox.showwarning("Atenção", "Preencha seu nome e o palpite.")
            return

        tempo_fim = datetime.now()
        tempo_gasto = max((tempo_fim - self.inicio_tempo).total_seconds(), 1)

        if palpite.lower() == self.pais_atual["nome"].lower():
            pontos_base = 1000 / tempo_gasto

            # Bônus matemático baseado da população 
            bonus = math.log(self.pais_atual["populacao"] + 1, 10)
            pontos_finais = math.floor(pontos_base / bonus)

            self.db.salvar_recorde(nome_jogador, pontos_finais)

            messagebox.showinfo(
                "Parabéns!",
                f"Você acertou vey!\nTempo: {tempo_gasto:.2f}s\nPontos: {pontos_finais}"
            )

            self.atualizar_tabela_visual()
            self.nova_rodada()
        else:
            messagebox.showerror("Erro", "País errado. Tente novamente.")

    def atualizar_tabela_visual(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for jogador in self.db.buscar_top_5():
            self.tree.insert("", tk.END, values=jogador)




