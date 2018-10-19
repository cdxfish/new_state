<template>
  <page ref="handPage">
    <md-tabs
      :titles="['接收任务', '移交任务']"
      :ink-bar-length="100"
      class="handover-tabs"
      @change="handleTabChange"
    >
    </md-tabs>

    <div class="tab-detail" v-if="tabIndex==0">
      <div class="tab-list">
        <list ref="receivingList" :filter="{}" type="receiving" :checkes="checkes1"></list>
      </div>

      <flexbox :gutter="0" class="detail-action">
        <flexbox-item>
          <cube-button light :disabled="checkes1.length==0" @click="handleTranspod1">转发</cube-button>
        </flexbox-item>
        <flexbox-item  >
          <cube-button @click="handleBack" :disabled="checkes1.length==0" :style="checkes1.length==0 ? '' : 'background: #e64340; border-color: #e64340; '">退回</cube-button>
        </flexbox-item>
        <flexbox-item>
          <cube-button primary :disabled="checkes1.length==0" @click="handleHandover">接收</cube-button>
        </flexbox-item>
      </flexbox>
    </div>


    <div class="tab-detail" v-if="tabIndex==1">

      <div class="tab-list">
        <list ref="workingList" :filter="{}" type="working" :checkes="checkes2"></list>
      </div>
      <flexbox :gutter="0" class="detail-action">
        <flexbox-item>
          <cube-button primary :disabled="checkes2.length==0" @click="handleTurnover">移交任务</cube-button>
        </flexbox-item>
      </flexbox>
    </div>

    <cube-dialog type="confirm" @confirm="handleJieshou" v-model="dialogVisible" :confirmBtn="{text: '确认接收'}" :cancelBtn="{text: '返回'}">
      <div slot="content" style="text-align: center;">
        <!-- <div>接收时间：06/13  09:30</div> -->
        <div>本次接收任务数 {{checkes1.length}} 条</div>
      </div>
    </cube-dialog>

    <cube-toast txt="转发成功" v-model="transpondSuccessed" type="correct" :time="500"></cube-toast>

    <cube-toast txt="移交成功" v-model="turnoverSuccessed" type="correct" :time="500"></cube-toast>


    <page-view></page-view>
  </page>
</template>

<script>
import Page from '../../components/Page'
import PageView from '../../components/View'
import { Flexbox, FlexboxItem } from 'vux/src/components/flexbox'
import List from './list'
// import config from '../../util/config.js'

export default {
  components: {
    Page,
    PageView,
    Flexbox,
    FlexboxItem,
    List
  },
  data () {
    return {
      tabIndex: 0,
      checkes1: [],
      checkes2: [],
      dialogVisible: false,
      transpondSuccessed: false,
      turnoverSuccessed: false,
      loadingToast: this.$createToast({
        txt: '',
        time: 0,
        mask: true
      })
    }
  },
  methods: {
    handleTabChange (index) {
      console.log(index)
      this.tabIndex = index
    },

    handleHandover () {
      this.dialogVisible = true
    },

    handleTranspod1 () {
      this.$router.push({name: 'handover-transpond', params: {tasks: this.checkes1.map(item => item.id).join(',')}})
    },

    handleTurnover () {
      console.log(this.checkes2)
      this.$router.push({name: 'handover-transpond', params: {tasks: this.checkes2.map(item => item.id).join(',')}})
    },

    handleJieshou () {
      console.log(this.checkes1)
      this.$refs.handPage.showLoading()
      this.rpc.call('repair_manage.task_page', 'accept_exchanging_task', [
        this.checkes1.map(item => item.id)
      ], {}).then(data => {
        this.$refs.receivingList && this.$refs.receivingList.refresh()
        this.$refs.handPage.hideLoading()
        this.$createToast({
          txt: '接收成功',
          type: 'correct'
        }).show()
      }).catch(e => {
        this.$refs.handPage.hideLoading()
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })
    },

    handleBack () {
      this.$refs.handPage.showLoading()
      this.rpc.call('repair_manage.task_page', 'reject', [
        this.checkes1.map(item => item.id)
      ], {}).then(data => {
        console.log('reject...', data)
        this.$refs.receivingList && this.$refs.receivingList.refresh()
        this.$refs.handPage.hideLoading()
        this.$createToast({
          txt: '退回成功',
          type: 'correct'
        }).show()
      }).catch(e => {
        this.$refs.handPage.hideLoading()
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })
    }
  },
  beforeRouteUpdate (to, from, next) {
    console.log('....', to)
    if (to.name === 'handover') {
      console.log(this.$refs)
      this.$refs.receivingList && this.$refs.receivingList.refresh()
      this.$refs.workingList && this.$refs.workingList.refresh()
    }
    next()
  }
}
</script>

<style lang="scss">
.handover-tabs{
  // height: 40px;
  font-size: 16px;

  .md-tab-bar{
    height: 40px;
    font-size: 16px;

    .ink-bar{
      height: 2px;
    }

    &::before{
      height: 0;
    }
  }

  .md-tab-content-wrapper{
    display: none !important;
  }
}
.detail-action{
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50px;
  z-index: 100;

  .cube-btn{
    border-radius: 0;
  }
}
.tab-detail{
  position: absolute;
  top: 40px;
  bottom: 0;
  left: 0;
  right: 0;

  .tab-list{
    height: calc(100vh - 90px);
  }
}
</style>
