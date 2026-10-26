"""
converter.py
------------
Converte arquivos DWG<->DXF em lote via ODA File Converter (gratuito, oficial, da Open
Design Alliance). Mesma ferramenta por baixo dos panos usada em outros pontos do curso
(qualquer skill que precise de DXF, ex. revisao-projeto ou vigas, parte de DXF).

Uso:
    python converter.py --origem "pasta/com/dwg" --direcao dwg2dxf
    python converter.py --origem "pasta/com/dxf" --direcao dxf2dwg --versao ACAD2018

Os arquivos convertidos vao pra uma subpasta nova dentro da pasta de origem
(Convertido_DXF ou Convertido_DWG), sem mexer nos originais.
"""

import os
import sys
import glob
import argparse
import subprocess

VERSOES_DWG_VALIDAS = [
    "ACAD2018", "ACAD2013", "ACAD2010", "ACAD2007", "ACAD2004", "ACAD2000", "ACAD14",
]


def localizar_conversor():
    candidatos = []
    if sys.platform == "win32":
        candidatos += glob.glob(r"C:\Program Files\ODA\ODAFileConverter*\ODAFileConverter.exe")
        candidatos += glob.glob(r"C:\Program Files (x86)\ODA\ODAFileConverter*\ODAFileConverter.exe")
    elif sys.platform == "darwin":
        candidatos += glob.glob("/Applications/ODAFileConverter*.app/Contents/MacOS/ODAFileConverter")
    else:
        candidatos += glob.glob("/usr/bin/ODAFileConverter") + glob.glob("/opt/ODA/ODAFileConverter*/ODAFileConverter")
    return candidatos[0] if candidatos else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--origem", required=True, help="pasta com os arquivos a converter")
    ap.add_argument("--direcao", required=True, choices=["dwg2dxf", "dxf2dwg"])
    ap.add_argument("--versao", default="ACAD2018", choices=VERSOES_DWG_VALIDAS,
                     help="versao do AutoCAD de saida, so usado em dxf2dwg")
    ap.add_argument("--recursivo", action="store_true", help="incluir subpastas")
    args = ap.parse_args()

    exe = localizar_conversor()
    if not exe:
        print("Erro: ODA File Converter nao encontrado. Instale antes de rodar.")
        sys.exit(1)

    pasta = os.path.abspath(args.origem)
    if not os.path.isdir(pasta):
        print(f"Erro: pasta nao encontrada: {pasta}")
        sys.exit(1)

    if args.direcao == "dwg2dxf":
        tipo_saida, versao_saida, filtro, nome_saida, ext_entrada = "DXF", "ACAD2013", "*.DWG", "Convertido_DXF", ".dwg"
    else:
        tipo_saida, versao_saida, filtro, nome_saida, ext_entrada = "DWG", args.versao, "*.DXF", "Convertido_DWG", ".dxf"

    total = sum(
        1 for raiz, _, arquivos in os.walk(pasta) for a in arquivos
        if a.lower().endswith(ext_entrada) and (args.recursivo or raiz == pasta)
    )
    if total == 0:
        print(f"Nenhum arquivo {ext_entrada} encontrado em {pasta}")
        sys.exit(1)

    pasta_saida = os.path.join(pasta, nome_saida)
    os.makedirs(pasta_saida, exist_ok=True)
    recurse = "1" if args.recursivo else "0"

    print(f"Convertendo {total} arquivo(s) {ext_entrada} -> {tipo_saida} em {pasta_saida} ...")
    resultado = subprocess.run([exe, pasta, pasta_saida, versao_saida, tipo_saida, recurse, "0", filtro])

    ext_saida = ".dxf" if tipo_saida == "DXF" else ".dwg"
    convertidos = sum(1 for _, _, arquivos in os.walk(pasta_saida) for a in arquivos if a.lower().endswith(ext_saida))
    print(f"Concluido: {convertidos} de {total} arquivo(s) convertido(s) em {pasta_saida}")
    if convertidos < total:
        print("Aviso: nem todos os arquivos foram convertidos, confira se algum DWG esta corrompido ou protegido.")
    sys.exit(0 if resultado.returncode == 0 else resultado.returncode)


if __name__ == "__main__":
    main()
