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
