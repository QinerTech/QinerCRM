# -*- coding: utf-8 -*-
from openerp import models, fields, api
import time, datetime


class crm_lead(models.Model):
    _inherit = "crm.lead"

    partner_id = fields.Many2one(
        string='School',
        required=True,
        domain=[('is_company', '=', 0), ('customer', '=', 1)]
    )


    major_id = fields.Many2one(
        string='Major',
        required=True,
        readonly=False,
        index=True,
        help=False,
        comodel_name='qcrm.major',
        ondelete='set null',
        size=50

    )

    target_major_id = fields.Many2one(
        string='Target Major',
        required=True,
        readonly=False,
        index=True,
        help=False,
        comodel_name='qcrm.major',
        ondelete='set null',
        size=50
    )

    phone = fields.Char(
        required=True,
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
        selection=[('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'),
                   ('2016', '2016')]
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

    '''客户编号
    opportunity_code = fields.Char(
        string='Opportunity ID',
        required=False,
        readonly=True,
        index=False,
        size=20,
    )'''

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
            values['name'] = self.env['res.partner'].browse(values.get('partner_id')).name

        return super(crm_lead, self).create(values)

    def log_next_activity_done(self, cr, uid, ids, context=None, next_activity_name=False):

        to_clear_ids = []
        for lead in self.browse(cr, uid, ids, context=context):
            if not lead.next_activity_id:
                continue
            body_html = """<div><b>${object.next_activity_id.name}</b></div>
%if object.title_action:
<div>${object.title_action}</div>
%endif"""

            body_html = self.pool['mail.template'].render_template(cr, uid, body_html, 'crm.lead', lead.id,
                                                                   context=context)
            print(body_html)
            to_clear_ids.append(lead.id)
            self.write(cr, uid, [lead.id], {'last_activity_id': lead.next_activity_id.id}, context=context)

        if to_clear_ids:
            self.cancel_next_activity(cr, uid, to_clear_ids, context=context)

        print(to_clear_ids)
        return True


class qcrm_major(models.Model):
    _name = "qcrm.major"

    name = fields.Char(
        string='Major Name',
        required=False,
        readonly=False,
        index=False,
        default=None,
        size=50,
    )
