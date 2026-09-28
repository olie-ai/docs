# Checklist de escrita da documentação da Olie

O objetivo é um só: **o leitor entende e consegue agir na primeira leitura.**

Este checklist adapta ao português e à Olie os cursos de escrita técnica do Google ([Technical Writing One](https://developers.google.com/tech-writing/one), [Two](https://developers.google.com/tech-writing/two) e [Writing Helpful Error Messages](https://developers.google.com/tech-writing/error-messages)) e os guias da Mintlify sobre [tipos de conteúdo](https://www.mintlify.com/docs/guides/content-types) e [estilo e tom](https://www.mintlify.com/docs/guides/style-and-tone).

> **Boa documentação = o que o leitor precisa saber − o que ele já sabe.**
> Explicar demais o fácil cansa, e explicar de menos o difícil trava o leitor.

**Como usar:** consulte ao escrever e percorra na revisão. Os itens marcados com 🤖 são verificados pelo script `scripts/lint_docs.py`. Os demais pedem leitura atenta.

---

## 0. Antes de escrever

- [ ] **Quem lê?** Escolha um público principal: quem opera o funil no dia a dia, quem administra a conta, dev integrando a API ou parceiro do marketplace. Um texto para todos acaba não servindo a ninguém.
- [ ] **O que a pessoa consegue fazer ou entender ao terminar?** Liste de 1 a 3 objetivos. Se não couberem numa frase cada, a página está grande demais.
- [ ] **Que tipo de página é?** Decida antes de escrever, porque o tipo define a estrutura, o tamanho e o que fica de fora. A divisão segue o [Diátaxis](https://diataxis.fr), também adotado pela [Mintlify](https://www.mintlify.com/docs/guides/content-types). Na dúvida, pergunte: **o que o leitor faz depois de ler?**

| Tipo | O leitor quer… | Depois de ler, ele… | Exemplo |
| --- | --- | --- | --- |
| Tutorial | aprender fazendo | concluiu algo completo pela primeira vez | `guides/automation/first-automation.mdx` |
| Guia de tarefa | resolver uma coisa específica | fez a tarefa | `guides/funnels/moving-projects.mdx` |
| Referência | consultar um dado exato | achou o valor, a opção ou o limite | `guides/fundamentals/limits.mdx` |
| Explicação | entender como e por que funciona | entende melhor e decide o que fazer | `guides/fundamentals/mental-model.mdx` |

Cada tipo tem regras próprias:

- **Tutorial:** diga no início o que a pessoa vai ter no final. Use um único exemplo completo, do começo ao fim. Evite escolhas: se há dois caminhos, escolha um e diga isso. Marque o progresso nos marcos ("Pronto, a automação já está ativa").
- **Guia de tarefa:** ponha a tarefa no título ("Mover um projeto para outro funil"). Parta do princípio de que a pessoa conhece o básico, dê os passos sem rodeios e coloque um link para a explicação.
- **Referência:** siga a estrutura do que está sendo documentado, não a jornada do usuário. Todo parâmetro, campo ou opção tem **tipo, valor padrão, descrição de uma linha e exemplo**. Documente limites e casos de borda: se a pessoa só descobre um limite por tentativa e erro, a falha é da documentação. Deixe as explicações para outra página.
- **Explicação:** comece pela pergunta que a página responde ("Qual a diferença entre status do funil e status do projeto?"). Explique por que a Olie funciona assim e conecte com o resto da plataforma. Não dê instruções: coloque um link para os guias de tarefa.
- **Solução de problemas** é um guia de tarefa organizado por sintoma. Veja a seção 12.

Uma página que explica um conceito, ensina um passo a passo e lista opções ao mesmo tempo é difícil de usar e de manter. Divida a página, ou escolha um tipo principal e coloque links para o resto.

- [ ] **Já existe página sobre isso?** Coloque um link em vez de repetir. Conteúdo duplicado fica desatualizado em um dos lugares.

## 1. A página

- [ ] 🤖 **Frontmatter completo.** Preencha `title`, `description` (até 160 caracteres) e `keywords`.
  - `title`: o que o leitor faz ou procura. Use "Criando sua primeira automação", não "Editor".
  - `description`: uma frase dizendo o que a página entrega.
  - `keywords`: termos que a pessoa digitaria na busca, incluindo os sinônimos do [glossário](../../../guides/fundamentals/glossary.mdx).
- [ ] 🤖 **Comece com um parágrafo, não com um título.** A primeira frase diz o que é ou o que a pessoa vai conseguir. Muita gente lê só esse parágrafo.
- [ ] **Delimite o escopo.** Diga o que a página cobre. Quando houver risco de confusão, diga também o que ela não cobre e onde encontrar isso.
- [ ] **Pré-requisitos antes dos passos, no texto**: permissão, plano e objetos que já precisam existir. Use uma seção "Antes de começar" com frases ou lista, não um callout, porque o pré-requisito é necessário para concluir a tarefa.
- [ ] **O porquê antes do como.** Uma frase de motivo antes da instrução faz o passo fazer sentido.
- [ ] **Do simples ao avançado.** Primeiro o caso mais comum, depois as variações. Casos avançados ficam no fim ou em outra página.
- [ ] **Feche indicando o próximo passo** ou as páginas relacionadas.
- [ ] **Corte o que não serve ao objetivo** definido no item 0, mesmo que seja verdade e interessante.

## 2. Títulos e seções

- [ ] **Títulos dizem o que o leitor faz ou encontra**, com palavras que ele já conhece. "Mover um projeto para outro funil" é melhor que "Vínculo com a etapa". Termos da Olie entram no título depois de apresentados.
- [ ] 🤖 **Só a primeira letra maiúscula** (além de nomes próprios), sem ponto final ou dois-pontos e com até cerca de 60 caracteres.
- [ ] 🤖 **Não pule níveis** (de `##` para `####`) e não use `#` no corpo, porque o título da página vem do frontmatter.
- [ ] **Títulos do mesmo nível são paralelos**: todos com verbo ou todos com substantivo.
- [ ] 🤖 **Toda seção abre com uma frase de contexto**, não direto com lista, tabela ou callout. Não é preciso fazer isso em abas (`<Tab>`) de variações de um mesmo exemplo.

## 3. Parágrafos

- [ ] **A primeira frase diz do que o parágrafo trata.** Quem lê só as primeiras frases deve entender o essencial.
- [ ] 🤖 **Um assunto por parágrafo**, de 2 a 4 frases. Acima de cerca de 100 palavras, divida o parágrafo ou transforme em lista.

## 4. Frases

- [ ] 🤖 **Uma ideia por frase.** Acima de 30 palavras, divida. A referência em inglês é de 25 palavras, e o português costuma ser uns 20% mais longo. Uma frase que precisa de várias vírgulas ou travessões para se sustentar geralmente vira duas.
- [ ] **Frase que enumera com vários "e" e "ou" vira lista.**
- [ ] **Condição antes da instrução.** A pessoa precisa saber se o passo vale para ela antes de executar.
  - ❌ Fale com o administrador se o botão não aparecer.
  - ✅ Se o botão não aparecer, fale com quem administra a conta.
- [ ] **Deixe claro quem faz a ação.** 🤖 Evite a passiva com "se" ("deve-se", "recomenda-se"). A passiva com "ser" pode ficar quando quem faz a ação não importa ("a chamada é recusada com HTTP 402"). O problema é a passiva esconder uma ação que **o leitor** precisa fazer. Isso a leitura avalia; o script não checa.
  - ❌ A etiqueta é aplicada quando o projeto é movido.
  - ✅ A automação aplica a etiqueta quando você move o projeto.
- [ ] **Instruções no imperativo, falando com "você".**
  - ❌ O usuário deve clicar em Salvar. / Vamos clicar em Salvar.
  - ✅ Clique em **Salvar**.
- [ ] 🤖 **Prefira a forma afirmativa** e evite dupla negação.
  - ❌ Não deixe o nome em branco. / Não é incomum que…
  - ✅ Preencha o nome. / É comum que…
- [ ] 🤖 **Corte palavras vazias.**

| Em vez de | Use |
| --- | --- |
| realizar a criação de | criar |
| efetuar | fazer |
| através de | pelo, pela, com |
| com o objetivo de, a fim de | para |
| no momento em que | quando |
| é possível configurar | você pode configurar |
| é capaz de, tem a capacidade de | pode |
| fazer uso de | usar |
| levar em consideração | considerar |
| devido ao fato de | porque |
| vale notar que, é importante ressaltar que, note que | (corte e diga direto) |

- [ ] **Sem pronome ambíguo.** Se "isso", "ele" ou "essa" estiver longe de quem se refere, ou se houver dois substantivos que possam ser o referente, repita o substantivo.
  - ❌ A automação move o projeto e depois ele recebe a etiqueta.
  - ✅ A automação move o projeto e depois aplica a etiqueta nele.

## 5. Palavras e termos

- [ ] 🤖 **Um nome para cada coisa: o do [glossário](../../../guides/fundamentals/glossary.mdx).** Se o texto diz "etiqueta", não alterne com "tag". Se diz "etapa", não alterne com "fase". **Projeto** é o objeto. **Cartão** só serve para falar do elemento visual no quadro ("o status pinta o cartão"). Se o glossário e as páginas divergirem, não escolha por conta própria: registre como pendência.
- [ ] **O mesmo texto que a interface mostra**, em **negrito**, para a pessoa achar o botão na tela.
- [ ] **Termo novo é definido ali mesmo, na primeira vez que aparece.** Uma oração curta resolve, e o link para o glossário ou para a página do conceito vem junto. Só o link obriga o leitor a sair da página.
  - ✅ Cada resposta tem um *pivot*, o objeto que diz onde o formulário está anexado ([ver o pivot](../../../api-reference/general/form-answer-pivot.mdx)).
- [ ] **Nomes de funcionalidades com a mesma grafia sempre**: Caderno, Automações, Marketplace. Não alterne entre maiúscula e minúscula.
- [ ] 🤖 **Siglas por extenso na primeira vez**, com a sigla entre parênteses. Só crie sigla se ela vai se repetir. Siglas conhecidas do público (API, URL, PDF) dispensam isso.
- [ ] **Nada de jargão interno** em guias de uso: nomes de tabela, codinomes de projeto ou nomes de serviço do back-end.
- [ ] **Sem gíria, regionalismo ou metáfora** que não se traduz. Parte do público lê com tradutor automático.
- [ ] 🤖 **Sem anglicismo desnecessário**: excluir (não "deletar"), definir (não "setar"), entrar (não "logar"), captura de tela (não "print"). Termos técnicos consagrados, como webhook, token e payload, podem ficar.

## 6. Tom da Olie

- [ ] 🤖 **Afirmativo e sem concorrentes.** Descreva como a Olie funciona. Nunca cite nem compare com outras ferramentas, como em "ao contrário de X…" ou "na maioria das ferramentas…". Isso inclui comparação com alternativas genéricas ("é aqui que a plataforma se diferencia de colar uma chave de API em um script"). Termos genéricos como kanban, quadro, board e pipeline são permitidos.
- [ ] 🤖 **Nada que faça a plataforma parecer difícil.** Evite "difícil", "confuso", "complicado", "se perder" e "desaprender". Prefira "vale um minuto de atenção", "uma distinção importante" ou "uma ideia central".
- [ ] 🤖 **Nada que faça o leitor se sentir lento.** Evite "simplesmente", "basta", "é fácil" e "obviamente". Se fosse óbvio para a pessoa, ela não estaria lendo.
- [ ] 🤖 **Fale com o leitor**: "você", não "nós" ou "vamos".
- [ ] 🤖 **Sem propaganda.** "Um recurso poderoso e intuitivo" é opinião. Diga o que o recurso faz e deixe o leitor concluir.
- [ ] **Direto, sem ser seco.** Use "Clique em **Salvar**", não "Por favor, clique no botão Salvar quando estiver pronto para prosseguir". O tom pode ser mais acolhedor num tutorial e mais denso numa referência de API.
- [ ] 🤖 **Sem desculpas nem humor** em avisos e erros: nada de "infelizmente", "desculpe", "ops" ou "por favor".
- [ ] **Não culpe o leitor.** Descreva o estado das coisas ou diga o que fazer.
  - ❌ Você esqueceu de selecionar a etapa.
  - ✅ Selecione a etapa de destino.

## 7. Listas e tabelas

- [ ] **Lista numerada para sequência**, com marcadores para o resto. Procedimentos com mais de 3 passos usam `<Steps>`. **Nunca use `<Steps>` nem lista numerada para itens sem ordem**, como boas práticas ou dicas.
- [ ] **Itens paralelos**: todos começam com verbo ou todos com substantivo, com a mesma pontuação.
- [ ] **Uma frase apresenta a lista ou a tabela.**
- [ ] **Use tabela quando comparar vários itens** em dois ou mais atributos, como em `limits.mdx`. Mantenha as células curtas.
- [ ] **Lista de um item vira frase.**

## 8. Procedimentos (passo a passo)

- [ ] **Uma ação por passo.** Se o passo tem "e depois", divida.
- [ ] **Primeiro onde, depois o quê.** Exemplo: "Em **Automações**, clique em **Nova automação**."
- [ ] 🤖 **Elementos da interface em negrito**, com o texto exato da tela.
- [ ] **Diga o resultado esperado** nos passos importantes e como confirmar que deu certo, usando `<Check>`.
- [ ] **Use exemplos concretos e realistas**, como a etapa "Proposta enviada" e a etiqueta "Aguardando retorno", e não "X", "teste" ou "foo".
- [ ] **Termine com um teste**: como a pessoa verifica que tudo funciona.

## 9. Callouts

| Componente | Quando usar |
| --- | --- |
| `<Warning>` | Risco real: perda de dados, ação irreversível, acesso amplo, cobrança ou limite que quebra algo |
| `<Info>` | Contexto útil que não é necessário para concluir a tarefa |
| `<Note>` | Detalhe útil que interromperia o fluxo do texto |
| `<Tip>` | Atalho ou boa prática opcional |
| `<Check>` | Confirmação de que o passo deu certo |

- [ ] **Informação necessária para concluir a tarefa vai no texto**, não em callout. Muita gente pula callouts. A única exceção é o risco real: ele pode ficar em `<Warning>`, desde que o texto antes dele introduza o assunto numa frase.
- [ ] 🤖 **Não empilhe callouts.** Quando tudo está em destaque, nada se destaca.
- [ ] **Não repita no callout o que o texto acabou de dizer.**

## 10. Imagens e diagramas

- [ ] **Use imagem só se ela explica melhor que o texto.** O texto precisa funcionar sem a imagem.
- [ ] 🤖 **Toda imagem tem texto alternativo.** Uma legenda curta diz o que observar.
- [ ] **Uma ideia por imagem.** Se precisar de mais de 5 tópicos para explicá-la, divida.
- [ ] **Em capturas de tela, destaque o que importa** com seta ou contorno e recorte o resto.
- [ ] **Capturas atualizadas e sem dados reais de clientes.** A skill `capturing-ui-screenshots` cuida disso.
- [ ] **Diagramas em SVG** sempre que possível, com contraste legível nos temas claro e escuro.

## 11. Exemplos e código

Vale para API, variáveis Twig e sintaxe avançada.

- [ ] **Todo exemplo funciona.** Teste contra a API ou o editor atual antes de publicar. Sem acesso à API, a fonte de verdade é o `api-reference/openapi.json`: nomes de campos, paths, tipos e enums dos exemplos precisam bater com ele.
- [ ] **Exemplo mínimo e completo para copiar**, com cabeçalhos, autenticação e campos obrigatórios. Numa série de variações, faça um exemplo completo (por exemplo, `curl` com `Authorization`) e deixe as variações curtas, mostrando só o que muda.
- [ ] **Dados da Olie nos exemplos**: projeto, etapa, cliente. Nada de `foo` e `bar`.
- [ ] **Mostre a saída ou a resposta esperada.**
- [ ] **Comentários explicam o que não é óbvio**, de preferência o porquê.
- [ ] **Do básico ao avançado**: primeiro o exemplo mínimo, depois as variações.
- [ ] 🤖 **Todo bloco de código indica a linguagem**, como ` ```json ` ou ` ```twig `.

## 12. Erros e solução de problemas

Vale para seções de solução de problemas, códigos de erro da API, registros de execução de automações e mensagens do produto citadas na documentação.

Toda descrição de erro responde **três perguntas**:

1. **O que aconteceu?** Cite a mensagem ou o código exato (`automation_run_limit_reached`), para a pessoa achar pela busca.
2. **Por quê?** Diga qual entrada ou configuração causou o erro e qual regra foi violada: limite, formato ou permissão.
3. **Como resolver?** Dê uma ação concreta. Se houver mais de uma, liste as opções.

- [ ] **Organize pelo sintoma**, ou seja, pelo que a pessoa vê. Veja o `<Warning>` de encadeamento em `limits.mdx`.
- [ ] **Mostre um exemplo do valor válido** quando o erro for de formato.
- [ ] **Sem culpa, sem desculpas e sem humor.**
  - ❌ Você informou uma data inválida.
  - ✅ Informe a data no formato `AAAA-MM-DD`, por exemplo `2026-09-28`.
- [ ] **Mensagens curtas e diretas.** Se a explicação for longa, dê a essencial e coloque um link para a página completa.

## 13. Revisão antes do PR

- [ ] 🤖 **Rode o script**: `python3 .claude/skills/revisando-documentacao/scripts/lint_docs.py --alterados`
- [ ] **Leia em voz alta**, ou com leitor de tela. Onde você tropeçar, reescreva.
- [ ] **Releia depois de um intervalo.** Os erros aparecem melhor com a cabeça descansada.
- [ ] **Faça o teste do leitor novo**: alguém que nunca usou a funcionalidade consegue seguir sozinho?
- [ ] **Confira os links** com `mint broken-links --files <arquivo>`.
- [ ] **Veja a pré-visualização** com `mint dev`, inclusive em tela de celular.
- [ ] **Ao usar IA para escrever**, informe o papel, o público, o tipo de página e o objetivo do leitor. Peça para usar só a fonte fornecida (código, especificação, tela) e confira cada afirmação. Quem responde pelo texto é você.
