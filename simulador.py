# -*- coding: utf-8 -*-
import tkinter as tk

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
        final_states = set()  # Usar um conjunto para rastrear estados finais
        for state, transitions in rules.items():
            for transition in transitions:
                symbol = transition[0]  # Primeiro caractere é o símbolo
                next_state = transition[1:] if len(transition) > 1 else None  # Se não houver próximo, é um estado final
                if state not in automaton:
                    automaton[state] = {}
                automaton[state][symbol] = next_state
                if next_state is None:  # Se não houver próximo, é um estado final
                    final_states.add(state)  # O estado atual é final
        return automaton, final_states
    
    def simulate_automaton(self, automaton, input_string, final_states):
        current_state = "S"
        for symbol in input_string:
            if symbol in automaton.get(current_state, {}):
                current_state = automaton[current_state][symbol]
            else:
                return False
        # Verifica se o estado atual após processar toda a string é um dos estados finais
        return current_state in final_states

    def analyze_string(self):
        grammar_text = self.grammar_input.get()
        input_string = self.string_input.get()
        
        # Parse e criar autômato
        rules = self.parse_grammar(grammar_text)
        automaton, final_states = self.generate_automaton(rules)
        
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
