<template>
  <page style="z-index: 200;">
    <cube-scroll
      class="detail-wrapper"
      ref="scroll"
      :options="{
        scrollbar: true,
        momentumLimitTime: 200
      }"
    >
      <div class="sign-detail ">
        <div class="cell-group ">
          <mt-cell title="选择签到站点" is-link @click.native="handleSelectLine">
            <span>{{line.name}}</span>
          </mt-cell>
        </div>
        <div id="map-container">

        </div>
        <div class="cell-group">
          <mt-cell :title="'距离：'+line.name+'  '+distance+'米'">
            <span><cube-button inline primary @click="handleRefresh">刷新</cube-button></span>
          </mt-cell>
          <div class="distance-warn">提示：现场签到地点与车站的距离不得大于2km，否则将无法签到!</div>
        </div>
        <div class="cell-group no-title">

          <div class="sign-record">
            <steps direction="vertical" :active="signSuccessed ? 2 : 1">
              <step>
                <span slot="title">未签到</span>
                <span slot="icon">
                </span>
                <span slot="description">未签到</span>
              </step>
              <step v-if="signSuccessed">
                <span slot="title">签到成功</span>
                <span slot="icon">
                </span>
                <span slot="description">地点：{{successData.address_name}}<br/></span>
                <span slot="description">{{successData.asign_tm}}</span>
              </step>
            </steps>
          </div>
        </div>
      </div>
    </cube-scroll>

    <flexbox :gutter="0" class="detail-action" v-if="lineOptions.length>0">
      <flexbox-item>
        <cube-button primary @click="handleSign" v-if="!signSuccessed"> {{isPhoto ? '拍照签到' : '签到'}}</cube-button>
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
    Step,
    Steps,
    FlexboxItem,
    Flexbox
  },
  data () {
    return {
      map: null,
      lineOptions: [],

      line: {},
      location: [0, 0],
      marker: null,
      circle: null,
      myMarker: null,
      distance: '--',
      loadingToast: this.$createToast({
        txt: '',
        time: 0,
        mask: true
      }),
      signSuccessed: false,
      successData: {}
    }
  },
  computed: {
    linePicker () {
      return this.$createPicker({
        title: '签到站点',
        data: [[...this.lineOptions]],
        alias: {
          value: 'id',
          text: 'name'
        },
        onSelect: (selectedVal, selectedIndex, selectedText) => {
          console.log(this.lineOptions[selectedIndex])
          this.line = this.lineOptions[selectedIndex]

          this.$nextTick(() => {
            this.updateMapInfo()
          })
        }
      })
    },
    isPhoto () {
      let di = parseInt(this.distance)
      if (di && di <= 2000) {
        return false
      } else {
        return true
      }
    }
  },
  mounted () {
    this.map = new window.AMap.Map('map-container', {
      resizeEnable: true,
      zoom: 18
    })

    this.rpc.call('repair_manage.task_page', 'get_sign_addresses', [this.$route.params.id], {}).then(data => {
      // alert(JSON.stringify(data))
      console.log('line options', data)
      this.lineOptions = data.map(item => ({
        id: item.id,
        name: item.display_name,
        position: item.bit_information ? item.bit_information.split(',') : ''
      }))

      if (this.lineOptions.length > 0) {
        this.line = this.lineOptions[0]
      }

      this.loadMapInfo()
    })
  },

  methods: {
    handleSelectLine () {
      this.linePicker.show()
    },
    loadMapInfo () {
      this.marker = new window.AMap.Marker({
        map: this.map,
        position: this.line.position
      })

      const _this = this

      this.getMyLocation().then(data => {
        _this.location = [data.longitude, data.latitude]
        console.log(_this.location)
        _this.myMarker = new window.AMap.Marker({
          map: _this.map,
          position: _this.location,
          icon: new window.AMap.Icon({
            size: new window.AMap.Size(20, 60),
            image: 'http://webapi.amap.com/theme/v1.3/markers/b/loc.png',
            imageSize: new window.AMap.Size(20, 20),
            imageOffset: new window.AMap.Pixel(0, 20)
            // imageOffset: new window.AMap.Pixel(0, -60)
          })
        })

        _this.addCirle()

        _this.map.setFitView()

        // 计算距离
        this.calcDistance(_this.line.position, _this.location)
      })
    },
    calcDistance (l1, l2) {
      let ll1 = new window.AMap.LngLat(l1[0], l1[1])
      let ll2 = new window.AMap.LngLat(l2[0], l2[1])
      this.distance = window.Math.round(ll1.distance(ll2)) + ''
    },
    addCirle () {
      this.circle = new window.AMap.Circle({
        center: this.line.position, // 圆心位置
        radius: 2000, // 半径
        strokeColor: '#1C81D2', // 线颜色
        strokeOpacity: 1, // 线透明度
        strokeWeight: 1, // 线粗细度
        fillColor: '#1C81D2', // 填充颜色
        fillOpacity: 0.35 // 填充透明度
      })

      // circle.setMap(this.map)
      this.map.add(this.circle)
    },
    updateMapInfo () {
      this.map.remove(this.circle)
      this.marker.setPosition(this.line.position)
      this.myMarker.setPosition(this.location)
      this.addCirle()
      this.map.setFitView()

      this.calcDistance(this.line.position, this.location)
    },
    handleSign () {
      if (this.isPhoto) {
        this.$router.replace({name: 'photo-sign', params: {address: this.line.id}})
      } else {
        this.loadingToast.show()

        this.rpc.call('repair_manage.task_page', 'address_asign', [
          this.$route.params.id,
          this.line.id,
          this.location.join(',')
        ], {}).then(data => {
          // this.$router.back()
          this.loadingToast.hide()
          // window.sessionStorage.setItem('cur_detail_id', data)
          this.successData = data
          this.signSuccessed = true
          this.$createToast({
            txt: '签到成功',
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
    },
    handleBack () {
      window.sessionStorage.setItem('cur_detail_id', this.successData.task_id)
      this.$router.back()
    },
    handleRefresh () {
      const _this = this
      this.getMyLocation().then(data => {
        console.log('location', data, this)

        _this.location = [data.longitude, data.latitude]

        _this.updateMapInfo()
      })
    },
    getMyLocation () {
      console.log('----')
      return new Promise((resolve, reject) => {
        window.dd.device.geolocation.get({
          targetAccuracy: 200,
          coordinate: 1,
          withReGeocode: false,
          useCache: false,
          onSuccess: function (result) {
            // console.log('----####---', result)
            resolve(result)
          },
          onFail: function (err) {
            // console.log('----####---0000', err)
            reject(err)
          }
        })
      })
    }
  },
  watch: {
    line (val) {
      console.log('aaa')
      // this.loadMapInfo()
      // this.updateMapInfo()
    }
  }
}
</script>

<style lang="scss">
#map-container{
  height: 300px;
}
.sign-detail{
  padding-bottom: 60px;
}
.sign-record{
  padding: 10px 15px;
  background: #fff;
}
.distance-warn{
  font-size: 10px;
  line-height: 20px;
  padding: 0 15px;
  // background: #fff;
  color: red;
}
</style>
