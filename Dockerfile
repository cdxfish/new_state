From registry-vpc.cn-hangzhou.aliyuncs.com/odoomaster/odoo11_update_base

# 拷贝项目本地文件到docker
ADD . /mnt/extra-addons/funenc_xa_station

# v2
ADD layui_theme /mnt/extra-addons/layui_theme
# master
ADD vue_template_manager /mnt/extra-addons/vue_template_manager
# xa_station
ADD cdtct_dingtalk /mnt/extra-addons/cdtct_dingtalk
ADD qiniu_service /mnt/extra-addons/qiniu_service

# 删除多余文件
RUN rm -rf /mnt/extra-addons/funenc_xa_station/layui_theme
RUN rm -rf /mnt/extra-addons/funenc_xa_station/vue_template_manager
RUN rm -rf /mnt/extra-addons/funenc_xa_station/cdtct_dingtalk
RUN rm -rf /mnt/extra-addons/funenc_xa_station/qiniu_service

# 安装其它依赖
ADD requirements.txt /opt/sources/requirements.txt
RUN pip3 install -r /opt/sources/requirements.txt

# 添加配置文件,一定要添加这两句
COPY odoo.conf /odoo/
RUN chown -R odoo:odoo /var/lib/odoo

RUN python3 ./etc/entrypoint.py

CMD ["/usr/bin/supervisord"]