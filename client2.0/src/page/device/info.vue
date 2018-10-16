<template>
  <page style="z-index: 11002;" ref="infoPage">
    <div class="info-page">
      <div class="cell-group" v-if="infoData.qr_code">
        <div class="group-title">设备二维码</div>
        <div class="group-detail">
          <img :src="infoData.qr_code">
        </div>
      </div>

      <div class="cell-group no-title">
        <mt-cell title="线别">
          {{infoData.line}}
        </mt-cell>
        <mt-cell title="站名">
          {{infoData.metro_addresse}}
        </mt-cell>
        <mt-cell title="设备分类">
          {{infoData.fault_specialty}}
        </mt-cell>
        <mt-cell title="设备名称">
          {{infoData.name}}
        </mt-cell>
        <mt-cell title="设备编号">
          {{infoData.equipment_code}}
        </mt-cell>
        <mt-cell title="规格型号">
          {{infoData.equipment_mpn}}
        </mt-cell>
        <mt-cell title="安装位置">
          {{infoData.line}}
        </mt-cell>
        <mt-cell title="所属系统">
          {{infoData.equipment_system}}
        </mt-cell>
        <mt-cell title="控制方式">
          {{infoData.control_mode}}
        </mt-cell>
        <mt-cell title="安装方式">
          {{infoData.installation_methon}}
        </mt-cell>
        <mt-cell title="上级电源">
          {{infoData.power_supply}}
        </mt-cell>
        <mt-cell title="投用时间">
          {{infoData.input_data}}
        </mt-cell>
        <mt-cell title="主要性能参数">
          {{infoData.main_performance}}
        </mt-cell>
      </div>
    </div>
  </page>
</template>

<script>
import Page from '../../components/Page'

export default {
  components: {
    Page
  },
  data () {
    return {
      infoData: {}
    }
  },
  mounted () {
    this.$refs.infoPage.showLoading()
    this.rpc.call('repair_manage.devices_api', 'get_dev_info', [this.$route.params.deviceId], {}).then(data => {
      console.log('device info', data)
      this.$refs.infoPage.hideLoading()
      this.infoData = data
    }).catch(e => {
      this.$refs.infoPage.hideLoading()
      this.$createToast({
        txt: e.message,
        type: 'error'
      }).show()
    })
  }
}
</script>

<style lang="scss">
.group-detail{
  background: #fff;
  padding: 5px 15px 10px;
}
.info-page{
  padding-bottom: 50px;
}
</style>
