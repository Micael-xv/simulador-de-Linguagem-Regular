import tkinter as tk
from tkinter import messagebox, scrolledtext, font
from graphviz import Digraph
import os

class Automato:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.transicoes = {}
        self.estadoInicial = None
        self.estadosDeAceitacao = set()

    def adicionar_estado(self, estado, inicial=False, aceitacao=False):
        self.estados.add(estado)
        if inicial:
            self.estadoInicial = estado
        if aceitacao:
            self.estadosDeAceitacao.add(estado)

    def adicionar_transicao(self, origem, simbolo, destino):
        if origem not in self.transicoes:
            self.transicoes[origem] = {}
        if simbolo not in self.transicoes[origem]:
            self.transicoes[origem][simbolo] = set()
        self.transicoes[origem][simbolo].add(destino)

    def validar_cadeia(self, cadeia):
        estados_atuais = {self.estadoInicial}
        for simbolo in cadeia:
            proximos_estados = set()
            for estado in estados_atuais:
                if estado in self.transicoes and simbolo in self.transicoes[estado]:
                    proximos_estados.update(self.transicoes[estado][simbolo])
            estados_atuais = proximos_estados
        return bool(estados_atuais & self.estadosDeAceitacao)

    def gerar_grafo(self, cadeia):
        dot = Digraph()
        for estado in self.estados:
            if estado == self.estadoInicial:
                dot.node(estado, shape='doublecircle', color='green')
            elif estado in self.estadosDeAceitacao:
                dot.node(estado, shape='doublecircle', color='red')
            else:
                dot.node(estado, shape='circle')

        for origem, transicoes in self.transicoes.items():
            for simbolo, destinos in transicoes.items():
                for destino in destinos:
                    dot.edge(origem, destino, label=simbolo)

        estados_atuais = {self.estadoInicial}
        for i, simbolo in enumerate(cadeia):
            proximos_estados = set()
            for estado in estados_atuais:
                if estado in self.transicoes and simbolo in self.transicoes[estado]:
                    proximos_estados.update(self.transicoes[estado][simbolo])
            estados_atuais = proximos_estados
            for estado in estados_atuais:
                dot.node(estado, color='blue')

        dot.render('automato', format='png', cleanup=True)
        return 'automato.png'

def converter_gramatica_para_automato(regras, simbolo_inicial):
    automato = Automato()
    for regra in regras:
        esquerda, direita = regra.split("->")
        esquerda = esquerda.strip()
        automato.adicionar_estado(esquerda, inicial=(esquerda == simbolo_inicial))
        producoes = direita.split("|")
        for producao in producoes:
            producao = producao.strip()
            if producao == "&":
                automato.adicionar_estado(esquerda, aceitacao=True)
            elif len(producao) == 1:  # Apenas terminal
                automato.adicionar_estado("final", aceitacao=True)
                automato.adicionar_transicao(esquerda, producao, "final")
            else:
                terminal, nao_terminal = producao[0], producao[1:]
                automato.adicionar_estado(nao_terminal)
                automato.adicionar_transicao(esquerda, terminal, nao_terminal)
    return automato


class SimuladorGramatica:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Simulador de Gramática e Autômato")
        self.janela.geometry("650x700")
        self.janela.configure(bg="#f5f5f5")

        fonte_titulo = font.Font(family="Helvetica", size=16, weight="bold")
        fonte_label = font.Font(family="Helvetica", size=12)

        titulo = tk.Label(
            self.janela, text="Simulador de Gramática e Autômato", font=fonte_titulo, bg="#f5f5f5", fg="#333"
        )
        titulo.pack(pady=10)

        self.framePrincipal = tk.Frame(self.janela, bg="#f5f5f5")
        self.framePrincipal.pack(pady=10, padx=10, fill="both", expand=True)

        tk.Label(
            self.framePrincipal, text="Gramática Regular:", font=fonte_label, bg="#f5f5f5"
        ).grid(row=0, column=0, padx=10, sticky="w")
        self.entradaGramatica = scrolledtext.ScrolledText(self.framePrincipal, width=40, height=10)
        self.entradaGramatica.grid(row=1, column=0, padx=10, pady=5)
        self.entradaGramatica.insert(tk.END, "S -> aA | bB\nA -> aS | &\nB -> bS | &")
        self.entradaGramatica.tag_configure("placeholder", foreground="grey")
        self.entradaGramatica.tag_add("placeholder", "1.0", "end")
        self.entradaGramatica.bind("<FocusIn>", self.clear_placeholder_gramatica)
        self.entradaGramatica.bind("<FocusOut>", self.add_placeholder_gramatica)

        tk.Label(
            self.framePrincipal, text="Símbolo Inicial:", font=fonte_label, bg="#f5f5f5"
        ).grid(row=0, column=1, padx=10, sticky="w")
        self.simboloInicial = tk.Entry(self.framePrincipal, width=15, fg="grey")
        self.simboloInicial.grid(row=1, column=1, padx=10, pady=5)
        self.simboloInicial.insert(0, "S")
        self.simboloInicial.bind("<FocusIn>", self.clear_placeholder_simbolo)
        self.simboloInicial.bind("<FocusOut>", self.add_placeholder_simbolo)

        tk.Label(
            self.framePrincipal, text="Cadeias (separadas por vírgula):", font=fonte_label, bg="#f5f5f5"
        ).grid(row=2, column=0, padx=10, sticky="w")
        self.cadeiasTeste = tk.Entry(self.framePrincipal, width=60, fg="grey")
        self.cadeiasTeste.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        self.cadeiasTeste.insert(0, "a, b, aa, ab, aaa, bbb, abab, baab, aabb")
        self.cadeiasTeste.bind("<FocusIn>", self.clear_placeholder_cadeias)
        self.cadeiasTeste.bind("<FocusOut>", self.add_placeholder_cadeias)

        self.botaoTestar = tk.Button(self.janela, text="Testar", command=self.executar_simulacao, bg="#4CAF50", fg="white", padx=10, pady=5)
        self.botaoTestar.pack(pady=10)

        self.botaoLimpar = tk.Button(self.janela, text="Limpar", command=self.limpar_campos, bg="#f44336", fg="white", padx=10, pady=5)
        self.botaoLimpar.pack(pady=10)

        tk.Label(
            self.framePrincipal, text="Resultados:", font=fonte_label, bg="#f5f5f5"
        ).grid(row=4, column=0, columnspan=2, pady=5)
        self.resultadoSaida = scrolledtext.ScrolledText(self.framePrincipal, width=70, height=10, state="disabled")
        self.resultadoSaida.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def clear_placeholder_gramatica(self, event):
        if self.entradaGramatica.get("1.0", tk.END).strip() == "S -> aA | bB\nA -> aS | &\nB -> bS | &":
            self.entradaGramatica.delete("1.0", tk.END)
            self.entradaGramatica.tag_remove("placeholder", "1.0", "end")
            self.entradaGramatica.config(fg="black")

    def add_placeholder_gramatica(self, event):
        if not self.entradaGramatica.get("1.0", tk.END).strip():
            self.entradaGramatica.insert(tk.END, "S -> aA | bB\nA -> aS | &\nB -> bS | &")
            self.entradaGramatica.tag_add("placeholder", "1.0", "end")
            self.entradaGramatica.config(fg="grey")

    def clear_placeholder_simbolo(self, event):
        if self.simboloInicial.get() == "S":
            self.simboloInicial.delete(0, tk.END)
            self.simboloInicial.config(fg="black")

    def add_placeholder_simbolo(self, event):
        if not self.simboloInicial.get():
            self.simboloInicial.insert(0, "S")
            self.simboloInicial.config(fg="grey")

    def clear_placeholder_cadeias(self, event):
        if self.cadeiasTeste.get() == "a, b, aa, ab, aaa, bbb, abab, baab, aabb":
            self.cadeiasTeste.delete(0, tk.END)
            self.cadeiasTeste.config(fg="black")

    def add_placeholder_cadeias(self, event):
        if not self.cadeiasTeste.get():
            self.cadeiasTeste.insert(0, "a, b, aa, ab, aaa, bbb, abab, baab, aabb")
            self.cadeiasTeste.config(fg="grey")

    def executar_simulacao(self):
        texto_gramatica = self.entradaGramatica.get("1.0", tk.END).strip()
        simbolo_inicial = self.simboloInicial.get().strip()
        cadeias_teste = self.cadeiasTeste.get().strip().split(",")

        if not texto_gramatica or not simbolo_inicial or not cadeias_teste:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        regras = texto_gramatica.splitlines()
        try:
            automato = converter_gramatica_para_automato(regras, simbolo_inicial)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar a gramática: {e}")
            return

        resultados = []
        for cadeia in cadeias_teste:
            cadeia = cadeia.strip()
            if automato.validar_cadeia(cadeia):
                resultados.append(f"'{cadeia}' -> Aceita")
            else:
                resultados.append(f"'{cadeia}' -> Rejeitada")

        self.resultadoSaida.config(state="normal")
        self.resultadoSaida.delete("1.0", tk.END)
        self.resultadoSaida.insert(tk.END, "\n".join(resultados))
        self.resultadoSaida.config(state="disabled")

        # Gerar e exibir o gráfico do autômato em uma nova janela
        if cadeias_teste:
            imagem = automato.gerar_grafo(cadeias_teste[0].strip())
            self.exibir_grafico(imagem)

    def exibir_grafico(self, imagem):
        nova_janela = tk.Toplevel(self.janela)
        nova_janela.title("Autômato")
        nova_janela.geometry("600x600")
        canvas = tk.Canvas(nova_janela, width=800, height=600, bg="#f5f5f5")
        canvas.pack()
        img = tk.PhotoImage(file=imagem)
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.image = img  # Manter uma referência da imagem para evitar que seja coletada pelo garbage collector

    def limpar_campos(self):
        self.entradaGramatica.delete("1.0", tk.END)
        self.entradaGramatica.insert(tk.END, "S -> aA | bB\nA -> aS | &\nB -> bS | &")
        self.entradaGramatica.tag_add("placeholder", "1.0", "end")
        self.entradaGramatica.config(fg="grey")
        self.simboloInicial.delete(0, tk.END)
        self.simboloInicial.insert(0, "S")
        self.simboloInicial.config(fg="grey")
        self.cadeiasTeste.delete(0, tk.END)
        self.cadeiasTeste.insert(0, "a, b, aa, ab, aaa, bbb, abab, baab, aabb")
        self.cadeiasTeste.config(fg="grey")
        self.resultadoSaida.config(state="normal")
        self.resultadoSaida.delete("1.0", tk.END)
        self.resultadoSaida.config(state="disabled")

if __name__ == "__main__":
    janela = tk.Tk()
    app = SimuladorGramatica(janela)
    janela.mainloop()