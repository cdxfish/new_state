# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrainLineMore(models.Model):
    '''
    线别信息
    '''
    _name = 'train_line_more.train_line_more'

    line_id = fields.Many2one(comodel_name="train_line.train_line", string="线别", required=True)
    station_ids = fields.One2many(comodel_name="train_station.train_station",
                                  inverse_name="train_line_more_id",
                                  string="站点信息",
                                  required=False,
                                  ondelete="restrict",
                                  domain=[('station_type', '!=', 'qy')])

    start_end_station = fields.Char(string='起始站点')
    station_num = fields.Integer(string="线路站点数",
                                 compute='compute_station_num',
                                 readonly=True,
                                 store=True)

    assist_num = fields.Integer(string="辅助线数",
                                required=False,
                                compute='compute_station_num',
                                readonly=True,
                                store=True)

    block_ids = fields.One2many(comodel_name="train_block.train_block", inverse_name="train_line_more_id",
                                string="区间", required=False)

    @api.one
    @api.depends('block_ids.location_name', 'block_ids.assist_line')
    def compute_station_num(self):
        '''
        计算站点个数
        :return:
        '''
        records_station = self.env['train_station.train_station'].search([
            ('train_line_more_id', '=', self.id)
        ])
        if len(records_station) > 0:
            self.station_num = len(records_station)
        else:
            self.station_num = 0

        # 辅助线数目
        records_assist_num = self.env['train_block.train_block'].search([
            ('train_line_more_id', '=', self.id),
            ('location_type', '!=', '0')])
        length_assist_line = 0
        for item in records_assist_num:
            length_assist_line += len(item.assist_line)

        if length_assist_line > 0:
            self.assist_num = length_assist_line
        else:
            self.assist_num = 0

    # 绑定站点
    @api.multi
    def bind_data(self):
        train_line_more_id = self.id
        records = self.env['train_station.train_station'].search([
            ('train_line_more_id', '=', train_line_more_id),
            ('station_type', '!=', 'qy')
        ])
        records_block = self.env['train_block.train_block'].search([
            ('train_line_more_id', '=', train_line_more_id)]).mapped('location_name').mapped('name')
        num = 1

        for i, item in enumerate(records):
            location_type = 'cz'
            if item.name not in records_block:
                if i == 0:
                    i = num
                    location_type = 'cc'
                else:
                    i += num + i
                self.env['train_block.train_block'] \
                    .create({'number': i,
                             'location_name': item.id,
                             'train_line_more_id': item.train_line_more_id.id,
                             'location_type': location_type
                             })

    # 绑定区间
    @api.multi
    def bind_data_add(self):
        records_train_block = self.env['train_block.train_block'].search([
            ('location_type', '!=', 'qy'),
            ('location_type', '!=', 'dx'),
            ('train_line_more_id', '=', self.id)
        ])
        records_train_block_qy = self.env['train_block.train_block'].search([
            ('location_type', '=', 'qy'),
            ('train_line_more_id', '=', self.id)
        ]).mapped('location_name')
        records_train_station = self.env['train_station.train_station'].search([
            ('train_line_more_id', '=', self.id),
            ('station_type', '!=', 'qy')
        ])
        if len(records_train_block) == len(records_train_station):
            number = 0
            station_combine = self.env['train_station.train_station'].search([]).mapped('name')
            for i, item in enumerate(records_train_block):
                if i == 0:
                    continue
                else:
                    number += 2
                location_name = records_train_block[i - 1].location_name.name + ' 至 ' + item.location_name.name
                if location_name not in station_combine:
                    record_id = self.env['train_station.train_station'].create({
                        'name': location_name,
                        'train_line_more_id': item.train_line_more_id.id,
                        'station_type': 'qy'
                    })

                    if location_name not in records_train_block_qy:
                        self.env['train_block.train_block']\
                            .create({'number': number,
                                     'location_name': record_id.id,
                                     'train_line_more_id': item.train_line_more_id.id,
                                     'location_type': 'qy'})
