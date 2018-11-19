<template>
  <page style="z-index: 200;" ref="guaqiPage">
    <div class="repair-page">

      <div class="cell-group">
        <div class="group-title">挂起原因</div>
        <mt-field placeholder="请填写挂起原因（必填）" type="textarea" rows="4" v-model="content"></mt-field>
        <div class="distance-warn">提示：工单挂起后，任务将处于冻结状态，如需重启任务，请联系机电中心调度员</div>
      </div>

      <div class="repair-action">
        <cube-button primary @click="handleSubmit" :disabled="!content">提交</cube-button>
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
      content: ''
    }
  },
  mounted () {
  },
  methods: {

    handleSubmit () {
      this.$refs.guaqiPage.showLoading()

      this.rpc.call('repair_manage.task_page', 'suspend_task', [
        this.$route.params.id,
        this.content
      ], {}).then(data => {
        console.log('aaa', data)
        this.$refs.guaqiPage.hideLoading()
        this.$createToast({
          txt: '提交成功',
          type: 'correct'
        }).show()
        setTimeout(() => {
          this.$router.back()
        }, 200)
      }).catch(e => {
        this.$refs.guaqiPage.hideLoading()
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
.repair-page {
  padding: 16px 0;
}
.repair-action{
  margin: 30px 10px;
}
.group-detail{
  background: #fff;
  padding: 5px 15px 10px;
}
.distance-warn{
  font-size: 10px;
  line-height: 20px;
  padding: 0 15px;
  // background: #fff;
  color: red;
}
</style>
