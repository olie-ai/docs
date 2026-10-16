# Documentação da Olie

Site Mintlify (`docs.json`), em português do Brasil. Os guias ficam em `guides/` e a referência da API em `api-reference/`.

## Escrita

Toda página nova ou alterada segue o [checklist de escrita](.claude/skills/revisando-documentacao/checklist.md). Para revisar ou validar, use a skill `revisando-documentacao` e rode:

```bash
python3 .claude/skills/revisando-documentacao/scripts/lint_docs.py --alterados
```

Essenciais:

- Decida o tipo da página antes de escrever: tutorial, guia de tarefa, referência ou explicação.
- Use os termos do [glossário](guides/fundamentals/glossary.mdx) e o texto exato da interface, em **negrito**.
- Fale com "você" e escreva as instruções no imperativo. Coloque a condição antes da instrução e mantenha uma ideia por frase.
- Nunca cite nem compare com outras ferramentas, nunca apresente a plataforma como difícil e não faça propaganda.

## Comandos

- `mint dev`: pré-visualização em `localhost:3000`
- `mint broken-links --files <arquivo>`: checa os links de uma página

## Branches, commits e PRs

- Nunca adicione coautoria nem atribuição de IA (`Co-Authored-By`, "Generated with", links de sessão ou qualquer variante) em commits, PRs, descrições ou qualquer texto escrito.
- Nunca invente nome de branch. Use o nome que está no card da Olie: ele aparece no conteúdo do card (e no formulário) depois que o card entra na etapa **Não iniciado**. Sem card ou sem nome de branch no card, pergunte antes de criar a branch.
- Fluxo de um card da Olie (funil **Dev - Olie Principal**):
  1. Se o card estiver em **Backlog**, mova para **Não iniciado**.
  2. Pegue o nome da branch no card e faça o checkout dela.
  3. Mova o card para **Em progresso** e desenvolva.
  4. Entregue tudo completo: PRs em todos os repositórios envolvidos, atendendo a todas as necessidades do card, e atualize no card o que for preciso (links dos PRs no formulário, documentação etc.).
  5. Quando todos os PRs estiverem prontos, mova o card para **QA/CR**.
