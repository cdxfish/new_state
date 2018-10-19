<template>
  <page style="z-index: 200;" ref="devicePage">
      <cube-scroll
        class="detail-wrapper"
        ref="scroll"
        :options="{
          scrollbar: true,
          momentumLimitTime: 200
        }"
      >
      <div class="sign-detail ">
        <div class="cell-group no-title" >
          <mt-cell :title="item.metro_lines + ' ' + item.metro_addresse" v-for="item in devices" :key="item.id">
            <span>{{item.name}}</span>
          </mt-cell>
        </div>

        <div class="cell-group no-title">

          <div class="sign-record">
            <steps direction="vertical" :active="scanSuccess ? 2 : 1">
              <step>
                <span slot="title">未签到</span>
                <span slot="icon">
                </span>
                <span slot="description">未签到</span>
              </step>
              <step v-if="scanSuccess">
                <span slot="title">签到成功</span>
                <span slot="icon">
                </span>
                <div slot="description">地点：{{successDevice.dev_line}} {{successDevice.dev_name}}<br/></div>
                <div slot="description">{{successDevice.asign_tm}}</div>
              </step>
            </steps>
          </div>
        </div>
      </div>
    </cube-scroll>

    <flexbox :gutter="0" class="detail-action">
      <flexbox-item>
        <cube-button primary @click="handleScan" v-if="!scanSuccess">扫码设备二维码</cube-button>
        <cube-button primary @click="handleBack" v-else>跳转到任务页</cube-button>
      </flexbox-item>
    </flexbox>
  </page>
</template>

<script>
import Page from '../../components/Page'
import Steps from 'element-ui/packages/steps'
import Step from 'element-ui/packages/step'
import 'element-ui/lib/theme-chalk/step.css'
import 'element-ui/lib/theme-chalk/steps.css'
import { Flexbox, FlexboxItem } from 'vux/src/components/flexbox'

export default {
  components: {
    Page,
    Steps,
    Step,
    Flexbox,
    FlexboxItem
  },
  data () {
    return {
      devices: [],
      scanSuccess: false,
      successDevice: {}
    }
  },
  mounted () {
    console.log('device', this.$route)
    this.$refs.devicePage.showLoading()
    this.rpc.call('repair_manage.task_page', 'get_task', [this.$route.params.id], {}).then(data => {
      console.log('device..._detail', data)
      this.devices = data.data.devs
      this.$refs.devicePage.hideLoading()
    }).catch(e => {
      this.$refs.devicePage.hideLoading()
      this.$createToast({
        txt: e.message,
        type: 'error',
        time: 2000
      }).show()
    })
  },
  methods: {
    handleBack () {
      window.sessionStorage.setItem('cur_detail_id', this.successDevice.task_id)
      this.$router.back()
    },
    handleScan () {
      const _this = this
      window.dd.biz.util.scan({
        type: 'qrCode',
        tips: '设备扫码',
        onSuccess: function (data) {
          console.log('data', data, this)
          _this.$refs.devicePage.showLoading()
          _this.rpc.call('repair_manage.task_page', 'code_asign', [
            _this.$route.params.id,
            JSON.stringify(data)
          ], {}).then(data => {
            _this.$refs.devicePage.hideLoading()
            _this.scanSuccess = true
            _this.successDevice = data
            _this.$createToast({
              txt: '签到成功',
              type: 'correct',
              time: 2000
            }).show()
          }).catch(e => {
            _this.$refs.devicePage.hideLoading()
            _this.$createToast({
              txt: e.message,
              type: 'error',
              time: 2000
            }).show()
          })
          // _this.$router.push({name: 'device-detail'})
        },
        onFail: function (err) {
          console.log('err', err)
          alert(JSON.stringify(err))
        }
      })
    }
  }
}
</script>

<style lang="scss">
.sign-detail{
  padding-bottom: 60px;
}
.sign-record{
  padding: 10px 15px;
  background: #fff;
}
</style>
