# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleCanvasRealizationLine(models.Model):
    _name = "sale_canvas_realization_line"
    _description = "Sales Canvas Realization Line"
    _inherit = [
        "mixin.product_line",
    ]

    canvas_id = fields.Many2one(
        comodel_name="sale_canvas",
        string="# Sales Canvas",
        required=True,
        ondelete="cascade",
    )
    realization_header_id = fields.Many2one(
        comodel_name="sale_canvas_realization_header",
        string="Realization Header",
        required=False,
        ondelete="set null",
    )
    line_id = fields.Many2one(
        string="Sale Canvas Line",
        comodel_name="sale_canvas_line",
        required=False,
    )
    sequence = fields.Integer(string="Sequence", required=True, default=10)
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
    )
    stock_move_ids = fields.Many2many(
        comodel_name="stock.move",
        string="Stock Moves",
        relation="rel_sale_canvas_realization_line_2_stock_move",
        column1="line_id",
        column2="move_id",
        copy=False,
    )
    product_id = fields.Many2one(
        required=True,
    )
    uom_id = fields.Many2one(
        required=True,
    )
    sale_line_id = fields.Many2one(
        string="Sales Order Line",
        comodel_name="sale.order.line",
        readonly=True,
    )
    sale_line_product_id = fields.Many2one(
        string="SO Line Product",
        related="sale_line_id.product_id",
        store=True,
    )
    sale_line_uom_id = fields.Many2one(
        string="SO Line UoM",
        related="sale_line_id.product_uom",
        store=True,
    )
    sale_line_uom_quantity = fields.Float(
        string="SO Line Qty", related="sale_line_id.product_uom_qty", store=True
    )

    @api.constrains(
        "sale_line_id",
        "sale_line_product_id",
        "sale_line_uom_id",
        "sale_line_uom_quantity",
    )
    def _sale_line_check(self):
        if self.env.context.get("force_update"):
            return False
        for rec in self:
            if rec.sale_line_id and (
                rec.product_id != rec.sale_line_product_id
                or rec.uom_id != rec.sale_line_uom_id
                or rec.uom_quantity != rec.sale_line_uom_quantity
            ):
                raise ValidationError(
                    _(
                        "You cannot change item details that created from sale canvas menu."
                    )
                )

    def _create_sale_order_line(self):
        self.ensure_one()
        OrderLine = self.env["sale.order.line"]
        line = OrderLine.create(
            self._prepare_sale_order_line(),
        )
        self.write(
            {
                "sale_line_id": line.id,
            }
        )

    def _prepare_sale_order_line(self):
        self.ensure_one()
        return {
            "order_id": self.realization_header_id.sale_id.id,
            "name": self.name,
            "price_unit": 0.0,
            "product_id": self.product_id.id,
            "product_uom": self.uom_id.id,
            "product_uom_qty": self.uom_quantity,
            "route_id": self.canvas_id.route_id.id,
        }
