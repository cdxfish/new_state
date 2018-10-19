# -*- coding: utf-8 -*-
from odoo import http
import requests,datetime
class FuencStation(http.Controller):
    @http.route('/funenc_xa_station/check_collect/', type='http', auth='none')
    def index(self, **kw):
        try:
            payload = {'appid': 'ding4484e57b2688826335c2f4657eb6378f', 'appsecret': '7E4S7vJhcnDQ4jUwCuCbHo7qkisscY5Yq8dP0gW0dsFYs0USp4bw8WuhLFa19trr'}
            _resp = requests.get('https://oapi.dingtalk.com/sns/gettoken', params=payload).json()
            url = 'https://oapi.dingtalk.com/sns/get_persistent_code?access_token={}'.format(_resp.get('access_token'))
            payload = {'tmp_auth_code': ''}
            res = requests.post(url, json=payload).json()
            openid = res.get('openid')
            user_id = self.env['cdtct_dingtalk.cdtct_dingtalk_users'].search([('openId','=', openid)])
            arrange_order_id=self.env['funenc_xa_station.sheduling_record'].search([('site_id','=',user_id.departments[0].id),
                                                                   ('user_id','=',user_id.id),
                                                                   ('sheduling_date','=',datetime.datetime.now())])
            values = {'line_id':user_id.line_id.id,
                      'site_id':user_id.departments[0].id,
                      'time':datetime.datetime.now(),
                      'user_id':user_id.id,
                      'arrange_order_id':arrange_order_id.id,
                      'clock_site':user_id.departments[0].id,
                      'clock_start_time':datetime.datetime.now(),
                      'is_overtime': 'no'
                      }
            self.env['fuenc_station.clock_record'].create(values)
        except Exception as e:
            print(e)

        return "打卡成功"

    @http.route('/funenc_xa_station/off_work/', type='http', auth='none')
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

            arrange_order_id = self.env['funenc_xa_station.sheduling_record'].search(
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
