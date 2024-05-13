# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import hashlib
from base64 import b64decode, b64encode
from io import BytesIO

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.graphics.shapes import Drawing, Line, Rect
from reportlab.lib.colors import black, transparent
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.http import request


class SignOcaRequest(models.Model):

    _name = "sign.oca.request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Sign Request"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    template_id = fields.Many2one("sign.oca.template", readonly=True)
    data = fields.Binary(
        required=True, readonly=True, states={"draft": [("readonly", False)]}
    )
    filename = fields.Char()
    signed = fields.Boolean(copy=False)
    signer_ids = fields.One2many(
        "sign.oca.request.signer",
        inverse_name="request_id",
        auto_join=True,
        copy=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("signed", "Signed"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        readonly=True,
        required=True,
        copy=False,
        tracking=True,
    )
    signed_count = fields.Integer(compute="_compute_signed_count")
    signer_count = fields.Integer(compute="_compute_signer_count")
    to_sign = fields.Boolean(compute="_compute_to_sign")
    signatory_data = fields.Serialized(
        default=lambda r: {},
        readonly=True,
        copy=False,
    )
    current_hash = fields.Char(readonly=True, copy=False)
    company_id = fields.Many2one(
        "res.company",
        default=lambda r: r.env.company.id,
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    next_item_id = fields.Integer(compute="_compute_next_item_id")

    @api.depends("signatory_data")
    def _compute_next_item_id(self):
        for record in self:
            record.next_item_id = (
                record.signatory_data and max(record.signatory_data.keys()) or 0
            ) + 1

    def get_info(self):
        self.ensure_one()
        return {
            "name": self.name,
            "items": self.signatory_data,
            "roles": [
                {"id": signer.id, "name": signer.role_id.name}
                for signer in self.signer_ids
            ],
            "fields": [
                {"id": field.id, "name": field.name}
                for field in self.env["sign.oca.field"].search([])
            ],
        }

    def _ensure_draft(self):
        self.ensure_one()
        if not self.signer_ids:
            raise ValidationError(
                _("There are no signers, please fill them before configuring it")
            )
        if not self.state == "draft":
            raise ValidationError(_("You can only configure requests in draft state"))

    def configure(self):
        self._ensure_draft()
        self._set_action_log("configure")
        return {
            "type": "ir.actions.client",
            "tag": "sign_oca_configure",
            "name": self.name,
            "params": {
                "res_model": self._name,
                "res_id": self.id,
            },
        }

    def delete_item(self, item_id):
        self._ensure_draft()
        data = self.signatory_data
        data.pop(item_id)
        self.signatory_data = data
        self._set_action_log("delete_field")

    def set_item_data(self, item_id, vals):
        self._ensure_draft()
        data = self.signatory_data
        data[str(item_id)].update(vals)
        self.signatory_data = data
        self._set_action_log("edit_field")

    def add_item(self, item_vals):
        self._ensure_draft()
        item_id = self.next_item_id
        field_id = self.env["sign.oca.field"].browse(item_vals["field_id"])
        signatory_data = self.signatory_data
        signatory_data[item_id] = {
            "id": item_id,
            "field_id": field_id.id,
            "field_type": field_id.field_type,
            "required": False,
            "name": field_id.name,
            "role": self.signer_ids[0].role_id.id,
            "page": 1,
            "position_x": 0,
            "position_y": 0,
            "width": 0,
            "height": 0,
            "value": False,
            "default_value": field_id.default_value,
            "placeholder": "",
        }
        signatory_data[item_id].update(item_vals)
        self.signatory_data = signatory_data
        self._set_action_log("add_field")
        return signatory_data[item_id]

    def cancel(self):
        self.write({"state": "cancel"})
        self._set_action_log("cancel")

    @api.depends("signer_ids")
    def _compute_signer_count(self):
        for record in self:
            record.signer_count = len(record.signer_ids)

    @api.depends("signer_ids", "signer_ids.signed_on")
    def _compute_signed_count(self):
        for record in self:
            record.signed_count = len(record.signer_ids.filtered(lambda r: r.signed_on))

    def open_template(self):
        return self.template_id.configure()

    def action_send(self, sign_now=False, message=""):
        self.ensure_one()
        if self.state != "draft":
            return
        self._set_action_log("validate")
        self.state = "sent"
        for signer in self.signer_ids:
            signer._portal_ensure_token()
            if sign_now and signer.partner_id == self.env.user.partner_id:
                continue
            render_result = self.env["ir.qweb"]._render(
                "sign_oca.sign_oca_template_mail",
                {"record": signer, "body": message, "link": signer.access_url},
                engine="ir.qweb",
                minimal_qcontext=True,
            )
            self.env["mail.thread"].message_notify(
                body=render_result,
                partner_ids=signer.partner_id.ids,
                subject=_("New document to sign"),
                subtype_id=self.env.ref("mail.mt_comment").id,
                mail_auto_delete=False,
                email_layout_xmlid="mail.mail_notification_light",
            )

    @api.depends("signer_ids.role_id", "signatory_data")
    @api.depends_context("uid")
    def _compute_to_sign(self):
        for record in self:
            record.to_sign = record.signer_ids.filtered(
                lambda r: r.partner_id.id == self.env.user.partner_id.id
                and not r.signed_on
            ).mapped("role_id")

    def _check_signed(self):
        self.ensure_one()
        if self.state != "sent":
            return
        if all(self.mapped("signer_ids.signed_on")):
            self.state = "signed"

    def sign(self):
        self.ensure_one()
        signer = self.signer_ids.filtered(
            lambda r: r.partner_id == self.env.user.partner_id
        )
        if not signer:
            return self.get_formview_action()
        return {
            "type": "ir.actions.client",
            "tag": "sign_oca",
            "name": self.template_id.name,
            "params": {
                "res_model": signer[0]._name,
                "res_id": signer[0].id,
            },
        }

    def _set_action_log_vals(self, action, **kwargs):
        vals = kwargs.copy()
        vals.update(
            {"action": action, "request_id": self.id, "ip": self._get_action_log_ip()}
        )
        return vals

    def _get_action_log_ip(self):
        if not request or not hasattr(request, "httprequest"):
            # This comes from a server call. Set as localhost
            return "0.0.0.0"
        return request.httprequest.access_route[-1]

    def _set_action_log(self, action, **kwargs):
        self.ensure_one()
        return (
            self.env["sign.oca.request.log"]
            .sudo()
            .create(self._set_action_log_vals(action, **kwargs))
        )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record._set_action_log("create")
        return records


class SignOcaRequestSigner(models.Model):

    _name = "sign.oca.request.signer"
    _inherit = "portal.mixin"
    _description = "Sign Request Value"

    data = fields.Binary(related="request_id.data")
    request_id = fields.Many2one("sign.oca.request", required=True, ondelete="cascade")
    partner_name = fields.Char(related="partner_id.name")
    partner_id = fields.Many2one("res.partner", required=True, ondelete="restrict")
    role_id = fields.Many2one("sign.oca.role", required=True, ondelete="restrict")
    signed_on = fields.Datetime(readonly=True)
    signature_hash = fields.Char(readonly=True)

    def _compute_access_url(self):
        result = super()._compute_access_url()
        for record in self:
            record.access_url = "/sign_oca/document/%s/%s" % (
                record.id,
                record.access_token,
            )
        return result

    def get_info(self, access_token=False):
        self.ensure_one()
        self._set_action_log("view", access_token=access_token)
        return {
            "role": self.role_id.id if not self.signed_on else False,
            "name": self.request_id.template_id.name,
            "items": self.request_id.signatory_data,
            "to_sign": self.request_id.to_sign,
            "partner": {
                "id": self.env.user.partner_id.id,
                "name": self.env.user.partner_id.name,
                "email": self.env.user.partner_id.email,
                "phone": self.env.user.partner_id.phone,
            },
        }

    def action_sign(self, items, access_token=False):
        self.ensure_one()
        if self.signed_on:
            raise ValidationError(
                _("Users %s has already signed the document") % self.partner_id.name
            )
        if self.request_id.state != "sent":
            raise ValidationError(_("Request cannot be signed"))
        self.signed_on = fields.Datetime.now()
        # current_hash = self.request_id.current_hash
        signatory_data = self.request_id.signatory_data

        input_data = BytesIO(b64decode(self.request_id.data))
        reader = PdfFileReader(input_data)
        output = PdfFileWriter()
        pages = {}
        for page_number in range(1, reader.numPages + 1):
            pages[page_number] = reader.getPage(page_number - 1)

        for key in signatory_data:
            if signatory_data[key]["role"] == self.role_id.id:
                signatory_data[key] = items[key]
                self._check_signable(items[key])
                item = items[key]
                page = pages[item["page"]]
                new_page = self._get_pdf_page(item, page.mediaBox)
                if new_page:
                    page.mergePage(new_page)
                pages[item["page"]] = page
        for page_number in pages:
            output.addPage(pages[page_number])
        output_stream = BytesIO()
        output.write(output_stream)
        output_stream.seek(0)
        signed_pdf = output_stream.read()
        final_hash = hashlib.sha1(signed_pdf).hexdigest()
        # TODO: Review that the hash has not been changed...
        self.request_id.write(
            {
                "signatory_data": signatory_data,
                "data": b64encode(signed_pdf),
                "current_hash": final_hash,
            }
        )
        self.signature_hash = final_hash
        self.request_id._check_signed()
        self._set_action_log("sign", access_token=access_token)
        # TODO: Add a return

    def _check_signable(self, item):
        if not item["required"]:
            return
        if not item["value"]:
            raise ValidationError(_("Field %s is not filled") % item["name"])

    def _get_pdf_page_text(self, item, box):
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=(box.getWidth(), box.getHeight()))
        if not item["value"]:
            return False
        par = Paragraph(item["value"], style=self._getParagraphStyle())
        par.wrap(
            item["width"] / 100 * float(box.getWidth()),
            item["height"] / 100 * float(box.getHeight()),
        )
        par.drawOn(
            can,
            item["position_x"] / 100 * float(box.getWidth()),
            (100 - item["position_y"] - item["height"]) / 100 * float(box.getHeight()),
        )
        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        return new_pdf.getPage(0)

    def _getParagraphStyle(self):
        return ParagraphStyle(name="Oca Sign Style")

    def _get_pdf_page_check(self, item, box):
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=(box.getWidth(), box.getHeight()))
        width = item["width"] / 100 * float(box.getWidth())
        height = item["height"] / 100 * float(box.getHeight())
        drawing = Drawing(width=width, height=height)
        drawing.add(
            Rect(
                0,
                0,
                width,
                height,
                strokeWidth=3,
                strokeColor=black,
                fillColor=transparent,
            )
        )
        if item["value"]:
            drawing.add(Line(0, 0, width, height, strokeColor=black, strokeWidth=3))
            drawing.add(Line(0, height, width, 0, strokeColor=black, strokeWidth=3))
        drawing.drawOn(
            can,
            item["position_x"] / 100 * float(box.getWidth()),
            (100 - item["position_y"] - item["height"]) / 100 * float(box.getHeight()),
        )
        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        return new_pdf.getPage(0)

    def _get_pdf_page_signature(self, item, box):
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=(box.getWidth(), box.getHeight()))
        if not item["value"]:
            return False
        par = Image(
            BytesIO(b64decode(item["value"])),
            width=item["width"] / 100 * float(box.getWidth()),
            height=item["height"] / 100 * float(box.getHeight()),
        )
        par.drawOn(
            can,
            item["position_x"] / 100 * float(box.getWidth()),
            (100 - item["position_y"] - item["height"]) / 100 * float(box.getHeight()),
        )
        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        return new_pdf.getPage(0)

    def _get_pdf_page(self, item, box):
        return getattr(self, "_get_pdf_page_%s" % item["field_type"])(item, box)

    def _set_action_log(self, action, **kwargs):
        self.ensure_one()
        return self.request_id._set_action_log(action, signer_id=self.id, **kwargs)

    def name_get(self):
        result = [(signer.id, (signer.partner_id.display_name)) for signer in self]
        return result


class SignRequestLog(models.Model):
    _name = "sign.oca.request.log"
    _log_access = False
    _description = "Log access and edition on requests"

    uid = fields.Many2one(
        "res.users",
        required=True,
        readonly=True,
        ondelete="cascade",
        default=lambda r: r.env.user.id,
    )
    date = fields.Datetime(
        required=True, readonly=True, default=lambda r: fields.Datetime.now()
    )
    partner_id = fields.Many2one(
        "res.partner", required=True, default=lambda r: r.env.user.partner_id.id
    )
    request_id = fields.Many2one("sign.oca.request", required=True, ondelete="cascade")
    signer_id = fields.Many2one("sign.oca.request.signer")
    action = fields.Selection(
        [
            ("create", "Create"),
            ("validate", "Validate"),
            ("view", "View Document"),
            ("sign", "Sign"),
            ("add_field", "Add field"),
            ("edit_field", "Edit field"),
            ("delete_field", "Delete field"),
            ("cancel", "Cancel"),
            ("configure", "Configure"),
        ],
        required=True,
        readonly=True,
    )
    access_token = fields.Char(readonly=True)
    ip = fields.Char(readonly=True)
