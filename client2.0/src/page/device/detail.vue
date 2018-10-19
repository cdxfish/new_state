<template>
  <page style="z-index: 10001;">
    <div class="device-detail-wrp">
      <div class="cell-group no-title">
        <mt-cell is-link @click.native="handleTodo">
          <div slot="title">提示：<span>有正在进行的任务</span></div>
          <span>点击查看</span>
        </mt-cell>
      </div>

      <div class="cell-group no-title">
        <mt-cell is-link @click.native="handleTodo">
          <div slot="title">
            <div class="title" style="color: #1C81D2;">故障提报</div>
            <div class="description">发现故障，上报到机电中心</div>
          </div>
        </mt-cell>
        <mt-cell is-link @click.native="handleRepairList">
          <div slot="title">
            <div class="title" >历史维修记录</div>
            <div class="description">查找历史的维修单</div>
          </div>
        </mt-cell>
        <mt-cell is-link @click.native="handleTodo">
          <div slot="title">
            <div class="title" >历史检修记录</div>
            <div class="description">查找历史的点巡检工单</div>
          </div>
        </mt-cell>
        <mt-cell is-link @click.native="handleInfo">
          <div slot="title">
            <div class="title" >设备台账</div>
            <div class="description">查看设备台账信息</div>
          </div>
        </mt-cell>
        <mt-cell is-link @click.native="handleTodo">
          <div slot="title">
            <div class="title" >技术资料</div>
            <div class="description">查找该设备相关技术手册</div>
          </div>
        </mt-cell>
      </div>

      <div class="cell-group">
        <div class="group-title">定位查看</div>
        <mt-cell title="设备定位" is-link @click.native="handleTodo"></mt-cell>
      </div>
    </div>

    <page-view></page-view>
  </page>
</template>

<script>
import Page from '../../components/Page'
import PageView from '../../components/View'

export default {
  components: {
    Page,
    PageView
  },
  data () {
    return {

    }
  },
  methods: {
    handleLocation () {
      this.$createToast({
        time: 1000,
        txt: '功能正在开发中',
        type: 'warn'
      }).show()
    },
    handleTodo () {
      this.$createToast({
        time: 1000,
        txt: '功能正在开发中',
        type: 'warn'
      }).show()
    },
    handleInfo () {
      this.$router.push({name: 'device-info'})
    },
    handleRepairList () {
      this.$router.push({name: 'device-task', params: {type: '5'}})
    }
  }
}
</script>

<style lang="scss">
.device-detail-wrp{
  .mint-cell-title{
    .title{
      line-height: 20px;
    }
    .description{
      color: #888;
      font-size: 10px;
      // line-height: 20px;
    }
  }
}
</style>
