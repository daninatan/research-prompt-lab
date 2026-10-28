# Research Prompt Lab

Laboratório de prompts para extrair informações de resumos científicos em português e organizar os resultados em fichas estruturadas.

O projeto explora três estratégias de extração, com um avaliador local em Python para verificar formato, informações ausentes e trechos de evidência.

## Funcionalidades

- Extração de objetivo, dados, métodos, métricas e limitações.
- Três versões de prompt: ficha textual, JSON simples e JSON com evidências.
- Casos sintéticos com informações completas, campos ausentes, números ambíguos e tentativas de prompt injection.
- Verificação automática das respostas com testes e integração contínua no GitHub Actions.

## Estratégias de prompt

| Versão | Abordagem | Saída |
|---|---|---|
| v1 | Extração direta a partir do texto | Ficha textual |
| v2 | Esquema explícito e tratamento de campos ausentes | JSON com strings ou null |
| v3 | Extração acompanhada de trechos literais da fonte | JSON com valor e evidência |

Os prompts estão disponíveis em [prompts/](prompts). Os quatro casos de exemplo e seus valores de referência estão em [data/cases.json](data/cases.json).

## Requisitos

Python 3.10 ou superior. Utiliza apenas a biblioteca padrão, sem dependências externas.

## Uso

Na raiz do projeto, monte um prompt para um dos casos disponíveis:

```bash
python src/lab.py prompt --version v3 --case injecao
```

O comando imprime o prompt com o texto de entrada para uso em um modelo de linguagem. A geração das respostas é manual; o programa não faz chamadas a APIs.

Avalie os exemplos incluídos:

```bash
python src/lab.py evaluate
```

A avaliação gera `results/evaluation.json` e `results/report.md`.

Execute os testes:

```bash
python -m unittest discover -s tests -v
```

### Avaliar novas respostas

Use `results/session_examples.json` como referência de formato. Crie um arquivo com suas respostas e registre a origem, o modelo, a data e os parâmetros disponíveis. Informe também se o modelo teve acesso ao gabarito.

```bash
python src/lab.py evaluate --runs meus_resultados.json --output results/minha_avaliacao
```

Os identificadores de casos devem corresponder aos definidos em `data/cases.json`.

## Avaliação

O avaliador verifica:

- Estrutura e tipos dos campos de cada versão.
- Correspondência dos valores com o gabarito.
- Uso de null nos campos sem informação.
- Presença de trechos literais como evidência na versão v3.
- Registros duplicados, casos desconhecidos e combinações ausentes.

O conjunto incluído contém 12 respostas demonstrativas elaboradas com assistência de IA e acesso aos gabaritos. Essas respostas servem para exercitar o avaliador; não representam execuções independentes dos prompts nem um benchmark de desempenho de LLMs.

A comparação exata com o gabarito pode rejeitar paráfrases corretas. A presença literal de uma evidência também não garante que ela sustente semanticamente a resposta. A análise de qualidade exige revisão humana.

Consulte o [relatório dos exemplos](results/report.md) e a [metodologia](docs/methodology.md) para detalhes sobre os dados e os critérios de avaliação.

## Estrutura

```text
research-prompt-lab/
├── prompts/            # Três versões dos prompts
├── data/               # Textos sintéticos e gabaritos
├── src/lab.py          # Montagem de prompts e avaliação
├── tests/              # Testes do avaliador
├── results/            # Exemplos e relatórios
├── docs/               # Metodologia
└── .github/workflows/  # Verificações automatizadas
```

## Próximos passos

- Ampliar os casos com novos temas e formatos de resumo.
- Executar os prompts em sessões independentes, sem acesso aos gabaritos.
- Registrar modelo, configurações, custo e latência quando disponíveis.
- Complementar a avaliação automática com revisão semântica das respostas.

## Licença

[MIT](LICENSE).
