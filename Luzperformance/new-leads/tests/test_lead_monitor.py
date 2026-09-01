import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).parents[1] / "monitor_leads.py"
spec = importlib.util.spec_from_file_location("monitor_leads", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Não foi possível carregar monitor_leads.py")
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


class LeadMonitorTests(unittest.TestCase):
    def test_format_phone_removes_brazil_country_code_and_formats_ddd(self):
        self.assertEqual(monitor.format_phone("+55 (48) 99999-1234"), "(48) 99999-1234")

    def test_format_phone_handles_country_code_without_plus(self):
        self.assertEqual(monitor.format_phone("5548999991234"), "(48) 99999-1234")

    def test_equal_last_two_rows_does_not_emit_a_lead(self):
        headers = ["Nome", "Telefone", "Email"]
        row = ["Ana", "+55 (48) 99999-1234", "ana@example.com"]
        self.assertIsNone(monitor.new_lead_message(headers, row, row))

    def test_different_last_row_emits_fields_and_formatted_phone(self):
        headers = ["Nome", "Telefone", "Email"]
        previous = ["Ana", "+55 (48) 99999-1234", "ana@example.com"]
        current = ["Bruno", "5548999887766", "bruno@example.com"]
        self.assertEqual(
            monitor.new_lead_message(headers, previous, current),
            "NOVO LEAD\nNome: Bruno\nTelefone: (48) 99988-7766\nEmail: bruno@example.com",
        )

    def test_notified_row_is_not_sent_again(self):
        row = ["Bruno", "5548999887766", "bruno@example.com"]
        self.assertFalse(monitor.should_notify(row, row))

    def test_new_row_is_sent_when_it_differs_from_the_last_notified_row(self):
        self.assertTrue(monitor.should_notify(["Bruno"], ["Ana"]))


if __name__ == "__main__":
    unittest.main()
