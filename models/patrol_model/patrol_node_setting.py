# -*- coding: utf-8 -*-

from odoo import api, models, fields
import qrcode
import base64
import datetime
import json
import os
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


class PatrolNodeSetting(models.Model):
    _name = 'funenc_xa_station.patrol_node_setting'
    _inherit = ['fuenc_station.station_base', 'mail.thread', 'mail.activity.mixin']
    _description = '巡更节点设置'
    _rec_name = 'node_name'

    create_time = fields.Datetime(string='创建时间')
    create_person = fields.Char(string='创建人')
    node_name = fields.Char(string='节点名称', required=True)
    node_number = fields.Char(string='节点编号', required=True)
    qr_code = fields.Binary(string='二维码')
    _sql_constraints = [('name_unique', 'unique(node_name)', "填写的节点名称必须唯一")]
    _sql_constraints = [('name_unique', 'unique(node_number)', "填写的节点编号必须唯一")]
    patrol_time = fields.Datetime(string='巡查时间')
    patrol_record = fields.Many2one('funenc_xa_station.patrol_infortation')

    # 保存的时候创建二维码
    @api.model
    def create(self, vals):
        create_new_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 创建时间
        vals['create_time'] = create_new_time
        vals['create_person'] = self.env.user.dingtalk_user.name
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        sele_id = super(PatrolNodeSetting, self).create(vals)
        dict_record = {
            "node_name": sele_id.node_name,
            "node_number": sele_id.node_number,
            "self_id": sele_id.id
        }
        data = json.dumps(dict_record)

        qr.add_data(data)

        qr.make(fit=True)
        img = qr.make_image()
        img.save('%s.png' % (sele_id.id))
        dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        font = ImageFont.truetype(dir + '/static/ttf/simsun.ttf', 25)
        im1 = Image.open('%s.png' % (sele_id.id))
        draw = ImageDraw.Draw(im1)
        draw.text((20, 0), '节点名称：{}'.format(sele_id.node_name), font=font)
        im1.save('123.png')
        imgs = open('123.png', 'rb')
        datas = imgs.read()
        im1.close
        encode_img = base64.b64encode(datas)
        imgs.close()
        os.remove('%s.png' % (sele_id.id))
        os.remove('123.png')
        sele_id.qr_code = encode_img
        return sele_id

    # 新增节点
    def new_increate_node(self):
        return {
            'name': '新增',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'funenc_xa_station.patrol_node_setting',
            'context': self.env.context,
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    # 查看二维码
    def search_qr_code(self):
        form_tree = self.env.ref('funenc_xa_station.patrol_node_setting_from_search_qr').id
        return {
            'name': '二维码',
            'type': 'ir.actions.act_window',
            "views": [[form_tree, "form"]],
            'res_model': 'funenc_xa_station.patrol_node_setting',
            'flags': {'initial_mode': 'edit'},
            'res_id': self.id,
            'context': self.env.context,
            'target': 'new',
        }

    # 删除当前的记录
    def delete_record(self):
        self.unlink()

    # 编辑当前的记录
    def edit_record(self):
        return {
            'name': '节点编辑',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'res_model': 'funenc_xa_station.patrol_node_setting',
            'context': self.env.context,
            'target': 'new',
        }
