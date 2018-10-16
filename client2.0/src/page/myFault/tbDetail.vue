<template>
  <page style="z-index: 9999;">
    <div class="detail-wrapper" v-if="!refreshLoading" style="z-index: 9999; height:100vh">
      <cube-scroll
        ref="scroll"
        :options="{
          scrollbar: true,
        }"
      >
      <div>
        <div class="repair-pages">
          <div class="cell-group" v-if="falut.name">
            <!-- <div class="group-title"></div> -->
            <mt-cell>
              <span slot="title">提报流水号：</span>
              <span>{{falut.name}}</span>
            </mt-cell>
          </div>
          <div class="cell-group">
            <mt-cell>
              <span slot="title">故障标签</span>
              <span>{{label}}</span>
            </mt-cell>
          </div>
          <div class="cell-group">
            <div class="group-title"></div>
            <mt-cell>
              <span slot="title">线别</span>
              <span>{{falut.falut_line_port[0].lines[1]}}</span>
              <!-- <span>{{falut.compute_line}}</span> -->
            </mt-cell>
            <mt-cell is-link  @click.native="goStationList" >
              <span slot="title">站点（区间）</span>
            </mt-cell>
          </div>
          <div class="cell-group">
            <div class="group-title"></div>
            <mt-cell>
              <span slot="title"  >问题分类</span>
              <span>{{problem_classify}}</span>
            </mt-cell>
            <mt-cell>
              <span slot="title"  >问题紧急程度</span>
              <span>{{urgency}}</span>
            </mt-cell>
          </div>
          <div class="cell-group">
            <div class="group-title">故障现象</div>
            <mt-field disabled type="textarea" rows="4" v-model="falut.failure"></mt-field>
          </div>
          <div class="cell-group">
            <div class="group-title">备注：</div>
            <mt-field disabled type="textarea" rows="4" v-model="falut.reporting_remarks"></mt-field>
          </div>
          <div class="cell-group" v-if="falut.reject_reason">
            <div class="group-title">驳回原因：</div>
            <mt-field disabled type="textarea" rows="4" v-model="falut.reject_reason"></mt-field>
          </div>

          <div class="cell-group">
            <div class="group-title">故障设备：</div>
            <mt-cell is-link  @click.native="goList">
              <span slot="title"  >查看设备</span>
            </mt-cell>
          </div>
          <div class="cell-group" v-if="falut.imgs && falut.imgs.length > 0">
            <div class="group-title">图片：</div>
            <div class="item-imgs" >
              <div class="image-wrp" v-for="item in falut.imgs" @click="showViewer(item)" :key="item.id">
                <div class="img"
                  :style="`background: url(${item.content}) center no-repeat;background-size:cover;`">
                </div>
              </div>
            </div>
          </div>
          <div class="cell-group" v-if="falut.videos && falut.videos.length > 0">
            <div class="group-title">视频：</div>
            <div class="item-imgs">
              <div class="image-wrp" v-for="(item, i) in falut.videos" :key="i">
                <div class="img"
                  :style="`background: url(${item.video_url}?vframe/png/offset/0) center no-repeat;background-size:cover;`">
                </div>
                <icon @click.native="showVideoViewer(item, i, $event)" name="regular/play-circle" class="item-video-icon" ></icon>
              </div>
            </div>
          </div>
        <image-viewer ref="imgsViewer" :imgs="this.imges"></image-viewer>
        <video-viewer ref="videoViewer" v-model="videoVisible" :src="videoSrc" :pic="videoPic"></video-viewer>
        </div>
        <div class="cell-group" v-if="falut.feedback_user">
          <div class="group-title"></div>
          <mt-cell>
            <span slot="title">反馈人员</span>
            <span>{{falut.feedback_user[1]}}</span>
          </mt-cell>
          <mt-cell>
            <span slot="title">反馈内容</span>
            <span>{{Reback}}</span>
          </mt-cell>
          <div class="cell-group">
            <div class="group-title">反馈备注：</div>
            <mt-field disabled type="textarea" rows="4" v-model="falut.remarks"></mt-field>
          </div>
        </div>
        <div class="cell-group" v-if="falut.display_evaluate_user">
          <div class="group-title"></div>
          <mt-cell>
            <span slot="title">评价人员</span>
            <!-- <span>{{falut.display_evaluate_user}}</span> -->
            <span>{{falut.compute_name}}</span>
          </mt-cell>
          <mt-cell>
            <span slot="title">评价内容</span>
            <span>{{Assess}}</span>
          </mt-cell>
          <div class="cell-group">
            <div class="group-title">评价备注：</div>
            <mt-field disabled type="textarea" rows="4" v-model="falut.opinion"></mt-field>
          </div>
        </div>
        <div class="cell-group" v-if="falut.supplement_info.length !== 0"  v-for="(item, index) in falut.supplement_info" :key="index">
            <div class="group-title">补充记录{{index + 1}}</div>
            <div class="record-item">
              <div class="item-header">
                <div class="left">
                  {{item.create_date}}
                </div>
                <div class="right">
                  处理人：{{item.user[1]}}
                </div>
              </div>
              <div class="item-content" v-if="item.content || item.remark">
                <div class="title" v-if="item.content">
                  内容：
                </div>
                <div class="text" v-if="item.content">
                  {{item.content}}
                </div>
              </div>
            </div>
          </div>
      </div>
      <div style="height:70px;"></div>
      </cube-scroll>
        <div class="detail_btns">
          <flexbox :gutter="0" >
            <flexbox-item v-if="falut.is_feedback">
              <cube-button primary  @click="goReBack">故障反馈</cube-button>
            </flexbox-item>
            <flexbox-item v-if="falut.state === 'admissible'">
              <cube-button primary  @click="goAddmsg">补充信息</cube-button>
            </flexbox-item>
            <flexbox-item v-if="falut.state === 'wait_carry'">
              <cube-button primary @click="handleSubmit">提报</cube-button>
            </flexbox-item>
            <flexbox-item v-if="falut.is_evaluate">
              <cube-button primary  @click="goAssess">评价</cube-button>
            </flexbox-item>
          </flexbox>
        </div>
    </div>
    <div v-else class="refresh-loading">
      <cube-loading></cube-loading>
    </div>

  <page-view></page-view>
  </page>
</template>

<script>
import Page from '../../components/Page'
import { Flexbox, FlexboxItem } from 'vux/src/components/flexbox'
import PageView from '../../components/View'
import Checklist from 'vux/src/components/checklist'
import ImageViewer from '../../components/ImageViewer'
import VideoViewer from '../../components/VideoViewer'
import { mapGetters, mapActions } from 'vuex'
import { getClssify, getUrgency, getReback, getAssess, getLable } from './status.js'
export default {
  components: {
    Page,
    PageView,
    Flexbox,
    ImageViewer,
    VideoViewer,
    FlexboxItem,
    Checklist
  },
  data () {
    return {
      stations: [],
      imges: [],
      scrollOptions: {
        scrollbar: true,
        pullDownRefresh: {
          txt: ' '
        }
      },
      refreshLoading: false,
      portsName: [],
      popupShow: true,
      popupVisible: false,
      loadingToast: this.$createToast({
        txt: '',
        time: 9999999999,
        mask: true
      }),
      videoVisible: false,
      videoViewerShow: false,
      videoSrc: '',
      videoPic: '',
      id: ''
    }
  },
  computed: {
    ...mapGetters(['falut']),
    urgency () {
      return getUrgency(this.falut.urgency)
    },
    Reback () {
      return getReback(this.falut.is_faulttreatment)
    },
    Assess () {
      return getAssess(this.falut.service_evaluation)
    },
    problem_classify () {
      return getClssify(this.falut.problem_classify)
    },
    label () {
      return getLable(this.falut.label)
    }
  },
  mounted () {
    // console.log(8888888, this.$route.params.id)
    this.id = this.$route.params.id
    this.refash()
  },
  methods: {
    ...mapActions(['falutDetail']),
    handleViewer (index) {
      this.$refs.uploadViewer.show(index)
    },
    showViewer (i) {
      this.imges = this.falut.imgs.map(item => ({
        src: item.content
      }))
      this.viewerIndex = i.id
      this.$refs.imgsViewer.show(1)
    },
    showVideoViewer (item, i) {
      console.log(i)
      this.videoSrc = item.video_url
      this.videoPic = item.video_url + '?vframe/png/offset/0'
      this.videoVisible = true
    },
    goList () {
      this.$router.push({name: 'faultEquement'})
    },
    goStationList () {
      this.$router.push({name: 'faultStation'})
    },
    goAssess () {
      this.$router.push({
        name: 'assess',
        params: {
          id: this.$route.params.id
        }
      })
    },
    goReBack () {
      this.$router.push({
        name: 'reBack',
        params: {
          id: this.$route.params.id
        }
      })
    },
    goAddmsg () {
      this.$router.push({
        name: 'shouliDteail',
        params: {
          id: this.$route.params.id
        }
      })
    },
    refash () {
      this.refreshLoading = true
      this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_reporting_record', [this.id], {}).then(data => {
        // console.log(1234,data)
        this.falutDetail(data)
        this.refreshLoading = false
        // this.falutDetail(data)
      }).catch(e => {
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
        this.refreshLoading = false
      })
    },
    handleSubmit () {
      // alert(this.$route.params.id)
      this.rpc.call('fault_reporting.reporting_mobile_pis', 'carry', [this.$route.params.id], {}).then(data => {
        // console.log(1234, data)
        // this.falutDetail(data)
        this.$createToast({
          txt: '提交成功',
          type: 'error'
        }).show()
        this.$router.back(-1)
      }).catch(e => {
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
        this.refreshLoading = false
      })
    },
    onChange (val) {
      console.log('val change', val)
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
  },
  watch: {
    $route (to, from) {
      this.refash()
    }
  }
}
</script>

<style lang="scss">
.repair-pages {
  padding-top: 16px;
  height:100vh;
}

.detail_btns{
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50px;
  z-index: 1000;
  .cube-btn{
    border-radius: 0;
  }
}
.item-i.content{
  padding: 10px 15px;
  background: #fff;
}

.item-video-icon{
  position: absolute;font-size: 30px; color: #fff;
  top: 5px;
  left: 5px;
}
.item-imgs{
  padding: 10px 15px;
  background: #fff;
}
.image-wrp{
  position:relative;
  display: inline-block;
  width:40px;
  height: 40px;
  margin-right: 8px;
  margin-bottom: 8px;
  // border-sizing: border-box;
  border-radius: 2px;
  // overflow: hidden;
  position: relative;

  .img{
    position: absolute;
    width: 100%;
    height: 100%;
  }
}
.record-item{
  background: #fff;
  color: rgb(127,127,127);
  font-size: 10px;

  .item-header{
    height: 32px;
    line-height: 32px;
    border-bottom: 1px solid #eee;
    padding: 0 15px;

    .left{
      float: left;
    }
    .right{
      float: right;
    }
  }

  .item-content{
    border-bottom: 1px solid #eee;
    padding: 10px 15px 0;

    .text{
      color: #595959;
      font-size: 12px;
      line-height: 20px;
      padding: 10px 0;
    }
  }

  .item-imgs{
    padding: 10px 15px;

  }

  .item-video-icon{
    position: absolute;font-size: 30px; color: #fff;
    top: 5px;
    left: 5px;
  }
}

.image-wrp{
  position:relative;
  display: inline-block;
  width:40px;
  height: 40px;
  margin-right: 8px;
  margin-bottom: 8px;
  // border-sizing: border-box;
  border-radius: 2px;
  // overflow: hidden;

  .img{
    position: absolute;
    width: 100%;
    height: 100%;
  }
}

</style>
