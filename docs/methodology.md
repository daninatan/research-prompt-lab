# Metodologia e limites

## Pergunta
Como tornar uma ficha científica verificável e evitar preencher lacunas por inferência?

## Dados
Quatro textos sintéticos em português: completo; incompleto; documento com comando malicioso; número sem métrica. Nos dois últimos, não aceitar o número como resultado é parte do comportamento esperado. Uma característica da base (por exemplo, origem regional) não deve virar uma limitação atribuída ao autor quando ele não a declara.

## Registro desta sessão
O assistente elaborou entradas, gabaritos, prompts e respostas na mesma conversa. As respostas foram redigidas com conhecimento do gabarito e não representam execução cega dos prompts. O arquivo `results/session_examples.json` contém essa proveniência em cada registro. Não há API, comparação entre modelos, amostragem independente ou identificação verificável de versão do modelo. O desenho é uma demonstração de contratos de extração, com viés de seleção explícito.

## Verificações
- v1: presença dos cinco rótulos e frases esperadas. Não mede qualidade de texto livre.
- v2: cinco chaves exatas e valores string/null.
- v3: cinco chaves, cada uma com valor/evidencia; evidência não vazia e literal quando há valor; ambos null em ausências.
- Para todos: comparação de valores com o gabarito e abstenção nos campos sem informação.

Não comparar contagens de verificações entre versões: os contratos são diferentes. A pontuação exata é uma checagem das fixtures, não acurácia científica. O avaliador não reconhece todas as paráfrases, não detecta toda alucinação e não garante que uma evidência sustente o valor. Isso exige revisão humana.

## Leitura qualitativa dos exemplos
v1 entrega leitura direta, mas exige tratamento de texto livre. v2 permite consumo programático, porém não mostra a origem de cada afirmação. v3 acrescenta trechos literais, ao custo de respostas maiores. Todos os exemplos se abstêm nos campos ausentes. Não se conclui que um LLM sempre fará isso: são exemplos preparados, com apenas quatro entradas.

## Reprodução
Os arquivos de respostas permanecem preservados. `python src/lab.py evaluate` reproduz apenas a avaliação local. Para reproduzir geração de maneira independente, executar novas sessões conforme o README e guardar as respostas brutas. Não há alegação de resultado empírico de geração reproduzível nesta versão.
