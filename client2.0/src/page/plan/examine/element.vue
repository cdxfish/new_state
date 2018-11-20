<template>
  <page style="z-index: 900;">
    <div class="cell-group">
      <div class="group-title"></div>
      <mt-cell>
        <span slot="title">23号屏蔽门</span>
        <span>已检修</span>
      </mt-cell>
    </div>
    <div class="cell-group">
      <mt-cell>
        <span slot="title">43号屏蔽门</span>
        <span>已检修</span>
      </mt-cell>
    </div>
    <div class="cell-group">
      <mt-cell>
        <span slot="title">FEP设备</span>
        <span>已完成</span>
      </mt-cell>
    </div>
    <div class="cell-group">
      <mt-cell>
        <span slot="title">FEP设备</span>
        <span>待检修</span>
      </mt-cell>
    </div>
    <div class="cell-group">
      <mt-cell>
        <span slot="title">FEP设备</span>
        <span>待检修</span>
      </mt-cell>
    </div>
    <div class="cell-group">
      <mt-cell>
        <span slot="title">FEP设备</span>
        <span>待检修</span>
      </mt-cell>
    </div>
    <div class="cell-group">
      <mt-cell>
        <span slot="title">FEP设备</span>
        <span>待检修</span>
      </mt-cell>
    </div>
  <page-view></page-view>
  </page>
</template>
<script>
import Page from '../../../components/Page'
import PageView from '../../../components/View'

export default {
  components: {
    Page,
    PageView
  },
  data () {
    return {
    }
  },
  mounted () {

    // this.rpc.call('repair_manage.task_page', 'get_order_devices', [this.$route.params.id], {}).then(data => {
    //   console.log(12345678, 'device list', data)
    //   this.equips = data.map(item => ({
    //     // id: item.device_id,
    //     value: item.device_id + '',
    //     label: item.device_name,
    //     valid: true
    //   }))
    //   this.devices = data.map(item => ({
    //     value: item.device_id + '',
    //     label: item.device_name,
    //     valid: true,
    //     checked: true
    //   }))
    // })
  },
  methods: {

    selsetEquipment () {
      this.$router.push({name: 'equipmentSearch'})
    },
    open () {
      this.$createToast({
        txt: '打开摄像头',
        type: 'error'
      }).show()
    }
  }
}
</script>

<style lang="scss">
.paln_detail {
  padding: 1.3rem 0;
}
.repair-action{
  margin: 30px 10px;
}
.group-detail{
  background: #fff;
  padding: 5px 15px 10px;
}

</style>
