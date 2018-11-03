# !user/bin/env python3
# -*- coding: utf-8 -*-


from odoo import api, models, fields
import datetime

class BelongToSummary(models.Model):
    _name = 'funenc_xa_station.belong_to_summary'

    line_id = fields.Char(string='线路')
    site_id = fields.Char(string='站点')
    post_check = fields.Char(string='检查岗位')
    summary_score = fields.Integer(string='总分值',default=100)
    mouth_score = fields.Integer(string='本月评分')
    check_count = fields.Integer(string='检查次数')

    @api.model
    def default_look_record(self):
        mouth = datetime.datetime.now()
        print(mouth)


    @api.model
    def belong_to_method(self):
        self.env.user.name
        return

    @api.model
    def add_count_line(self):
        line = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('department_hierarchy', '=', 2)],
                                                                               ['id', 'name'])
        return line

    @api.model

    def add_count_site(self):
        site = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('department_hierarchy', '=', 3)],
                                                                               ['id', 'name'])
        return site

    @api.model
    def search_site(self, date):
        site_parent = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read([('id', '=', date)],
                                                                                       ['departmentId'])
        site_son = self.env['cdtct_dingtalk.cdtct_dingtalk_department'].search_read(
            [('parentid', '=', site_parent[0]['departmentId'])], ['name'])

        return site_son

    @api.model
    def search_record(self):
        pass

    @api.model
    def search_date_record_now(self,date,line,site,person_id):
        if not person_id:
            date = date[:10]
            d = datetime.datetime.strptime(date, '%Y-%m-%d')
            delta = datetime.timedelta(days=8)
            open_time = d + delta
            date_new = open_time.strftime('%Y-%m-%d %H:%M:%S')
            # print(date,line,site,person_id)
            # print(date_new)
            record = {}
            line = self.env['funenc_xa_station.belong_to_management'].search_read([('site_id','=',site)]
                        ,['line_id','site_id','post_check','summary_score','check_time','check_score'])
            date_list = [check_record for check_record in line if check_record.get('check_time')[:7] == date_new[:7]]

            for list1 in date_list:
                record[list1.get('post_check')] = list1
            # count  得分
            for list2 in record:
                i = 0
                fs = 0
                for list3 in date_list:
                    if list2 == list3.get('post_check'):
                        i = i + 1
                        fs = fs + list3.get('check_score')
                record[list2].update({'check_count': i})
                record[list2].update({'mouth_score': fs+100})
                record[list2].update({'summary_score': 100})
                record[list2].update({'line_id':list3.get('line_id')[1]})
                record[list2].update({'site_id':list3.get('site_id')[1]})
            record_list=[record.get(key) for key in record]
            for ii in record_list:
                if ii['post_check'] == 'guard':
                    ii['post_check'] ='保安'
                if ii['post_check'] == 'check':
                    ii['post_check'] = '安检'
                if ii['post_check'] == 'clean':
                    ii['post_check'] = '保洁'
            return record_list

        #用来判断输入的人名和工号
        elif person_id:
            date = date[:10]
            d = datetime.datetime.strptime(date, '%Y-%m-%d')
            delta = datetime.timedelta(days=8)
            open_time = d + delta
            date_new = open_time.strftime('%Y-%m-%d %H:%M:%S')
            # print(date,line,site,person_id)
            # print(date_new)
            record = {}
            line = self.env['funenc_xa_station.belong_to_management'].search_read(['|',('write_person', '=', person_id),
                                                                                   ('job_number', '=', person_id)])
            date_list = [check_record for check_record in line if check_record.get('check_time')[:7] == date_new[:7]]

            for list1 in date_list:
                record[list1.get('post_check')] = list1
            # count  得分
            for list2 in record:
                i = 0
                fs = 0
                for list3 in date_list:
                    if list2 == list3.get('post_check'):
                        i = i + 1
                        fs = fs + list3.get('check_score')
                record[list2].update({'check_count': i})
                record[list2].update({'mouth_score': fs + 100})
                record[list2].update({'summary_score': 100})
                record[list2].update({'line_id': list3.get('line_id')[1]})
                record[list2].update({'site_id': list3.get('site_id')[1]})
            record_list = [record.get(key) for key in record]
            for ii in record_list:
                if ii['post_check'] == 'guard':
                    ii['post_check'] = '保安'
                if ii['post_check'] == 'check':
                    ii['post_check'] = '安检'
                if ii['post_check'] == 'clean':
                    ii['post_check'] = '保洁'
            return record_list

    @api.model
    def search_details_button(self,date,line,site,person_id):
        date = date[:10]
        d = datetime.datetime.strptime(date, '%Y-%m-%d')
        delta = datetime.timedelta(days=8)
        open_time = d + delta
        date_new = open_time.strftime('%Y-%m-%d %H:%M:%S')

        # domain = self.env['funenc_xa_station.belong_to_management'].search([('line_id','=',line),('site_id','=',site)])



        view_tree = self.env.ref('funenc_xa_station.belong_to_management_tree').id
        return {
            'name': '属地汇总',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': "[('line_id','=',%s),('site_id','=',%s),('check_time','=',%s)]" % (int(line), int(site)),
            "views": [[view_tree, "list"]],
            'res_model': 'funenc_xa_station.belong_to_management',
            'context': self.env.context,
        }





