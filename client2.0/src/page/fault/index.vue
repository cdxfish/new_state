<template>
  <page style="z-index: 200;">
    <div class="fault-page">
      <cube-scroll
          ref="scroll"
          :options="{
            scrollbar: true,
          }"
        >
        <div >
          <div class="cell-group">
            <mt-cell is-link @click.native="handleTag">
              <span slot="title"  >*故障标签</span>
              <span>{{lable.name}}</span>
            </mt-cell>
          </div>
          <div class="cell-group">
            <div class="group-title"></div>
            <mt-cell is-link @click.native="handleSelectType">
              <span slot="title"  >*线别</span>
              <span>{{line.name}}</span>
            </mt-cell>
            <mt-cell is-link @click.native="handleSelectStation">
              <span slot="title"  >*站点（区间）</span>
              <span v-if="ports[0]">已选择{{ports.length}}个</span>
              <span v-else>请选择</span>
            </mt-cell>
          </div>
          <div class="cell-group">
            <div class="group-title">区域</div>
            <mt-field placeholder="区域（选填）" type="textarea" rows="1" v-model="reglon"></mt-field>
          </div>

          <div class="cell-group">
            <div class="group-title"></div>
            <mt-cell is-link @click.native="questionType">
              <span slot="title">*问题分类</span>
              <span>{{prooblem_classify.name}}</span>
            </mt-cell>
            <mt-cell is-link @click.native="handleUrgent">
              <span slot="title"  >*问题紧急程度</span>
              <span>{{urgent.name}}</span>
            </mt-cell>
          </div>
          <div class="cell-group">
            <div class="group-title">*故障现象</div>
            <mt-field placeholder="请填写现象（必填）" type="textarea" rows="4" v-model="failure"></mt-field>
          </div>

          <div class="cell-group">
            <div class="group-title">备注：</div>
            <mt-field placeholder="选填" type="textarea" rows="4" v-model="remark"></mt-field>
          </div>

          <div class="cell-group">
            <div class="group-title">故障设备(选填）：</div>
            <mt-cell is-link @click.native="selsetEquipment">
              <span slot="title"  >选择设备</span>
              <span>已选择{{equement.length}}台</span>
            </mt-cell>
            <!-- <equipment-search v-model="equips" @on-confirm="handleDeviceConfirm"></equipment-search> -->
          </div>

          <div class="cell-group">
            <div class="group-title">照片上传（选填）</div>

            <div class="group-detail">
              <upload v-model="imgs"  v-if="uptoken" :token="uptoken"></upload>
              <!-- <upload v-model="imgs"  :token="uptoken"></upload> -->
            </div>
          </div>
          <div class="cell-group">
            <div class="group-title">视频上传（选填）</div>
            <div class="group-detail">
              <upload v-model="videoes" :type="'video'"  v-if="uptoken" :token="uptoken"></upload>
            </div>
          </div>
        </div>
        <div style="height:90px;"></div>
      </cube-scroll>
    </div>

    <div :gutter="0" class="details-actioen" >
      <cube-button primary @click="handleSubmit" :disabled="failure.trim()==''">提交</cube-button>
    </div>
    <div class="stations_con">
      <md-popup
        v-model="popupVisible"
        position="right"
        prevent-scroll
        transition="slide-left"
      >
        <div style="height:100vh;background: #fff;">
          <cube-scroll
            ref="scroll"
            :options="scrollOptions"
          >
            <mt-checklist
              title="站点列表"
              v-model="ports"
              :options="stations">
            </mt-checklist>
            <!-- <checklist name-position="left" @on-change="change" :options="" v-model="ports" ></checklist> -->
          </cube-scroll>
        </div>
      </md-popup>
    </div>
  <page-view></page-view>
  </page>
</template>
<script>
import Page from '../../components/Page'
import Upload from '../../components/upload'
import PageView from '../../components/View'
import { mapGetters, mapActions } from 'vuex'
import PopupPicker from 'vux/src/components/popup-picker'
import Group from 'vux/src/components/group'
import Checklist from 'vux/src/components/checklist'
import { Flexbox, FlexboxItem } from 'vux/src/components/flexbox'

const questions = [{ id: 'driving', name: '影响行车' }, { id: 'passenger_flow', name: '影响客流' }]
const urgents = [ { id: 'normal', name: '正常处理' }, { id: 'urgent', name: '需加急处理' } ]
const tags = [{ id: '', name: '无' }, { id: 'cm', name: '故障性维修' }, { id: 'pm', name: '预防性维修' }]
export default {
  components: {
    Page,
    Upload,
    PopupPicker,
    Flexbox,
    FlexboxItem,
    PageView,
    Group,
    Checklist
  },
  computed: {
    ...mapGetters(['equement', 'name'])
  },
  data () {
    return {
      stations: [],
      ports: [],
      portsName: [],
      popupShow: true,
      popupVisible: false,
      line: { id: 2, name: '1' },
      lable: { id: '', name: '无' },
      prooblem_classify: { id: 'driving', name: '影响行车' },
      urgent: { id: 'normal', name: '正常处理' },
      reglon: '',
      questionPicker: this.$createPicker({
        title: '问题分类选择',
        data: [[...questions]],
        alias: {
          value: 'id',
          text: 'name'
        },
        onSelect: (selectedVal, selectedIndex, selectedText) => {
          // this.type = selectedText.join(' ')
          console.log(questions[0])
          this.prooblem_classify = questions[selectedIndex[0]]
        }
      }),
      urgentPicker: this.$createPicker({
        title: '问题紧急分类选择',
        data: [[...urgents]],
        alias: {
          value: 'id',
          text: 'name'
        },
        onSelect: (selectedVal, selectedIndex, selectedText) => {
          console.log(urgents[0])
          this.urgent = urgents[selectedIndex[0]]
        }
      }),
      loadingToast: this.$createToast({
        txt: '',
        time: 9999999999,
        mask: true
      }),
      uptoken: '',
      imgs: [],
      videoes: [],
      equips: [],
      devices: [],
      failure: '',
      remark: '',
      id: '',
      scrollOptions: {
        scrollbar: false,
        pullDownRefresh: {
          txt: ' '
        }
      }
    }
  },

  mounted () {
    this.rpc.call('qiniu_service.qiniu_upload_bucket', 'get_upload_token', ['jdv2']).then(data => {
      this.uptoken = data.token
    })
    this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_cuttent_line_port', []).then(data => {
      // console.log( data)
      // alert(1)
      if (data.line) {
        this.line = data.line
        this.ports[0] = data.port.id
        this.portsName[0] = data.port.name
      }
    })
    this.getSelectStation()
  },
  methods: {
    ...mapActions(['changeEquement']),
    handleSubmit () {
      if (this.ports.length === 0) {
        this.$createToast({
          txt: '请选择线路和站点',
          type: 'correct'
        }).show()
        return false
      }
      if (this.failure === '') {
        this.$createToast({
          txt: '请填写问题现象',
          type: 'correct'
        }).show()
        return false
      }
      // console.log(444,
      //   this.line.id,
      //   this.ports,
      //   this.prooblem_classify.id,
      //   this.urgent.id,
      //   this.failure,
      //   this.remark,
      //   this.devices,
      //   this.imgs,
      //   this.videoes)
      this.loadingToast.show()
      this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_add_reporting', [
        this.line.id,
        this.ports,
        this.prooblem_classify.id,
        this.urgent.id,
        this.failure,
        this.lable.id,
        this.remark,
        this.equement,
        this.imgs,
        this.videoes,
        this.reglon
      ], {}).then(data => {
        console.log(333, data)
        this.loadingToast.hide()
        this.$createToast({
          txt: '提交成功',
          type: 'correct'
        }).show()
        this.$router.push({name: 'home'})
      }).catch(e => {
        this.loadingToast.hide()
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })
    },
    change (val, label) {
      console.log('change', val, label)
      this.ports = val
      this.portsName = label
    },
    handleSelectType () {
      this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_all_line', []).then(data => {
        console.log(data)
        this.$createPicker({
          title: '线路选择',
          data: [data],
          alias: {
            value: 'id',
            text: 'name'
          },
          onSelect: (selectedVal, selectedIndex, selectedText) => {
            // console.log(123,selectedVal, 456,selectedIndex, 4567,selectedText)
            this.line = data[selectedIndex[0]]
          }
        }).show()
      })
      // console.log(12345678,this.line)
      this.ports = []
    },
    handleSelectStation () {
      this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_port', [this.line.id]).then(data => {
        this.stations = data.map(item => ({
          value: item.id,
          label: item.name
        }))
      })
      this.popupVisible = true
    },
    handleSelectReglon () {
      this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_all_line', []).then(data => {
        this.$createPicker({
          title: '区域选择',
          data: [data],
          alias: {
            value: 'id',
            text: 'name'
          },
          onSelect: (selectedVal, selectedIndex, selectedText) => {
            this.reglons = data[selectedIndex[0]]
          }
        }).show()
      })
    },
    getSelectStation () {
      this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_port', [this.line.id]).then(data => {
        this.stations = data.map(item => ({
          value: item.id,
          label: item.name
        }))
      })
    },
    handleTag () {
      this.$createPicker({
        title: '标签选择',
        data: [[...tags]],
        alias: {
          value: 'id',
          text: 'name'
        },
        onSelect: (selectedVal, selectedIndex, selectedText) => {
          this.lable = tags[selectedIndex[0]]
        }
      }).show()
    },
    submit () {
      this.popupVisible = false
    },
    onChange (val) {
      console.log('val change', val)
    },
    questionType () {
      this.questionPicker.show()
    },
    handleUrgent () {
      this.urgentPicker.show()
    },

    handleDeviceConfirm (data) {
      this.devices = data
    },
    selsetEquipment () {
      console.log(this.line, this.ports)
      this.$router.push({
        name: 'equipmentSearch',
        params: {
          line: this.line,
          stations: this.ports
        }

      })
    }
  }
  // beforeRouteUpdate (to, from, next) {
  //   console.log('....', to)
  //   if (to.name === 'task') {
  //     // alert('....')
  //     this.$refs.taskList.refresh()
  //   }
  //   this.$refs.taskList.refresh()
  //   next()
  // }
}
</script>

<style lang="scss">
.fault-page {
  padding: 16px 0;
  margin-bottom:50px;
  height: 100vh;
}
.repair-action{
  margin: 30px 10px;
}
.group-detail{
  background: #fff;
  padding: 5px 15px 10px;
}
.stations_con{
  .query-filter {
    width: 100%;
    height: 100vh;
    overflow: auto;

    .vux-checker-box{
      padding: 10px 15px;
    }
  }
  .query-actions {
    height: 49px;
    z-index: 999;
    position: absolute;
    left: 0;
    right: 0;
    bottom: -1;
    .cube-btn {
      border-radius: 0;
    }
  }

  .demo5-item {
    width: 65px;
    text-align: center;
    border-radius: 3px;
    border: 1px solid #ccc;
    background-color: #fff;
    margin-right: 6px;
    margin-bottom: 6px;
    padding:  10px;
    font-size: 12px;
  }
  .demo5-item-selected {
    z-index:9999999;
    background: rgb(18, 71, 114);
    border-color: #1C81D2;
    color: #ccc;
  }
}
.details-actioen {
 position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50px;
  z-index: 1;
  .cube-btn{
    border-radius: 0;
  }
}

</style>
