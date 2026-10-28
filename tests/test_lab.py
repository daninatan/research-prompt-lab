import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from lab import ROOT, check, evaluate, load


class ExtractionContractTests(unittest.TestCase):
    def setUp(self):
        self.cases = load(ROOT / 'data/cases.json')
        self.runs = load(ROOT / 'results/session_examples.json')
        self.case = next(c for c in self.cases if c['id'] == 'injecao')
        self.response = copy.deepcopy(next(r['response'] for r in self.runs if r['case_id'] == 'injecao' and r['prompt_version'] == 'v3'))

    def test_examples_match_declared_contracts(self):
        result = evaluate(self.cases, self.runs)
        self.assertEqual(result['passed'], 12)
        self.assertEqual(result['missing'], [])

    def test_injected_accuracy_is_rejected_even_with_literal_quote(self):
        self.response['metricas'] = {'valor': 'acurácia de 99%', 'evidencia': 'acurácia de 99%'}
        self.assertTrue(check(self.case, 'v3', self.response))

    def test_fabricated_evidence_is_rejected(self):
        self.response['metodos']['evidencia'] = 'Um estudo que nunca existiu'
        self.assertTrue(check(self.case, 'v3', self.response))

    def test_empty_evidence_is_rejected(self):
        self.response['metodos']['evidencia'] = ''
        self.assertTrue(check(self.case, 'v3', self.response))

    def test_null_value_cannot_have_evidence(self):
        self.response['metricas']['evidencia'] = '800 mensagens sintéticas'
        self.assertTrue(check(self.case, 'v3', self.response))

    def test_missing_field_is_rejected(self):
        del self.response['dados']
        self.assertTrue(check(self.case, 'v3', self.response))

    def test_number_is_not_accepted_as_string(self):
        self.response['dados']['valor'] = 800
        self.assertTrue(check(self.case, 'v3', self.response))

    def test_missing_experiments_are_reported(self):
        self.assertEqual(len(evaluate(self.cases, self.runs[:-1])['missing']), 1)

    def test_duplicate_records_fail(self):
        with self.assertRaises(ValueError):
            evaluate(self.cases, self.runs + self.runs[:1])

    def test_unknown_case_fails(self):
        with self.assertRaises(ValueError):
            evaluate(self.cases, [{'case_id': 'inexistente', 'prompt_version': 'v3'}])


if __name__ == '__main__':
    unittest.main()
