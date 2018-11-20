<template>
  <page >
    <div style="height:100vh;">
      <cube-scroll
        ref="scroll"
        :options="scrollOptions"
        @pulling-down="onPullingDown"
      >
          <div class="home-page">
            <div class="cell-group">
              <div class="home-header">
                <div class="avator">
                  <img :src="homeData.avatar">
                </div>
                <div class="text">欢迎您！{{homeData.worker_name}}</div>
                <div class="desc">
                  {{state == 'working' ? '在班' : '未在班'}}
                </div>
                <cube-button inline class="btn" primary @click="handleSign">
                  {{state=='working' ? '签退' : '签到'}}
                </cube-button>
              </div>
            </div>

            <div class="cell-group">
              <div class="group-title">故障维修</div>

              <div class="chart-warpper" id="chart"></div>
            </div>
            <div class="cell-group">
              <div class="group-title">故障提报</div>

              <mt-cell title="故障提报" is-link @click.native="handleToFault">
                <img slot="icon" src="../../assets/Rectangle 6.png" width="24" height="24">
              </mt-cell>
              <mt-cell title="我的提报" is-link @click.native="toMyfault('my')">
                 <span>{{homeData.reporting_count ? homeData.reporting_count : 0}}条</span>
                <!-- <span>24条</span> -->
                <img slot="icon" src="../../assets/Rectangle 6 Copy 7@2x.png" width="24" height="24">
              </mt-cell>
              <!-- <mt-cell title="全部提报" is-link @click.native="toMyfault('all')">
                 <span>{{homeData.reporting_all_count ? homeData.reporting_all_count : 0}}条</span>
                <img slot="icon" src="../../assets/Rectangle 6 Copy 12@2x.png" width="24" height="24">
              </mt-cell> -->
            </div>

            <div class="cell-group">
              <div class="group-title">任务管理</div>
               <mt-cell title="我的待办" is-link @click.native="handleList1">
                <span>{{homeData.cur_task_count ? homeData.cur_task_count : 0}}条</span>
                <img slot="icon" src="../../assets/Group16@3x.png" width="24" height="24">
              </mt-cell>

              <mt-cell title="重点故障" is-link @click.native="handleList2">
                <span>{{homeData.key_fault_count ? homeData.key_fault_count : 0}}条</span>
                <img slot="icon" src="../../assets/Group 13@3x.png" width="24" height="24">
              </mt-cell>

              <mt-cell title="未兑现任务" is-link @click.native="handleList3">
                <span>{{homeData.expired_task_count ? homeData.expired_task_count : 0}}条</span>
                <img slot="icon" src="../../assets/Group 12@3x.png" width="24" height="24">
              </mt-cell>

              <mt-cell title="任务挂起" is-link @click.native="handleList4">
                <span>{{homeData.suspend_task_count ? homeData.suspend_task_count : 0}}条</span>
                <img slot="icon" src="../../assets/Group 11@3x.png" width="24" height="24">
              </mt-cell>

              <mt-cell title="委外工单" is-link @click.native="handleList6">
                <img slot="icon" src="../../assets/Rectangle 6@3x.png" width="24" height="24">
              </mt-cell>

              <mt-cell title="任务交接" is-link @click.native="toHandover">
                <img slot="icon" src="../../assets/Group 10@3x.png" width="24" height="24">
              </mt-cell>

            </div>

            <div class="cell-group">
              <div class="group-title">维修计划</div>

              <mt-cell title="我的待办" is-link @click.native="handleToPlan">
                <img slot="icon" src="../../assets/Group 6@3x.png" width="24" height="24">
              </mt-cell>
            </div>

            <div class="cell-group" v-if="showManage">
              <div class="group-title">工单管理</div>

              <mt-cell title="工单看板" is-link @click.native="handleToTaskAll">
                <img slot="icon" src="../../assets/Rectangle 6 Copy 8@3x.png" width="24" height="24">
              </mt-cell>

              <mt-cell title="在班管理" is-link @click.native="handleToWork">
                <img slot="icon" src="../../assets/在班.jpg" width="24" height="24">
              </mt-cell>
            </div>

            <div class="cell-group">
              <div class="group-title">设备履历</div>

              <mt-cell title="设备查找" is-link @click.native="handleDevice">
                <img slot="icon" src="../../assets/Rectangle 6 Copy 9@2x.png" width="24" height="24">
              </mt-cell>

              <mt-cell title="扫码查看" is-link @click.native="handleDeviceScan">
                <img slot="icon" src="../../assets/Rectangle 6 Copy 10@2x.png" width="24" height="24">
              </mt-cell>
            </div>

            <div class="cell-group">
              <div class="group-title">分析统计</div>

              <mt-cell title="分析统计" is-link @click.native="handleToStatistics">
                <img slot="icon" src="../../assets/Group 5@3x.png" width="24" height="24">
              </mt-cell>
            </div>

            <!-- <div class="cell-group">
              <div class="group-title"></div>
              <mt-field label="用户名" placeholder="请输入用户名" ></mt-field>
              <mt-field label="自我介绍" placeholder="自我介绍" type="textarea" rows="4"></mt-field>
              <cube-input  ></cube-input>
            </div> -->
          </div>
      </cube-scroll>
    </div>

    <page-view></page-view>
  </page>
</template>

<script>
import Page from '../../components/Page'
import PageView from '../../components/View'
import { mapGetters, mapActions } from 'vuex'

const echarts = require('echarts')

export default {
  components: {
    Page,
    PageView
  },
  data () {
    return {
      reporting_count: '',
      scrollOptions: {
        scrollbar: true,
        pullDownRefresh: {
          txt: ' '
        }
      },
      items: [],
      myChart: null,
      state: 'rest',
      loadingToast: this.$createToast({
        txt: '',
        time: 0,
        mask: true
      }),
      homeData: {},
      showManage: false
    }
  },
  computed: {
    ...mapGetters(['uf'])
  },
  mounted () {
    this.myChart = echarts.init(document.getElementById('chart'))
    // this.rpc.call('funenc_flowable.funenc_flowable_history', 'queryHistoryActivities', []).then(data => {
    //   console.log('the data is:', data)
    // })
    this.loadRefresh()
  },
  methods: {
    ...mapActions(['changeuf']),
    loadRefresh () {
      this.loadingToast.show()
      this.rpc.call('repair_manage.sign_api', 'get_sign_in_state', []).then(data => {
        console.log('get_sign_in_state', data)
        this.state = data.state
        this.loadingToast.hide()
      }).catch(e => {
        console.log('err', e)
        this.loadingToast.hide()
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })

      this.rpc.call('repair_manage.index_page', 'get_index_page_info', [], {}).then(data => {
        console.log('home page', data)
        this.homeData = data
        this.changeuf(data)
        this.showManage = data.show_kan_ban
        this.loadChart()
      })
    },
    handleSign () {
      this.$router.push({name: 'sign'})
    },
    handleNextPage () {
      this.$router.push({name: 'test'})
    },
    toHandover () {
      this.$router.push({name: 'handover'})
    },
    handleToStatistics () {
      this.$router.push({name: 'statistics'})
    },
    handleToWork () {
      this.$router.push({name: 'work'})
    },
    handleDevice () {
      this.$router.push({name: 'device'})
    },
    handleToPlan () {
      this.$router.push({name: 'plan'})
    },
    handleToFault () {
      this.$router.push({name: 'fault'})
    },
    toMyfault (type) {
      this.$router.push({
        name: 'myFault',
        params: {
          type: type
        }
      })
    },

    handleToTaskAll () {
      this.$router.push({name: 'task', params: {type: 'all'}})
    },
    handleList1 () {
      this.$router.push({name: 'task', params: {type: '1'}})
    },
    handleList2 () {
      this.$router.push({name: 'task', params: {type: '2'}})
    },
    handleList3 () {
      this.$router.push({name: 'task', params: {type: '3'}})
    },
    handleList4 () {
      this.$router.push({name: 'task', params: {type: '4'}})
    },
    handleList6 () {
      this.$router.push({name: 'task', params: {type: '6'}})
    },
    onPullingDown () {
      // 模拟更新数据
      setTimeout(() => {
        this.$refs.scroll.forceUpdate()
      }, 1000)
    },
    loadChart () {
      this.myChart.setOption({
        color: ['#39c7c8', '#c9b4f2', '#5eb2ed', '#faba84'],
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          x: 'left',
          // show: false,
          data: ['待接报', '待签到', '维修中', '已完成']
        },
        series: [
          {
            name: '故障状态',
            type: 'pie',
            radius: ['50%', '80%'],
            avoidLabelOverlap: false,
            label: {
              normal: {
                show: false,
                position: 'center'
              },
              emphasis: {
                show: true,
                textStyle: {
                  fontSize: '14',
                  fontWeight: 'bold'
                }
              }
            },
            labelLine: {
              normal: {
                show: false
              }
            },
            data: [
              {value: this.homeData.accept_count ? this.homeData.accept_count : 0, name: '待接报'},
              {value: this.homeData.sign_count ? this.homeData.sign_count : 0, name: '待签到'},
              {value: this.homeData.repair_count ? this.homeData.repair_count : 0, name: '维修中'},
              {value: this.homeData.finish_count ? this.homeData.finish_count : 0, name: '已完成'}
            ]
          }
        ]
      })
    },
    handleDeviceScan () {
      const _this = this
      window.dd.biz.util.scan({
        type: 'qrCode',
        tips: '设备扫码',
        onSuccess (data) {
          console.log('data', data, this)
          _this.$router.push({name: 'device-detail', params: {deviceId: data.text}})
        },
        onFail (err) {
          console.log('err', err)
        }
      })
    }
  },
  beforeRouteUpdate (to, from, next) {
    console.log('....', to)
    if (to.name === 'home') {
      this.loadRefresh()
    }

    next()
  }
}
</script>

<style lang="scss">
.home-page {
  padding: 16px 0;
}

.chart-warpper {
  background: #fff;
  padding: 10px 15px;
  height: 160px;
}

.home-header {
  height: 46px;
  padding: 10px 15px;
  position: relative;
  background: #fff;

  .text {
    padding-left: 60px;
    font-size: 16px;
    line-height: 30px;
  }

  .desc {
    padding-left: 60px;
    font-size: 12px;
    line-height: 16px;
    color: rgb(127, 127, 127);
  }

  .avator {
    height: 46px;
    width: 46px;
    background: #ccc;
    position: absolute;
    left: 15px;
    top: 10px;
    border-radius: 50%;
    overflow: hidden;

    img{
      width: 100%;
      height: 100%;
    }
  }

  .btn {
    position: absolute !important;
    width: 80px;
    right: 15px;
    top: 20px;
  }
}
</style>
