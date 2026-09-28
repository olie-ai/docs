---
name: revisando-documentacao
description: Use ao escrever, revisar ou validar páginas .mdx da documentação da Olie — checar clareza, tom, terminologia, estrutura, tipo de página e descrições de erro contra o checklist de escrita. Gatilhos: "revisa essa página", "valida a doc", "passa o checklist", "isso está fácil de entender?", antes de abrir PR com mudanças em guides/ ou api-reference/.
---

# Revisando a documentação da Olie

O critério é um só: **o leitor entende e consegue agir na primeira leitura.** As regras estão em [checklist.md](checklist.md). Os itens marcados com 🤖 são checados pelo script. O resto depende da sua leitura.

## Fluxo

1. **Escolha os alvos.** Revise o arquivo ou a pasta que foi pedida. Se nada foi pedido, use `--alterados`, que pega o que mudou em relação à `main`.

2. **Rode o script**, a partir da raiz do repositório:

   ```bash
   python3 .claude/skills/revisando-documentacao/scripts/lint_docs.py <arquivos-ou-pastas>
   python3 .claude/skills/revisando-documentacao/scripts/lint_docs.py --alterados --nivel sugestao
   python3 .claude/skills/revisando-documentacao/scripts/lint_docs.py --resumo   # visão geral
   ```

   Os níveis são: `erro`, que bloqueia (hoje só para citação de concorrente); `aviso`, que deve ser corrigido; e `sugestao`, que exige avaliar caso a caso. O script devolve código 1 quando há erro.

3. **Leia cada página inteira** antes de julgar. Identifique:
   - o **público** (quem opera o funil, quem administra a conta, dev de integração ou parceiro);
   - o **tipo** (tutorial, guia de tarefa, referência ou explicação, conforme a seção 0 do checklist);
   - o **objetivo**: o que o leitor faz depois de ler.

4. **Percorra os itens manuais do checklist**, principalmente os que o script não pega:
   - uma página com tipos misturados;
   - escopo e pré-requisitos ausentes;
   - o como antes do porquê;
   - caso avançado antes do caso comum;
   - condição depois da instrução;
   - pronome ambíguo;
   - itens de lista sem paralelismo;
   - callout com informação necessária para concluir a tarefa;
   - exemplo irreal ou que não funciona;
   - erro descrito sem as três respostas (o que aconteceu, por quê, como resolver);
   - termo novo usado sem definição no próprio lugar.

5. **Filtre os falsos positivos do script.** A passiva com "ser" é aceitável quando quem faz a ação não importa. Uma frase longa dentro de uma lista enumerativa às vezes é a melhor opção. "Tag" pode ser o nome de um campo da API. Não repasse um achado que você não confirmou lendo o trecho.

6. **Faça o relatório** por página, ordenado pelo **impacto na compreensão**, não pela quantidade:
   - uma linha de veredito: tipo, público e se a página cumpre o objetivo;
   - no máximo 10 problemas, cada um com `arquivo:linha`, o trecho, o motivo em uma frase e uma **reescrita sugerida**;
   - deixe de fora os detalhes que não afetam o entendimento.

7. **Só corrija quando pedirem.** Ao corrigir:
   - mantenha o sentido e **nunca invente comportamento do produto**. Se a reescrita depende de um fato que você não confirmou, pergunte ou marque como pendência;
   - use os termos do [glossário](../../../guides/fundamentals/glossary.mdx) e o texto exato da interface;
   - rode o script de novo e, se mexer em links, rode `mint broken-links --files <arquivo>`.

## Regras que não se negociam

- **Nunca cite nem compare com concorrentes.** O script trata isso como `erro`.
- **Nunca apresente a plataforma como difícil** e nunca faça o leitor se sentir lento.
- **Nada de propaganda.** Descreva o que o recurso faz.

## Ajustando o script

As listas de padrões (`PADROES`, `VERBOSIDADE`, `TERMOS` e `SIGLAS_CONHECIDAS`) ficam no topo de `scripts/lint_docs.py`. Quando um termo entrar ou sair do glossário, atualize `TERMOS`. Se uma regra gerar muito ruído, mude o nível dela antes de removê-la.
