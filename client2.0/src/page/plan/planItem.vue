<template>
  <page style="z-index: 900;">
    <div class="paln_detail">
      <div class="cell-group">
        <mt-cell is-link @click.native="handleStart(1)">
          <span slot="title">施工登记-要点：</span>
          <span>待执行</span>
        </mt-cell>
        <mt-cell is-link @click.native="handleStart(2)">
          <span slot="title">安全交底：</span>
          <span>待执行</span>
        </mt-cell>
        <mt-cell is-link @click.native="handleStart(3)">
          <span slot="title">工具物料准备：</span>
          <span>待执行</span>
        </mt-cell>
        <mt-cell is-link @click.native="handleStart(4)">
          <span slot="title">执行检修项：</span>
          <span>待执行</span>
        </mt-cell>
        <mt-cell is-link @click.native="handleStart(5)">
          <span slot="title">出清确认：</span>
          <span>待执行</span>
        </mt-cell>
        <mt-cell is-link @click.native="handleStart(6)">
          <span slot="title">施工销记：</span>
          <span>待执行</span>
        </mt-cell>
      </div>
    </div>
    <div style="position:absolute; bottom: 0; left:0;right:0">
      <cube-button primary @click="open" >提交</cube-button>
    </div>
  <page-view></page-view>
  </page>
</template>
<script>
import Page from '../../components/Page'
import PageView from '../../components/View'

export default {
  components: {
    Page,
    PageView
    // EquipmentSearch
  },
  data () {
    return {
      isPopupShow: false
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
    handleStart (type) {
      this.$router.push({ name: 'asgin', params: {type: type} })
    },
    showitem () {
      this.$router.push({name: 'examine'})
    },
    open () {
      this.$createToast({
        txt: '打开摄像头',
        type: 'error'
      }).show()
    },
    handleSubmit () {
      this.loadingToast.show()

      console.log(this.devices)

      this.rpc.call('repair_manage.task_page', 'repair', [
        this.$route.params.id,
        this.type.id,
        this.content,
        this.remark,
        this.devices,
        this.images,
        this.videoes
      ], {}).then(data => {
        this.$router.back()
        this.loadingToast.hide()
        window.sessionStorage.setItem('cur_detail_id', data)
        this.$createToast({
          txt: '提交成功',
          type: 'correct'
        }).show()
      }).catch(e => {
        this.loadingToast.hide()
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })
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
