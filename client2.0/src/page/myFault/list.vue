<template>
  <cube-scroll
    ref="scroll"
    :options="scrollOptions"
    :data="items"
    @pulling-up="onPullingUp"
  >
  <!--   @pulling-down="onPullingDown" -->
    <div v-if="!refreshLoading" >
      <task-item v-for="item in items" :data="item" :key="item.id" @click.native="handleDetail(item)"></task-item>
    </div>
    <div v-else class="refresh-loading">
      <cube-loading></cube-loading>
    </div>
  </cube-scroll>
</template>

<script>
import TaskItem from './item'
import { mapActions } from 'vuex'

export default {
  components: {
    TaskItem
  },
  props: ['filter'],
  data () {
    return {
      scrollOptions: {
        scrollbar: true,
        pullUpLoad: true
        // momentumLimitTime: 10
      },
      items: [],
      refreshLoading: false,
      lastId: '',
      pageIndex: 0,
      pageSize: 12
    }
  },
  mounted () {
    this.refresh()
  },

  methods: {
    ...mapActions(['falutDetail']),
    onPullingDown () {
      // 模拟更新数据
      this.pageIndex = 0
      this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_search_reporting', [
        this.filter.status,
        this.filter.problem_classify,
        this.filter.urgency,
        this.filter.lable,
        this.pageIndex * this.pageSize,
        this.pageSize,
        this.filter.type
      ], {}).then(data => {
        this.items = data
        if (data.length) {
          this.lastId = data[data.length - 1].db_id
          this.pageIndex++
        }
        this.$refs.scroll.forceUpdate()
      }).catch(e => {
        this.$refs.scroll.forceUpdate()
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })
    },
    onPullingUp () {
      this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_search_reporting', [
        this.filter.status,
        this.filter.problem_classify,
        this.filter.urgency,
        this.filter.lable,
        this.pageIndex * this.pageSize,
        this.pageSize,
        this.filter.type
      ], {}).then(data => {
        if (data.length) {
          this.pageIndex++
          this.items = this.items.concat(data)
        }
        this.$refs.scroll.forceUpdate()
      }).catch(e => {
        this.$refs.scroll.forceUpdate()
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })
    },
    refresh () {
      this.refreshLoading = true
      this.pageIndex = 0
      // alert(this.filter.type)
      // console.log('1234filter...', this.filter)
      this.rpc.call('fault_reporting.reporting_mobile_pis', 'get_search_reporting', [
        this.filter.status,
        this.filter.problem_classify,
        this.filter.urgency,
        this.filter.lable,
        this.pageIndex * this.pageSize,
        this.pageSize,
        this.filter.type
      ], {}).then(data => {
        // console.log('123提报 list', data)
        this.$refs.scroll.forceUpdate()
        this.refreshLoading = false
        if (data.length) {
          this.lastId = data[data.length - 1].db_id
          this.pageIndex++
        }
        this.items = data
      }).catch(e => {
        this.refreshLoading = false
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })
    },
    handleDetail (item) {
      this.$router.push({
        name: 'tbDetail',
        params: {id: item.id}
      })
    }
  },
  watch: {
    filter: {
      deep: true,
      handler (val) {
        console.log('....', val)
        this.refresh()
      }
    }
  }
}
</script>

<style lang="scss">
.refresh-loading{
  margin-top: 20px;
  text-align: center;
  .cube-loading{
    display: inline-block;
  }
}
</style>
