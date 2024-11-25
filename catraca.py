import tkinter as tk
from tkinter import messagebox

class Catraca:
    def __init__(self, master):
        self.master = master
        self.estado = "Fechado"
        
        self.label = tk.Label(master, text="Estado da Catraca: Fechado")
        self.label.pack(pady=10)
        
        self.botao_cartao = tk.Button(master, text="Inserir Cartão", command=self.entrada_cartao)
        self.botao_cartao.pack(pady=5)
        
        self.botao_pagamento = tk.Button(master, text="Efetuar Pagamento", command=self.pagamento_efetuado)
        self.botao_pagamento.pack(pady=5)
        
        self.botao_passagem = tk.Button(master, text="Passar pela Catraca", command=self.passagem)
        self.botao_passagem.pack(pady=5)
    
    def entrada_cartao(self):
        if self.estado == "Fechado":
            self.estado = "Paga"
            self.label.config(text="Estado da Catraca: Cartão inserido")
            messagebox.showinfo("Catraca", "Cartão inserido. Aguardando pagamento...")
        else:
            messagebox.showwarning("Catraca", "Ação inválida. A catraca já está em outro estado.")
    
    def pagamento_efetuado(self):
        if self.estado == "Paga":
            self.estado = "Aberto"
            self.label.config(text="Estado da Catraca: Aberto")
            messagebox.showinfo("Catraca", "Pagamento efetuado. Catraca aberta.")
        else:
            messagebox.showwarning("Catraca", "Ação inválida. Não é necessário pagamento.")
    
    def passagem(self):
        if self.estado == "Aberto":
            self.estado = "Fechado"
            self.label.config(text="Estado da Catraca: Fechado")
            messagebox.showinfo("Catraca", "Passagem realizada. Catraca fechada.")
        else:
            messagebox.showwarning("Catraca", "Ação inválida. A catraca está fechada.")

# Interface
root = tk.Tk()
root.title("Sistema de Catraca do Shopping")
root.geometry("500x400")

app = Catraca(root)

root.mainloop()
