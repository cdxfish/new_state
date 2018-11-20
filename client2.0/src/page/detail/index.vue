<template>
  <page style="z-index: 199;" ref="detailPage">
    <div class="detail-wrapper">
      <cube-scroll

        ref="scroll"
        :options="{
          scrollbar: true,

        }"
        id="detail-content"
      >
      <!-- <div class="detail-wrapper"> -->
        <div>
          <md-notice-bar :closable="false" class="notice-bar" icon="">请在截止时间前接收并完成维修任务！</md-notice-bar>

          <div class="cell-group">
            <mt-cell >
              <span slot="title">已耗时：<span style="color: #debd42;">{{parseInt(detailData.ellapse/60)}}h {{detailData.ellapse%60}}min</span></span>
              <span>{{detailData.no}}h</span>
            </mt-cell>
            <mt-cell >
              <span slot="title">通报时间：{{detailData.notice_tm ? detailData.notice_tm.substr(0,16) : ''}}</span>
              <span>截止时间：{{detailData.end_tm ? detailData.end_tm.substr(0,16) : ''}}</span>
            </mt-cell>
          </div>

          <div class="cell-group no-title">

            <mt-cell title="签到站点：">
              <span>{{detailData.asign_address}}</span>
            </mt-cell>
          </div>

          <div class="cell-group no-title">

            <mt-cell title="故障类型：">
              <span>{{detailData.fault_name}}</span>
            </mt-cell>
            <mt-cell title="故障等级：">
              <span>{{detailData.fault_grade}}</span>
            </mt-cell>
          </div>

          <div class="cell-group">
            <div class="group-title">故障现象</div>

            <div class="detail-text">
              {{detailData.detail}}
            </div>
          </div>

          <div class="cell-group no-title" v-if="detailData.fault_lines && detailData.fault_lines.length > 0">
            <div class="group-title">故障设备</div>

            <mt-cell :title="item.metro_lines + ' ' + item.metro_addresse" v-for="item in detailData.devs" :key="item.id">
              <span>{{item.name}}</span>
            </mt-cell>
          </div>

          <div class="cell-group no-title">

            <mt-cell title="设备专业：">
              <span>{{detailData.equipment_class}}</span>
            </mt-cell>
          </div>

          <div class="cell-group no-title">

            <mt-cell title="线别：">
              <span>{{detailData.line}}</span>
            </mt-cell>
            <mt-cell title="车站">
              <span>{{detailData.ports}}</span>
            </mt-cell>
          </div>

          <md-tabs
            :titles="['维修记录', '维修进度']"
            :ink-bar-length="100"
            class="detail-tabs"
          >
            <div>
              <repair-record :items="repairRecords" :imgs="imgs" @on-viewer="showViewer" @on-video="showVideoViewer"></repair-record>
            </div>
            <div>
              <repair-progress :items="repairRecords"></repair-progress>
            </div>
          </md-tabs>


          <div style="height:60px;"></div>
        </div>
      <!-- </div> -->
      </cube-scroll>
    </div>

    <flexbox :gutter="0" class="detail-action" v-if="detail.id && $route.params.type != '5' && (detail.is_my_task || (detail.monitor && $route.params.type=='all')) && detail.status != 'suspended' && detail.status != 'finish' && detail.status != 'repair_audit'">
      <template v-if="$route.params.type=='all' && !detail.finished">
        <flexbox-item>
          <cube-button light @click="handleTranspond">转发</cube-button>
        </flexbox-item>

        <flexbox-item>
          <cube-button primary @click="handGuaqi">工单挂起</cube-button>
        </flexbox-item>
      </template>
      <template v-if="$route.params.type!='all' && !detail.finished">
        <flexbox-item v-if="detail.status == 'accept' || detail.status == 'asign' || detail.status == 'repair' || detail.status == 'exchange_out' || detail.status == 'turn'">
          <cube-button light @click="handleTranspond">转发</cube-button>
        </flexbox-item>
        <flexbox-item v-if="detail.status=='repair'">
          <cube-button @click="handleOutput" style="background: #e64340; border-color: #e64340;">销项</cube-button>
        </flexbox-item>
        <flexbox-item v-if="detail.status == 'exchange_out' || detail.status == 'turn'" >
          <cube-button @click="handleBack" style="background: #e64340; border-color: #e64340;">退回</cube-button>
        </flexbox-item>
        <flexbox-item v-if="detail.status=='repair'">
          <cube-button primary @click="handleRepair">维修</cube-button>
        </flexbox-item>
        <flexbox-item v-if="detail.status=='accept'">
          <cube-button primary @click="handleReport">接报</cube-button>
        </flexbox-item>
        <flexbox-item v-if="detail.status == 'exchange_out' || detail.status == 'turn'">
          <cube-button primary @click="handleJieshou">接报</cube-button>
        </flexbox-item>
        <flexbox-item v-if="detail.status=='asign'">
          <cube-button primary @click="handleSign">维修签到</cube-button>
        </flexbox-item>
      </template>

    </flexbox>

    <page-view ></page-view>

    <md-image-viewer
      v-model="isViewerShow"
      :list="imgs"
      :has-dots="true"
      :initial-index="viewerIndex">
    </md-image-viewer>

    <image-viewer ref="imageViewer" :imgs="imgs.map(item => ({
        src: item.url
      }))"></image-viewer>

    <video-viewer ref="videoViewer" v-model="videoVisible" :src="videoSrc" :pic="videoPic"></video-viewer>

    <cube-toast txt="接报成功" v-model="reportSuccessed" type="correct" :time="500"></cube-toast>

    <cube-toast txt="转发成功" v-model="transpondSuccessed" type="correct" :time="500"></cube-toast>
  </page>
</template>

<script>
import Page from '../../components/Page'
import PageView from '../../components/View'
import { Flexbox, FlexboxItem } from 'vux/src/components/flexbox'
import RepairRecord from './repairRecord'
import RepairProgress from './repairProgress'
// import config from '../../util/config.js'
import ImageViewer from '../../components/ImageViewer'
import VideoViewer from '../../components/VideoViewer'

export default {
  components: {
    Page,
    Flexbox,
    FlexboxItem,
    PageView,
    RepairRecord,
    RepairProgress,
    ImageViewer,
    VideoViewer
  },
  data () {
    return {
      loadingToast: this.$createToast({
        txt: '',
        time: 0,
        mask: true
      }),
      imgs: [],
      isViewerShow: false,
      viewerIndex: 0,
      reportSuccessed: false,
      transpondSuccessed: false,
      detail: {},
      detailData: {},
      repairRecords: [],
      videoVisible: false,
      videoSrc: '',
      videoPic: ''
    }
  },
  mounted () {
    this.loadData(this.$route.params.id)

    console.log(this.$route)
  },
  methods: {
    handleRepair () {
      this.$router.push({name: 'repair', params: {repairId: 1}})
    },
    handGuaqi () {
      this.$router.push({name: 'guaqi'})
    },
    handleOutput () {
      this.$router.push({name: 'output'})
    },
    handleBack () {
      this.$createDialog({
        type: 'confirm',
        icon: 'cubeic-alert',
        content: '确认退回该工单吗？',
        confirmBtn: {
          text: '确定退回',
          active: true,
          disabled: false,
          href: 'javascript:;'
        },
        cancelBtn: {
          text: '取消',
          active: false,
          disabled: false,
          href: 'javascript:;'
        },
        onConfirm: () => {
          this.$refs.detailPage.showLoading()
          this.rpc.call('repair_manage.task_page', 'reject_single_task', [
            this.$route.params.id
          ], {}).then(data => {
            this.$refs.detailPage.hideLoading()
            if (data) {
              // window.sessionStorage.setItem('cur_detail_id', data)
              // this.$router.replace({name: this.$route.name, params: {id: data}})
              this.$router.back()
            } else {
              this.$router.back()
            }
          }).catch(e => {
            this.$refs.detailPage.hideLoading()
            this.$createToast({
              txt: e.message,
              type: 'error',
              time: 2000
            }).show()
          })
        }
      }).show()
    },
    loadData (id) {
      if (id === 0) return
      // this.loadingToast.show()
      this.$refs.detailPage.showLoading()

      // this.rpc()
      this.rpc.call('repair_manage.task_page', 'get_task', [id], {}).then(data => {
        console.log('repiar_detail', data)
        // this.loadingToast.hide()
        this.$refs.detailPage.hideLoading()
        this.detail = data
        this.detailData = data.data

        console.log('...query', this.$route.query)
        // if (/*this.detail.finished &&*/ this.$route.query.message) {

        // }
        if (this.$route.query.message && this.detail.finished) {
          this.$createDialog({
            type: 'alert',
            title: '消息已处理',
            icon: 'cubeic-alert',
            confirmBtn: {
              text: '我知道了',
              active: true
            }
          }).show()
        }
      }).catch(e => {
        // this.loadingToast.hide()
        this.$refs.detailPage.hideLoading()
        this.$createToast({
          txt: e.message,
          type: 'error',
          time: 2000
        }).show()
      })

      this.rpc.call('repair_manage.task_page', 'get_repair_his', [id], {}).then(data => {
        console.log('record ', data)
        this.repairRecords = data
      }).catch(e => {
        this.$createToast({
          txt: e.message,
          type: 'error',
          time: 2000
        }).show()
      })
    },
    showViewer (imgs, index) {
      this.imgs = imgs
      this.viewerIndex = index
      // this.isViewerShow = true
      this.$nextTick(() => {
        this.$refs.imageViewer.show(index)
      })
    },
    showVideoViewer (video) {
      this.videoSrc = video
      this.videoPic = video + '?vframe/png/offset/0'

      this.videoVisible = true
    },
    handleTranspond () {
      // todo:  调用钉钉api
      // this.rpc.getDingTalkConfig(config.url).then(data => {
      //   console.log('config data', data)

      //   const _this = this

      //   window.dd.biz.contact.complexPicker({
      //     title: '转发',
      //     corpId: data.corp_id,
      //     multiple: false,
      //     maxUsers: 1000,
      //     pickedUsers: [],
      //     pickedDepartments: [],
      //     disabledUsers: [],
      //     disabledDepartments: [],
      //     requiredUsers: [],
      //     requiredDepartments: [],
      //     appId: config.agentId,
      //     permissionType: 'GLOBAL',
      //     responseUserOnly: false,
      //     startWithDepartmentId: 0,
      //     onSuccess: function (result) {
      //       console.log('---', result)
      //       _this.loadingToast.show()

      //       setTimeout(() => {
      //         _this.loadingToast.hide()
      //         _this.transpondSuccessed = true
      //       }, 1000)
      //     },
      //     onFail: function (err) {
      //       console.log('err', err)
      //     }
      //   })
      // })

      this.$router.push({name: 'transpond', params: {transId: this.detail.id}})
    },
    handleReport () {
      this.loadingToast.show()

      this.rpc.call('repair_manage.task_page', 'accept', [this.detail.id], {}).then(data => {
        this.loadingToast.hide()
        this.reportSuccessed = true
        console.log('repair callback', data)
        if (data) {
          this.$router.replace({name: this.$route.name, params: {id: data}})
          // setTimeout(() => {
          //   this.$router.replace({name: this.$route.name, params: {id: data}})
          // }, 200)
        } else {
          this.$router.back()
        }
      }).catch(e => {
        this.loadingToast.hide()
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })
    },
    handleJieshou () {
      this.$refs.detailPage.showLoading()
      this.rpc.call('repair_manage.task_page', 'accept_single_exchanging_task', [this.detail.id], {}).then(data => {
        this.$refs.detailPage.hideLoading()
        this.$createToast({
          txt: '接收成功',
          type: 'correct'
        }).show()
        if (data) {
          this.$router.replace({name: this.$route.name, params: {id: 0}})
          this.$router.replace({name: this.$route.name, params: {id: data}})
        } else {
          this.$router.back()
        }
      }).catch(e => {
        this.$refs.detailPage.hideLoading()
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })
    },
    handleSign () {
      if (this.detailData.fault_lines && this.detailData.fault_lines.length) {
        this.$createActionSheet({
          title: '选择签到方式',
          data: [
            {
              content: '设备二维码签到'
            },
            {
              content: '位置签到'
            }
          ],
          onSelect: (item, index) => {
            if (index) {
              this.$router.push({name: 'map-sign'})
            } else {
              this.$router.push({name: 'device-sign'})
            }
          }
        }).show()
      } else {
        this.$router.push({name: 'map-sign'})
      }

      // this.$router.push({name: 'map-sign'})
    }
  },
  beforeRouteUpdate (to, from, next) {
    console.log('....', to)
    if (to.name === 'task-detail') {
      let curDetailId = window.sessionStorage.getItem('cur_detail_id')
      if (curDetailId) {
        window.sessionStorage.removeItem('cur_detail_id')
        this.$router.replace({name: 'task-detail', params: {id: 0}})
        this.$router.replace({name: 'task-detail', params: {id: curDetailId}})
        this.loadData(curDetailId)
      } else {
        this.loadData(to.params.id)
      }
    }

    next()
  }
}
</script>

<style lang="scss">
.detail-wrapper{
  height: calc(100vh);

  .notice-bar{
    height: 25px;
    line-height: 25px;
    font-size: 12px;
    padding-left: 0;
    text-align: center;

    .md-icon.md{
      width: 10px;
      height: 10px;
      left: 10px;
    }
  }
}

.detail-text{
  background: #fff;
  padding: 10px 15px;
  font-size: 12px;
  line-height: 20px;
  color: rgb(127, 127, 127);
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
.detail-tabs{
  // height: 40px;
  margin-top: 16px;
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
}
</style>
