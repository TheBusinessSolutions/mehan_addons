# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from datetime import timedelta, date, datetime
from odoo.exceptions import ValidationError, UserError


class DeceasedInfo(models.Model):
    _name = 'deceased.info'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'deceased.info'
    _order = 'create_date DESC'

    name = fields.Char('Name', tracking=True)
    public_serial = fields.Char('Serial', tracking=True)
    cert_management_serial = fields.Char('Cert Management Serial', tracking=True)
    cert_management_image = fields.Binary('Cert Management Image', attachment=True)
    job_id = fields.Many2one('mehan.job', string="Job")
    work_place_id = fields.Many2one('work.place', string="Main Work Place", domain="[('tag_id', '=', tag_id)]")
    sub_work_place_id = fields.Many2one('work.place.lines', string="Sub Work Place",
                                        domain="[('place_id', '=', work_place_id)]")
    tag_id = fields.Many2one('work.place.tag', string="Work Place Tag", tracking=True)
    committee_id = fields.Many2one('mehan.committee', string="Committee", tracking=True)
    expense_type_id = fields.Many2one('mehan.expense', string="Expense Type", tracking=True)
    pension_payment = fields.Binary()
    no_55 = fields.Char('No.55')
    no_224 = fields.Char('No.224')
    date_55 = fields.Date('Date.55')
    date_224 = fields.Date('Date.224')
    national_id = fields.Char('National ID', size=14)
    birth_date = fields.Date('Date Of Birth', compute='_get_birth_date', store=True)
    death_date = fields.Date('Date Of Death')
    age = fields.Integer(compute='_get_age', store=True)
    age_months = fields.Integer(compute='_get_age', store=True)
    age_days = fields.Integer(compute='_get_age', store=True)
    beneficiaries_no = fields.Integer('Beneficiaries Number', compute='_get_num', store=True, tracking=True)
    death_Beneficiaries_ids = fields.One2many('death.beneficiaries.lines', 'dead_id', String='Beneficiaries Lines',
                                              tracking=True)

    member_type = fields.Selection([
        ('injured', 'Injured'),
        ('dead', 'Dead')
    ], default='injured', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review55', 'Review 55 Done'),
        ('review244', 'Review 244 Done'),
        ('certified', 'Certified')
    ], string='Status', tracking=True)

    fundamental_supporter = fields.Selection([
        ('administrative', 'Administrative certificate')]
        , string='Fundamental Supporter', default='administrative', tracking=True)
    fundamental_supporter_2 = fields.Selection([
        ('injury', 'Injury death certificate'),
        ('stress', 'Stress death certificate')
    ], string='Fundamental Supporter', tracking=True)
    fundamental_supporter_attach = fields.Binary()
    fund_subscription_payment = fields.Binary()
    fundamental_supporter_location = fields.Char()
    is_administrative = fields.Boolean(compute='_get_fundamental_supporter', store=True, tracking=True)
    compensation_amount = fields.Many2one('compensation.amount', string="Compensation Amount", tracking=True)
    compensation_percentage = fields.Float(string="Compensation Percentage", digits=(12, 3),
                                           compute='_get_compensation_percentage', store=True)
    is_new_member = fields.Boolean()
    injury_class_id = fields.Many2one('injuries.classification', tracking=True)
    injury_category = fields.Char(string='Category', related='injury_class_id.injury_category')
    injury_place = fields.Char(string='Injury Place')
    payment_amount = fields.Float(string="Payment Amount", tracking=True)
    registration_date = fields.Date()

    phone = fields.Char()
    bank_id = fields.Many2one('mehan.bank', string='Bank', tracking=True)
    branch_id = fields.Many2one('mehan.bank.branch', string='Branch', domain="[('bank_id', '=', bank_id)]",
                                tracking=True)
    accounting_no = fields.Char('Accounting No.', size=22, tracking=True)
    iban_no = fields.Char('IBAN No.', size=29, default='EG', tracking=True)
    national_id_attachment = fields.Binary()

    @api.model
    def create(self, vals):
        vals['state'] = 'draft'
        vals['public_serial'] = self.env['ir.sequence'].next_by_code('serial.mehan.sequence')
        result = super(DeceasedInfo, self).create(vals)
        serial = 0
        for line in result.death_Beneficiaries_ids:
            serial += 1
            line.serial = serial
        return result

    def write(self, values):
        res = super(DeceasedInfo, self).write(values)
        serial = 0
        for line in self.death_Beneficiaries_ids:
            serial += 1
            line.serial = serial
        return res

    def action_new_member(self):
        self.write({"is_new_member": True})

    def action_review55(self):
        if not self.no_55:
            raise ValidationError(_("Add No. 55"))
        elif not self.date_55:
            raise ValidationError(_("Add Date 55"))
        else:
            self.write({"state": "review55"})

    def action_review244(self):
        if not self.no_224:
            raise ValidationError(_("Add No. 224"))
        elif not self.date_224:
            raise ValidationError(_("Add Date 224"))
        else:
            self.write({"state": "review244"})

    def action_certify(self):
        self.write({"state": "certified"})

    def action_set_draft(self):
        self.write({"state": "draft"})

    @api.depends('national_id')
    def _get_birth_date(self):
        for rec in self:
            rec.birth_date = False
            if rec.national_id:
                if len(rec.national_id) < 14:
                    raise ValidationError(_("Invalid National ID"))
                else:
                    id_num = rec.national_id
                    if len(id_num) == 14:
                        if id_num[0] == '2' and id_num[3:5] <= '12' and id_num[5:7] <= '31':
                            db = '19' + id_num[1:7]
                            rec.birth_date = datetime.strptime(db, '%Y%m%d').date()
                        elif id_num[0] == '3' and id_num[3:5] <= '12' and id_num[5:7] <= '31':
                            db = '20' + id_num[1:7]
                            rec.birth_date = datetime.strptime(db, '%Y%m%d').date()

                    else:
                        rec.birth_date = False

    @api.depends('death_Beneficiaries_ids')
    def _get_num(self):
        for rec in self:
            rec.beneficiaries_no = len(rec.death_Beneficiaries_ids)

    def get_days_in_month(self, month, year):
        # Returns the number of days in a given month and year
        if month == 2:  # February
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                return 29  # Leap year
            else:
                return 28
        elif month in [4, 6, 9, 11]:  # April, June, September, November
            return 30
        else:
            return 31

    @api.depends('birth_date', 'death_date', 'registration_date')
    def _get_age(self):
        for rec in self:
            if rec.death_date and rec.birth_date and rec.member_type == 'dead':
                years = rec.death_date.year - rec.birth_date.year
                months = rec.death_date.month - rec.birth_date.month
                days = rec.death_date.day - rec.birth_date.day
                if days < 0:
                    months -= 1
                    days += self.get_days_in_month(rec.birth_date.month, rec.birth_date.year)
                if months < 0:
                    years -= 1
                    months += 12
                rec.age = years
                rec.age_months = months
                rec.age_days = days
            elif rec.birth_date and rec.member_type == 'injured' and rec.registration_date:
                current_date = rec.registration_date
                years = current_date.year - rec.birth_date.year
                months = current_date.month - rec.birth_date.month
                days = current_date.day - rec.birth_date.day
                if days < 0:
                    months -= 1
                    days += rec.get_days_in_month(rec.birth_date.month, rec.birth_date.year)
                if months < 0:
                    years -= 1
                    months += 12
                rec.age = years
                rec.age_months = months
                rec.age_days = days
            else:
                rec.age = 0
                rec.age_months = 0
                rec.age_days = 0

    @api.onchange('member_type')
    def _get_beneficiaries(self):
        for rec in self:
            rec.death_Beneficiaries_ids = False
            rec.injury_class_id = False
            rec.death_date = False

    @api.depends('death_date')
    def _get_fundamental_supporter(self):
        for rec in self:
            rec.is_administrative = False
            if str(rec.death_date) < '2020-02-13':
                raise ValidationError(_("Invalid Date"))

            if str(rec.death_date) <= '2021-09-27' and str(rec.death_date) >= '2020-02-13':
                rec.is_administrative = True

    @api.depends('death_Beneficiaries_ids')
    def _get_compensation_percentage(self):
        for rec in self:
            compensation_percentage = 0.0
            for line in rec.death_Beneficiaries_ids:
                compensation_percentage += line.payment_percentage
            rec.compensation_percentage = compensation_percentage
            if rec.compensation_percentage > 100:
                raise ValidationError(_("Compensation percentage cannot be over 100%. "))

            for record in rec.death_Beneficiaries_ids:
                if len(rec.death_Beneficiaries_ids) < 3:
                    if rec.compensation_percentage != 0.0:
                        percentage = record.payment_percentage / rec.compensation_percentage
                        record.payment_amount = percentage * rec.compensation_amount.name
                        record.compensation_percentage = percentage * 100
                else:
                    if rec.compensation_percentage != 0.0:
                        record.payment_amount = record.payment_percentage * rec.compensation_amount.name / 100
                        record.compensation_percentage = record.payment_percentage

    # @api.onchange('member_type')
    # def _get_last_amount(self):
    #     amount = self.env['compensation.amount'].search([])
    #     if amount:
    #         date = max(dt.date for dt in amount)
    #         self.compensation_amount = amount.filtered(lambda l: l.date == date)
    #     expenses = self.env['mehan.expense'].search([('member_type', '=', self.member_type)]).ids
    #     domain = [('id', 'in', expenses)]
    #     return {'domain': {'expense_type_id': domain}}

    @api.onchange('member_type', 'death_date', 'registration_date')
    def _get_last_amount(self):
        """
        Onchange method for UI updates - calculates compensation based on date
        """
        # Determine which date to use based on member type
        reference_date = None
        if self.member_type == 'dead' and self.death_date:
            reference_date = self.death_date
        elif self.member_type == 'injured' and self.registration_date:
            reference_date = self.registration_date
        
        if reference_date:
            # Search for compensation amounts where date <= reference_date
            # Order by date descending to get the most recent applicable amount
            applicable_amount = self.env['compensation.amount'].search(
                [('date', '<=', reference_date)],
                order='date desc',
                limit=1
            )
            
            if applicable_amount:
                self.compensation_amount = applicable_amount
            else:
                self.compensation_amount = False
        else:
            self.compensation_amount = False
        
        # Keep the existing expense type domain logic
        expenses = self.env['mehan.expense'].search([('member_type', '=', self.member_type)]).ids
        domain = [('id', 'in', expenses)]
        return {'domain': {'expense_type_id': domain}}
    @api.onchange('injury_class_id')
    def _get_injury_payment(self):
        for rec in self:
            rec.payment_amount = rec.injury_class_id.percentage * rec.compensation_amount.name / 100

    @api.constrains('national_id')
    def _check_unique_national_id(self):
        for rec in self:
            exist_national_id = self.env['deceased.info'].search(
                [('national_id', '=', rec.national_id), ('id', '!=', rec.id)])
            if exist_national_id:
                raise ValidationError(_('National ID must be unique.'))


class DeathBeneficiariesLines(models.Model):
    _name = 'death.beneficiaries.lines'
    _description = 'death.beneficiaries.lines'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    dead_id = fields.Many2one('deceased.info')
    order_id = fields.Many2one('mehan.order.payment')
    name = fields.Char()
    serial = fields.Integer('Serial')
    relationship_degree_id = fields.Many2one('relationship.degree', string="Relation degree")
    age_phase = fields.Selection([
        ('adult', 'Adult'),
        ('underage', 'Underage')
    ], string='Age Phase', compute='_get_age_phase', store=True)
    birth_date = fields.Date('Date Of Birth', compute='_get_birth_date', store=True)
    age_years = fields.Integer(compute='_get_age', store=True)
    age_months = fields.Integer(compute='_get_age', store=True)
    age_days = fields.Integer(compute='_get_age', store=True)
    bank_id = fields.Many2one('mehan.bank', string='Bank')
    branch_id = fields.Many2one('mehan.bank.branch', string='Branch', domain="[('bank_id', '=', bank_id)]")
    accounting_no = fields.Char('Accounting No.', size=22)
    iban_no = fields.Char('IBAN No.', size=29, default='EG')
    national_id = fields.Char('National ID', size=14)
    payment_amount = fields.Float(string="Payment Amount", digits=(12, 2))
    payment_percentage = fields.Float(digits=(12, 5))
    compensation_percentage = fields.Float(string="Compensation Percentage", digits=(12, 2))
    expected_payment_amount = fields.Float(string="Expected Payment Amount", compute='_get_expected_payment_amount',
                                           store=True)
    bank_letter = fields.Binary()
    is_bank_letter = fields.Boolean('Bank Letter')
    prosecution_letter = fields.Binary()
    is_prosecution_letter = fields.Boolean('Prosecution Letter')
    birth_certificate = fields.Binary()
    is_birth_certificate = fields.Boolean('Birth Certificate')
    state = fields.Selection([
        ('new', 'New'),
        ('done', 'Done'),
        ('return', 'Return'),
    ], string='Status', default='new')
    phone = fields.Char()
    tax_position = fields.Selection([
        ('fulfilled', 'Fulfilled'),
        ('notfulfilled', 'Not fulfilled'),
    ], string='Tax Position', default='notfulfilled', tracking=True)
    tax_certificate = fields.Binary()
    gb_Beneficiaries_ids = fields.One2many('gb.beneficiaries.lines', 'gb_id', String='GB Beneficiaries Lines')
    tax_amount = fields.Float(tracking=True)
    errand_id = fields.Many2one('tax.errand', tracking=True)
    tax_letter = fields.Binary(tracking=True)
    required_acc_number = fields.Boolean(related='bank_id.required_acc_number')
    national_id_attachment = fields.Binary()
    registration_date = fields.Date(tracking=True)
    no_55 = fields.Char('No.55', tracking=True)
    no_224 = fields.Char('No.224', tracking=True)
    date_55 = fields.Date('Date.55', tracking=True)
    date_224 = fields.Date('Date.224', tracking=True)
    exchange_note = fields.Binary(string='Exchange Note', tracking=True)
    no_gp = fields.Char('GP ', tracking=True, size=14)
    date_gp = fields.Date('GP Date', tracking=True)
    is_return = fields.Boolean('Return order')

    def print_Beneficiary_report(self):
        self.is_return = False
        return self.env.ref('n2d_mehan.death_beneficiaries_lines_report').report_action(self)

    @api.depends('national_id')
    def _get_birth_date(self):
        for rec in self:
            rec.birth_date = False
            if rec.national_id:
                if len(rec.national_id) < 14:
                    raise ValidationError(_("Invalid National ID"))
                else:
                    id_num = rec.national_id
                    if len(id_num) == 14:
                        if id_num[0] == '2' and id_num[3:5] <= '12' and id_num[5:7] <= '31':
                            db = '19' + id_num[1:7]
                            rec.birth_date = datetime.strptime(db, '%Y%m%d').date()
                        elif id_num[0] == '3' and id_num[3:5] <= '12' and id_num[5:7] <= '31':
                            db = '20' + id_num[1:7]
                            rec.birth_date = datetime.strptime(db, '%Y%m%d').date()

                    else:
                        rec.birth_date = False

    def get_days_in_month(self, month, year):
        # Returns the number of days in a given month and year
        if month == 2:  # February
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                return 29  # Leap year
            else:
                return 28
        elif month in [4, 6, 9, 11]:  # April, June, September, November
            return 30
        else:
            return 31

    @api.depends('birth_date', 'registration_date')
    def _get_age(self):
        fmt = '%Y-%m-%d'
        for line in self:
            if line.birth_date and line.registration_date:
                years = line.registration_date.year - line.birth_date.year
                months = line.registration_date.month - line.birth_date.month
                days = line.registration_date.day - line.birth_date.day
                if days < 0:
                    months -= 1
                    days += self.get_days_in_month(line.birth_date.month, line.birth_date.year)
                if months < 0:
                    years -= 1
                    months += 12
                line.age_years = years
                line.age_months = months
                line.age_days = days
            else:
                line.age_years = 0
                line.age_months = 0
                line.age_days = 0

    @api.depends('age_years')
    def _get_age_phase(self):
        for rec in self:
            rec.age_phase = False
            if rec.age_years < 21:
                rec.age_phase = 'underage'
            else:
                rec.age_phase = 'adult'

    @api.depends('payment_percentage')
    def _get_expected_payment_amount(self):
        self.expected_payment_amount = 0.0
        for rec in self:
            rec.expected_payment_amount = rec.payment_percentage * rec.dead_id.compensation_amount.name / 100

    def action_done(self):
        if self.tax_position != 'fulfilled':
            raise ValidationError(_("Tax position not fulfilled"))
        else:
            self.write({"state": 'done'})

    def action_return(self):
        self.write({"state": 'return'})

    @api.constrains('national_id')
    def _check_unique_national_id(self):
        for rec in self:
            exist_national_id = self.env['deceased.info'].search(
                [('national_id', '=', rec.national_id), ('id', '!=', rec.id)])
            if exist_national_id:
                raise ValidationError(_('National ID must be unique.'))


class MehanJob(models.Model):
    _name = 'mehan.job'
    _description = 'mehan.job'
    _order = 'create_date DESC'

    name = fields.Char('Job Name')


class MehanWorkPlace(models.Model):
    _name = 'work.place'
    _description = 'work.place'
    _order = 'create_date DESC'

    name = fields.Char('Work Place')
    tag_id = fields.Many2one('work.place.tag', string='Tag')
    work_places_ids = fields.One2many('work.place.lines', 'place_id', String='Work Places')


class WorkPlaceLines(models.Model):
    _name = 'work.place.lines'

    place_id = fields.Many2one('work.place')
    name = fields.Char('Name')
    code = fields.Char('Code')


class MehanExpense(models.Model):
    _name = 'mehan.expense'
    _description = 'mehan.expense'
    _order = 'create_date DESC'

    name = fields.Char('Expense Type')
    member_type = fields.Selection([
        ('injured', 'Injured'),
        ('dead', 'Dead')])


class MehanCommittee(models.Model):
    _name = 'mehan.committee'
    _description = 'mehan.committee'
    _order = 'create_date DESC'

    name = fields.Char('Committee Name')


class RegistrationStage(models.Model):
    _name = 'registration.stage'
    _description = 'registration.stage'
    _order = 'create_date DESC'

    name = fields.Char('Registration stage')


class RelationshipDegree(models.Model):
    _name = 'relationship.degree'
    _description = 'relationship.degree'
    _order = 'create_date DESC'

    name = fields.Char('Relationship degree')


class MehanBank(models.Model):
    _name = 'mehan.bank'
    _description = 'mehan.bank'
    _order = 'create_date DESC'

    name = fields.Char('Bank name')
    required_acc_number = fields.Boolean(default=True)


class MehanBankBranch(models.Model):
    _name = 'mehan.bank.branch'
    _description = 'mehan.bank.branch'
    _order = 'create_date DESC'

    name = fields.Char('Branch name')
    bank_id = fields.Many2one('mehan.bank', string='Bank')


class MehanYearFinance(models.Model):
    _name = 'mehan.year.finance'
    _description = 'mehan.year.finance'
    _order = 'create_date DESC'

    name = fields.Char('Year finance')


class MehanWorkPlaceTag(models.Model):
    _name = 'work.place.tag'
    _description = 'work.place.tag'
    _order = 'create_date DESC'

    name = fields.Char('Tag')


class CompensationAmount(models.Model):
    _name = 'compensation.amount'
    _description = 'compensation.amount'
    _order = 'create_date DESC'

    name = fields.Float('Compensation Amount')
    date = fields.Date()
    description = fields.Char()

    _sql_constraints = [('date_uniqe', 'unique (date)',
                         "Date already exists.!")]


class InjuriesClassification(models.Model):
    _name = 'injuries.classification'
    _order = 'create_date DESC'

    name = fields.Char('Section')
    percentage = fields.Float(string='Percentage %')
    injury_category = fields.Char(string='Category')


class GbBeneficiariesLines(models.Model):
    _name = 'gb.beneficiaries.lines'
    _description = 'gb.beneficiaries.lines'

    gb_id = fields.Many2one('death.beneficiaries.lines')
    name = fields.Char(size=14)
    description = fields.Char()
    date = fields.Date()
    bank_id = fields.Many2one('mehan.bank', string='Bank')
    branch_id = fields.Many2one('mehan.bank.branch', string='Branch', domain="[('bank_id', '=', bank_id)]",)
    account_no = fields.Char(string='Account Number', size=22)
    no_55 = fields.Char('No.55', tracking=True)
    no_224 = fields.Char('No.224', tracking=True)
    date_55 = fields.Date('Date.55', tracking=True)
    date_224 = fields.Date('Date.224', tracking=True)
    settlement_number = fields.Char('Settlement Number', tracking=True)
    settlement_date = fields.Date('Settlement Date', tracking=True)
    gp_file = fields.Binary('GP File')

    @api.constrains('name')
    def _check_unique_gpname(self):
        for rec in self:
            if rec.name and self.search_count([('name', '=', rec.name), ('id', '!=', rec.id)]):
                raise ValidationError("GP must be unique!")

    @api.constrains('bank_id', 'branch_id', 'account_no', 'settlement_number', 'settlement_date')
    def _check_required_fields(self):
        for rec in self:
            if not rec.bank_id:
                raise ValidationError(_("Bank Required."))
            elif not rec.branch_id:
                raise ValidationError(_("Bank Branch Required."))
            elif not rec.account_no:
                raise ValidationError(_("Account Number Required."))
            elif not rec.settlement_number:
                raise ValidationError(_("Settlement Number Required."))
            elif not rec.settlement_date:
                raise ValidationError(_("Settlement Date Required."))

    def unlink(self):
        for line in self:
            raise ValidationError(_("Can not delete GP"))
        return super(GbBeneficiariesLines, self).unlink()


class TaxErrand(models.Model):
    _name = 'tax.errand'
    _order = 'create_date DESC'

    name = fields.Char()
