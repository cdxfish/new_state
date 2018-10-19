
<template>
  <div>

    <mt-cell title="选择设备" is-link @click.native="handleSearch">
      <div style="width: 200px; line-height: 18px;">{{selectsShow.map(item => item.label).join('、')}}</div>
    </mt-cell>

    <md-popup
      v-model="exitsVisible"
      position="bottom"
      prevent-scroll
      transition="slide-up"
      v-if="popupShow1"
    >
      <div class="search-wrp exists">
        <mt-search
          v-model="existQuery"
          autofocus
          cancel-text="取消"
          placeholder="搜索">
        </mt-search>

        <div class="cell-group no-title">
          <mt-cell title="添加新设备" is-link @click.native="handleAddDevice">
          </mt-cell>
        </div>

        <cube-scroll
          class="result-wrapper"
          ref="scroll"
          :options="{
            scrollbar: true,
            momentumLimitTime: 200
          }"
        >
          <div>
            <cube-checkbox-group v-model="checkList">
              <cube-checkbox :option="item" v-for="item in deviceResult.filter(item => (item.label + '').indexOf(existQuery) >= 0)" :key="item.value"><i>{{item.label}}</i><span v-if="item.valid" class="check-mark">(默认)</span></cube-checkbox>
            </cube-checkbox-group>
            <!-- <mt-checklist
              v-model="selects"
              :options="result">
            </mt-checklist> -->
          </div>
        </cube-scroll>

        <flexbox :gutter="0" class="detail-action" >
          <!-- <flexbox-item>
            <cube-button light @click="exitsVisible = false">取消</cube-button>
          </flexbox-item> -->
          <flexbox-item>
            <cube-button primary @click="handleSure">关闭</cube-button>
          </flexbox-item>
        </flexbox>
      </div>
    </md-popup>

    <md-popup
      v-model="searchVisible"
      position="bottom"
      prevent-scroll
      transition="slide-up"
      v-if="popupShow"
    >
      <div class="search-wrp">
        <mt-search
          v-model="query"
          autofocus
          cancel-text="取消"
          placeholder="搜索">
        </mt-search>

        <cube-scroll
          class="result-wrapper"
          ref="scroll"
          :options="{
            scrollbar: true,
            momentumLimitTime: 200
          }"
        >
          <div>
            <cube-checkbox-group v-model="selects">
              <cube-checkbox :option="item" v-for="item in queryResult.filter(item => (item.label + '').indexOf(query) >= 0)" :key="item.value"><i>{{item.label}}</i></cube-checkbox>
            </cube-checkbox-group>
            <!-- <mt-checklist
              v-model="selects"
              :options="result">
            </mt-checklist> -->
          </div>
        </cube-scroll>

        <flexbox :gutter="0" class="detail-action" >
          <flexbox-item>
            <cube-button light @click="searchVisible = false">取消</cube-button>
          </flexbox-item>
          <flexbox-item>
            <cube-button primary @click="handleConfirm">确定</cube-button>
          </flexbox-item>
        </flexbox>
      </div>
    </md-popup>


  </div>
</template>

<script>
import { Flexbox, FlexboxItem } from 'vux/src/components/flexbox'

export default {
  components: {
    Flexbox,
    FlexboxItem
  },
  props: {
    value: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      searchVisible: false,
      exitsVisible: false,
      selects: [],
      selectsShow: [],
      query: '',
      existQuery: '',
      popupShow: false,
      popupShow1: false,
      checkList: this.value.map(item => item.value),
      queryResult: [],
      deviceResult: this.value
    }
  },
  methods: {
    handleSearch () {
      // this.searchVisible = true
      this.exitsVisible = true
    },

    handleConfirm () {
      console.log(this.selects)
      // this.selects = [...this.checkList]
      // this.searchVisible = false
      // this.selectsShow = this.selects.map(item => {
      //   for (let i = 0; i < this.result.length; i++) {
      //     if (this.result[i].value === item) {
      //       return this.result[i]
      //     }
      //   }
      // })
      // console.log(this.selectsShow)

      for (let i = 0; i < this.selects.length; i++) {
        let currentSelect = this.selects[i]

        let currentSelectObj = this.queryResult.find(item => item.value + '' === currentSelect)

        let existObj = this.deviceResult.find(item => item.value + '' === currentSelect)

        if (!existObj) {
          this.deviceResult.push(currentSelectObj)
        }

        this.$nextTick(() => {
          if (this.checkList.indexOf(currentSelect) < 0) {
            this.checkList.push(currentSelect)
          }
        })
      }

      this.searchVisible = false
    },

    handleAddDevice () {
      this.searchVisible = true

      this.selects = []

      this.rpc.call('repair_manage.devices_api', 'get_all_devices', [], {}).then(data => {
        console.log('device all ', data)

        this.queryResult = []

        data.forEach(item => {
          if (this.checkList.indexOf(item.device_id + '') < 0) {
            this.queryResult.push({
              value: item.device_id + '',
              label: item.device_name
            })
          }
        })

        // this.queryResult = data.map(item => ({
        //   value: item.device_id + '',
        //   label: item.device_name
        // }))
      })
    },

    handleSure () {
      this.exitsVisible = false

      // 整理数据
      let emitData = []
      for (let i = 0; i < this.deviceResult.length; i++) {
        let currentDevice = this.deviceResult[i]

        if (this.checkList.indexOf(currentDevice.value) >= 0) {
          emitData.push({...currentDevice, checked: true})
        } else {
          emitData.push({...currentDevice, checked: false})
        }
      }

      console.log(emitData)
      this.$emit('on-confirm', emitData)
    },

    validCancel (deviceId) {
      // alert(deviceId)
      this.checkList.push(deviceId)

      let current = this.deviceResult[this.deviceResult.findIndex(item => item.value === deviceId)]

      let info

      if (current.valid) {
        info = prompt('请填写删减故障设备原因', '')

        if (info) {
          this.checkList.splice(this.checkList.indexOf(deviceId), 1)
        }
      } else {
        this.checkList.splice(this.checkList.indexOf(deviceId), 1)
      }

      this.deviceResult[this.deviceResult.findIndex(item => item.value === deviceId)] = {
        ...this.deviceResult[this.deviceResult.findIndex(item => item.value === deviceId)],
        info: info
      }
    }
  },
  watch: {
    checkList (val, oldVal) {
      console.log(val, oldVal)
      if (val.length < oldVal.length) {
        for (let j = 0; j < oldVal.length; j++) {
          if (val.indexOf(oldVal[j]) < 0) {
            this.validCancel(oldVal[j])
            break
          }
        }
      }
    },
    value (val) {
      // this.selects = val
      this.deviceResult = val
      this.checkList = val.map(item => item.value)
    },
    searchVisible (val) {
      if (val) {
        this.popupShow = val
      } else {
        setTimeout(() => {
          this.popupShow = val
        }, 200)
      }
    },
    exitsVisible (val) {
      if (val) {
        this.popupShow1 = val
      } else {
        setTimeout(() => {
          this.popupShow1 = val
        }, 200)
      }
    }
  }
}
</script>

<style lang="scss">
.search-wrp{
  background: #efeff4;
  width: 100%;
  height: 100vh;
  position: relative;

  .mint-search{
    font-size: 12px;
    height: 50px;

    .mint-searchbar-core{
      line-height: 28px;
    }

    .mint-search-list{
      display: none;
    }
  }

  .result-wrapper{
    height: calc(100vh - 100px);
    width: 100%;
  }

  .check-mark{
    font-size: 12px;
    // float: right;
    margin-left: 15px;
    color: #1c81d2;
  }

  &.exists {
    .result-wrapper{
      height: calc(100vh - 165px);
      width: 100%;
      margin-top: 8px;
    }
  }
}
</style>
