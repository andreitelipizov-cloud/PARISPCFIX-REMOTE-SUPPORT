import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build', ROOT/'build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

class BuildEditionTests(unittest.TestCase):
    def test_original_build_has_no_brand_feature(self):
        with patch.dict(os.environ, {'PARISPCFIX_EDITION': ''}):
            args = build.make_parser().parse_args(['--flutter'])
            self.assertEqual(build.get_features(args), ['flutter'])

    def test_each_installer_selects_its_own_engine_edition(self):
        for edition in ('client', 'admin'):
            with self.subTest(edition=edition), patch.dict(os.environ, {'PARISPCFIX_EDITION': edition}):
                args = build.make_parser().parse_args(['--flutter'])
                self.assertEqual(build.get_features(args), ['parispcfix-'+edition, 'flutter'])

    def test_invalid_edition_is_rejected(self):
        with patch.dict(os.environ, {'PARISPCFIX_EDITION': '--bad'}):
            args = build.make_parser().parse_args(['--flutter'])
            with self.assertRaises(ValueError):
                build.get_features(args)

if __name__ == '__main__':
    unittest.main()
