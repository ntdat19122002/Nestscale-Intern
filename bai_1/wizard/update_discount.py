from odoo import api,models,fields

class UpdateDiscountWizard(models.TransientModel):
    _name = "update.discount.wizard"

    vip_code = fields.Char(string= "Update vip code")
    # default_customer_ids = fields.One2many('res.partner','name')

    def action_update_discount(self):
        # print(self.default_customer_ids)
        for i in self.env.context['active_ids']:
            self.env['res.partner'].browse(i).customer_discount_code = self.vip_code