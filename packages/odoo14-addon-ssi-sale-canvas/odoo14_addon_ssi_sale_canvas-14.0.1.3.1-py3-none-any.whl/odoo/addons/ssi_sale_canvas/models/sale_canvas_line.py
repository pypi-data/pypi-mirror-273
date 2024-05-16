# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleCanvasLine(models.Model):
    _name = "sale_canvas_line"
    _description = "Sales Canvas Line"
    _inherit = [
        "mixin.product_line",
    ]

    canvas_id = fields.Many2one(
        comodel_name="sale_canvas",
        string="# Sales Canvas",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(string="Sequence", required=True, default=10)
    stock_move_ids = fields.Many2many(
        comodel_name="stock.move",
        string="Stock Moves",
        relation="rel_sale_canvas_line_2_stock_move",
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
    qty_to_receive = fields.Float(
        string="Qty to Receive", compute="_compute_qty_to_receive", store=True
    )
    qty_incoming = fields.Float(
        string="Qty Incoming",
        compute="_compute_qty_incoming",
    )
    qty_received = fields.Float(
        string="Qty Received", compute="_compute_qty_received", store=True
    )
    qty_to_deliver = fields.Float(
        string="Qty to Deliver", compute="_compute_qty_to_deliver", store=True
    )
    qty_outgoing = fields.Float(
        string="Qty Outgoing",
        compute="_compute_qty_outgoing",
    )
    qty_delivered = fields.Float(
        string="Qty Delivered", compute="_compute_qty_delivered", store=True
    )
    qty_to_sell = fields.Float(
        string="Qty To Sell",
        compute="_compute_qty_to_sell",
        store=True,
    )
    qty_sold = fields.Float(
        string="Qty Solf",
        compute="_compute_qty_sold",
        store=True,
    )
    realization_line_ids = fields.One2many(
        string="Realization Detail",
        comodel_name="sale_canvas_realization_line",
        inverse_name="line_id",
    )

    @api.depends(
        "realization_line_ids",
        "realization_line_ids.sale_line_id",
        "realization_line_ids.sale_line_id.product_uom_qty",
        "realization_line_ids.sale_line_id.order_id.state",
    )
    def _compute_qty_sold(self):
        for record in self:
            result = 0.0
            for line in record.realization_line_ids:
                if line.sale_line_id and line.sale_line_id.order_id.state in [
                    "sale",
                    "done",
                ]:
                    result += line.sale_line_id.product_uom_qty
            record.qty_sold = result

    @api.depends(
        "realization_line_ids",
        "realization_line_ids.sale_line_id",
        "realization_line_ids.sale_line_id.product_uom_qty",
        "realization_line_ids.sale_line_id.order_id.state",
    )
    def _compute_qty_to_sell(self):
        for record in self:
            result = 0.0
            for line in record.realization_line_ids:
                if line.sale_line_id and line.sale_line_id.order_id.state in [
                    "draft",
                    "sent",
                ]:
                    result += line.sale_line_id.product_uom_qty
            record.qty_to_sell = result

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
        "qty_delivered",
        "qty_received",
        "qty_incoming",
        "qty_sold",
        "canvas_id.state",
    )
    def _compute_qty_to_receive(self):
        for record in self:
            record.qty_to_receive = (
                record.qty_delivered
                - record.qty_sold
                - record.qty_incoming
                - record.qty_received
            )

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
        "canvas_id.state",
    )
    def _compute_qty_incoming(self):
        for record in self:
            states = [
                "draft",
                "confirmed",
                "partially_available",
                "assigned",
            ]
            record.qty_incoming = record._get_move_qty(states, "in")

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
        "canvas_id.state",
    )
    def _compute_qty_received(self):
        for record in self:
            states = [
                "done",
            ]
            record.qty_received = record._get_move_qty(states, "in")

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
        "uom_quantity",
        "qty_delivered",
        "qty_outgoing",
        "qty_incoming",
        "qty_received",
        "qty_to_receive",
        "canvas_id.state",
    )
    def _compute_qty_to_deliver(self):
        for record in self:
            record.qty_to_deliver = (
                record.uom_quantity - record.qty_outgoing - record.qty_delivered
            )

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
        "canvas_id.state",
    )
    def _compute_qty_outgoing(self):
        for record in self:
            states = [
                "draft",
                "confirmed",
                "partially_available",
                "assigned",
            ]
            record.qty_outgoing = record._get_move_qty(states, "out")

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
        "canvas_id.state",
    )
    def _compute_qty_delivered(self):
        for record in self:
            states = [
                "done",
            ]
            record.qty_delivered = record._get_move_qty(states, "out")

    def _get_move_qty(self, states, direction):
        result = 0.0
        outbound_location = self.canvas_id.outbound_location_id
        inbound_location = self.canvas_id.inbound_location_id
        if direction == "in":
            for move in self.stock_move_ids.filtered(
                lambda m: m.state in states and m.location_dest_id == inbound_location
            ):
                result += move.product_qty
        else:
            for move in self.stock_move_ids.filtered(
                lambda m: m.state in states and m.location_id == outbound_location
            ):
                result += move.product_qty
        return result

    def _create_delivery(self):
        self.ensure_one()
        group = self.canvas_id.procurement_group_id
        qty = self.qty_to_deliver
        values = self._get_delivery_procurement_data()

        procurements = []
        try:
            procurement = group.Procurement(
                self.product_id,
                qty,
                self.uom_id,
                values.get("location_id"),
                values.get("origin"),
                values.get("origin"),
                self.env.company,
                values,
            )

            procurements.append(procurement)
            self.env["procurement.group"].with_context().run(procurements)
        except UserError as error:
            raise UserError(error)

    def _create_receipt(self):
        self.ensure_one()
        group = self.canvas_id.procurement_group_id
        qty = self.qty_to_receive
        values = self._get_receipt_procurement_data()

        procurements = []
        try:
            procurement = group.Procurement(
                self.product_id,
                qty,
                self.uom_id,
                values.get("location_id"),
                values.get("origin"),
                values.get("origin"),
                self.env.company,
                values,
            )

            procurements.append(procurement)
            self.env["procurement.group"].with_context().run(procurements)
        except UserError as error:
            raise UserError(error)

    def _get_delivery_procurement_data(self):
        group = self.canvas_id.procurement_group_id
        origin = self.canvas_id.name
        warehouse = self.canvas_id.outbound_warehouse_id
        location = self.canvas_id.salesperson_id.partner_id.canvas_location_id
        route = self.canvas_id.outbound_route_id
        result = {
            "name": origin,
            "group_id": group,
            "origin": origin,
            "warehouse_id": warehouse,
            "date_planned": fields.Datetime.now(),
            "product_id": self.product_id.id,
            "product_qty": self.qty_to_deliver,
            "partner_id": False,
            "product_uom": self.uom_id.id,
            "location_id": location,
            "route_ids": route,
            "sale_canvas_line_ids": [(4, self.id)],
        }
        return result

    def _get_receipt_procurement_data(self):
        group = self.canvas_id.procurement_group_id
        origin = self.canvas_id.name
        warehouse = self.canvas_id.inbound_warehouse_id
        location = self.canvas_id.inbound_location_id
        route = self.canvas_id.inbound_route_id
        result = {
            "name": origin,
            "group_id": group,
            "origin": origin,
            "warehouse_id": warehouse,
            "date_planned": fields.Datetime.now(),
            "product_id": self.product_id.id,
            "product_qty": self.qty_to_deliver,
            "partner_id": False,
            "product_uom": self.uom_id.id,
            "location_id": location,
            "route_ids": route,
            "sale_canvas_line_ids": [(4, self.id)],
        }
        return result

    def _create_realization_detail(self, partner):
        self.ensure_one()
        RealizationDetail = self.env["sale_canvas_realization_line"]
        RealizationDetail.create(self._prepare_realization_detail(partner))

    def _prepare_realization_detail(self, header):
        self.ensure_one()
        return {
            "canvas_id": self.canvas_id.id,
            "realization_header_id": header.id,
            "partner_id": header.partner_id.id,
            "product_id": self.product_id.id,
            "name": self.name,
            "uom_quantity": 0.0,
            "uom_id": self.uom_id.id,
            "line_id": self.id,
        }
