"""Conversor DWG <-> DXF: janela de arrastar e soltar em cima do ODA File Converter (gratuito, oficial)."""

import glob
import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from tkinterdnd2 import DND_FILES, TkinterDnD

VERSOES_DWG = [
    "ACAD2018",
    "ACAD2013",
    "ACAD2010",
    "ACAD2007",
    "ACAD2004",
    "ACAD2000",
    "ACAD14",
]


def localizar_conversor():
    candidatos = glob.glob(r"C:\Program Files\ODA\ODAFileConverter*\ODAFileConverter.exe")
    candidatos += glob.glob(r"C:\Program Files (x86)\ODA\ODAFileConverter*\ODAFileConverter.exe")
    return candidatos[0] if candidatos else None


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor DWG ⇄ DXF")
        self.root.geometry("460x420")
        self.root.resizable(False, False)

        self.pasta_origem = tk.StringVar(value="")
        self.direcao = tk.StringVar(value="dwg2dxf")
        self.versao_dwg = tk.StringVar(value="ACAD2018")
        self.recursivo = tk.BooleanVar(value=True)

        self._montar_ui()
        self.exe = localizar_conversor()
        if not self.exe:
            messagebox.showerror(
                "ODA File Converter não encontrado",
                "Não achei o ODAFileConverter.exe instalado. Reinstale com:\n"
                "winget install --id ODA.ODAFileConverter -e",
            )

    def _montar_ui(self):
        pad = {"padx": 16, "pady": 8}

        titulo = tk.Label(self.root, text="Conversor DWG ⇄ DXF", font=("Segoe UI", 14, "bold"))
        titulo.pack(pady=(14, 0))

        sub = tk.Label(
            self.root,
            text="Converte TODOS os arquivos da pasta (use uma pasta só com o que quer converter)",
            font=("Segoe UI", 8),
            fg="#666",
        )
        sub.pack()

        self.drop_zone = tk.Label(
            self.root,
            text="Arraste aqui uma pasta\n(ou clique para escolher)",
            font=("Segoe UI", 11),
            bg="#f2f2f2",
            fg="#444",
            relief="ridge",
            bd=2,
            width=46,
            height=6,
            justify="center",
        )
        self.drop_zone.pack(**pad)
        self.drop_zone.drop_target_register(DND_FILES)
        self.drop_zone.dnd_bind("<<Drop>>", self._on_drop)
        self.drop_zone.bind("<Button-1>", lambda e: self._escolher_pasta())

        self.label_pasta = tk.Label(self.root, text="Nenhuma pasta selecionada", font=("Segoe UI", 8), fg="#888")
        self.label_pasta.pack()

        frame_direcao = tk.LabelFrame(self.root, text="Direção", padx=10, pady=6)
        frame_direcao.pack(fill="x", **pad)
        tk.Radiobutton(
            frame_direcao, text="DWG → DXF", variable=self.direcao, value="dwg2dxf", command=self._atualizar_versao
        ).pack(side="left", padx=10)
        tk.Radiobutton(
            frame_direcao, text="DXF → DWG", variable=self.direcao, value="dxf2dwg", command=self._atualizar_versao
        ).pack(side="left", padx=10)

        frame_opcoes = tk.Frame(self.root)
        frame_opcoes.pack(fill="x", **pad)

        self.label_versao = tk.Label(frame_opcoes, text="Versão do AutoCAD (saída DWG):")
        self.combo_versao = ttk.Combobox(frame_opcoes, textvariable=self.versao_dwg, values=VERSOES_DWG, state="readonly", width=14)

        tk.Checkbutton(frame_opcoes, text="Incluir subpastas", variable=self.recursivo).pack(side="left")

        self._atualizar_versao()

        self.btn_converter = tk.Button(
            self.root, text="Converter", font=("Segoe UI", 11, "bold"), bg="#2d6cdf", fg="white",
            command=self._converter, height=2,
        )
        self.btn_converter.pack(fill="x", **pad)

        self.progress = ttk.Progressbar(self.root, mode="determinate")

        self.status = tk.Label(self.root, text="", font=("Segoe UI", 9), fg="#333", wraplength=420, justify="left")
        self.status.pack(fill="x", padx=16)

    def _atualizar_versao(self):
        if self.direcao.get() == "dxf2dwg":
            self.label_versao.pack(side="left", padx=(0, 6))
            self.combo_versao.pack(side="left", padx=(0, 20))
        else:
            self.label_versao.pack_forget()
            self.combo_versao.pack_forget()

    def _on_drop(self, event):
        caminhos = self.root.tk.splitlist(event.data)
        if not caminhos:
            return
        caminho = caminhos[0]
        pasta = caminho if os.path.isdir(caminho) else os.path.dirname(caminho)
        self._definir_pasta(pasta)

    def _escolher_pasta(self):
        pasta = filedialog.askdirectory(title="Escolha a pasta com os arquivos")
        if pasta:
            self._definir_pasta(pasta)

    def _definir_pasta(self, pasta):
        self.pasta_origem.set(pasta)
        self.label_pasta.config(text=pasta, fg="#222")

        dwgs = glob.glob(os.path.join(pasta, "*.dwg")) + glob.glob(os.path.join(pasta, "*.DWG"))
        dxfs = glob.glob(os.path.join(pasta, "*.dxf")) + glob.glob(os.path.join(pasta, "*.DXF"))
        if dwgs and not dxfs:
            self.direcao.set("dwg2dxf")
        elif dxfs and not dwgs:
            self.direcao.set("dxf2dwg")
        self._atualizar_versao()

    def _contar_arquivos(self, pasta, extensao, recursivo):
        total = 0
        if recursivo:
            for _, _, arquivos in os.walk(pasta):
                total += sum(1 for a in arquivos if a.lower().endswith(extensao))
        else:
            total = sum(
                1 for a in os.listdir(pasta)
                if a.lower().endswith(extensao) and os.path.isfile(os.path.join(pasta, a))
            )
        return total

    def _converter(self):
        if not self.exe:
            messagebox.showerror("Erro", "ODA File Converter não encontrado.")
            return
        pasta = self.pasta_origem.get()
        if not pasta or not os.path.isdir(pasta):
            messagebox.showwarning("Falta a pasta", "Escolha ou arraste uma pasta primeiro.")
            return

        if self.direcao.get() == "dwg2dxf":
            tipo_saida = "DXF"
            versao_saida = "ACAD2013"
            filtro = "*.DWG"
            nome_saida = "Convertido_DXF"
            ext_entrada = ".dwg"
            self._ext_saida = ".dxf"
        else:
            tipo_saida = "DWG"
            versao_saida = self.versao_dwg.get()
            filtro = "*.DXF"
            nome_saida = "Convertido_DWG"
            ext_entrada = ".dxf"
            self._ext_saida = ".dwg"

        recursivo = self.recursivo.get()
        total = self._contar_arquivos(pasta, ext_entrada, recursivo)
        if total == 0:
            messagebox.showwarning("Nada pra converter", f"Não achei nenhum arquivo {ext_entrada} nessa pasta.")
            return

        pasta_saida = os.path.join(pasta, nome_saida)
        os.makedirs(pasta_saida, exist_ok=True)
        recurse = "1" if recursivo else "0"

        self._total_arquivos = total
        self._pasta_saida_atual = pasta_saida

        self.progress["maximum"] = total
        self.progress["value"] = 0
        self.progress.pack(fill="x", padx=16, pady=(0, 6), before=self.status)

        self.btn_converter.config(state="disabled", text="Convertendo...")
        self.status.config(text=f"Convertendo... 0/{total}")

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0  # SW_HIDE
        self.processo = subprocess.Popen(
            [self.exe, pasta, pasta_saida, versao_saida, tipo_saida, recurse, "0", filtro],
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        threading.Thread(target=self._esperar_processo, daemon=True).start()
        self.root.after(300, self._poll_progresso)

    def _contar_saida(self):
        total = 0
        for _, _, arquivos in os.walk(self._pasta_saida_atual):
            total += sum(1 for a in arquivos if a.lower().endswith(self._ext_saida))
        return total

    def _poll_progresso(self):
        n = self._contar_saida()
        self.progress["value"] = min(n, self._total_arquivos)
        if self.processo.poll() is None:
            self.status.config(text=f"Convertendo... {n}/{self._total_arquivos}")
            self.root.after(400, self._poll_progresso)

    def _esperar_processo(self):
        try:
            self.processo.wait(timeout=300)
            convertidos = self._contar_saida()
            msg = f"Pronto! {convertidos} de {self._total_arquivos} arquivo(s) em:\n{self._pasta_saida_atual}"
        except Exception as exc:
            msg = f"Deu erro: {exc}"

        self.root.after(0, self._finalizar, msg, self._pasta_saida_atual)

    def _finalizar(self, msg, pasta_saida):
        self.progress["value"] = self._total_arquivos
        self.status.config(text=msg)
        self.btn_converter.config(state="normal", text="Converter")
        self.progress.pack_forget()
        if os.path.isdir(pasta_saida) and os.listdir(pasta_saida):
            if messagebox.askyesno("Concluído", msg + "\n\nAbrir a pasta?"):
                os.startfile(pasta_saida)


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    App(root)
    root.mainloop()
