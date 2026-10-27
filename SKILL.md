---
name: conversor-dwg-dxf
description: Converte arquivos DWG para DXF (ou DXF para DWG) em lote, usando o ODA File Converter gratuito. Use quando o usuário só tiver o arquivo em DWG e precisar de DXF (por exemplo pra usar em outra skill do curso que exige DXF, como revisão de projeto ou cálculo de viga), ou mencionar "converter DWG", "não tenho o DXF, só o DWG", "transformar em DXF".
---

# Conversor DWG ⇄ DXF

Converte arquivos DWG/DXF em lote, sem precisar do AutoCAD, via ODA File Converter
(gratuito, oficial, da Open Design Alliance).

No Windows (o caso mais comum no curso), abre uma janelinha de arrastar e soltar
(`scripts/app.pyw`). Em Mac/Linux, onde essa janela não é suportada, usa o modo terminal
(`scripts/converter.py`).

## Fase 0 — Checar o que falta instalar

```
python scripts/converter.py --check
```

Isso só verifica se o ODA File Converter está instalado, sem converter nada. Se faltar:

- **Windows**: perguntar se pode instalar via
  ```
  winget install --id ODA.ODAFileConverter -e
  ```
- **Mac/Linux**: não tem instalação automática confiável. Indicar que o instalador
  oficial está em https://www.opendesign.com/guestfiles/oda_file_converter, e pedir pro
  usuário baixar e instalar manualmente antes de continuar

No Windows, a janela (`app.pyw`) também precisa do pacote `tkinterdnd2` (não vem padrão
no Python, é só ele que falta — `tkinter` em si já vem instalado com o Python normal).
Checar com:
```
python -c "import tkinterdnd2"
```
Se der erro, perguntar se pode instalar com `pip install tkinterdnd2` antes de abrir a
janela.

Nunca instalar nada sem perguntar antes.

## Fase 1 — Converter

**Windows — abrir a janela:**

Depois que o ODA e o `tkinterdnd2` estiverem prontos (Fase 0), perguntar ao usuário,
nessa ordem:

1. "Posso criar um atalho do conversor na área de trabalho?" — se sim, criar com
   (trocar `<CAMINHO_ABSOLUTO_DA_SKILL>` pelo caminho real de onde a skill foi clonada,
   e `<USUARIO>` pelo usuário do Windows atual):
   ```
   powershell -Command "$s = (New-Object -COM WScript.Shell).CreateShortcut('C:\Users\<USUARIO>\Desktop\Conversor DWG-DXF.lnk'); $s.TargetPath = 'pythonw.exe'; $s.Arguments = '\"<CAMINHO_ABSOLUTO_DA_SKILL>\scripts\app.pyw\"'; $s.WorkingDirectory = '<CAMINHO_ABSOLUTO_DA_SKILL>\scripts'; $s.Save()"
   ```
2. "Posso abrir o programinha agora?" — se sim:
   ```
   pythonw scripts/app.pyw
   ```
   Rodar em background (não travar esperando o usuário fechar a janela)

Avisar que abriu uma janelinha: é só arrastar a pasta com os arquivos (ou clicar pra
escolher), escolher a direção (DWG → DXF ou o contrário) e clicar em Converter. A janela
já acha o ODA File Converter sozinha e mostra o progresso.

**Mac/Linux, ou se o usuário preferir terminal:**
```
python scripts/converter.py --origem "pasta/com/arquivos" --direcao dwg2dxf
```
- Perguntar qual é a pasta de origem, se não tiver vindo junto do pedido
- `--direcao` é `dwg2dxf` ou `dxf2dwg`. Se o usuário não disser, olhar quais arquivos tem
  na pasta (`.dwg` ou `.dxf`) e confirmar a direção com ele antes de rodar
- `--recursivo` inclui subpastas, perguntar se é o caso
- Em `dxf2dwg`, perguntar a versão de saída do AutoCAD só se o usuário tiver uma
  preferência; sem isso, usar o padrão (`ACAD2018`)
- Converte **todos** os arquivos da pasta de uma vez, nunca um arquivo só. Se o usuário
  quiser converter só alguns, avisar que precisa separar numa pasta própria antes

## Fase 2 — Entregar

- Pela janela, o próprio app mostra quantos arquivos converteram e oferece abrir a pasta
  de saída ao final. Pelo terminal, confirmar isso na tela de resultado
- Os arquivos convertidos vão pra uma subpasta nova (`Convertido_DXF` ou `Convertido_DWG`)
  dentro da pasta de origem — os arquivos originais nunca são alterados
- Se algum arquivo não converteu, avisar que pode ser DWG corrompido ou protegido por
  senha, e sugerir abrir no AutoCAD/visualizador pra confirmar antes de insistir

## Regras

1. Nunca instalar o ODA File Converter nem o `tkinterdnd2` sem perguntar antes
2. Nunca inventar o caminho do instalador — usar só o link oficial já confirmado
3. Nunca apagar ou sobrescrever os arquivos originais, a conversão sempre vai pra uma
   subpasta nova
4. `app.pyw` é só Windows (acha o ODA pelo caminho padrão do `Program Files`). Em
   Mac/Linux, usar sempre o modo terminal
