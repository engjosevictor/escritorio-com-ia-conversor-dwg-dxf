---
name: conversor-dwg-dxf
description: Converte arquivos DWG para DXF (ou DXF para DWG) em lote, usando o ODA File Converter gratuito. Use quando o usuário só tiver o arquivo em DWG e precisar de DXF (por exemplo pra usar em outra skill do curso que exige DXF, como revisão de projeto ou cálculo de viga), ou mencionar "converter DWG", "não tenho o DXF, só o DWG", "transformar em DXF".
---

# Conversor DWG ⇄ DXF

Converte arquivos DWG/DXF em lote, sem precisar do AutoCAD, via ODA File Converter
(gratuito, oficial, da Open Design Alliance).

## Fase 0 — Checar se o ODA File Converter está instalado

Rodar `python scripts/converter.py --origem "<pasta>" --direcao dwg2dxf` já falha com uma
mensagem clara se não encontrar o programa instalado. Antes de rodar, ou se der esse erro:

- **Windows**: perguntar se pode instalar via
  ```
  winget install --id ODA.ODAFileConverter -e
  ```
- **Mac/Linux**: não tem instalação automática confiável. Indicar que o instalador
  oficial está em https://www.opendesign.com/guestfiles/oda_file_converter, e pedir pro
  usuário baixar e instalar manualmente antes de continuar

Nunca instalar nada sem perguntar antes.

## Fase 1 — Converter

```
python scripts/converter.py --origem "pasta/com/arquivos" --direcao dwg2dxf
```

- Perguntar qual é a pasta de origem, se não tiver vindo junto do pedido
- `--direcao` é `dwg2dxf` (o caso mais comum no curso, já que as outras skills pedem
  DXF) ou `dxf2dwg`. Se o usuário não disser, olhar quais arquivos tem na pasta
  (`.dwg` ou `.dxf`) e confirmar a direção com ele antes de rodar
- `--recursivo` inclui subpastas, perguntar se é o caso
- Em `dxf2dwg`, perguntar a versão de saída do AutoCAD só se o usuário tiver uma
  preferência; sem isso, usar o padrão (`ACAD2018`)
- Converte **todos** os arquivos da pasta de uma vez, nunca um arquivo só. Se o usuário
  quiser converter só alguns, avisar que precisa separar numa pasta própria antes

## Fase 2 — Entregar

- Confirmar quantos arquivos foram convertidos e onde ficaram (subpasta nova,
  `Convertido_DXF` ou `Convertido_DWG`, dentro da pasta de origem — os arquivos
  originais não são alterados)
- Se algum arquivo não converteu, avisar que pode ser DWG corrompido ou protegido por
  senha, e sugerir abrir no AutoCAD/visualizador pra confirmar antes de insistir

## Regras

1. Nunca instalar o ODA File Converter sem perguntar antes
2. Nunca inventar o caminho do instalador — usar só o link oficial já confirmado
3. Nunca apagar ou sobrescrever os arquivos originais, a conversão sempre vai pra uma
   subpasta nova
