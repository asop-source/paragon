from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


class StockLocationInherit(models.Model):
    _inherit='stock.location'

    is_approval = fields.Boolean("Is Approval")
    user_id = fields.Many2one("res.users","User Approval")

    @api.onchange("is_approval")
    def clear_approv(self):
        if not self.is_approval:
            self.user_id = False
