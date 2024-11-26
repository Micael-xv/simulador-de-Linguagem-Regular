import tkinter as tk
from tkinter import messagebox, scrolledtext, font

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

def converter_gramatica_para_automato(regras, simbolo_inicial):
    automato = Automato()
    for regra in regras:
        esquerda, direita = regra.split("->")
        esquerda = esquerda.strip()
        automato.adicionar_estado(esquerda, inicial=(esquerda == simbolo_inicial))
        producoes = direita.split("|")
        for producao in producoes:
            producao = producao.strip()
            if producao == "ε":
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
        self.janela.geometry("800x500")
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

        tk.Label(
            self.framePrincipal, text="Símbolo Inicial:", font=fonte_label, bg="#f5f5f5"
        ).grid(row=0, column=1, padx=10, sticky="w")
        self.simboloInicial = tk.Entry(self.framePrincipal, width=15)
        self.simboloInicial.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(
            self.framePrincipal, text="Cadeias (separadas por vírgula):", font=fonte_label, bg="#f5f5f5"
        ).grid(row=2, column=0, padx=10, sticky="w")
        self.cadeiasTeste = tk.Entry(self.framePrincipal, width=60)
        self.cadeiasTeste.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.botaoTestar = tk.Button(self.janela, text="Testar", command=self.executar_simulacao, bg="#4CAF50", fg="white", padx=10, pady=5)
        self.botaoTestar.pack(pady=10)

        tk.Label(
            self.framePrincipal, text="Resultados:", font=fonte_label, bg="#f5f5f5"
        ).grid(row=4, column=0, columnspan=2, pady=5)
        self.resultadoSaida = scrolledtext.ScrolledText(self.framePrincipal, width=70, height=10, state="disabled")
        self.resultadoSaida.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

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

if __name__ == "__main__":
    janela = tk.Tk()
    app = SimuladorGramatica(janela)
    janela.mainloop()
