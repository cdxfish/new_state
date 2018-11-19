<template>
  <page style="z-index: 900;">
    <div class="paln_detail">
      <div class="cell-group">
        <mt-cell>
          <span slot="title">作业项目：</span>
          <span>网络柜</span>
        </mt-cell>
        <mt-cell  @click.native="handleSelectStation">
          <span slot="title"  >作业地点：</span>
          <span>全线各站点以及场段，控制中心</span>
        </mt-cell>
        <mt-cell  @click.native="handleSelectStation">
          <span slot="title"  >执行单号：</span>
          <span>2018-2-30</span>
        </mt-cell>
        <mt-cell  @click.native="handleSelectStation">
          <span slot="title"  >执行单号：</span>
          <span>J29382390r53920</span>
        </mt-cell>
      </div>
      <div class="cell-group">
        <div class="group-title"></div>
        <mt-cell is-link  @click.native="showPopUp" >
          <span slot="title">设备列表</span>
          <span>1/5</span>
        </mt-cell>
      </div>
      <div class="cell-group">
        <div class="group-title"></div>
        <mt-cell is-link  @click.native="showitem" >
          <span slot="title">查看检修项</span>
          <span>3/5</span>
        </mt-cell>
      </div>

    </div>
    <div  style="position:absolute; bottom: 0; left:0;right:0">
      <cube-button primary @click="open" >执行检修单</cube-button>
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
    showPopUp (type) {
      this.$router.push({name: 'element'})
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
