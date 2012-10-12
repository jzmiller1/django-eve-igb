#!/usr/bin/env python

import os
import sys

from django.conf import settings

EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
]

INTERNAL_APPS = ['eveigb','django_nose',]
INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS

COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', 'urls$', 'locale$',
    'migrations', 'fixtures', 'admin$', 'django_extensions',
]

COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS

if not settings.configured:
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        INSTALLED_APPS=INSTALLED_APPS,
        COVERAGE_MODULE_EXCLUDES=COVERAGE_MODULE_EXCLUDES,
        COVERAGE_REPORT_HTML_OUTPUT_DIR=os.path.join(
            os.path.dirname(__file__), 'coverage'),
        SITE_ID=1
    )
        

from django_coverage.coverage_runner import CoverageRunner
from django_nose import NoseTestSuiteRunner

class NoseCoverageTestRunner(CoverageRunner, NoseTestSuiteRunner):
    pass

def runtests(*test_args):
    failures = NoseCoverageTestRunner(
        verbosity=2,
        interactive=True
    ).run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])