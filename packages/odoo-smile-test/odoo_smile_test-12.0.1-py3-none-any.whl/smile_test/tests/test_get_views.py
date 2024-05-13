# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestGetViews(TransactionCase):

    def test_check_get_views(self):
        """I check all get_views."""
        errors = []
        models = self.env["ir.model"].search([])
        for model in models:
            if getattr(model, "_abstract", False):
                continue
            for view_type in ["form", "tree"]:
                try:
                    self.env[model.model].get_views(views=[(False, view_type)])
                except Exception as e:
                    err_info = (model.model, view_type, repr(e))
                    errors.append(err_info)
        err_details = "\n".join(
            "({model}, {view_type}): {err}".format(
                model=model, view_type=view_type, err=err
            )
            for model, view_type, err in errors
        )
        error_msg = (
            "Error in get_views for models/view_type "
            "and error:\n%s" % err_details
        )
        self.assertEqual(len(errors), 0, error_msg)
