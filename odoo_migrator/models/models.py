# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .odoo_api import OdooApi
from odoo.exceptions import ValidationError


class MigrateModels(models.Model):
    _name = 'migarator.models'
    src_model = fields.Char(string='Src Model', required=True)
    dest_model = fields.Char(string='Dest Model', required=True)
    is_write = fields.Boolean(string='Write')
    src_res_id = fields.Integer(string='Src Res Id')
    dest_res_id = fields.Integer(string='Dest Res Id')
    finsihed = fields.Boolean(string='Finished')
    state = fields.Selection(string='Status',
                             selection=[('draft', 'Draft'),
                                        ('done', 'Done'), ],
                             default='draft', )
    fields_not_in = fields.Char(
        string='Fields Not In',
        required=False)

    line_ids = fields.One2many(
        comodel_name='migarator.models.lines',
        inverse_name='migarator_id',
        string='Line_ids',
        required=False)

    length = fields.Integer(
        string='Length',
        required=False)
    domain = fields.Char(
        string='Domain',
        required=False,default="[]")

    def get_api(self):
        with_user = self.env['ir.config_parameter'].sudo()
        migarator_host_name = with_user.get_param('odoo_migrator.migarator_host_name')
        migarator_database = with_user.get_param('odoo_migrator.migarator_database')
        migarator_user_name = with_user.get_param('odoo_migrator.migarator_user_name')
        migarator_password = with_user.get_param('odoo_migrator.migarator_password')
        api = OdooApi(migarator_host_name, migarator_database, migarator_user_name, migarator_password)
        return api

    def get_data_from_api(self):
        if self.length:
            for loop in range(1,self.length+1,10):
                api = self.get_api()
                if self.is_write:
                    data = api.search2(self.src_model, [[['id', '=', self.src_res_id]]], self.line_ids.mapped('src_field'))
                else:
                    # data = api.search2(self.src_model, [[['active','in',[False,True]]]], self.line_ids.mapped('src_field'))
                    # data = api.search2(self.src_model, [[['active','in',[False]]]], self.line_ids.mapped('src_field'))
                    # data = api.search2(self.src_model, [[['alias_name','=',False]]], self.line_ids.mapped('src_field'))
                    # data = api.search2(self.src_model, [[['journal_id', 'not in', [24, 25]]]],
                    #                    self.line_ids.mapped('src_field'))
                    if self.domain:
                        data = api.search6(self.src_model,eval(self.domain) , self.line_ids.mapped('src_field'),limit=10,offset=loop)
                    else:
                        data = api.search6(self.src_model,[[]] , self.line_ids.mapped('src_field'),limit=10,offset=loop)
                if data:
                    print("loop", self.src_model,loop, data[0]['id'])
                    recods = []
                    for datas in data:
                        # if datas.get('invocie_ids'):
                        if 1 == 1:
                            val = {}
                            for line in self.line_ids:
                                if datas.get(line.src_field):
                                    if line.is_many_2_one:
                                        val.update(
                                            {
                                                line.dest_field: datas.get(line.src_field)[0]
                                            }
                                        )
                                    elif line.is_many_2_many:
                                        val.update(
                                            {
                                                line.dest_field: [(6, 0, [x for x in datas.get(line.src_field)])]
                                            }
                                        )
                                    elif line.is_selection:
                                        val.update(
                                            {
                                                line.dest_field: str(datas[line.src_field])
                                            }
                                        )
                                    else:
                                        val.update(
                                            {
                                                line.dest_field: datas[line.src_field]
                                            }
                                        )

                            recods.append(val)
                for recod in recods:
                    self.create_record(recod)
            self.state = 'done'
        else:
            api = self.get_api()
            if self.is_write:
                data = api.search2(self.src_model, [[['id', '=', self.src_res_id]]], self.line_ids.mapped('src_field'))
            else:
                # data = api.search2(self.src_model, [[['active','in',[False,True]]]], self.line_ids.mapped('src_field'))
                # data = api.search2(self.src_model, [[['active','in',[False]]]], self.line_ids.mapped('src_field'))
                # data = api.search2(self.src_model, [[['alias_name','=',False]]], self.line_ids.mapped('src_field'))
                # data = api.search2(self.src_model, [[['journal_id', 'not in', [1, 2]]]],
                #                    self.line_ids.mapped('src_field'))
                # data = api.search6(self.src_model, [[['discount','>',0]]], self.line_ids.mapped('src_field'))
                data = api.search6(self.src_model, [[]], self.line_ids.mapped('src_field'))
            if data:
                recods = []
                for datas in data:
                    # if datas.get('invocie_ids'):
                    if 1 == 1:
                        val = {}
                        for line in self.line_ids:
                            if datas.get(line.src_field):
                                if line.is_many_2_one:
                                    val.update(
                                        {
                                            line.dest_field: datas.get(line.src_field)[0]
                                        }
                                    )
                                elif line.is_many_2_many:
                                    val.update(
                                        {
                                            line.dest_field: [(6, 0, [x for x in datas.get(line.src_field)])]
                                        }
                                    )
                                elif line.is_selection:
                                    val.update(
                                        {
                                            line.dest_field: str(datas[line.src_field])
                                        }
                                    )
                                else:
                                    val.update(
                                        {
                                            line.dest_field: datas[line.src_field]
                                        }
                                    )

                        recods.append(val)
            for recod in recods:
                self.create_record(recod)
            self.state = 'done'

    def check_fields_many2one(self):
        api = self.get_api()
        data = api.search6(self.src_model, [[]], [],limit=20)
        print(">SS>", data)
        fields = []
        lines = []
        lines.append((0, 0, {
            'src_field': 'id',
            'dest_field': 'id',
            'is_many_2_one': False,
            'is_many_2_many': False,
            'is_selection': False,
        }))
        for datas in data:
            for key in datas.keys():
                if key not in fields:
                    fields.append(key)
            print(">", fields)
        for field in fields:
            record = self.check_field_found(field)
            if record:
                if record.ttype in ['many2one']:
                    lines.append((0, 0, {
                        'src_field': field,
                        'dest_field': field,
                        'is_many_2_one': True if record.ttype == 'many2one' else False,
                        'is_many_2_many': True if record.ttype == 'many2many' else False,
                        'is_selection': True if record.ttype == 'selection' else False,
                    }))

            else:
                self.fields_not_in = self.fields_not_in or "" + "," + field
        self.line_ids = [(5, 0, 0)]
        self.line_ids = lines

    def check_fields_many2many(self):
        api = self.get_api()
        data = api.search6(self.src_model, [[]], [],limit=20)
        print(">SS>", data)
        fields = []
        lines = []
        lines.append((0, 0, {
            'src_field': 'id',
            'dest_field': 'id',
            'is_many_2_one': False,
            'is_many_2_many': False,
            'is_selection': False,
        }))
        for datas in data:
            for key in datas.keys():
                if key not in fields:
                    fields.append(key)
            print(">", fields)
        for field in fields:
            record = self.check_field_found(field)
            if record:
                if record.ttype in ['many2many']:
                    lines.append((0, 0, {
                        'src_field': field,
                        'dest_field': field,
                        'is_many_2_one': True if record.ttype == 'many2one' else False,
                        'is_many_2_many': True if record.ttype == 'many2many' else False,
                        'is_selection': True if record.ttype == 'selection' else False,
                    }))

            else:
                self.fields_not_in = self.fields_not_in or "" + "," + field
        self.line_ids = [(5, 0, 0)]
        self.line_ids = lines

    def check_fields_selection(self):
        api = self.get_api()
        data = api.search6(self.src_model, [[]], [],limit=20)
        print(">SS>", data)
        fields = []
        lines = []
        lines.append((0, 0, {
            'src_field': 'id',
            'dest_field': 'id',
            'is_many_2_one': False,
            'is_many_2_many': False,
            'is_selection': False,
        }))
        for datas in data:
            for key in datas.keys():
                if key not in fields:
                    fields.append(key)
            print(">", fields)
        for field in fields:
            record = self.check_field_found(field)
            if record:
                if record.ttype in ['selection']:
                    lines.append((0, 0, {
                        'src_field': field,
                        'dest_field': field,
                        'is_many_2_one': True if record.ttype == 'many2one' else False,
                        'is_many_2_many': True if record.ttype == 'many2many' else False,
                        'is_selection': True if record.ttype == 'selection' else False,
                    }))

            else:
                self.fields_not_in = self.fields_not_in or "" + "," + field
        self.line_ids = [(5, 0, 0)]
        self.line_ids = lines


    def check_fields_all(self):
        api = self.get_api()
        data = api.search6(self.src_model, [[]], [],limit=20)
        fields = []
        lines = []
        for datas in data:
            for key in datas.keys():
                if key not in fields:
                    fields.append(key)
            print(">", fields)
        for field in fields:
            record = self.check_field_found(field)
            if record:
                if record.ttype not in ['one2many', 'many2one', 'many2many', 'selection']:
                    lines.append((0, 0, {
                        'src_field': field,
                        'dest_field': field,
                        'is_many_2_one': True if record.ttype == 'many2one' else False,
                        'is_many_2_many': True if record.ttype == 'many2many' else False,
                        'is_selection': True if record.ttype == 'selection' else False,
                    }))

            else:
                self.fields_not_in = self.fields_not_in or "" + "," + field
        self.line_ids = [(5, 0, 0)]
        self.line_ids = lines


    def check_fields_all2(self):
        api = self.get_api()
        data = api.search6(self.src_model, [[]], [],limit=20)
        print(">SS>", data)
        fields = []
        lines = []
        for datas in data:
            for key in datas.keys():
                if key not in fields:
                    fields.append(key)
            print(">", fields)
        for field in fields:
            record = self.check_field_found(field)
            if record:
                if record.ttype not in ['one2many']:
                    lines.append((0, 0, {
                        'src_field': field,
                        'dest_field': field,
                        'is_many_2_one': True if record.ttype == 'many2one' else False,
                        'is_many_2_many': True if record.ttype == 'many2many' else False,
                        'is_selection': True if record.ttype == 'selection' else False,
                    }))

            else:
                self.fields_not_in = self.fields_not_in or "" + "," + field
        self.line_ids = [(5, 0, 0)]
        self.line_ids = lines

    def check_field_found(self, field):
        record = self.env['ir.model.fields'].search([('model_id.model', '=', self.dest_model), ('name', '=', field)])
        if record:
            return record
        else:
            return False

    def get_selct(self):
        st = "select id,"
        for line in self.line_ids:
            st += line.src_field + ","
        st += " from stock_move"
        print(st)

    def create_record(self, record):
        # if record['state'] not in ['draft','posted']:
        #     if record['state'] =='cancelled':
        #         record['state']='cancel'
        #     else:
        #         record['state']='posted'
        # if not record['partner_id'] in [114,46]:
        # if  record['id'] in [5281]:
        # if record not in ['draft','cancel']:
        #     if record['state']=='paid':
        #         record['payment_state']='paid'
        #     record['state']='posted'

        # if record.get('credit'):
        #     record['debit'] = 0
        #     record['amount_currency'] = -1*record.get('credit')
        # if record.get('debit'):
        #     record['credit'] = 0
        #     record['amount_currency'] = record.get('debit')
        # print(">D>D", record)
        # record['alias_model_id']=726
        # record['alias_parent_model_id']=644
        # record['type_id']=1
        #
        # if not record.get('active'):
        #     record['active'] = False
        # if record.get('code')=='incoming':
        #     record['sequence_code'] = "IN"
        # if record.get('code')=='outgoing':
        #     record['sequence_code'] = "OUT"
        # if record.get('code')=='internal':
        #     record['sequence_code'] = "INT"
        # if not record.get('active'):
        #     record['active']=False
        # if record['type']=='add':
        #     print("D>D>>D>DD>D>>D>")
        # record['ks_global_discount_type']='amount'
        print(">>",record)
        if 1==1:
            print("D>D",record)
            # record.pop('type')
            if 1 == 1:
                if self.is_write:
                    self.env[self.dest_model].sudo().browse(self.dest_res_id).write(record)
                else:
                    self.env[self.dest_model].sudo().create(record)
                    # res = self.env[self.dest_model].sudo().search([('id','=',record['id']),('active','in',(True,False))])
                    # res = self.env[self.dest_model].sudo().search([('id', '=', record['id'])])
                    # if res:
                    #     res.sudo().write(record)
                    # else:
                    #     self.env[self.dest_model].sudo().create(record)




    # def create_cron_all(self):
    #     api = self.get_api()
    #     data = api.search2('ir.model', [[]], ['model'])
    #     print("D>>D", data)
    #     for datas in data:
    #         try:
    #             record = self.env['migarator.models'].create(
    #                 {'src_model': datas['model'], 'dest_model': datas['model']})
    #             record.check_fields()
    #         except:
    #             print("D>D", datas)
    #
    # def run_cron_all(self):
    #     records = self.env['migarator.models'].search([('state', '=', 'draft')])
    #     for datas in records:
    #         try:
    #             datas.get_data_from_api()
    #         except:
    #             pass

    def reseq(self):
        for record in self.search([('state','=','done')]):
            try:
                self.env.cr.execute("""SELECT setval(\'{model}\', max(id)) FROM {model2};""".format(model=str(record.dest_model).replace('.','_') +'_id_seq',model2=str(record.dest_model).replace('.','_')))
            except:
                pass

class MigrateModelsLines(models.Model):
    _name = 'migarator.models.lines'
    migarator_id = fields.Many2one(
        comodel_name='migarator.models',
        string='Migarator_id',
        required=False)
    src_field = fields.Char(string='Src Field', required=True)
    dest_field = fields.Char(string='Dest Field', required=True)
    is_many_2_one = fields.Boolean(string='Is Many2one Field', required=True)
    is_many_2_many = fields.Boolean(string='Is Many2many Field', required=True)
    is_selection = fields.Boolean(string='Is Selection Field', required=True)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    migarator_host_name = fields.Char(string='Host Name')
    migarator_database = fields.Char(string='Database')
    migarator_user_name = fields.Char(string='User Name')
    migarator_password = fields.Char(string='Password')

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        with_user = self.env['ir.config_parameter'].sudo()
        with_user.set_param('odoo_migrator.migarator_host_name', self.migarator_host_name)
        with_user.set_param('odoo_migrator.migarator_database', self.migarator_database)
        with_user.set_param('odoo_migrator.migarator_user_name', self.migarator_user_name)
        with_user.set_param('odoo_migrator.migarator_password', self.migarator_password)

        return res

    @api.model
    def get_values(self):
        values = super(ResConfigSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        values['migarator_host_name'] = with_user.get_param('odoo_migrator.migarator_host_name')
        values['migarator_database'] = with_user.get_param('odoo_migrator.migarator_database')
        values['migarator_user_name'] = with_user.get_param('odoo_migrator.migarator_user_name')
        values['migarator_password'] = with_user.get_param('odoo_migrator.migarator_password')

        return values


