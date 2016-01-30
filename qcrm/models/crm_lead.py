# -*- coding: utf-8 -*-
from openerp import models, fields, api
import time, datetime


class crm_lead(models.Model):
    _inherit = "crm.lead"

    partner_id = fields.Many2one(
        domain = [('is_company','=',0),('customer','=',1)]
    )

    school_id = fields.Many2one(
        string='School',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='res.partner',
        domain=[('is_company','=',1),('customer','=',1)],
        context={},
        limit=None
    )

    major = fields.Char(
        string='Major',
        required=True,
        readonly=False,
        index=True,
        help=False,
        size=50

    )

    target_major = fields.Char(
        string='TargetMajor',
        required=True,
        readonly=False,
        index=True,
        help=False,
        size=50
    )

    qq = fields.Integer(
        string='QQ',
        required=False,
        readonly=False,
        index=False,
        help=False,
        size=50
    )

    year = fields.Selection(
        string='Year',
        required=False,
        readonly=False,
        index=False,
        help=False,
        selection=[('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016')]
    )

    target_country_ids = fields.Many2many(
        string='Target Country',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='res.country',
        relation='crm_lead_res_country_rel',
        domain=[],
        context={},
        limit=None
    )

    opportunity_code = fields.Char(
        string='Opportunity ID',
        required=False,
        readonly=True,
        index=False,
        size=20,
    )

    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            contact_id = self.partner_id.address_get().get('contact', False)
            if contact_id:
                contact = self.env['res.partner'].browse(contact_id)
                self.name = contact.name
                self.email = contact.email
                self.phone = contact.phone

    @api.model
    def create(self, values):
        if values.get('name', 'New') == 'New':
            values['name'] = values.get('partner_id', 'Other')

        return super(crm_lead, self).create(values)