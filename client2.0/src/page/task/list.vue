<template>
  <cube-scroll
    ref="scroll"
    :options="scrollOptions"
    @pulling-down="onPullingDown"
    @click="onClick"
    :data="items"
    @pulling-up="onPullingUp"
  >
    <div v-if="!refreshLoading" >
      <task-item v-for="item in items" :is-weiwai="$route.params.type=='6'" :data="item" :key="item.id" @click.native="handleDetail(item)"></task-item>
    </div>
    <div v-else class="refresh-loading">
      <cube-loading></cube-loading>
    </div>
  </cube-scroll>

</template>

<script>
import TaskItem from './item'

export default {
  components: {
    TaskItem
  },
  props: ['filter'],
  data () {
    return {
      scrollOptions: {
        scrollbar: true,
        pullUpLoad: true,
        // momentumLimitTime: 200,
        pullDownRefresh: {
          txt: ' '
        }
      },
      items: [],
      refreshLoading: false,
      lastId: '',
      pageIndex: 0,
      pageSize: 10
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    onPullingDown () {
      // 模拟更新数据
      this.pageIndex = 0
      this.rpc.call('repair_manage.task_page', 'queryTasks', [
        this.filter.status ? this.filter.status : '',
        this.filter.type ? this.filter.type : '',
        this.filter.level ? this.filter.level : '',
        this.filter.sort ? this.filter.sort : '',
        this.$route.params.type === 'all' ? 'kanban' : 'normal',
        this.$route.params.type === '5' ? this.$route.params.deviceId : '',
        this.filter.query
      ], {}).then(data => {
        console.log('task list', data)
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
      this.rpc.call('repair_manage.task_page', 'queryTasks', [
        this.filter.status ? this.filter.status : 'all',
        this.filter.type ? this.filter.type : '',
        this.filter.level ? this.filter.level : '',
        this.filter.sort ? this.filter.sort : '',
        this.$route.params.type === 'all' ? 'kanban' : 'normal',
        this.$route.params.type === '5' ? this.$route.params.deviceId : '',
        this.pageIndex * this.pageSize,
        this.pageSize,
        this.filter.query
      ], {}).then(data => {
        console.log('task list', data)
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
    onClick (item) {
      console.log(item)
    },
    refresh () {
      this.refreshLoading = true
      this.pageIndex = 0

      console.log('filter...', this.filter)

      this.rpc.call('repair_manage.task_page', 'queryTasks', [
        this.filter.status ? this.filter.status : 'all',
        this.filter.type ? this.filter.type : '',
        this.filter.level ? this.filter.level : '',
        this.filter.sort ? this.filter.sort : '',
        this.$route.params.type === 'all' ? 'kanban' : 'normal',
        this.$route.params.type === '5' ? this.$route.params.deviceId : '',
        this.pageIndex * this.pageSize,
        this.pageSize,
        this.filter.query
      ], {}).then(data => {
        console.log('task list', data)
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
      console.log('9999')
      if (this.$route.params.type === '5') {
        this.$router.push({name: 'device-task-detail', params: {id: item.id}})
      } else {
        this.$router.push({name: 'task-detail', params: {id: item.id}})
      }
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
