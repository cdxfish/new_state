# -*- coding: utf-8 -*-
from odoo import models, fields

class ErrorModel(models.Model):
    _name = 'funenc_xa_station.error_model'
    _description = u'错误显示模型'

    error_content = fields.Html(string='错误内容',default=lambda self:self.default_error_content()
                                )

    def default_error_content(self):
        if self._context.get('error_content', False):
            return self._context['error_content']


