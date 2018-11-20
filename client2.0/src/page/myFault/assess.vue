
<template>
  <page style="z-index:999999;">
    <div class="repair-page123"  style="z-index:99999;">
      <div class="cell-group" style="z-index:99999;">
        <mt-cell @click.native="handleTag">
          <span slot="title">当前身份</span>
          <span>{{falut.current_identity}}</span>
        </mt-cell>
      </div>
      <div class="cell-group">
        <div class="group-title">评价本次维修的服务质量</div>
        <div style="background-color:#fff;padding-top:8px;padding-left:15px">
           <checker
            v-model="finshed"
            default-item-class="demo3-item"
            selected-item-class="demo3-item-selected"
            radio-required
            >
              <checker-item value="very_nice">非常好</checker-item>
              <checker-item value="fine">很好</checker-item>
              <checker-item value="commonly">一般</checker-item>
              <checker-item value="difference">差</checker-item>
              <checker-item value="very_poor">非常差</checker-item>
          </checker>
        </div>
      </div>
      <div class="cell-group">
        <div class="group-title">意见或建议：</div>
        <mt-field placeholder="一般、差和非常差请输入十字以上意见或建议！ " type="textarea" rows="4" v-model="remark"></mt-field>
      </div>
      <flexbox :gutter="0" class="d_btns" >
        <flexbox-item>
          <cube-button primary @click="accept">提交评价</cube-button>
        </flexbox-item>
      </flexbox>
    </div>

  <page-view></page-view>
  </page>
</template>

<script>
import Page from '../../components/Page'
import { Flexbox, FlexboxItem } from 'vux/src/components/flexbox'
import PageView from '../../components/View'
import Group from 'vux/src/components/group'
import {Checker, CheckerItem} from 'vux/src/components/checker'
import { mapGetters } from 'vuex'

export default {
  components: {
    Page,
    Flexbox,
    FlexboxItem,
    Group,
    Checker,
    CheckerItem,
    PageView
  },
  computed: {
    ...mapGetters(['falut'])
  },
  data () {
    return {
      remark: '',
      show: false,
      finshed: ''
    }
  },
  methods: {
    accept () {
      // alert(1)
      if (this.finshed === '') {
        this.$createToast({
          txt: '请选择服务质量',
          type: 'correct'
        }).show()
        return false
      }
      if ((this.finshed === 'commonly' && this.remark.length < 10) || (this.finshed === 'difference' && this.remark.length < 10) || (this.finshed === 'very_poor' && this.remark.length < 10)) {
        this.$createToast({
          txt: '十字以上评价',
          type: 'correct'
        }).show()
        return false
      }

      this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_evaluate', [
        this.falut.id,
        this.finshed,
        this.remark
      ], {}).then(data => {
        this.show = true
        this.$router.back(-1)
        this.$createToast({
          txt: '提交成功',
          type: 'correct'
        }).show()
      }).catch(e => {
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

.d_btns{
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50px;
  z-index: 19990999;
  .cube-btn{
    border-radius: 0;
  }
}

.demo3-item {
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
.demo3-item-selected {
  background: rgba(28, 129, 210, .2);
  border-color: #1C81D2;
}


</style>
