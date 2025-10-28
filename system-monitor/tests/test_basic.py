import unittest
import importlib

class TestImport(unittest.TestCase):
    def test_import(self):
        # Basic import check (ensures dependencies are resolvable, module loads)
        mod = importlib.import_module("monitor")
        self.assertTrue(hasattr(mod, "format_bytes"))
        self.assertTrue(callable(mod.format_bytes))

    def test_format_bytes(self):
        from monitor import format_bytes
        self.assertEqual(format_bytes(1023), "1023.0 B")
        self.assertEqual(format_bytes(1024), "1.0 KB")
        self.assertEqual(format_bytes(1024*1024), "1.0 MB")

if __name__ == "__main__":
    unittest.main()
