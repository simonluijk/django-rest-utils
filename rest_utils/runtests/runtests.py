#!/usr/bin/env python

import os
import sys

# fix sys path so we don't need to setup PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rest_utils.runtests.settings'

import django
from django.conf import settings
from django.test.utils import get_runner


def main():
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    module_name = 'rest_utils.tests'
    if django.VERSION[0] == 1 and django.VERSION[1] < 6:
        module_name = 'rest_utils'

    failures = test_runner.run_tests([module_name])
    sys.exit(failures)


if __name__ == '__main__':
    main()
