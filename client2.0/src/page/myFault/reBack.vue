
<template >
  <page style="z-index:1910000;">
    <div class="repair-page" style="z-index: 19100;">
      <div class="cell-group">
        <mt-cell is-link @click.native="handleTag">
          <span slot="title"  >当前身份</span>
          <span>{{falut.current_identity}}</span>
        </mt-cell>
      </div>
      <div class="cell-group">
        <div class="group-title">该故障是否已处理</div>
        <div style="background-color:#fff;padding-top:8px;padding-left:15px">
        <checker
          v-model="finshed"
          default-item-class="demo3-item"
          selected-item-class="demo3-item-selected"
          radio-required
          >
            <checker-item value="processed">已处理</checker-item>
            <checker-item value="untreated">未处理</checker-item>
        </checker>
        </div>
      </div>
      <div class="cell-group">
        <div class="group-title">备注：</div>
        <mt-field placeholder="请输入备注" type="textarea" rows="4" v-model="remark"></mt-field>
      </div>
    </div>
    <flexbox :gutter="0" class="detail-actioen" >
      <flexbox-item>
        <cube-button primary  @click="submit">保存</cube-button>
        <!-- :disabled="finshed" -->
      </flexbox-item>
    </flexbox>
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
      finshed: ''
    }
  },
  methods: {
    submit () {
      if (this.finshed === '') {
        this.$createToast({
          txt: '请选择状态',
          type: 'correct'
        }).show()
        return false
      }
      this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_feedback', [
        this.falut.id,
        this.finshed,
        this.remark
      ], {}).then(data => {
        this.$createToast({
          txt: '提交成功',
          type: 'correct'
        }).show()
        this.$router.back(-1)
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
.detail-actioen{
  position: absolute;
  bottom: 0;
  left: 0;
  right:0;
}
.demo3-item {
  width: 65px;
  // height: 30px;
  // line-height: 30px;
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
