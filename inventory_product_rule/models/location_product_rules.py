# models/models.py
from odoo import api, fields, models
from odoo.exceptions import UserError



class LocationProductRules(models.Model):
    _name = 'location.product.rules'
    _description = 'Location Product Rules'
    _rec_name = "rule_name"

    location_id = fields.Many2one('stock.location', string="Location", required=True)
    product_id = fields.Many2one('product.product', string="Allowed Product", required=True)
    rule_name = fields.Char(string="Rule Name", compute="_compute_rule_name", store=True)

    @api.depends('location_id', 'product_id')
    def _compute_rule_name(self):
        for rule in self:
            rule.rule_name = f"{rule.location_id.name} - {rule.product_id.name}"




class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.constrains('location_dest_id', 'product_id')
    def _check_location_product_rules(self):
        for move in self:
            rule = self.env['location.product.rules'].search([
                ('location_id', '=', move.location_dest_id.id),
                ('product_id', '=', move.product_id.id)
            ], limit=1)
            if not rule:
                raise UserError(
                    f"Product '{move.product_id.name}' is not allowed in destination location '{move.location_dest_id.name}'."
                )
