from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError 

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    estimated_production_time = fields.Float(
        string="Estimated Production Time (hours)",
        help="Estimated production time based on BOM and product."
    )

    @api.onchange('product_id', 'bom_id')
    def _compute_estimated_production_time(self):
        for record in self:
            record.estimated_production_time = record.bom_id.days_to_prepare_mo


    def action_plan_production(self):
        for order in self:
            if order.date_start and order.estimated_production_time:
                start_date = order.date_start
                end_date = start_date + timedelta(hours=order.estimated_production_time)
                order.write({
                    'date_finished': end_date,
                })
            else:
                raise UserError("Please specify the planned start date and estimated production time.")
