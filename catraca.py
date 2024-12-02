import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Catraca:
    def __init__(self, master):
        self.master = master
        self.estado = "Fechado"
        self.tentativas_senha = 0
        self.max_tentativas = 3
        
        self.label = tk.Label(master, text="Estado da Catraca: Fechado")
        self.label.pack(pady=10)
        
        self.frame_botoes_cartao = tk.Frame(master)
        self.frame_botoes_cartao.pack(pady=5)
        
        self.botao_cartao_com_saldo = tk.Button(self.frame_botoes_cartao, text="Utilizar Cartão com Saldo", command=self.entrada_cartao_com_saldo)
        self.botao_cartao_com_saldo.pack(side=tk.LEFT, padx=5)
        
        self.botao_cartao_sem_saldo = tk.Button(self.frame_botoes_cartao, text="Utilizar Cartão sem Saldo", command=self.entrada_cartao_sem_saldo)
        self.botao_cartao_sem_saldo.pack(side=tk.LEFT, padx=5)
        
        self.frame_botoes_senha = tk.Frame(master)
        self.frame_botoes_senha.pack(pady=5)
        
        self.botao_senha_correta = tk.Button(self.frame_botoes_senha, text="Inserir Senha Correta", command=self.senha_correta, state=tk.DISABLED)
        self.botao_senha_correta.pack(side=tk.LEFT, padx=5)
        
        self.botao_senha_incorreta = tk.Button(self.frame_botoes_senha, text="Inserir Senha Incorreta", command=self.senha_incorreta, state=tk.DISABLED)
        self.botao_senha_incorreta.pack(side=tk.LEFT, padx=5)
        
        self.botao_pagamento = tk.Button(master, text="Efetuar Pagamento", command=self.pagamento_efetuado, state=tk.DISABLED)
        self.botao_pagamento.pack(pady=5)
        
        self.botao_passagem = tk.Button(master, text="Passar pela Catraca", command=self.passagem, state=tk.DISABLED)
        self.botao_passagem.pack(pady=5)
        
        self.botao_reiniciar = tk.Button(master, text="Reiniciar Catraca", command=self.reinicializar)
        self.botao_reiniciar.pack(pady=5)
        
        self.log = tk.Text(master, state=tk.DISABLED, height=10, width=50)
        self.log.pack(pady=10)
    
    def log_acao(self, acao):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, f"{acao}\n")
        self.log.config(state=tk.DISABLED)
        self.log.see(tk.END)
    
    def entrada_cartao_com_saldo(self):
        if self.estado == "Fechado" or self.estado == "Cartão Recusado":
            self.estado = "Cartão Aceito"
            self.label.config(text="Estado da Catraca: Cartão Aceito")
            self.botao_senha_correta.config(state=tk.NORMAL)
            self.botao_senha_incorreta.config(state=tk.NORMAL)
            self.log_acao("Cartão com saldo aceito.")
            messagebox.showinfo("Catraca", "Cartão com saldo aceito. Por favor, insira a senha.")
        else:
            self.log_acao("Tentativa de inserir cartão com saldo falhou.")
            messagebox.showwarning("Catraca", "Ação inválida. A catraca já está em outro estado.")
    
    def entrada_cartao_sem_saldo(self):
        if self.estado == "Fechado" or self.estado == "Cartão Recusado":
            self.estado = "Cartão Recusado"
            self.label.config(text="Estado da Catraca: Cartão Recusado")
            self.log_acao("Cartão sem saldo recusado.")
            messagebox.showwarning("Catraca", "Cartão sem saldo recusado. Tente outro cartão.")
        else:
            self.log_acao("Tentativa de inserir cartão sem saldo falhou.")
            messagebox.showwarning("Catraca", "Ação inválida. A catraca já está em outro estado.")
    
    def senha_correta(self):
        if self.estado == "Cartão Aceito":
            self.estado = "Senha Correta"
            self.label.config(text="Estado da Catraca: Senha Correta")
            self.botao_senha_correta.config(state=tk.DISABLED)
            self.botao_senha_incorreta.config(state=tk.DISABLED)
            self.botao_pagamento.config(state=tk.NORMAL)
            self.log_acao("Senha correta inserida.")
            messagebox.showinfo("Catraca", "Senha correta. Por favor, efetue o pagamento.")
        else:
            self.log_acao("Tentativa de senha correta falhou.")
            messagebox.showwarning("Catraca", "Ação inválida. A catraca já está em outro estado.")
    
    def senha_incorreta(self):
        if self.estado == "Cartão Aceito":
            self.tentativas_senha += 1
            self.log_acao("Senha incorreta inserida.")
            messagebox.showwarning("Catraca", "Senha incorreta. Tente novamente.")
            self.verificar_tentativas_senha()
        else:
            self.log_acao("Tentativa de senha incorreta falhou.")
            messagebox.showwarning("Catraca", "Ação inválida. A catraca já está em outro estado.")
    
    def verificar_tentativas_senha(self):
        if self.tentativas_senha >= self.max_tentativas:
            self.estado = "Cartão Bloqueado"
            self.label.config(text="Estado da Catraca: Cartão Bloqueado")
            self.botao_senha_correta.config(state=tk.DISABLED)
            self.botao_senha_incorreta.config(state=tk.DISABLED)
            self.botao_pagamento.config(state=tk.DISABLED)
            self.log_acao("Número máximo de tentativas de senha atingido. Cartão bloqueado.")
            messagebox.showerror("Catraca", "Número máximo de tentativas de senha atingido. Cartão bloqueado.")
    
    def pagamento_efetuado(self):
        if self.estado == "Senha Correta":
            self.estado = "Aberto"
            self.label.config(text="Estado da Catraca: Aberto")
            self.botao_pagamento.config(state=tk.DISABLED)
            self.botao_passagem.config(state=tk.NORMAL)
            self.log_acao("Pagamento efetuado.")
            messagebox.showinfo("Catraca", "Pagamento efetuado. Catraca aberta.")
        else:
            self.log_acao("Tentativa de pagamento falhou.")
            messagebox.showwarning("Catraca", "Ação inválida. Não é necessário pagamento.")
    
    def passagem(self):
        if self.estado == "Aberto":
            self.estado = "Fechado"
            self.label.config(text="Estado da Catraca: Fechado")
            self.botao_passagem.config(state=tk.DISABLED)
            self.log_acao("Passagem realizada.")
            messagebox.showinfo("Catraca", "Passagem realizada.")
        else:
            self.log_acao("Tentativa de passagem falhou.")
            messagebox.showwarning("Catraca", "Ação inválida. A catraca não está aberta.")
    
    def reinicializar(self):
        self.estado = "Fechado"
        self.label.config(text="Estado da Catraca: Fechado")
        self.botao_senha_correta.config(state=tk.DISABLED)
        self.botao_senha_incorreta.config(state=tk.DISABLED)
        self.botao_pagamento.config(state=tk.DISABLED)
        self.botao_passagem.config(state=tk.DISABLED)
        self.tentativas_senha = 0
        self.log_acao("Catraca reinicializada.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulação de Catraca de Shopping")
    app = Catraca(root)
    root.mainloop()