<template>
  <page style="z-index: 200;" :title="title">
    <div class="repair-pages">
      <div class="cell-group" v-if="this.$route.params.type === 1">
        <div class="group-title">要点登记</div>
        <mt-field placeholder="请填写内容（必填）" type="textarea" rows="6" v-model="content"></mt-field>
      </div>
      <div class="cell-group" v-if="this.$route.params.type === 2">
        <div class="group-title">要点登记</div>
        <mt-field placeholder="请填写内容（必填）" type="textarea" rows="6" v-model="content"></mt-field>
      </div>
      <div class="cell-group" v-if="this.$route.params.type === 3">
        <div class="group-title">要点登记</div>
        <mt-field placeholder="请填写内容（必填）" type="textarea" rows="6" v-model="content"></mt-field>
      </div>
      <div class="cell-group" v-if="this.$route.params.type === 4">
        <div class="group-title">要点登记</div>
        <mt-field placeholder="请填写内容（必填）" type="textarea" rows="6" v-model="content"></mt-field>
      </div>
      <div class="cell-group" v-if="this.$route.params.type === 5">
        <div class="group-title">要点登记</div>
        <mt-field placeholder="请填写内容（必填）" type="textarea" rows="6" v-model="content"></mt-field>
      </div>
      <div class="cell-group" v-if="this.$route.params.type === 6">
        <div class="group-title">要点登记</div>
        <mt-field placeholder="请填写内容（必填）" type="textarea" rows="6" v-model="content"></mt-field>
      </div>
      <div class="cell-group">
        <div class="group-title">照片上传（选填）</div>
        <div class="group-detail">
          <!-- <upload v-model="imgs"  v-if="uptoken" :token="uptoken"></upload> -->
          <upload v-model="imgs"  :token="uptoken"></upload>
        </div>
      </div>
      <div class="cell-group">
        <div class="group-title">视频上传（选填）</div>
        <div class="group-detail">
          <!-- <upload v-model="videoes" :type="'video'"  v-if="uptoken" :token="uptoken"></upload> -->
          <upload v-model="videoes" :type="'video'"  :token="uptoken"></upload>
        </div>
      </div>
    </div>
    <div :gutter="0" class="details-actioen" >
      <cube-button primary @click="handleSubmit" :disabled="content.trim()==''">提交</cube-button>
    </div>
  <page-view></page-view>
  </page>
</template>
<script>
import Page from '../../../components/Page'
import Upload from '../../../components/upload'
import PageView from '../../../components/View'
import { mapGetters, mapActions } from 'vuex'
export default {
  components: {
    Page,
    Upload,
    PageView
  },
  computed: {
    ...mapGetters(['equement', 'name'])
  },
  data () {
    return {
      loadingToast: this.$createToast({
        txt: '',
        time: 9999999999,
        mask: true
      }),
      content: '',
      uptoken: '',
      imgs: [],
      videoes: [],
      equips: [],
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
  },
  // computed: {
  //   title () {
  //     // alert(this.$route.params.type)
  //     if (this.$route.params.type === '1') {
  //       return '施工登记-要点'
  //     } else if (this.$route.params.type === '2') {
  //       return '安全交底'
  //     } else if (this.$route.params.type === '3') {
  //       return '工具物料准备'
  //     } else if (this.$route.params.type === '4') {
  //       return '执行检修项目'
  //     } else if (this.$route.params.type === '5') {
  //       return '出清确认'
  //     } else {
  //       return '施工销记-销点'
  //     }
  //   }
  // },
  methods: {
    ...mapActions(['changeEquement']),
    handleSubmit () {
      if (this.content === '') {
        this.$createToast({
          txt: '请填写内容',
          type: 'correct'
        }).show()
        return false
      }
      // console.log(444,
      //   this.line.id,
      //   this.imgs,
      //   this.videoes)
      this.$router.back(-1)
      this.loadingToast.show()
      this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_add_reporting', [
        this.imgs,
        this.videoes,
        this.content
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
    }
  }
}
</script>

<style lang="scss">
.details-actioen {
  height: 50px;
  z-index: inherit;
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;

  .cube-btn {
    border-radius: 0;
  }
}
</style>
