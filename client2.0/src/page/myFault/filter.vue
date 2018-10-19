<template>
  <div style="height: 100%; width: 100%;">
    <cube-scroll
      class="query-filter"
      :options="scrollOptions"
    >
      <div style="padding: 20px 0;">
        <div class="cell-group">
          <div class="group-title">提报筛选</div>
          <checker
            v-model="filter.type"
            default-item-class="demo5-item"
            selected-item-class="demo5-item-selected"
            radio-required
            >
            <checker-item value="my">我的提报</checker-item>
            <checker-item value="all">全部提报</checker-item>
          </checker>
        </div>
        <div class="cell-group" v-if="route!='5'">
          <div class="group-title">状态筛选</div>
          <checker
            v-model="filter.status"
            default-item-class="demo5-item"
            selected-item-class="demo5-item-selected"
            radio-required
            >
              <checker-item value="">全部状态</checker-item>
              <checker-item value="admissible">待受理</checker-item>
              <checker-item value="notify">已指派</checker-item>
              <checker-item value="under_repair">维修中</checker-item>
              <checker-item value="deal_complete">已完成</checker-item>
              <checker-item value="output_complete">已销项</checker-item>
              <checker-item value="processed">已处理</checker-item>
              <checker-item value="reject">已拒绝</checker-item>
              <checker-item value="stay_feedback">待反馈</checker-item>
              <checker-item value="stay_evaluate">待评价</checker-item>
          </checker>
        </div>

        <div class="cell-group">
          <div class="group-title">问题分类型筛选</div>
          <checker
            v-model="filter.problem_classify"
            default-item-class="demo5-item"
            selected-item-class="demo5-item-selected"
            radio-required
            >
            <checker-item value="">全部</checker-item>
            <checker-item value="driving">影响行车</checker-item>
            <checker-item value="passenger_flow">影响客运</checker-item>
          </checker>
        </div>
        <div class="cell-group">
          <div class="group-title">问题紧急程度</div>
          <checker
            v-model="filter.urgency"
            default-item-class="demo5-item"
            selected-item-class="demo5-item-selected"
            radio-required
            >
              <checker-item value="">全部</checker-item>
              <checker-item value="urgent">需加急处理</checker-item>
              <checker-item value="normal">正常处理</checker-item>
          </checker>
        </div>
        <div class="cell-group">
          <div class="group-title">故障标签</div>
          <checker
            v-model="filter.lable"
            default-item-class="demo5-item"
            selected-item-class="demo5-item-selected"
            radio-required
            >
              <checker-item value="">全部</checker-item>
              <checker-item value="wu">无</checker-item>
              <checker-item value="cm">故障性维修</checker-item>
              <checker-item value="pm">预防性维修</checker-item>
          </checker>
        </div>
      </div>
    </cube-scroll>
    <div class="query-actions">
      <cube-button primary @click="handleSubmit">确定</cube-button>
    </div>
  </div>
</template>

<script>
import Group from 'vux/src/components/group'
import {Checker, CheckerItem} from 'vux/src/components/checker'

export default {
  components: {
    Group,
    Checker,
    CheckerItem
  },
  props: ['value', 'route'],
  data () {
    return {
      scrollOptions: {
        scrollbar: true
      },
      filter: {
        problem_classify: '',
        status: '',
        urgency: '',
        lable: '',
        type: 'my'
      }
    }
  },
  mounted () {
    this.filter = {...this.filter, ...this.value}
  },
  methods: {
    handleSubmit () {
      this.$emit('on-filter', this.filter)
    }
  },
  watch: {
    value (val) {
      this.filter = {...this.filter, ...this.value}
    }
  }
}
</script>


<style lang="scss">
.query-filter {
  width: 100%;
  height: calc(100% - 50px);
  .vux-checker-box{
    padding: 10px 15px;
  }
}
.query-actions {
  height: 50px;
  z-index: 999;
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;

  .cube-btn {
    border-radius: 0;
  }
}

.demo5-item {
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
.demo5-item-selected {
  background: rgba(28, 129, 210, .2);
  border-color: #1C81D2;
}
</style>
