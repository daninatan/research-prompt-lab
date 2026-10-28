# Research Prompt Lab

Laboratório de engenharia de prompts para extrair fichas de resumos científicos em português.

Projeto de portfólio criado por daninatan com assistência de IA. Relaciona o contexto de pesquisa em Machine Learning à experimentação com modelos de linguagem. Todos os textos de teste são **sintéticos**, sem resultados provenientes da IC ou dados pessoais.

## O problema

Transformar um resumo em uma ficha com objetivo, dados, métodos, métricas e limitações, preservando a diferença entre fatos explícitos e informações ausentes. O foco é rastreabilidade, especialmente quando o texto contém números ambíguos ou instruções maliciosas.

## Três estratégias

| Versão | Estratégia | Formato |
|---|---|---|
| v1 | Pedido direto, restrito ao texto | Ficha textual |
| v2 | Esquema explícito e regra de ausência | JSON com strings/null |
| v3 | Extração com evidências e regras contra inferências | JSON com valor e trecho literal |

Os prompts completos estão em [prompts](prompts). Há quatro casos em [data/cases.json](data/cases.json): resumo completo, informações ausentes, tentativa de prompt injection e número sem métrica identificada.

## O que foi realmente feito

Foram criados três prompts e **12 respostas demonstrativas**, redigidas pelo assistente na mesma sessão de criação (três formatos para quatro casos). São exemplos trabalhados de comportamento esperado. **Não são 12 chamadas independentes ao modelo**, nem um benchmark controlado. O assistente teve acesso aos gabaritos; os exemplos não medem a capacidade de generalização de um LLM. O identificador exato do modelo e a temperatura não estão disponíveis, por isso são registrados como null. O histórico de commits representa etapas de implementação, não uma cronologia de experimentos científicos.

O avaliador executável verifica contratos de saída, abstenção nos campos ausentes, correspondência ao gabarito e presença literal das evidências. A correspondência textual ao gabarito é restritiva: uma paráfrase correta pode falhar. Evidência literal por si só não prova suporte semântico. A revisão humana continua necessária.

## Executar (Python 3.10+)

```bash
python src/lab.py prompt --version v3 --case injecao
python src/lab.py evaluate
python -m unittest discover -s tests -v
```

Sem API, chave, dependência externa ou serviço pago. O comando `prompt` monta o pedido para copiar em um chat; ele **não chama um modelo**. `evaluate` reavalia os exemplos registrados e atualiza `results/evaluation.json` e `results/report.md`.

Para avaliar respostas próprias, copie `results/session_examples.json`, substitua as respostas e atualize a proveniência com ferramenta/modelo, data, parâmetros e se houve acesso ao gabarito. Depois execute:

```bash
python src/lab.py evaluate --runs meus_resultados.json --output results/minha_avaliacao
```

## Resultados e interpretação

Veja [o relatório reproduzível](results/report.md) e [a metodologia](docs/methodology.md). v3 permite checar trechos de origem; v2 facilita integração por JSON; v1 favorece leitura direta. Esses são atributos dos formatos, **não evidência de superioridade de um modelo**. Não há medição de economia de tempo, usuários em produção ou robustez geral contra ataques.

## Próxima rodada independente

1. Escrever novos resumos e separar os gabaritos das entradas do modelo.
2. Executar cada prompt em conversas novas, sem mostrar outras respostas nem gabaritos.
3. Registrar modelo, data, configurações disponíveis e respostas sem corrigir.
4. Fazer revisão humana de correção, omissão e alegações sem suporte, além das verificações automáticas.
5. Comparar múltiplas repetições e contabilizar também custo e latência, se disponíveis.

## Estrutura

- `prompts/`: versões completas para copiar e adaptar.
- `data/`: entradas sintéticas, valores esperados e trechos de referência.
- `results/`: exemplos da sessão e avaliações reproduzíveis.
- `src/lab.py`: montagem dos prompts e validação das respostas.
- `tests/`: casos negativos para verificar o avaliador.
- `docs/`: metodologia e apresentação do projeto.

## Como apresentar

“Desenvolvi, com assistência de IA, um laboratório de prompts para extração de informações de resumos científicos, com três estratégias, casos sintéticos e validação automática de formato e evidências. O repositório inclui exemplos demonstrativos e documenta as limitações da avaliação.”

Este projeto demonstra prompts estruturados e uma exploração assistida por LLM. Não deve ser apresentado como solução em produção ou benchmark independente. Licença MIT.
