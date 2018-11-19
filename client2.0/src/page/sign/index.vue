<template>
  <page :title="pageTitle" style="z-index: 200;">
    <div style="height:100vh;">
      <cube-scroll>
        <div class="sign-page">
          <div class="cell-group">

            <mt-cell title="时间：" >
              <span>{{workTime}}</span>
            </mt-cell>

            <mt-cell title="当前工班：" >
              <span>{{workName}}</span>
            </mt-cell>
          </div>

          <div class="cell-group" v-if="state=='working'">
            <div class="group-title">目前在班情况</div>

            <mt-cell :title="item.name" v-for="item in currentWorks" :key="item.id">
              <span style="margin: 0 15px;color: rgb(28, 129, 210);">
                {{item.sign_info.work_state == 'repair' ? '维修' : '值班'}}
              </span>
              <span>{{item.sign_info.sign_in_data}}</span>
              <img slot="icon" src="" width="24" height="24">
            </mt-cell>
          </div>

          <div class="cell-group">
            <div class="group-title">签到记录</div>

            <div class="steps-record">
              <steps direction="vertical" :active="1">
                <template v-if="state=='working'">
                  <step>
                    <span slot="title">在班签到</span>
                    <span slot="icon">
                    </span>
                    <span slot="description">
                      {{signInfo.sign_in_data}}
                      <span style="margin-left: 5px; color: #1C81D2;">{{signInfo.work_state == 'repair' ? '维修' : '值班'}}</span>
                    </span>
                  </step>
                  <step>
                    <span slot="title">下班签退</span>
                    <span slot="icon">
                    </span>
                  </step>
                </template>
                <template v-else>
                  <step>
                    <span slot="title">在班签到</span>
                    <span slot="icon">
                    </span>
                    <span slot="description">未签到</span>
                  </step>
                </template>
              </steps>
            </div>
          </div>

          <div class="cell-group" v-if="state=='rest'">
            <div class="group-title"></div>

            <div>

              <cube-radio-group v-model="selected2" :options="[{value: 'repair', label: '维修'}, {value: 'keep_watch', label: '值班'}]" position="left" :hollow-style="true" />
            </div>

          </div>
        </div>
      </cube-scroll>
    </div>


    <div class="sign-action" v-if="state=='rest' && !$route.params.worker">
      <div class="time">
        {{nowTime}}
      </div>

      <cube-button :primary="true" @click="handleSignIn" >确认签到</cube-button>
    </div>
    <div class="sign-action" v-if="state=='working'">
      <div class="time">
        {{nowTime}}
      </div>
      <cube-button :primary="true" @click="handleSignOut" >签退</cube-button>
    </div>

    <page-view></page-view>
  </page>
</template>

<script>
import Page from '../../components/Page'
import PageView from '../../components/View'
import moment from 'moment'
import Steps from 'element-ui/packages/steps'
import Step from 'element-ui/packages/step'
import 'element-ui/lib/theme-chalk/step.css'
import 'element-ui/lib/theme-chalk/steps.css'

export default {
  components: {
    Page,
    Steps,
    Step,
    PageView
  },
  data () {
    return {
      nowTime: '',
      selected2: 'repair',
      signInfo: {},
      state: 'rest',
      workTime: '',
      workName: '',
      currentWorks: [],
      loadingToast: this.$createToast({
        txt: '',
        time: 0,
        mask: true
      }),
      current: {}
    }
  },
  computed: {
    pageTitle () {
      return this.state === 'rest' ? '签到' : '签退'
    }
  },
  created () {
    this.loadingToast.show()
    this.rpc.call('repair_manage.sign_page', 'get_page_info', [
      this.$route.params.worker ? this.$route.params.worker : ''
    ], {}).then(data => {
      console.log('get_sign_in_state', data)
      this.state = data.sign_in_state.state
      this.signInfo = data.sign_in_state.sign_info
      this.workTime = data.date
      this.workName = data.user_info.work_class.name
      this.currentWorks = data.working_class.result
      this.current = data.user_info
      this.loadingToast.hide()
    }).catch(e => {
      console.log('err', e)
      this.loadingToast.hide()
      this.$createToast({
        txt: e.message,
        type: 'error'
      }).show()
    })
  },
  mounted () {
    this.getNowTime()
    setInterval(() => {
      this.getNowTime()
    }, 1000)
  },
  methods: {
    getNowTime () {
      this.nowTime = moment().format('HH:mm:ss')
    },

    handleSignIn () {
      const toast = this.$createToast({
        mask: true
      })

      toast.show()
      this.rpc.call('repair_manage.sign_api', 'sign_in', [
        this.selected2,
        this.$route.params.worker ? this.$route.params.worker : ''
      ], {}).then(data => {
        if (data.result) {
          this.$createToast({
            txt: '签到成功',
            type: 'correct',
            time: 1000
          }).show()
          this.$router.back()
        } else {
          this.$createToast({
            txt: data.msg,
            type: 'error'
          }).show()
        }
      })
    },

    handleSignOut () {
      let ct = this.$route.params.worker ? `记得将 ${this.current.name} 的维修任务进行交接哦~ 否则任务会继续计时` : '记得将你的任务进行交接哦~ 否则任务会继续计时'

      this.$createDialog({
        type: 'confirm',
        icon: 'cubeic-alert',
        content: ct,
        confirmBtn: {
          text: '去交接',
          active: true,
          disabled: false,
          href: 'javascript:;'
        },
        cancelBtn: {
          text: '继续签退',
          active: false,
          disabled: false,
          href: 'javascript:;'
        },
        onConfirm: () => {
          if (this.$route.params.worker) {
            this.$router.push({name: 'work-signhandover'})
          } else {
            this.$router.push({name: 'signhandover'})
          }
        },
        onCancel: () => {
          console.log('on-cancel')
          this.loadingToast.show()
          this.rpc.call('repair_manage.sign_api', 'sign_out', [
            this.$route.params.worker ? this.$route.params.worker : ''
          ], {}).then(data => {
            console.log('sign_out', data)
            this.loadingToast.hide()
            if (data.result) {
              this.$router.back()
            } else {
              this.$createToast({
                txt: data.msg,
                type: 'error'
              }).show()
            }
          })
        }
      }).show()
    }
  }
}
</script>

<style lang="scss">
.sign-page {
  padding: 16px 0 100px;
  overflow: auto;
}
.initHeight {
  height: 180px;
}
.steps-record {
  background: #fff;
  padding: 10px 15px;
}
.sign-action {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 10;

  button {
    border-radius: 0;
  }

  .time {
    height: 24px;
    line-height: 24px;
    text-align: center;
    font-size: 14px;
    background: #959595;
    color: #fff;
  }
}
</style>
