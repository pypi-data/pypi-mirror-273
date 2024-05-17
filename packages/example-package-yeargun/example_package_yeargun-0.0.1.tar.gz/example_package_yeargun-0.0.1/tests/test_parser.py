import unittest
from json24 import parse_partial_json, parse_partial_json_with_logging, ParseOptions, FaultyJson

class TestJson24(unittest.TestCase):

    def test_parse_partial_json(self):
        json_string = '{"key1": "value1", "key2": 42, "key3": true, "key4": false, "key5": null}'
        options = ParseOptions(has_null=True)
        result = parse_partial_json(json_string, options)
        expected = {"key1": "value1", "key2": 42, "key3": True, "key4": False, "key5": None}
        self.assertEqual(result, expected)

    def test_parse_partial_json_with_logging(self):
        json_string = '{"key1": "value1", "key2": 42, "key3": true, "key4": false, "key5": null}'
        options = ParseOptions(has_null=True)
        result = parse_partial_json_with_logging(json_string, options)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["key5"], None)

if __name__ == '__main__':
    unittest.main()
