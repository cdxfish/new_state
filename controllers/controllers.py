# -*- coding: utf-8 -*-
from odoo import http
import requests, datetime, time

import logging

_logger = logging.getLogger(__name__)


class FuencStation(http.Controller):
    @http.route('/funenc_xa_station2/check_collect/', type='http', auth='none')
    def index(self, **kw):
        try:
            payload = {'appid': 'ding4484e57b2688826335c2f4657eb6378f',
                       'appsecret': '7E4S7vJhcnDQ4jUwCuCbHo7qkisscY5Yq8dP0gW0dsFYs0USp4bw8WuhLFa19trr'}
            _resp = requests.get('https://oapi.dingtalk.com/sns/gettoken', params=payload).json()
            url = 'https://oapi.dingtalk.com/sns/get_persistent_code?access_token={}'.format(_resp.get('access_token'))
            payload = {'tmp_auth_code': ''}
            res = requests.post(url, json=payload).json()
            openid = res.get('openid')
            user_id = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search([('openId', '=', openid)])
            arrange_order_id = self.env['funenc_xa_station2.sheduling_record'].search(
                [('site_id', '=', user_id.departments[0].id),
                 ('user_id', '=', user_id.id),
                 ('sheduling_date', '=', datetime.datetime.now())])
            values = {'line_id': user_id.line_id.id,
                      'site_id': user_id.departments[0].id,
                      'time': datetime.datetime.now(),
                      'user_id': user_id.id,
                      'arrange_order_id': arrange_order_id.id,
                      'clock_site': user_id.departments[0].id,
                      'clock_start_time': datetime.datetime.now(),
                      'is_overtime': 'no'
                      }
            self.env['fuenc_station.clock_record'].create(values)
        except Exception as e:
            print(e)

        return "打卡成功"

    @http.route('/funenc_xa_station2/off_work/', type='http', auth='none')
    def off_work(self, **kw):
        try:
            payload = {'appid': 'ding4484e57b2688826335c2f4657eb6378f',
                       'appsecret': '7E4S7vJhcnDQ4jUwCuCbHo7qkisscY5Yq8dP0gW0dsFYs0USp4bw8WuhLFa19trr'}
            _resp = requests.get('https://oapi.dingtalk.com/sns/gettoken', params=payload).json()
            url = 'https://oapi.dingtalk.com/sns/get_persistent_code?access_token={}'.format(_resp.get('access_token'))
            payload = {'tmp_auth_code': ''}
            res = requests.post(url, json=payload).json()
            openid = res.get('openid')
            user_id = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search([('openId', '=', openid)])

            arrange_order_id = self.env['funenc_xa_station2.sheduling_record'].search(
                [('site_id', '=', user_id.departments[0].id),
                 ('user_id', '=', user_id.id),
                 ('sheduling_date', '=', datetime.datetime.now())])
            values = {'line_id': user_id.line_id.id,
                      'site_id': user_id.departments[0].id,
                      'time': datetime.datetime.now(),
                      'user_id': user_id.id,
                      'arrange_order_id': arrange_order_id.id,
                      'clock_site': user_id.departments[0].id,
                      'clock_end_time': datetime.datetime.now()
                      }
            self.env['fuenc_station.clock_record'].create(values)
        except Exception as e:
            print(e)

        return http.local_redirect('/fnt_fm1212/static/home_pc.html?t=%s' % int(round(time.time())))

    @http.route('/fuenc_station/fuenc_station/objects/<model("fuenc_station.fuenc_station"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('fuenc_station.object', {
            'object': obj
        })

    # @http.route('controllers/training_plan/punch_the_clock', type='http', auth='none')
    # def punch_the_clock(self):
    #     '''
    #     培训打卡
    #     :param kw:
    #     :return:
    #     '''
    #
    #     return "打卡成功"

    @http.route('/controllers/training_plan/punch_the_clock', type='http', auth='none')
    def training_plan_local_redirect_1(self, **kw):
        print('redirect')
        # &t=%s % int(round(time.time()))

        return http.local_redirect(
            '/funenc_xa_station2/static/html/get_code.html?training_plan_id={}'.format(kw.get('training_plan_id')))

    @http.route('/funenc_xa_station2/training_plan_get_code', type='http', auth='none')
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
                        personnel_situation = http.request.env['funenc_xa_station2.personnel_situation'].sudo().create({
                            'training_plan_id': training_plan_id,
                            'sign_in_time': current_time,
                            'user_id': user.id
                        })

                        training_plan = http.request.env['funenc_xa_station2.training_plan'].sudo().search(
                            [('id', '=', training_plan_id)])
                        site_training_results = http.request.env[
                            'funenc_xa_station2.site_training_results'].sudo().search([('site_id', '=', site_id),
                                                                                      ('training_plan_id', '=',
                                                                                       training_plan_id)])
                        if not site_training_results:
                            create = http.request.env['funenc_xa_station2.site_training_results'].sudo().create({
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
        print('redirect')
        # &t=%s % int(round(time.time()))

        return http.local_redirect(
            '/funenc_xa_station2/static/html/get_drill_plan_code.html?drill_plan_id={}'.format(kw.get('drill_plan_id')))

    @http.route('/funenc_xa_station2/get_code', type='http', auth='none')
    def get_code_1(self, **kw):
        training_plan_id = kw.get('drill_plan_id')
        code = kw.get('code')
        user = self.get_user_by_code(code)

        try:
            # 生成签到
            check_in = http.request.env['funenc_xa_station2.drill_plan_sign_in'].sudo().search(
                [('sign_user_id', '=', user.id), ('drill_plan_sign_in_id', '=', training_plan_id)])

            if check_in:
                return '<h1>你已签到</h1>'


            # 签到人员统计
            drill_plan = http.request.env['funenc_xa_station2.drill_plan'].sudo().search(
                [('id', '=', training_plan_id)])

            if user.departments[0].id in drill_plan.partake_site_ids.ids:

                obj = http.request.env['funenc_xa_station2.drill_plan_sign_in'].sudo().create({
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
