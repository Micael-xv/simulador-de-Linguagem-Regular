# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

class RegularLanguageSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulador de Linguagem Regular")

        # Definição da Gramática
        tk.Label(master, text="Defina as Produções da Gramática (ex: S->aA;A->bB;B->c)").pack()
        self.grammar_input = tk.Entry(master, width=50)
        self.grammar_input.pack()

        # Entrada dos Estados Finais
        tk.Label(master, text="Defina os Estados Finais (ex: A,B):").pack()
        self.final_states_input = tk.Entry(master, width=50)
        self.final_states_input.pack()

        # Entrada da String
        tk.Label(master, text="String a ser analisada:").pack()
        self.string_input = tk.Entry(master, width=50)
        self.string_input.pack()

        # Botão de Análise
        tk.Button(master, text="Analisar String", command=self.analyze_string).pack()

        # Resultado
        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def parse_grammar(self, grammar_text):
        rules = {}
        productions = grammar_text.split(";")
        for production in productions:
            production = production.strip()  # Remove espaços em branco
            if "->" not in production:
                continue  # Ignora produções que não estão no formato esperado
            left, right = production.split("->")
            if left not in rules:
                rules[left] = []
            rules[left].append(right)
        return rules

    def generate_automaton(self, rules):
        automaton = {}
        for state, transitions in rules.items():
            for transition in transitions:
                symbol = transition[0]  # Primeiro caractere é o símbolo
                next_state = transition[1:] if len(transition) > 1 else None
                if state not in automaton:
                    automaton[state] = {}
                if symbol not in automaton[state]:
                    automaton[state][symbol] = []
                automaton[state][symbol].append(next_state)
        return automaton

    def simulate_automaton(self, automaton, input_string, final_states):
        def dfs(state, index):
            # Se processamos toda a string, verifica se estamos em um estado final
            if index == len(input_string):
                return state in final_states
            
            # Obter o símbolo atual da string
            symbol = input_string[index]
            
            # Verifica se há transições válidas para o estado atual
            if state not in automaton or symbol not in automaton[state]:
                return False
            
            # Explora todas as transições possíveis para o símbolo atual
            for next_state in automaton[state][symbol]:
                if next_state is not None and dfs(next_state, index + 1):
                    return True
            
            return False

        return dfs("S", 0)

    def analyze_string(self):
        grammar_text = self.grammar_input.get()
        input_string = self.string_input.get()
        final_states_text = self.final_states_input.get()

        if not grammar_text or not input_string or not final_states_text:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        # Parse e criar autômato
        rules = self.parse_grammar(grammar_text)
        final_states = set(final_states_text.split(","))
        automaton = self.generate_automaton(rules)

        # Simular autômato com a string
        is_valid = self.simulate_automaton(automaton, input_string, final_states)

        # Resultado
        if is_valid:
            self.result_label.config(text="A string é válida para a linguagem.", fg="green")
        else:
            self.result_label.config(text="A string NÃO é válida para a linguagem.", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    simulator = RegularLanguageSimulator(root)
    root.mainloop()
