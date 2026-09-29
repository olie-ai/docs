#!/usr/bin/env python3
"""Verificações automáticas do checklist de escrita da documentação da Olie.

Cobre só o que dá para detectar por padrão de texto. Clareza, escopo, ordem
das ideias e correção dos exemplos continuam exigindo leitura — ver
checklist.md.

Uso:
  python3 lint_docs.py                      # todas as páginas
  python3 lint_docs.py guides/automation    # uma pasta ou arquivos
  python3 lint_docs.py --alterados          # só o que mudou em relação à main
  python3 lint_docs.py --nivel sugestao     # inclui sugestões
  python3 lint_docs.py --resumo             # contagem por regra
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[4]
PASTAS_PADRAO = ["index.mdx", "guides", "api-reference"]
IGNORAR_TERMOS = {"guides/fundamentals/glossary.mdx"}

NIVEIS = {"erro": 0, "aviso": 1, "sugestao": 2}

# (regra, nível, regex, mensagem). Buscadas em texto corrido, fora de código.
PADROES = [
    ("concorrente", "erro",
     r"\b(Trello|Pipefy|ClickUp|Jira|Pipedrive|Notion|Asana|Monday(?:\.com)?|HubSpot|Salesforce|Bitrix24?|Kommo|RD Station|Agendor|Runrun\.it|Zoho)\b",
     "Não cite nem compare com outras ferramentas. Descreva como a Olie funciona."),
    ("tom-dificuldade", "aviso",
     r"\b(difícil|difíceis|dificuldades?|complicad[oa]s?|confus[oa]s?|confusão|desconfortável|desaprender|(?<!que )se perdem?|se perder)\b",
     "Não sugira que a plataforma é difícil. Prefira 'vale um minuto de atenção' ou 'uma distinção importante'."),
    ("tom-minimizador", "aviso",
     r"\b(simplesmente|(?<!não )basta|obviamente|óbvio|é fácil|facilmente|trivial|claro que)\b",
     "Palavra que minimiza o esforço do leitor. Remova ou reescreva."),
    ("tom-desculpa", "aviso",
     r"\b(infelizmente|desculp\w*|por favor|ops|oops)\b",
     "Sem desculpas, 'por favor' ou humor em avisos. Diga o que aconteceu e o que fazer."),
    ("primeira-pessoa", "sugestao",
     r"\b(nós|vamos|veremos|faremos)\b",
     "Fale com o leitor ('você'). Instruções no imperativo."),
    ("passiva-se", "aviso",
     r"\b(deve|devem|pode|podem|recomenda|sugere|utiliza|usa|faz|nota|observa|verifica|clica|seleciona|configura|cria|define|preenche)-se\b",
     "Passiva com 'se' esconde quem age. Use o imperativo ou diga quem faz a ação."),
    ("dupla-negacao", "aviso",
     r"\bnão\s+(é|são|está|estão|parece)\s+(incomu\w+|impossíve\w+|inválid\w+|incorret\w+|indisponíve\w+|desnecessári\w+|improváve\w+|incompatíve\w+|inadequad\w+|desconhecid\w+|inativ\w+|ilimitad\w+|irrelevante\w*)\b|\bnão\s+deixa[m]?\s+de\b",
     "Dupla negação. Reescreva na forma afirmativa."),
    ("tom-propaganda", "aviso",
     r"\b(poderos[oa]s?|incríve(l|is)|revolucionári[oa]s?|perfeit[oa]s?|mágic[oa]s?|sem esforço|intuitiv[oa]s?|robust[oa]s?)\b",
     "Opinião ou propaganda. Documente o que o recurso faz, não o quanto ele é bom."),
    ("link-generico", "aviso",
     r"\[(aqui|clique aqui|este link|neste link|link|saiba mais)\]\(",
     "O texto do link deve dizer para onde ele leva."),
    ("ui-sem-negrito", "sugestao",
     r"\b[Cc]lique\s+(em|no|na|nos|nas)\s+(o botão |a opção |a aba |o menu )?(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])",
     "Elemento da interface em **negrito**, com o texto exato da tela."),
]

# Palavras vazias: (regex, substituição sugerida)
VERBOSIDADE = [
    (r"\brealiza[r]?\s+(a|o)\s+\w+ção\b", "use o verbo direto (ex.: 'criar' em vez de 'realizar a criação')"),
    (r"\befetua\w*\b", "'fazer'"),
    (r"\batravés\s+d[aoe]s?\b", "'pelo', 'pela' ou 'com'"),
    (r"\bcom\s+(o\s+objetivo|a\s+finalidade)\s+de\b", "'para'"),
    (r"\ba\s+fim\s+de\b", "'para'"),
    (r"\bno\s+momento\s+em\s+que\b", "'quando'"),
    (r"\b(é\s+capaz\s+de|tem\s+a\s+capacidade\s+de)\b", "'pode'"),
    (r"\bfaz(er)?\s+uso\s+de\b", "'usar'"),
    (r"\blevar\s+em\s+considera[çc][ãa]o\b", "'considerar'"),
    (r"\bdevido\s+ao\s+fato\s+de\b", "'porque'"),
    (r"\bde\s+forma\s+a\b", "'para'"),
    (r"\b(vale|cabe)\s+(notar|ressaltar|destacar|lembrar|mencionar|registrar)(\s+que)?\b", "corte e diga direto"),
    (r"\bé\s+importante\s+(notar|ressaltar|destacar|lembrar)\s+que\b", "corte e diga direto"),
    (r"\bnote\s+que\b", "corte e diga direto"),
]

# Termos fora do glossário: (regex, termo da Olie). Ignorados no próprio glossário.
TERMOS = [
    (r"\b(fases?)\b", "etapa"),
    (r"\b(tags?)\b", "etiqueta"),
    (r"\b(cards?)\b", "cartão (visual) ou projeto (o objeto)"),
    (r"\bcampos?\s+(customizad|personalizad)\w+", "campo do formulário dinâmico"),
    (r"\b(delet\w+)\b", "excluir"),
    (r"\b(set(ar|ado|ada|e))\b", "definir"),
    (r"\b(log(ar|ado|ue|ou))\b", "entrar / acessar"),
    (r"\b(prints?|printar)\b", "captura de tela"),
]

SIGLAS_CONHECIDAS = set("""
API APIs URL URLs MCP IA PDF CSV JSON HTTP HTTPS ID IDs CPF CNPJ SLA PIX SQL UUID
CRM OAuth SSO SMS HTML CSS JS XML UTC GMT PNG JPG JPEG GIF SVG MB GB KB TB OK
REST CEP RG UF SDK CLI JWT GET POST PUT PATCH DELETE LGPD CNAE NF NFe DOCX XLSX
FAQ AI LLM IP TLS SSL DNS PT BR US EUA TI RH ERP BI KPI KPIs OKR OKRs QR ZIP
OU E UTF ISO AND OR NOT NULL TRUE FALSE
SAML SOC TOTP PCI DSS H1 H2 H3 H4 H5 H6 TODO UI
""".split())

CALLOUT_ABRE = re.compile(r"^\s*<(Note|Tip|Warning|Info|Check)\b")
CALLOUT_FECHA = re.compile(r"</(Note|Tip|Warning|Info|Check)>\s*$")
LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
CODIGO_INLINE = re.compile(r"`[^`]*`")
COMENTARIO = re.compile(r"\{/\*.*?\*/\}")
CITACAO = re.compile(r"[\"“][^\"”]{15,}[\"”]")
ABRE_BLOCO = re.compile(r"^\s*<(CardGroup|AccordionGroup|Tabs|Steps|Columns)\b")
SECAO_DE_LINKS = re.compile(r"^(próximos passos|páginas relacionadas|por onde continuar|veja também|leia também)", re.I)
TAG_JSX = re.compile(r"</?[A-Za-z][^>]*>")
FIM_FRASE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ\"“(*])")


class Achado:
    def __init__(self, arquivo, linha, nivel, regra, msg, trecho=""):
        self.arquivo, self.linha, self.nivel = arquivo, linha, nivel
        self.regra, self.msg, self.trecho = regra, msg, trecho


def limpar(texto):
    """Remove comentários, código inline, tags JSX e marcação, mantendo o texto dos links."""
    texto = COMENTARIO.sub("", texto)
    texto = CODIGO_INLINE.sub("CODIGO", texto)
    texto = LINK.sub(r"\1", texto)
    texto = TAG_JSX.sub("", texto)
    texto = re.sub(r"https?://\S+", "", texto)
    return texto.replace("**", "").replace("__", "")


def classificar(linhas):
    """Devolve (nº da linha, tipo, texto) para cada linha do corpo."""
    saida, em_codigo, cerca, em_comentario = [], False, "", False
    inicio = 0
    if linhas and linhas[0].strip() == "---":
        for i in range(1, len(linhas)):
            if linhas[i].strip() == "---":
                inicio = i + 1
                break
    for i in range(inicio, len(linhas)):
        bruta = linhas[i]
        s = bruta.strip()
        if em_codigo:
            if s.startswith(cerca):
                em_codigo = False
            saida.append((i + 1, "codigo", bruta))
            continue
        if em_comentario or (s.startswith("{/*") and "*/}" not in s):
            em_comentario = "*/}" not in s
            saida.append((i + 1, "comentario", bruta))
            continue
        if s.startswith("{/*") and s.endswith("*/}"):
            saida.append((i + 1, "comentario", bruta))
            continue
        m = re.match(r"^(```+|~~~+)(.*)$", s)
        if m:
            em_codigo, cerca = True, m.group(1)
            saida.append((i + 1, "cerca", m.group(2).strip()))
            continue
        if not s:
            tipo = "vazia"
        elif s.startswith("#"):
            tipo = "titulo"
        elif s.startswith("|"):
            tipo = "tabela"
        elif s.startswith(("import ", "export ")):
            tipo = "import"
        elif s.startswith("<") or s.startswith("{/*"):
            tipo = "componente"
        elif re.match(r"^([-*+]|\d+\.)\s", s):
            tipo = "lista"
        elif s.startswith(">"):
            tipo = "citacao"
        else:
            tipo = "texto"
        saida.append((i + 1, tipo, bruta))
    return saida, inicio


def ler_frontmatter(linhas, fim):
    campos = {}
    for bruta in linhas[1:max(fim - 1, 1)]:
        m = re.match(r"^(\w+):\s*(.*)$", bruta)
        if m:
            campos[m.group(1)] = m.group(2).strip().strip("\"'")
    return campos


def paragrafos(classes):
    """Agrupa linhas de texto consecutivas em parágrafos: (linha inicial, texto)."""
    atual, inicio = [], None
    for n, tipo, bruta in classes + [(0, "vazia", "")]:
        if tipo == "texto":
            if not atual:
                inicio = n
            atual.append(bruta.strip())
        else:
            if atual:
                yield inicio, " ".join(atual)
            atual = []
        if tipo == "lista":
            yield n, re.sub(r"^\s*([-*+]|\d+\.)\s+", "", bruta)


def contar_palavras(texto):
    """Conta palavras de prosa; trechos de código inline não entram na conta."""
    return len(re.findall(r"[\wÀ-ÿ'-]+", texto.replace("CODIGO", "")))


def analisar(caminho, max_palavras):
    rel = caminho.relative_to(ROOT).as_posix()
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    classes, fim_fm = classificar(linhas)
    achados = []

    def add(linha, nivel, regra, msg, trecho=""):
        achados.append(Achado(rel, linha, nivel, regra, msg, trecho.strip()[:110]))

    # Frontmatter
    if fim_fm == 0:
        add(1, "erro", "frontmatter", "Página sem frontmatter (title, description, keywords).")
    else:
        fm = ler_frontmatter(linhas, fim_fm)
        for campo in ("title", "description"):
            if not fm.get(campo):
                add(1, "erro", "frontmatter", f"Frontmatter sem '{campo}'.")
        if len(fm.get("description", "")) > 160:
            add(1, "aviso", "frontmatter",
                f"'description' com {len(fm['description'])} caracteres (máx. 160). Uma frase dizendo o que a página entrega.")
        if "keywords" not in fm:
            add(1, "sugestao", "frontmatter", "Sem 'keywords'. Inclua os termos que o leitor buscaria.")

    # Estrutura: primeiro conteúdo, títulos, seções
    corpo = [c for c in classes if c[1] not in ("vazia", "import", "comentario")]
    if corpo and corpo[0][1] == "titulo":
        add(corpo[0][0], "aviso", "abertura",
            "A página começa com título. Abra com um parágrafo que diga o que a página entrega.")

    nivel_anterior, h1s = 1, []
    for idx, (n, tipo, bruta) in enumerate(corpo):
        if tipo != "titulo":
            continue
        m = re.match(r"^(#+)\s*(.*)$", bruta.strip())
        nivel, texto = len(m.group(1)), m.group(2).strip()
        if nivel == 1:
            h1s.append(n)
        if nivel > nivel_anterior + 1:
            add(n, "aviso", "titulo", f"Pulo de nível de título (h{nivel_anterior} → h{nivel}).", texto)
        nivel_anterior = nivel
        if re.search(r"[.:]$", texto):
            add(n, "aviso", "titulo", "Título sem ponto final nem dois-pontos.", texto)
        if len(limpar(texto)) > 60:
            add(n, "sugestao", "titulo", "Título longo (> 60 caracteres). Diga o que o leitor faz ou encontra.", texto)
        palavras = re.findall(r"\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+\b", texto)
        if len(palavras) >= 3 and len(palavras) >= len(texto.split()) - 1:
            add(n, "sugestao", "titulo", "Título Com Todas Maiúsculas. Em português, só a primeira letra e nomes próprios.", texto)
        prox = corpo[idx + 1] if idx + 1 < len(corpo) else None
        if prox and prox[1] == "titulo":
            nivel_prox = len(re.match(r"^(#+)", prox[2].strip()).group(1))
            if nivel_prox <= nivel:
                add(n, "aviso", "secao-vazia", "Seção sem conteúdo.", texto)
        elif prox and not SECAO_DE_LINKS.match(limpar(texto)) and (
                prox[1] in ("lista", "tabela") or CALLOUT_ABRE.match(prox[2]) or ABRE_BLOCO.match(prox[2])):
            add(n, "sugestao", "secao-sem-contexto",
                "Seção abre direto com lista, tabela, callout ou grupo de componentes. Introduza com uma frase.", texto)

    if h1s:
        add(h1s[0], "aviso", "titulo",
            f"{len(h1s)} título(s) com '#' no corpo (linhas {', '.join(map(str, h1s[:8]))}). "
            "O título da página vem do frontmatter; use '##' para seções.")

    # Frases e parágrafos
    for n, par in paragrafos(classes):
        texto = limpar(par)
        if contar_palavras(texto) > 100:
            add(n, "sugestao", "paragrafo-longo",
                f"Parágrafo com {contar_palavras(texto)} palavras. Um assunto por parágrafo; divida ou use lista.", texto)
        for frase in FIM_FRASE.split(texto):
            qtd = contar_palavras(CITACAO.sub("CITACAO", frase))
            if qtd > max_palavras:
                add(n, "aviso", "frase-longa",
                    f"Frase com {qtd} palavras (máx. {max_palavras}). Uma ideia por frase.", frase)

    # Padrões de texto, linha a linha, fora de código
    ignora_termos = rel in IGNORAR_TERMOS
    siglas_vistas = set()
    for n, tipo, bruta in classes:
        if tipo in ("codigo", "cerca", "import", "vazia", "comentario"):
            continue
        original = CODIGO_INLINE.sub("CODIGO", bruta)
        texto = limpar(bruta) if tipo != "componente" else limpar(re.sub(r'\w+="[^"]*"', "", bruta))
        for regra, nivel, rx, msg in PADROES:
            alvo = original if regra in ("link-generico", "ui-sem-negrito") else texto
            flags = 0 if regra == "concorrente" else re.IGNORECASE
            if regra == "ui-sem-negrito":
                flags = 0
            for m in re.finditer(rx, alvo, flags):
                add(n, nivel, regra, msg, f"…{alvo[max(0, m.start() - 30):m.end() + 40].strip()}…")
        for rx, sugestao in VERBOSIDADE:
            for m in re.finditer(rx, texto, re.IGNORECASE):
                add(n, "sugestao", "verbosidade", f"'{m.group(0)}' → {sugestao}.")
        if not ignora_termos and tipo != "tabela":
            for rx, termo in TERMOS:
                for m in re.finditer(rx, texto, re.IGNORECASE):
                    add(n, "sugestao", "terminologia", f"'{m.group(0)}' → use '{termo}' (glossário).",
                        f"…{texto[max(0, m.start() - 30):m.end() + 30].strip()}…")
        for m in re.finditer(r"\b[A-Z][A-Z0-9]{1,5}s?\b", texto):
            sigla = m.group(0)
            if sigla in SIGLAS_CONHECIDAS or sigla in siglas_vistas or sigla == "CODIGO":
                continue
            siglas_vistas.add(sigla)
            vizinho = texto[max(0, m.start() - 2):m.end() + 2]
            entre_parenteses = any(a.start() < m.start() < a.end() for a in re.finditer(r"\([^)]*\)", texto))
            if "(" not in vizinho and not entre_parenteses:
                add(n, "sugestao", "sigla",
                    f"Sigla '{sigla}' sem definição na primeira ocorrência. Escreva por extenso e a sigla entre parênteses.")

    # Blocos JSON precisam ser JSON válido (sem comentários nem reticências)
    bloco, inicio_bloco, linguagem = None, 0, ""
    for n, tipo, bruta in classes:
        if tipo == "cerca":
            bloco, inicio_bloco, linguagem = [], n, bruta.split()[0].lower() if bruta else ""
        elif tipo == "codigo" and bloco is not None and re.match(r"^\s*(```|~~~)", bruta):
            if linguagem == "json":
                try:
                    json.loads("\n".join(bloco))
                except ValueError as e:
                    add(inicio_bloco, "aviso", "json-invalido",
                        f"Bloco ```json inválido ({e.msg}, linha {e.lineno} do bloco). "
                        "Exemplo precisa ser copiável: sem comentários nem '...'.")
            bloco = None
        elif tipo == "codigo" and bloco is not None:
            bloco.append(bruta)

    # Imagens e blocos de código
    for n, tipo, bruta in classes:
        if tipo == "cerca" and not bruta:
            add(n, "sugestao", "codigo-sem-linguagem", "Bloco de código sem linguagem (```json, ```twig…).")
        if tipo in ("codigo", "cerca"):
            continue
        for m in re.finditer(r"!\[\s*\]\(", bruta):
            add(n, "aviso", "imagem-sem-alt", "Imagem sem texto alternativo.")
        if re.search(r"<img\b(?![^>]*\balt=)", bruta):
            add(n, "aviso", "imagem-sem-alt", "<img> sem atributo alt.")

    # Callouts empilhados e densidade
    total_palavras = sum(contar_palavras(limpar(b)) for _, t, b in classes if t in ("texto", "lista"))
    callouts, ultimo_fim, ultimo_tipo = 0, None, None
    for n, tipo, bruta in classes:
        if tipo in ("codigo", "cerca", "comentario"):
            continue
        m_callout = CALLOUT_ABRE.match(bruta)
        if m_callout:
            callouts += 1
            atual = m_callout.group(1)
            dois_riscos = atual == "Warning" and ultimo_tipo == "Warning"
            ultimo_tipo = atual
            if ultimo_fim is not None and not dois_riscos and all(
                    t == "vazia" for ln, t, _ in classes if ultimo_fim < ln < n):
                add(n, "sugestao", "callouts-empilhados",
                    "Callouts em sequência. Funda em um ou leve parte para o texto.")
        if CALLOUT_FECHA.search(bruta):
            ultimo_fim = n
    if callouts > 4 and callouts > total_palavras / 100:
        add(1, "sugestao", "callouts-demais",
            f"{callouts} callouts para ~{total_palavras} palavras. Destaque só o essencial.")

    return achados


def arquivos_alterados():
    cmds = [["git", "diff", "--name-only", "--diff-filter=ACMR", "origin/main...HEAD"],
            ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD"],
            ["git", "ls-files", "--others", "--exclude-standard"]]
    nomes = set()
    for cmd in cmds:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            nomes.update(x for x in r.stdout.split() if x.endswith(".mdx"))
    return [ROOT / x for x in sorted(nomes) if (ROOT / x).exists()]


def coletar(alvos):
    saida = []
    alvos = [x for alvo in alvos for x in (alvo.split() if not (ROOT / alvo).exists() else [alvo])]
    for alvo in alvos:
        p = (ROOT / alvo) if not pathlib.Path(alvo).is_absolute() else pathlib.Path(alvo)
        if p.is_dir():
            saida.extend(sorted(p.rglob("*.mdx")))
        elif p.suffix == ".mdx" and p.exists():
            saida.append(p)
        else:
            print(f"Ignorado (não é .mdx ou não existe): {alvo}", file=sys.stderr)
    return saida


def main():
    ap = argparse.ArgumentParser(description="Valida páginas da documentação contra o checklist de escrita.")
    ap.add_argument("alvos", nargs="*", help="arquivos .mdx ou pastas (padrão: toda a documentação)")
    ap.add_argument("--alterados", action="store_true", help="só arquivos alterados em relação à main")
    ap.add_argument("--nivel", choices=NIVEIS, default="aviso", help="nível mínimo exibido (padrão: aviso)")
    ap.add_argument("--max-palavras", type=int, default=30, help="palavras por frase (padrão: 30)")
    ap.add_argument("--resumo", action="store_true", help="só a contagem por regra")
    args = ap.parse_args()

    arquivos = arquivos_alterados() if args.alterados else coletar(args.alvos or PASTAS_PADRAO)
    if not arquivos:
        print("Nenhuma página para verificar.")
        return 0

    limite = NIVEIS[args.nivel]
    todos = [a for f in arquivos for a in analisar(f, args.max_palavras) if NIVEIS[a.nivel] <= limite]

    if args.resumo:
        por_regra = Counter((a.nivel, a.regra) for a in todos)
        for (nivel, regra), qtd in sorted(por_regra.items(), key=lambda x: (NIVEIS[x[0][0]], -x[1])):
            print(f"{qtd:5d}  {nivel:<9} {regra}")
        por_arquivo = Counter(a.arquivo for a in todos)
        print("\nPáginas com mais ocorrências:")
        for arq, qtd in por_arquivo.most_common(10):
            print(f"{qtd:5d}  {arq}")
    else:
        atual = None
        for a in sorted(todos, key=lambda a: (a.arquivo, a.linha, NIVEIS[a.nivel])):
            if a.arquivo != atual:
                atual = a.arquivo
                print(f"\n{atual}")
            print(f"  {a.linha:>4}  {a.nivel:<9} {a.regra:<20} {a.msg}")
            if a.trecho:
                print(f"{'':>8}› {a.trecho}")

    c = Counter(a.nivel for a in todos)
    print(f"\n{c['erro']} erro(s), {c['aviso']} aviso(s), {c['sugestao']} sugestão(ões) em {len(arquivos)} página(s).")
    return 1 if c["erro"] else 0


if __name__ == "__main__":
    sys.exit(main())
