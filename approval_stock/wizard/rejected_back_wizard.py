from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ReasonStockWizard(models.TransientModel):
    _name = 'rejected.stock.wizard'
    _description ="Stock rejected"


    description = fields.Text("Description")





    def action_generate(self):
        if not self.description:
            raise ValidationError("The description cannot be empty !")
        docs = self.env['stock.picking'].browse(self.env.context.get('active_id'))
        docs.message_post(body="Reason Rejected : %s" %(self.description))
        docs._back_process()

