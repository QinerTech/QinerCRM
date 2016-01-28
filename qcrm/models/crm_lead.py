# -*- coding: utf-8 -*-
from openerp import models, fields, api
import time, datetime


class crm_lead(models.Model):
    _inherit = "crm.lead"

    school_ids = fields.Many2one(
        string='School',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='qcrm.school',
        domain=[],
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

    target_country = fields.Many2many(
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

    venue = fields.Char(
        string='Venue',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help=False,
        size=50,
        states={'done': [('readonly', True)], 'confirm': [('readonly', True) ]}
    )

    opportunity_code = fields.Char(
        string='Opportunity ID',
        required=False,
        readonly=True,
        index=False,
        size=20,
    )

    _defaults = {
        'show_menu': True,
        'show_tracks': True,
        'show_track_proposal': False,
        'date_tz': 'Asia/Shanghai',
    }


class qrcm_school(models.Model):
    _name = "qcrm.school"
    _description = 'School List'

    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help=False,
        size=50,
        translate=True
    )

