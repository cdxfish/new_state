<template>
  <page style="z-index: 200">
    <div>
      <div class="cell-group">
        <div class="group-title">照片上传</div>

        <div class="group-detail">
           <upload v-model="images" :length="1" v-if="uptoken" :token="uptoken"></upload>
           <div v-if="err">{{err}}</div>
        </div>
      </div>
    </div>

    <flexbox :gutter="0" class="detail-action">
      <flexbox-item>
        <cube-button primary @click="handleSign" :disabled="images.length==0">提交</cube-button>
      </flexbox-item>
    </flexbox>
  </page>
</template>

<script>
import Page from '../../components/Page'
import Upload from '../../components/upload'
import { Flexbox, FlexboxItem } from 'vux/src/components/flexbox'

export default {
  components: {
    Page,
    Upload,
    Flexbox,
    FlexboxItem
  },
  data () {
    return {
      images: [],
      uptoken: '',
      loadingToast: this.$createToast({
        txt: '',
        time: 0,
        mask: true
      })
    }
  },
  mounted () {
    this.rpc.call('qiniu_service.qiniu_upload_bucket', 'get_upload_token', ['jdv2']).then(data => {
      console.log(data)
      this.uptoken = data.token
      this.err = data.err
    })
  },
  methods: {
    handleSign () {
      this.loadingToast.show()

      this.rpc.call('repair_manage.task_page', 'pic_asign', [
        this.$route.params.id,
        this.$route.params.address,
        this.images[0].url
      ], {}).then(data => {
        this.$router.back()
        this.loadingToast.hide()
        window.sessionStorage.setItem('cur_detail_id', data)
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
  }
}
</script>

<style lang="scss">
.group-detail{
  background: #fff;
  padding: 5px 15px 10px;
}
</style>
