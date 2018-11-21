# -*- coding: utf-8 -*-
from odoo import http
import requests, datetime, time

import logging

_logger = logging.getLogger(__name__)


class FuencStation(http.Controller):

    @http.route('/funenc_xa_station/redirect/check_collect', type='http', auth='none',cors='*')
    def redirect_check_collect(self,**kw):
        user_id = int(kw.get('user_id'))
        site_id = int(kw.get('site_id'))

        if kw.get('type') == 'work':
            arrange_order_id = http.request.env['funenc_xa_station.sheduling_record'].sudo().search(
                [('site_id', '=', site_id),
                 ('user_id', '=', user_id),
                 ('sheduling_date', '=', datetime.datetime.now())])
            values = {
                      # 'line_id': user_id.line_id.id,
                      'site_id': site_id,
                      'time': datetime.datetime.now(),
                      'user_id': user_id,
                      'arrange_order_id': arrange_order_id.id if arrange_order_id else None,
                      'clock_site': site_id,
                      'clock_start_time': datetime.datetime.now(),
                      'is_overtime': 'no'
                      }
            http.request.env['fuenc_station.clock_record'].sudo().create(values)

            return '上班打卡成功'

        else:
            clock_records = http.request.env['fuenc_station.clock_record'].sudo().search([('site_id', '=', site_id)],
                                                                                         order='id desc')
            lens = len(clock_records)
            if clock_records:
                clock_record = clock_records[lens-1]
                if clock_record.clock_end_time:
                    return '请先上班打卡'
                else:
                    clock_record.clock_end_time = datetime.datetime.now()
                    return '下班打卡成功'
            else:
                return '请先上班打卡'


    @http.route('/funenc_xa_station/check_collect', type='http', auth='none')
    def check_collect(self, **kw):
        try:
            code = kw.get('code')
            site_id = kw.get('site_id')
            user_id = self.get_code(code)

            arrange_order_id = http.request.env['funenc_xa_station.sheduling_record'].sudo().search(
                [('site_id', '=', site_id),
                 ('user_id', '=', user_id.id),
                 ('sheduling_date', '=', datetime.datetime.now())])
            values = {'line_id': user_id.line_id.id,
                      'site_id': user_id.departments[0].id,
                      'time': datetime.datetime.now(),
                      'user_id': user_id.id,
                      'arrange_order_id': arrange_order_id.id,
                      'clock_site': site_id,
                      'clock_start_time': datetime.datetime.now(),
                      'is_overtime': 'no'
                      }
            http.request.env['fuenc_station.clock_record'].sudo().create(values)
        except Exception as e:
            return "失败"

        return "打卡成功"

    @http.route('/funenc_xa_station/off_work', type='http', auth='none')
    def off_work(self, **kw):
        try:
            code = kw.get('code')
            user_id = self.get_code(code)
            site_id = kw.get('site_id')

            arrange_order_id = http.request.env['funenc_xa_station.sheduling_record'].sudo().search(
                [('site_id', '=', site_id),
                 ('user_id', '=', user_id.id),
                 ('sheduling_date', '=', datetime.datetime.now())])
            values = {'line_id': user_id.line_id.id,
                      'site_id': user_id.departments[0].id,
                      'time': datetime.datetime.now(),
                      'user_id': user_id.id,
                      'arrange_order_id': arrange_order_id.id,
                      'clock_site': site_id,
                      'clock_end_time': datetime.datetime.now()
                      }
            http.request.env['fuenc_station.clock_record'].sudo().create(values)
        except Exception as e:
            return '下班打卡失败'

        return '下班打卡成功'

    @http.route('/fuenc_station/fuenc_station/objects/<model("fuenc_station.fuenc_station"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('fuenc_station.object', {
            'object': obj
        })


    @http.route('/controllers/training_plan/punch_the_clock', type='http', auth='none')
    def training_plan_local_redirect_1(self, **kw):
        print('redirect')
        # &t=%s % int(round(time.time()))
        print('/funenc_xa_station/static/html/get_code.html?training_plan_id={}'.format(kw.get('training_plan_id')))

        return http.local_redirect(
            '/funenc_xa_station/static/html/get_code.html?training_plan_id={}'.format(kw.get('training_plan_id')))

    @http.route('/funenc_xa_station/training_plan_get_code', type='http', auth='none')
    def get_code(self, **kw):
        training_plan_id = kw.get('training_plan_id')
        code = kw.get('code')
        cdtct_dingtalk_account = http.request.env['cdtct_dingtalk.cdtct_dingtalk_account'].sudo().search([])[0]
        if cdtct_dingtalk_account:
            if cdtct_dingtalk_account.corpid:
                if cdtct_dingtalk_account.secret:
                    try:
                        url = 'https://oapi.dingtalk.com/gettoken?corpid={corpid}&corpsecret={corpsecret}'
                        content = requests.get(
                            url.format(corpid=cdtct_dingtalk_account.corpid, corpsecret=cdtct_dingtalk_account.secret))
                        access_token = content.json().get('access_token')
                        url1 = 'https://oapi.dingtalk.com/user/getuserinfo?access_token={}&code={}'.format(access_token,
                                                                                                           code)
                        _resp = requests.get(url1).json()
                        user_id = _resp.get('userid')
                        current_time = datetime.datetime.now()
                        user = http.request.env['cdtct_dingtalk.cdtct_dingtalk_users'].sudo().search(
                            [('userid', '=', user_id)])
                        line_id = user.line_id.id
                        site_id = user.departments[0].id
                        #  打卡
                        personnel_situation = http.request.env['funenc_xa_station.personnel_situation'].sudo().create({
                            'training_plan_id': training_plan_id,
                            'sign_in_time': current_time,
                            'user_id': user.id
                        })

                        training_plan = http.request.env['funenc_xa_station.training_plan'].sudo().search(
                            [('id', '=', training_plan_id)])
                        site_training_results = http.request.env[
                            'funenc_xa_station.site_training_results'].sudo().search([('site_id', '=', site_id),
                                                                                      ('training_plan_id', '=',
                                                                                       training_plan_id)])
                        if not site_training_results:
                            create = http.request.env['funenc_xa_station.site_training_results'].sudo().create({
                                'line_id': line_id,
                                'site_id': site_id,
                                'training_person_time': 1,
                                'training_plan_id': training_plan_id,
                            })

                            personnel_situation.site_training_results_id = create.id


                        else:
                            site_training_results.write({
                                'training_person_time': site_training_results.training_person_time + 1
                            })
                    except Exception:
                        logging.info('{}'.format(Exception))
                        return '打卡失败'


                else:
                    return '<h1>打卡失败,企业secret未设置</h1>'
            else:
                return '<h1>打卡失败,企业id未设置</h1>'
        else:
            return '<h1>打卡失败,企业账号未设置</h1>'

        return '<h1>打卡成功</h1>'

    def get_user_by_code(self, code=None):
        try:
            code = code
            url = 'https://oapi.dingtalk.com/gettoken?corpid={corpid}&corpsecret={corpsecret}'
            cdtct_dingtalk_account = http.request.env['cdtct_dingtalk.cdtct_dingtalk_account'].sudo().search([])[0]
            content = requests.get(
                url.format(corpid=cdtct_dingtalk_account.corpid, corpsecret=cdtct_dingtalk_account.secret))
            access_token = content.json().get('access_token')
            url1 = 'https://oapi.dingtalk.com/user/getuserinfo?access_token={}&code={}'.format(access_token, code)
            _resp = requests.get(url1).json()
            user_id = _resp.get('userid')
            user = http.request.env['cdtct_dingtalk.cdtct_dingtalk_users'].sudo().search([('userid', '=', user_id)])
        except Exception:
            return []

        return user

    @http.route('/controllers/drill_plan/punch_the_clock', type='http', auth='none')
    def training_plan_local_redirect(self, **kw):
        # &t=%s % int(round(time.time()))
        print('/funenc_xa_station/static/html/get_drill_plan_code.html?drill_plan_id={}'.format(kw.get('drill_plan_id')))
        return http.local_redirect(
            '/funenc_xa_station/static/html/test.html?drill_plan_id={}'.format(kw.get('drill_plan_id')))

    @http.route('/funenc_xa_station/get_code', type='http', auth='none')
    def get_code_1(self, **kw):
        training_plan_id = kw.get('drill_plan_id')
        code = kw.get('code')
        user = self.get_user_by_code(code)

        try:
            # 生成签到
            check_in = http.request.env['funenc_xa_station.drill_plan_sign_in'].sudo().search(
                [('sign_user_id', '=', user.id), ('drill_plan_sign_in_id', '=', training_plan_id)])

            if check_in:
                return '<h1>你已签到</h1>'


            # 签到人员统计
            drill_plan = http.request.env['funenc_xa_station.drill_plan'].sudo().search(
                [('id', '=', training_plan_id)])

            if user.departments[0].id in drill_plan.partake_site_ids.ids:

                obj = http.request.env['funenc_xa_station.drill_plan_sign_in'].sudo().create({
                    'sign_in_time': datetime.datetime.now(),
                    'sign_user_id': user.id,
                    'drill_plan_sign_in_id': training_plan_id,
                    # 'site_drill_plan_id': ''

                })

                for drill_result_id in drill_plan.drill_result_ids:
                    if drill_result_id.site_id.id == user.departments[0].id:
                        # 统计
                        drill_result_id.people_number = drill_result_id.people_number + 1

                for site_drill_plan_id in drill_plan.site_drill_plan_ids:
                    if site_drill_plan_id.position.id == user.departments[0].id:
                        # 人员签到和站点关联
                        obj.write({'site_drill_plan_id': site_drill_plan_id.id})
            else:
                return '<h1>你不属于演练签到人员</h1>'




        except Exception:
            return '<h1>签到失败</h1>'

        return '<h1>签到成功</h1>'


    def get_user_by_id(self,id):

        user = http.request.env['cdtct_dingtalk.cdtct_dingtalk_users'].sudo().search([('id','=',id)])

        return user

    @http.route('/app_index', type='http', auth='none', cors='*')
    def app_index(self, **kw):
        return http.local_redirect(
            '/funenc_xa_station/static/static/index.html')
