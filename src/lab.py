"""Laboratório local de contratos de extração. Não executa chamadas a LLMs."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ('objetivo', 'dados', 'metodos', 'metricas', 'limitacoes')


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def check(case, version, response):
    errors = []
    expected = dict(zip(FIELDS, case['values']))
    if version == 'v1':
        if not isinstance(response, str):
            return ['v1 exige texto']
        lines = response.splitlines()
        if len(lines) != len(FIELDS):
            errors.append('v1 exige exatamente cinco linhas rotuladas')
        for field, value in expected.items():
            wanted = f'{field}: {value if value is not None else "Não informado."}'
            if wanted not in lines:
                errors.append(f'{field}: linha diferente do gabarito')
        return errors
    if version not in ('v2', 'v3'):
        return ['versão desconhecida']
    if not isinstance(response, dict) or set(response) != set(FIELDS):
        return ['chaves da ficha inválidas']
    for field in FIELDS:
        item = response[field]
        if version == 'v3':
            if not isinstance(item, dict) or set(item) != {'valor', 'evidencia'}:
                errors.append(f'{field}: estrutura inválida')
                continue
            value, evidence = item['valor'], item['evidencia']
            if value is None:
                if evidence is not None:
                    errors.append(f'{field}: ausência exige evidência null')
            elif not isinstance(evidence, str) or not evidence.strip() or evidence not in case['text']:
                errors.append(f'{field}: evidência literal ausente ou inválida')
        else:
            value = item
        if value is not None and not isinstance(value, str):
            errors.append(f'{field}: valor deve ser string/null')
        if value != expected[field]:
            errors.append(f'{field}: valor diferente do gabarito')
    return errors


def evaluate(cases, runs):
    by_id = {c['id']: c for c in cases}
    seen = set()
    rows = []
    for run in runs:
        key = (run.get('case_id'), run.get('prompt_version'))
        if key in seen:
            raise ValueError(f'Registro duplicado: {key}')
        seen.add(key)
        if key[0] not in by_id:
            raise ValueError(f'Caso desconhecido: {key[0]}')
        errors = check(by_id[key[0]], key[1], run.get('response'))
        rows.append(dict(case_id=key[0], prompt_version=key[1], passed=not errors, errors=errors))
    missing = sorted(set((c['id'], v) for c in cases for v in ('v1', 'v2', 'v3')) - seen)
    return dict(scope='Verificação de exemplos; não mede desempenho independente de LLM.',
                records=len(rows), passed=sum(r['passed'] for r in rows),
                missing=[list(x) for x in missing], results=rows)


def report(result):
    lines = ['# Verificação dos exemplos da sessão', '', result['scope'], '',
             f"Registros: {result['records']}. Aprovados nas verificações: {result['passed']}. Combinações ausentes: {len(result['missing'])}.", '',
             '| Caso | Prompt | Contrato e gabarito |', '|---|---|---|']
    for row in result['results']:
        lines.append(f"| {row['case_id']} | {row['prompt_version']} | {'OK' if row['passed'] else 'FALHOU'} |")
    lines += ['', 'Os exemplos foram elaborados com acesso ao gabarito; aprovação não demonstra robustez, acurácia de geração ou superioridade de uma versão.', '',
              'A comparação é de contratos: v1 produz texto; v2 produz JSON; v3 acrescenta evidências. Diferentes exigências impedem tratar as verificações como uma competição justa de desempenho.', '',
              'A evidência literal requer revisão semântica humana. Campos sem informação devem permanecer ausentes. Nenhum resultado da pesquisa original foi utilizado.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    prompt = sub.add_parser('prompt', help='Monta um prompt para uso manual; não chama uma API')
    prompt.add_argument('--version', choices=('v1', 'v2', 'v3'), required=True)
    prompt.add_argument('--case', required=True)
    ev = sub.add_parser('evaluate')
    ev.add_argument('--runs', type=Path, default=ROOT / 'results/session_examples.json')
    ev.add_argument('--output', type=Path, default=ROOT / 'results')
    args = parser.parse_args()
    cases = load(ROOT / 'data/cases.json')
    if args.command == 'prompt':
        case = next((c for c in cases if c['id'] == args.case), None)
        if case is None:
            parser.error('Caso desconhecido. Opções: ' + ', '.join(c['id'] for c in cases))
        template = (ROOT / f'prompts/{args.version}.txt').read_text(encoding='utf-8')
        print(template.replace('{{texto}}', case['text']))
    else:
        result = evaluate(cases, load(args.runs))
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / 'evaluation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (args.output / 'report.md').write_text(report(result), encoding='utf-8')
        print(f"{result['passed']}/{result['records']} exemplos aprovados; {len(result['missing'])} combinações ausentes.")
        if result['missing'] or any(not r['passed'] for r in result['results']):
            raise SystemExit(1)


if __name__ == '__main__':
    main()
