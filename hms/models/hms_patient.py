from odoo import models, fields, api

import time
from datetime import date,datetime
from dateutil.relativedelta import relativedelta

import re

from odoo.exceptions import ValidationError


class hms_patient(models.Model):
    _name = "hms.patient"
    _rec_name = 'fname'


    fname=fields.Char()
    lname=fields.Char()
    birth_date=fields.Date()
    history=fields.Html()
    CR_ratio=fields.Float()
    blood_type=fields.Selection([('A+','A+'),
                                 ('A-','A-'),
                                 ('B+', 'B+'),
                                 ('B-', 'B-'),
                                 ('AB+','AB+'),
                                 ('AB-','AB-'),
                                 ('O+','O+'),
                                 ('O-', 'O-')
                                 ],
                                default="A+")
    PCR=fields.Boolean()
    image=fields.Binary("Image")
    address=fields.Text()
    Age=fields.Integer(compute="compute_age", store=True)
    department_id=fields.Many2one(comodel_name='hms.department')
    department_capacity=fields.Integer(related='department_id.capacity')
    status=fields.Selection([
        ("undetermined",'undetermined'),
        ("good","good"),
        ("fair","fair"),
        ("serious","serious")
    ],default="undetermined")
    doctors=fields.Many2many(comodel_name="hms.doctors")
    logs=fields.One2many(comodel_name="hms.logs",inverse_name="patient_id")
    email=fields.Char()

    def change_status(self):
        if self.status=="undetermined":
            self.status="good"
        elif self.status=="good":
            self.status="fair"
        elif self.status=="fair":
            self.status="serious"
        elif self.status=="serious":
            self.status="undetermined"
        self.logs.create({
           "patient_id": self.id,
           "description": self.fname + "'s status has changed to " + self.status,
        })

    @api.onchange('Age')
    def onchange_age(self):
        if self.Age<30:
            PCR_domain=[('checked','=',True)]
        else:
            PCR_domain=[]
        return {
                'domain':{'history':PCR_domain},
                'warning':{
                    'title':'age change',
                    'message':'PCR has been checked!'
                }
            }

    @api.depends("birth_date")
    def compute_age(self):
        for rec in self:
            if rec.birth_date:
                dt=str(rec.birth_date)
                dob = datetime.strptime(dt, "%Y-%m-%d").date()
                today = date.today()
                relative_data = relativedelta(today, dob)
                rec.Age = int(relative_data.years)


    @api.constrains("email")
    def check_email(self):
        for rec in self:
            if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", rec.email):
                raise ValidationError("Invalid Email!")


    _sql_constraints = [
        ("valid email",'UNIQUE(email)',"the email you inserted already exists")
    ]