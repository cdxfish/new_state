<template>
  <page style="z-index: 200;">
    <div class="repair-page">

      <div class="cell-group">
        <div class="group-title">销项原因</div>
        <mt-field placeholder="请填写销项原因（必填）" type="textarea" rows="4" v-model="content"></mt-field>
      </div>

      <div class="cell-group">
        <div class="group-title">备注：</div>
        <mt-field placeholder="选填" type="textarea" rows="4" v-model="remark"></mt-field>
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

export default {
  components: {
    Page,
    Upload
  },
  data () {
    return {
      loadingToast: this.$createToast({
        txt: '',
        time: 0,
        mask: true
      }),
      uptoken: '',
      images: [],
      videoes: [],
      content: '',
      remark: ''
    }
  },
  mounted () {
    this.rpc.call('qiniu_service.qiniu_upload_bucket', 'get_upload_token', ['jdv2']).then(data => {
      this.uptoken = data.token
    })
  },
  methods: {

    handleSubmit () {
      this.loadingToast.show()

      this.rpc.call('repair_manage.task_page', 'cancel_order', [
        this.$route.params.id,
        this.content,
        this.remark,
        this.images,
        this.videoes
      ], {}).then(data => {
        this.loadingToast.hide()
        window.sessionStorage.setItem('cur_detail_id', data)
        this.$createToast({
          txt: '提交成功',
          type: 'correct'
        }).show()
        this.$nextTick(() => {
          this.$router.back()
        })
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
