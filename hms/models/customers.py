from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Customers(models.Model):
    _inherit = "res.partner"

    related_patient_id=fields.Many2one("hms.patient")

    @api.constrains("email")
    def check_email(self):
        for rec in self:
            if rec.email:
                patient_emails=self.env['hms.patient'].search([('email', '=',rec.email)])
                if patient_emails:
                    raise ValidationError("there is a patient with this email!")

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("you can't delete this user there's a related patient to him!")
        return super().unlink()