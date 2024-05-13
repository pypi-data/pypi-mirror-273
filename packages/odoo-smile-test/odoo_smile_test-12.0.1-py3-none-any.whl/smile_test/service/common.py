# -*- coding: utf-8 -*-

import logging
import os
import threading
import coverage

from odoo.service import common
from odoo.service.db import check_super
from odoo.tests.common import BaseCase
from odoo.tools import config
from odoo.modules import get_module_path

from .. import tools

_logger = logging.getLogger(__name__)


OMIT_FILES = [
    "__manifest__.py",
    "__openerp__.py",
    "__terp__.py",
    "__init__.py",
]
OMIT_DIRS = ["web", "static", "controllers", "doc", "test", "tests"]


class NewServices:

    @staticmethod
    def coverage_start():
        if hasattr(common, "coverage"):
            return False
        _logger.info("Starting code coverage...")
        module_path = get_module_path('smile_test')
        dft_config_file = os.path.join(module_path, ".coveragerc")
        _logger.info('default coveragerc file: %s', dft_config_file)
        config_file = config.get("coverage_config_file") or dft_config_file
        _logger.info('coverage config file: %s', config_file)
        data_file = config.get("coverage_data_file") or '/tmp/.coveragerc'
        common.coverage = coverage.coverage(
            data_file=data_file,
            config_file=config_file,
        )
        common.coverage.start()
        return True

    @staticmethod
    def coverage_stop():
        if not hasattr(common, "coverage"):
            return False
        _logger.info("Stopping code coverage...")
        common.coverage.stop()
        common.coverage.save()
        coverage_result = tools.test_utils._get_coverage_result_file()
        common.coverage.xml_report(
            outfile=coverage_result,
            ignore_errors=True,
        )
        del common.coverage
        return True

    @staticmethod
    def run_tests(dbname, modules=None, with_coverage=True):
        init_test_enable = config.get("test_enable")
        config["test_enable"] = True
        threading.currentThread().dbname = dbname
        modules = tools.filter_modules_list(dbname, modules)
        tools.test_utils._remove_results_files()
        tools.run_unit_tests(dbname, modules)
        tools.run_other_tests(dbname, modules)
        config["test_enable"] = init_test_enable
        return True

    @staticmethod
    def prepare_results_files():
        result = {"tests": {}}
        coverage_result_file = tools.test_utils._get_coverage_result_file()
        test_result_directory = tools.test_utils._get_test_result_directory()
        for file in os.listdir(test_result_directory):
            file_path = os.path.join(test_result_directory, file)
            with open(file_path, "r") as test:
                result["tests"][file] = test.read()
        with open(coverage_result_file, "r") as file:
            result["coverage"] = file.read()
        return result


native_dispatch = common.dispatch
additional_methods = [
    attr
    for attr in dir(NewServices)
    if not attr.startswith("_") and callable(getattr(NewServices, attr))
]

def new_dispatch(*args):
    i = 0
    method = args[i]
    if method in additional_methods:
        params = args[i + 1]
        admin_passwd, params = params[0], params[1:]
        check_super(admin_passwd)
        return getattr(NewServices, method)(*params)
    return native_dispatch(*args)


common.dispatch = new_dispatch

# only if AUTO_COVERAGE env var is set
if os.environ.get("AUTO_COVERAGE", False):
    NewServices.coverage_start()

@classmethod
def tearDownClass(cls):
    if hasattr(cls, "cr"):
        cls.cr.close()
    old_tearDownClass()


old_tearDownClass = BaseCase.tearDownClass
BaseCase.tearDownClass = tearDownClass
