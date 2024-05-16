# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleCanvasRealizationHeader(models.Model):
    _name = "sale_canvas_realization_header"
    _description = "Sales Canvas Realization Header"

    canvas_id = fields.Many2one(
        comodel_name="sale_canvas",
        string="# Sales Canvas",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(string="Sequence", required=True, default=10)
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        default=lambda self: self._default_date(),
    )
    line_ids = fields.One2many(
        string="Realization Detail",
        comodel_name="sale_canvas_realization_line",
        inverse_name="realization_header_id",
    )
    sale_id = fields.Many2one(
        string="# Sale Order",
        comodel_name="sale.order",
        readonly=True,
    )

    @api.model
    def _default_date(self):
        return fields.Date.today()

    def _create_realization_detail(self):
        self.ensure_one()
        for detail in self.canvas_id.line_ids:
            detail._create_realization_detail(self)

    def _create_sale_order(self):
        self.ensure_one()

        if not self.sale_id:
            SaleOrder = self.env["sale.order"]
            sale = SaleOrder.create(
                self._prepare_sale_order(),
            )
            self.write(
                {
                    "sale_id": sale.id,
                }
            )
        else:
            self.sale_id.write(self._prepare_sale_order())

        for detail in self.line_ids.filtered(lambda r: r.uom_quantity > 0.0):
            detail._create_sale_order_line()

        self.sale_id.recalculate_prices()

    def _prepare_sale_order(self):
        self.ensure_one()
        return {
            "partner_id": self.partner_id.id,
            "date_order": self.date,
            "partner_invoice_id": self.partner_id.id,
            "partner_shipping_id": self.partner_id.id,
            "type_id": 1,  # TODO
            "pricelist_id": self.canvas_id.pricelist_id.id,
            "warehouse_id": self.canvas_id.outbound_warehouse_id.id,
        }

    def _cancel_sale_order(self):
        self.ensure_one()

        if not self.sale_id or self.sale_id.state not in ["draft", "sent"]:
            return True

        self.sale_id.action_cancel()

    @api.constrains(
        "canvas_id",
        "partner_id",
    )
    def check_double_partner(self):
        for rec in self:
            other_ids = self.search([
                ("canvas_id", "=", rec.canvas_id.id),
                ("partner_id", "=", rec.partner_id.id),
                ("id", "!=", rec.id),
            ])
            if other_ids:
                raise ValidationError(_(f"Double partner {rec.partner_id.display_name} in realization is not allowed."))
