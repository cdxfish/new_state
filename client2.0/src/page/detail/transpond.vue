<template>
  <page style="z-index: 300;">
    <div class="transpond-wrp">
      <mt-search
        v-model="query"

        cancel-text="取消"
        placeholder="搜索">
      </mt-search>

      <cube-tab-bar v-model="selectedLabel" showSlider class="tab-bar-wrp">
        <cube-tab v-for="(item) in tabs" :label="item.label" :key="item.label"></cube-tab>
      </cube-tab-bar>
      <cube-tab-panels class="result-wrapper" v-model="selectedLabel" >
        <cube-tab-panel  v-for="(item) in tabs" :label="item.label" :key="item.label">
          <cube-scroll
            class="result-detail"
            v-if="item.label == '本工班'"
            ref="scroll"
            :options="{
              scrollbar: true
            }"
            :data="options"
          >
            <div v-if="!refreshLoading" class="cell-group detail">
              <cube-radio-group v-model="selected" :options="options" :hollow-style="true" />
            </div>
            <div v-else class="refresh-loading">
              <cube-loading></cube-loading>
            </div>
          </cube-scroll>

          <cube-scroll
            class="result-detail"
            v-if="item.label == '委外工班' || item.label == '内部工班'"
            ref="scroll"
            :options="{
              scrollbar: true
            }"
          >
            <div v-if="!refreshLoading2" class="cell-group detail">
              <cube-radio-group v-if="tabs[1].label === '内部工班'" v-model="selected" :options="outerOptions" :hollow-style="true" />
              <group v-if="tabs[1].label === '委外工班'">
                <template v-for="(option, index) in outerOptions"
                  >
                  <cell
                  :title="option.name"
                  is-link
                  :key="index"
                  :border-intent="false"
                  :arrow-direction="showContent001 ? 'up' : 'down'"
                  @click.native="showContent001 = !showContent001"></cell>

                  <template v-if="showContent001" >
                    <cube-radio-group  v-model="selected" :options="option.children" :hollow-style="true" />
                  </template>
                </template>


              </group>
            </div>
            <div v-else class="refresh-loading">
              <cube-loading></cube-loading>
            </div>
          </cube-scroll>
        </cube-tab-panel>
      </cube-tab-panels>

      <flexbox :gutter="0" class="detail-action" >
        <flexbox-item>
          <cube-button primary :disabled="!selected" @click="handleConfirm">确定</cube-button>
        </flexbox-item>
      </flexbox>
    </div>


  </page>
</template>

<script>
import Page from '../../components/Page'
import { Flexbox, FlexboxItem } from 'vux/src/components/flexbox'
import Group from 'vux/src/components/group/index.vue'
import Cell from 'vux/src/components/cell/index.vue'

export default {
  components: {
    Page,
    Flexbox,
    FlexboxItem,
    Group,
    Cell
  },
  data () {
    return {
      query: '',
      refreshLoading: false,
      refreshLoading2: false,
      selected: '',
      options: [],
      loadingToast: this.$createToast({
        txt: '',
        time: 0,
        mask: true
      }),
      selectedLabel: '本工班',
      tabs: [{
        label: '本工班'
      }, {
        label: '委外工班'
      }],
      outerOptions: [],
      showContent001: false
    }
  },
  mounted () {
    this.loadData()
  },
  methods: {
    handleDetail () {
      this.$router.push({name: 'device-detail'})
    },
    loadList () {
      this.refreshLoading = true
      this.refreshLoading2 = true

      this.rpc.call('repair_manage.transmit_page', 'get_transmit_target', [
        this.query
      ], {}).then(data => {
        console.log('transmit_targt', data)
        this.refreshLoading = false
        // alert(JSON.stringify(data))
        this.options = data.employees.map(item => ({
          value: item.id,
          label: item.name + '  ' + (item.work_state === 'rest' ? '（未在班）' : '（在班）')
        }))
      }).catch(e => {
        this.refreshLoading = false
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })

      this.$route.params.id && this.rpc.call('repair_manage.task_page', 'get_output_workers', [
        this.$route.params.id,
        this.query
      ], {}).then(data => {
        console.log('output_ws', data)
        this.refreshLoading2 = false
        // this.outerOptions = []
        this.outerOptions = []

        if (this.tabs[1].label === '委外工班') {
          Object.keys(data).forEach(i => {
            this.outerOptions.push({
              name: i,
              children: data[i].map(item => ({
                value: item.id,
                label: item.name + '  ' + (item.work_state === 'rest' ? '（未在班）' : '（在班）')
              }))
            })
          })
        } else {
          this.outerOptions = data.map(item => ({
            value: item.id,
            label: item.name + '  ' + (item.work_state === 'rest' ? '（未在班）' : '（在班）')
          }))
        }
        console.log('.....', this.outerOptions)

        // this.outerOptions = data.map(item => ({
        //   value: item.id,
        //   label: item.name + '  ' + (item.work_state === 'rest' ? '（未在班）' : '（在班）')
        // }))
      }).catch(e => {
        this.refreshLoading2 = false
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })
    },
    loadData () {
      if (!this.$route.params.id) {
        this.tabs.splice(1, 1)
        this.loadList()
      } else {
        this.rpc.call('repair_manage.user_api', 'get_working_class', [], {}).then(data => {
          console.log('...status', data)
          if (data.type === 'inside') {
            this.$set(this.tabs[1], 'label', '委外工班')
          } else {
            this.$set(this.tabs[1], 'label', '内部工班')
          }

          this.$nextTick(() => {
            this.loadList()
          })
        })
      }
    },
    handleConfirm () {
      this.loadingToast.show()

      if (this.$route.params.tasks) {
        console.log('task ids', this.$route.params.tasks, this.selected)
        this.rpc.call('repair_manage.task_page', 'turn_out_tasks', [
          this.$route.params.tasks.split(','),
          this.selected
        ], {}).then(data => {
          this.loadingToast.hide()
          this.$createToast({
            txt: '转发成功',
            type: 'correct'
          }).show()
          this.$router.back()
        }).catch(e => {
          this.loadingToast.hide()
          this.$createToast({
            txt: e.message,
            type: 'error'
          }).show()
        })
      } else {
        this.rpc.call('repair_manage.task_page', 'exchange', [this.$route.params.transId, this.selected], {}).then(data => {
          this.loadingToast.hide()
          window.sessionStorage.setItem('cur_detail_id', data)
          this.$createToast({
            txt: '转发成功',
            type: 'correct'
          }).show()
          this.$router.back()
        }).catch(e => {
          this.loadingToast.hide()
          this.$createToast({
            txt: e.message,
            type: 'error'
          }).show()
        })
      }
      // this.$router.back()
    }
  },
  watch: {
    query (val) {
      this.loadData()
    },
    selectedLabel (newV) {
      console.log(newV)
    }
  }
}
</script>

<style lang="scss">
.tab-bar-wrp{
  position: absolute;
  top: 55px;
  left: 0;
  right: 0;
  background: #fff;
  height: 40px;
}

.cube-tab_active{
  color: #1C81D2 !important;
}

.cube-tab-bar-slider{
  background-color: #1C81D2 !important;
}

.transpond-wrp{
  .mint-search{
    font-size: 12px;
    height: 50px;
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    z-index: 10001;

    .mint-searchbar-core{
      line-height: 28px;
    }

    .mint-search-list{
      display: none;
    }
  }

  .md-radio .md-field .md-field-item{
    padding: 14px 20px;
    font-size: 12px;

    .md-radio-content{
      font-size: 12px;
    }

    .md-icon.sm{
      width: 12px;
      height: 12px;
    }
  }

  .md-drop-menu .md-drop-menu-list{
    padding-top: 40px;
  }

  .md-popup.with-mask{
    top: 50px;
  }

  .md-drop-menu .md-drop-menu-bar .bar-item span:after{
    border-width: 6px;
    top: 55%;
  }

  .result-wrapper{
    height: calc(100vh - 150px);
    // margin-top: 2px;
    position: absolute;
    top: 100px;
    left: 0;
    width: 100%;
    bottom: 50px;

    .detail{
      padding: 10px 0;
    }
  }

  .result-detail{
    height: calc(100vh - 150px);
    overflow: hidden;
  }

  .refresh-loading{
    margin-top: 16px;
    text-align: center;

    .cube-loading{
      display: inline-block;
    }
  }

  .vux-label{
    font-size: 14px;
  }
}
</style>
