from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


class StockQuantInherit(models.Model):
    _inherit='stock.quant'

    is_approval = fields.Boolean("Is Approval", related="location_id.is_approval", store=True)
    is_done = fields.Boolean("Is Done", store=True)
    is_validate = fields.Boolean("Is Validate", compute="get_approval")
    accounting_date = fields.Date(string='accounting_date')

    @api.model
    def _get_inventory_fields_write(self):
        # Inherit method to add custom fields
        fields = super()._get_inventory_fields_write()
        return fields + ['is_approval', 'is_done','is_validate']

    @api.model_create_multi
    def create(self, vals_list):
        result = super(StockQuantInherit, self).create(vals_list)
        for rec in result:
            rec.is_done = False
        return result

    @api.model
    def write(self, vals):
        result = super(StockQuantInherit, self).write(vals)
        if 'is_done' not in vals and 'inventory_quantity' in vals:
            self.is_done = False
        return result


    @api.depends('location_id','inventory_quantity','product_id')
    def get_approval(self):
        for pic in self:
            location = pic.location_id
            user = self.env.user
            if location.is_approval and location.user_id.id == user.id and pic.is_done:
                pic.is_validate = True
            else:
                pic.is_validate = False


    def action_apply_inventory(self):
        for qu in self:
            if qu.is_approval and not qu.is_done:
                qu.is_done = True
            elif qu.is_approval and qu.is_done and qu.is_validate:
                qu.action_user_validate()
            elif not qu.is_approval:
                qu.action_user_validate()


    def action_user_validate(self):
        products_tracked_without_lot = []
        for quant in self:
            rounding = quant.product_uom_id.rounding
            if fields.Float.is_zero(quant.inventory_diff_quantity, precision_rounding=rounding)\
                    and fields.Float.is_zero(quant.inventory_quantity, precision_rounding=rounding)\
                    and fields.Float.is_zero(quant.quantity, precision_rounding=rounding):
                continue
            if quant.product_id.tracking in ['lot', 'serial'] and\
                    not quant.lot_id and quant.inventory_quantity != quant.quantity and not quant.quantity:
                products_tracked_without_lot.append(quant.product_id.id)
        # for some reason if multi-record, env.context doesn't pass to wizards...
        ctx = dict(self.env.context or {})
        ctx['default_quant_ids'] = self.ids
        quants_outdated = self.filtered(lambda quant: quant.is_outdated)
        if quants_outdated:
            ctx['default_quant_to_fix_ids'] = quants_outdated.ids
            return {
                'name': _('Conflict in Inventory Adjustment'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'views': [(False, 'form')],
                'res_model': 'stock.inventory.conflict',
                'target': 'new',
                'context': ctx,
            }
        if products_tracked_without_lot:
            ctx['default_product_ids'] = products_tracked_without_lot
            return {
                'name': _('Tracked Products in Inventory Adjustment'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'views': [(False, 'form')],
                'res_model': 'stock.track.confirmation',
                'target': 'new',
                'context': ctx,
            }
        self._apply_inventory()
        self.inventory_quantity_set = False


    def action_set_inventory_quantity(self):
        self.is_done = False
        return super(StockQuantInherit, self).action_set_inventory_quantity()

    def action_clear_inventory_quantity(self):
        self.is_done = False
        return super(StockQuantInherit, self).action_clear_inventory_quantity()





