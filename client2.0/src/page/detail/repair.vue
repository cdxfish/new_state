<template>
  <page style="z-index: 200;">
    <div class="repair-page">
      <div class="cell-group">
        <mt-cell is-link @click.native="handleSelectType">
          <span slot="title" style="color: red;">选择维修类型</span>
          <span>{{type.name}}</span>
        </mt-cell>
      </div>

      <div class="cell-group">
        <div class="group-title">维修内容</div>
        <mt-field placeholder="请填写维修内容（必填）" type="textarea" rows="4" v-model="content"></mt-field>
      </div>

      <div class="cell-group">
        <div class="group-title">备注：</div>
        <mt-field placeholder="选填" type="textarea" rows="4" v-model="remark"></mt-field>
      </div>

      <div class="cell-group">
        <div class="group-title">故障设备：</div>
        <equipment-search v-model="equips" @on-confirm="handleDeviceConfirm"></equipment-search>
      </div>

      <div class="cell-group">
        <div class="group-title">照片上传（选填）</div>

        <div class="group-detail">
           <upload v-model="images"  v-if="uptoken" :token="uptoken"></upload>
        </div>
      </div>

      <div class="cell-group">
        <div class="group-title">视频上传（选填）</div>

        <div class="group-detail">
           <upload v-model="videoes" :type="'video'"  v-if="uptoken" :token="uptoken"></upload>
        </div>
      </div>

      <div class="repair-action">
        <cube-button primary @click="handleSubmit" :disabled="!content">提交</cube-button>
      </div>
    </div>
  </page>
</template>

<script>
import Page from '../../components/Page'
import Upload from '../../components/upload'
import EquipmentSearch from './equipmentSearch'

const typeData = [{ id: 'temp_repair', name: '临时维修' }, { id: 'temp_resolve', name: '临时修复' }, { id: 'repair', name: '完全维修' }]

export default {
  components: {
    Page,
    Upload,
    EquipmentSearch
  },
  data () {
    return {
      typePicker: this.$createPicker({
        title: '维修类型',
        data: [[...typeData]],
        alias: {
          value: 'id',
          text: 'name'
        },
        onSelect: (selectedVal, selectedIndex, selectedText) => {
          // this.type = selectedText.join(' ')
          console.log(typeData[0])
          this.type = typeData[selectedIndex[0]]
        }
      }),
      type: { id: 'temp_repair', name: '临时维修' },
      loadingToast: this.$createToast({
        txt: '',
        time: 9999999999,
        mask: true
      }),
      uptoken: '',
      images: [],
      videoes: [],
      equips: [],
      devices: [],
      content: '',
      remark: ''
    }
  },
  mounted () {
    this.rpc.call('qiniu_service.qiniu_upload_bucket', 'get_upload_token', ['jdv2']).then(data => {
      this.uptoken = data.token
    })

    this.rpc.call('repair_manage.task_page', 'get_order_devices', [this.$route.params.id], {}).then(data => {
      console.log('device list', data)
      this.equips = data.map(item => ({
        // id: item.device_id,
        value: item.device_id + '',
        label: item.device_name,
        valid: true
      }))
      this.devices = data.map(item => ({
        value: item.device_id + '',
        label: item.device_name,
        valid: true,
        checked: true
      }))
    })
  },
  methods: {
    handleSelectType () {
      this.typePicker.show()
    },

    handleDeviceConfirm (data) {
      this.devices = data
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

</style>
