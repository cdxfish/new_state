<template>
  <div style="height: 100%; width: 100%;">
    <cube-scroll
      class="query-filter"
      ref="scroll"
      :options="scrollOptions"
    >
      <div style="padding: 20px 0;">

        <div class="cell-group" v-if="route!='5'">
          <div class="group-title">状态筛选</div>

          <checker
            v-model="filter.status"
            default-item-class="demo5-item"
            selected-item-class="demo5-item-selected"
            radio-required
            >
                <template v-if="route != '6'">
                <checker-item value="all">全部状态</checker-item>
                <checker-item value="unfinished">未完成</checker-item>
                <checker-item value="accept">待接报</checker-item>
                <checker-item value="repairing">维修中</checker-item>
                <checker-item value="turnning">交接中</checker-item>
                <checker-item value="exchanging">转发中</checker-item>
                <checker-item value="cancel_order">销项中</checker-item>
                <checker-item value="finished">已完成</checker-item>
                <checker-item value="suspend">挂起</checker-item>
                <!-- <checker-item value="stopped">撤回工单</checker-item> -->
                <checker-item value="unfilled">未兑现</checker-item>
                </template>
                <template v-else>
                  <checker-item value="outside_order">委外工单</checker-item>
                </template>
          </checker>
        </div>

        <div class="cell-group">
          <div class="group-title">故障类型筛选</div>

          <checker
            v-model="filter.type"
            default-item-class="demo5-item"
            selected-item-class="demo5-item-selected"
            radio-required
            >
              <!-- <template v-if="route == '2'">
                <checker-item value="重点">重点故障</checker-item>
              </template>
              <template v-else> -->
                <checker-item value="">全部</checker-item>
                <checker-item value="重点故障">重点故障</checker-item>
                <checker-item value="食堂故障">食堂类故障</checker-item>
                <checker-item value="办公故障">办公室故障</checker-item>
              <!-- </template> -->

          </checker>
        </div>

        <div class="cell-group">
          <div class="group-title">故障等级</div>

          <checker
            v-model="filter.level"
            default-item-class="demo5-item"
            selected-item-class="demo5-item-selected"
            radio-required
            >
              <checker-item value="">全部</checker-item>
              <checker-item value="A">A</checker-item>
              <checker-item value="B">B</checker-item>
              <checker-item value="C">C</checker-item>
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
        type: this.route === '2' ? '重点故障' : '',
        status: this.route === '1' ? 'unfinished' : this.route === '3' ? 'unfilled' : this.route === '4' ? 'suspend' : this.route === '5' ? 'finished' : this.route === '6' ? 'outside_order' : 'all',
        level: ''
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
