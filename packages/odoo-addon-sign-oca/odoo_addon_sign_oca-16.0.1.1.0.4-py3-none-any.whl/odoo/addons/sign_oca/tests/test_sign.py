# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.modules.module import get_module_resource
from odoo.tests.common import Form, TransactionCase


class TestSign(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = base64.b64encode(
            open(
                get_module_resource("sign_oca", "tests", "empty.pdf"),
                "rb",
            ).read()
        )
        cls.template = cls.env["sign.oca.template"].create(
            {
                "data": cls.data,
                "name": "Demo template",
                "filename": "empty.pdf",
            }
        )
        cls.signer = cls.env["res.partner"].create({"name": "Signer"})
        cls.request = cls.env["sign.oca.request"].create(
            {
                "data": cls.data,
                "name": "Demo template",
                "signer_ids": [
                    (
                        0,
                        0,
                        {
                            "partner_id": cls.signer.id,
                            "role_id": cls.env.ref("sign_oca.sign_role_customer").id,
                        },
                    )
                ],
            }
        )

    def configure_template(self):
        self.template.add_item(
            {
                "field_id": self.env.ref("sign_oca.sign_field_name").id,
                "page": 1,
                "position_x": 10,
                "position_y": 10,
                "width": 10,
                "height": 10,
                "required": True,
            }
        )

    def configure_request(self):
        return self.request.add_item(
            {
                "field_id": self.env.ref("sign_oca.sign_field_name").id,
                "role_id": self.env.ref("sign_oca.sign_role_customer").id,
                "page": 1,
                "position_x": 10,
                "position_y": 10,
                "width": 10,
                "height": 10,
                "required": True,
            }
        )

    def test_template_configuration(self):
        self.assertFalse(self.template.get_info()["items"])
        self.configure_template()
        self.assertTrue(self.template.get_info()["items"])

    def test_template_field_edition(self):
        self.configure_template()
        self.assertEqual(
            self.template.item_ids.role_id, self.env.ref("sign_oca.sign_role_customer")
        )
        self.template.set_item_data(
            self.template.item_ids.id,
            {"role_id": self.env.ref("sign_oca.sign_role_employee").id},
        )
        self.assertEqual(
            self.template.item_ids.role_id, self.env.ref("sign_oca.sign_role_employee")
        )

    def test_template_field_delete(self):
        self.configure_template()
        self.assertTrue(self.template.item_ids)
        self.template.delete_item(self.template.item_ids.id)
        self.assertFalse(self.template.item_ids)

    def test_request_configuration(self):
        self.assertFalse(self.request.get_info()["items"])
        self.configure_request()
        self.assertTrue(self.request.get_info()["items"])

    def test_request_field_edition(self):
        item = self.configure_request()
        self.assertEqual(
            self.request.get_info()["items"][str(item["id"])]["role_id"],
            self.env.ref("sign_oca.sign_role_customer").id,
        )
        self.request.set_item_data(
            str(item["id"]), {"role_id": self.env.ref("sign_oca.sign_role_employee").id}
        )
        self.assertEqual(
            self.request.get_info()["items"][str(item["id"])]["role_id"],
            self.env.ref("sign_oca.sign_role_employee").id,
        )

    def test_request_field_delete(self):
        item = self.configure_request()
        self.assertTrue(self.request.get_info()["items"])
        self.request.delete_item(str(item["id"]))
        self.assertFalse(self.request.get_info()["items"])

    def test_auto_sign_template(self):
        self.configure_template()
        self.assertEqual(0, self.template.request_count)
        f = Form(
            self.env["sign.oca.template.generate"].with_context(
                default_template_id=self.template.id, default_sign_now=True
            )
        )
        action = f.save().generate()
        self.assertEqual(action["tag"], "sign_oca")
        signer = self.env[action["params"]["res_model"]].browse(
            action["params"]["res_id"]
        )
        self.assertEqual(1, self.template.request_count)
        self.assertIn(signer.request_id, self.template.request_ids)
        self.assertEqual(self.env.user.partner_id, signer.partner_id)
        self.assertTrue(signer.get_info()["items"])
        data = {}
        for key in signer.get_info()["items"]:
            val = signer.get_info()["items"][key].copy()
            val["value"] = "My Name"
            data[key] = val
        signer.action_sign(data)
        self.assertEqual(signer.request_id.state, "signed")

    def test_auto_sign_template_cancel(self):
        self.configure_template()
        self.assertEqual(0, self.template.request_count)
        f = Form(
            self.env["sign.oca.template.generate"].with_context(
                default_template_id=self.template.id, default_sign_now=True
            )
        )
        action = f.save().generate()
        self.assertEqual(action["tag"], "sign_oca")
        signer = self.env[action["params"]["res_model"]].browse(
            action["params"]["res_id"]
        )
        signer.request_id.cancel()
        self.assertEqual(signer.request_id.state, "cancel")
