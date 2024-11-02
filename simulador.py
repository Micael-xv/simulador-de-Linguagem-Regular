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
                next_state = transition[1:] if len(transition) > 1 else "F"  # Estado final se não houver próximo
                if state not in automaton:
                    automaton[state] = {}
                automaton[state][symbol] = next_state
        return automaton

    def simulate_automaton(self, automaton, input_string):
        current_state = "S"
        for symbol in input_string:
            if symbol in automaton.get(current_state, {}):
                current_state = automaton[current_state][symbol]
            else:
                return False
        return current_state == "F"

    def analyze_string(self):
        grammar_text = self.grammar_input.get()
        input_string = self.string_input.get()
        
        # Parse e criar autômato
        rules = self.parse_grammar(grammar_text)
        automaton = self.generate_automaton(rules)
        
        # Simular autômato com a string
        is_valid = self.simulate_automaton(automaton, input_string)
        
        # Resultado
        if is_valid:
            self.result_label.config(text="A string é válida para a linguagem.", fg="green")
        else:
            self.result_label.config(text="A string NÃO é válida para a linguagem.", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    simulator = RegularLanguageSimulator(root)
    root.mainloop()
