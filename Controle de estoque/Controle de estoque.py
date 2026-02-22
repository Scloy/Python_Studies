import customtkinter as ctk
import json
import os

# --- 1. SISTEMA DE SALVAMENTO (JSON) ---
ARQUIVO_DADOS = "dados_estoque.json"

def carregar_estoque():
    """Lê o arquivo JSON. Se não existir, carrega o estoque padrão."""
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except Exception as e:
            print(f"Erro ao carregar os dados: {e}")
    
    # Estoque padrão caso seja a primeira vez abrindo o programa
    return {
        "Placa de vídeo": ["RTX 5060 Ti"],
        "Processador": ["Ryzen 5 5600"],
        "Placa Mãe": ["Asus TUF B550M"],
        "Memória RAM": ["Corsair 16GB"],
        "SSD": ["Kingston 1TB"],
        "Fonte": ["XPG 650W"]
    }

def salvar_estoque():
    """Grava o dicionário atual dentro do arquivo JSON."""
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(estoque, arquivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

# Carrega o estoque logo ao abrir o programa
estoque = carregar_estoque()

# --- 2. CONFIGURAÇÃO DA JANELA ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
# app.iconbitmap("TECH.ico")
app.title("Techlojinha - Gestão de Estoque")
app.geometry("600x750") 

# --- 3. FUNÇÕES DE LÓGICA ---

def atualizar_tela():
    caixa_exibicao.configure(state="normal")
    caixa_exibicao.delete("1.0", "end")
    
    texto = "📦 ESTOQUE ATUALIZADO:\n"
    texto += "-"*40 + "\n"
    
    for cat, lista_produtos in estoque.items():
        if lista_produtos:
            produtos_formatados = ", ".join(lista_produtos)
            texto += f"• {cat}: {produtos_formatados}\n"
    
    caixa_exibicao.insert("1.0", texto)
    caixa_exibicao.configure(state="disabled")

def adicionar():
    cat = entry_cat.get().strip()
    prod = entry_prod.get().strip()
    
    if cat and prod:
        if cat in estoque:
            estoque[cat].append(prod)
        else:
            estoque[cat] = [prod]
            
        salvar_estoque() # <--- Salva no SSD logo após adicionar
        atualizar_tela()
        entry_cat.delete(0, "end")
        entry_prod.delete(0, "end")

def vender():
    cat = entry_cat.get().strip()
    prod = entry_prod.get().strip()
    
    if not cat or not prod:
        caixa_exibicao.configure(state="normal")
        caixa_exibicao.delete("1.0", "end")
        caixa_exibicao.insert("1.0", "⚠️ ERRO: Digite a Categoria e o Produto para vender!\n")
        caixa_exibicao.configure(state="disabled")
        return
    
    if cat in estoque:
        if prod in estoque[cat]:
            estoque[cat].remove(prod)
            
            if not estoque[cat]:
                del estoque[cat]
                
            salvar_estoque() # <--- Salva no SSD logo após vender
            atualizar_tela()
            entry_cat.delete(0, "end")
            entry_prod.delete(0, "end")
        else:
            caixa_exibicao.configure(state="normal")
            caixa_exibicao.delete("1.0", "end")
            texto = f"❌ ERRO: O produto '{prod}' não foi encontrado em '{cat}'.\n\n"
            texto += "Dica: O nome deve ser escrito EXATAMENTE como está no estoque."
            caixa_exibicao.insert("1.0", texto)
            caixa_exibicao.configure(state="disabled")
    else:
        caixa_exibicao.configure(state="normal")
        caixa_exibicao.delete("1.0", "end")
        texto = f"❌ ERRO: A categoria '{cat}' não existe no estoque.\n\n"
        texto += "Dica: Verifique os acentos e as letras."
        caixa_exibicao.insert("1.0", texto)
        caixa_exibicao.configure(state="disabled")

def buscar_categoria():
    cat = entry_cat.get().strip()
    
    caixa_exibicao.configure(state="normal")
    caixa_exibicao.delete("1.0", "end")
    
    if not cat:
        atualizar_tela()
        return
        
    if cat in estoque:
        texto = f"🔍 RESULTADO DA BUSCA: [{cat}]\n"
        texto += "-"*40 + "\n"
        produtos_formatados = ", ".join(estoque[cat])
        texto += f"• Produtos: {produtos_formatados}\n"
    else:
        texto = f"❌ A categoria '{cat}' não foi encontrada no estoque.\n\n"
        texto += "Dica: Deixe o campo vazio e clique em 'Buscar Categoria' para ver tudo novamente."
        
    caixa_exibicao.insert("1.0", texto)
    caixa_exibicao.configure(state="disabled")

# --- 4. INTERFACE VISUAL (WIDGETS) ---

titulo = ctk.CTkLabel(app, text="Gerenciamento Techlojinha", font=("Arial", 24, "bold"))
titulo.pack(pady=20)

entry_cat = ctk.CTkEntry(app, placeholder_text="Categoria (ex: Processador)", width=400)
entry_cat.pack(pady=10)

entry_prod = ctk.CTkEntry(app, placeholder_text="Produto (ex: Ryzen 5 5600)", width=400)
entry_prod.pack(pady=10)

btn_add = ctk.CTkButton(app, text="Adicionar Peça", command=adicionar)
btn_add.pack(pady=5)

btn_vender = ctk.CTkButton(app, text="Vender Peça", command=vender, fg_color="indianred", hover_color="darkred")
btn_vender.pack(pady=5)

btn_buscar = ctk.CTkButton(app, text="Buscar Categoria", command=buscar_categoria, fg_color="seagreen", hover_color="darkgreen")
btn_buscar.pack(pady=5)

caixa_exibicao = ctk.CTkTextbox(app, width=500, height=300)
caixa_exibicao.pack(pady=20)

atualizar_tela()
app.mainloop()