from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


class StockMoveInherit(models.Model):
    _inherit='stock.move'

    state = fields.Selection([
        ('draft', 'New'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='Status',
        copy=False, default='draft', index=True, readonly=True,
        help="* New: The stock move is created but not confirmed.\n"
             "* Waiting Another Move: A linked stock move should be done before this one.\n"
             "* Waiting Availability: The stock move is confirmed but the product can't be reserved.\n"
             "* Available: The product of the stock move is reserved.\n"
             "* Done: The product has been transferred and the transfer has been confirmed.")


class StockPickingInherit(models.Model):
    _inherit='stock.picking'


    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")


    is_approval = fields.Boolean("Is Approval", related="location_dest_id.is_approval", store=True, copy=False)
    is_validate = fields.Boolean("Is Validate", compute="get_approval")
    is_assigned = fields.Boolean("Is Assigned", default=False, copy=False)
    country_code = fields.Char(string='Country Code')

    @api.depends('state','location_dest_id','location_dest_id.is_approval','location_dest_id.user_id')
    def get_approval(self):
        for pic in self:
            location = pic.location_dest_id
            user = self.env.user
            if location.is_approval and location.user_id.id == user.id:
                pic.is_validate = True
            else:
                pic.is_validate = False

    @api.depends('move_type', 'move_ids.state', 'move_ids.picking_id')
    def _compute_state(self):
        for rec in self:
            if rec.is_approval and rec.state in ['draft','assigned'] and rec.is_assigned:
                self.state = 'approved'
            else:
                return super(StockPickingInherit, self)._compute_state()


    def action_back_process(self):
        return {
                'name' : _("Rejected With Comment"),
                'view_type' : 'form',
                'res_model' : 'rejected.stock.wizard',
                'view_mode' : 'form',
                'type':'ir.actions.act_window',
                'target': 'new',
            }


    def _back_process(self):
        if self.state == 'approved' and self.is_approval:
            self.state = 'assigned'
            self.is_assigned = False
            return True

    def button_validate(self):
        self.ensure_one()
        if self.is_approval and self.state in ['draft','assigned'] and not self.is_assigned:
            self.state = 'approved'
            self.is_assigned = True
        else:
            return super(StockPickingInherit, self).button_validate()


