from odoo import api,models,fields

class Warranty(models.Model):
    _inherit = 'product.template'

    date_to = fields.Datetime()
    date_from = fields.Datetime()
    product_warranty = fields.Text(string="Product Warranty", compute="_compute_code", store=True)



    @api.depends('date_to','date_from')
    def _compute_code(self):
        for rec in self:
            datefrom = self.makefull(str(rec.date_from.day))+self.makefull(str(rec.date_from.month))+str(rec.date_from.year)[2:]
            dateto = self.makefull(str(rec.date_to.day))+self.makefull(str(rec.date_to.month))+str(rec.date_to.year)[2:]

            rec.product_warranty ='PWR'+'/'+datefrom+'/'+dateto

    def makefull(self,a):
        if len(a) == 1:
            a="0"+a
        return a

