<template>
  <cube-scroll
    ref="scroll"
    :options="scrollOptions"
    @pulling-down="onPullingDown"
    @click="onClick"
    :data="items"
  >
    <div v-if="!refreshLoading">
      <task-item @click.native="handleCheck(i)" v-for="i in items" :data="i"  is-check :active="checkes.findIndex(item => item.id == i.id)>=0" :key="i.id" ></task-item>
    </div>
    <div v-else class="refresh-loading">
      <cube-loading></cube-loading>
    </div>
  </cube-scroll>

</template>

<script>
import TaskItem from '../task/item'

export default {
  components: {
    TaskItem
  },
  props: ['filter', 'checkes', 'type'],
  data () {
    return {
      scrollOptions: {
        scrollbar: true,
        pullDownRefresh: {
          txt: ' '
        }
      },
      items: [],
      refreshLoading: false
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    onPullingDown () {
      if (this.type === 'receiving') {
        this.rpc.call('repair_manage.task_page', 'get_receiving_tasks', []).then(data => {
          console.log('receiving task', data)
          this.$refs.scroll.forceUpdate()
          this.items = data
        })
      } else {
        this.rpc.call('repair_manage.task_page', 'get_working_tasks', []).then(data => {
          console.log('working task', data)
          this.$refs.scroll.forceUpdate()
          this.items = data
        })
      }
    },
    onPullingUp () {
      console.log('-------')
      setTimeout(() => {
        if (Math.random() > 0.5) {
          // If have new data, just update the data property.
          let newPage = this.items.map(item => item * 2)

          this.items = this.items.concat(newPage)

          this.$refs.scroll.forceUpdate()

          console.log('.....')
        } else {
          // If no new data, you need use the method forceUpdate to tell us the load is done.
          this.$refs.scroll.forceUpdate()

          // console.log('###')
        }
      }, 1000)
    },
    onClick (item) {
      console.log(item)
    },
    refresh () {
      this.refreshLoading = true

      if (this.type === 'receiving') {
        this.rpc.call('repair_manage.task_page', 'get_receiving_tasks', [
          this.$route.params.worker ? this.$route.params.worker : ''
        ]).then(data => {
          console.log('receiving task', data)
          this.refreshLoading = false
          this.items = data
        })
      } else {
        this.rpc.call('repair_manage.task_page', 'get_working_tasks', [
          this.$route.params.worker ? this.$route.params.worker : ''
        ]).then(data => {
          console.log('working task', data)
          this.refreshLoading = false
          this.items = data
        })
      }
    },
    handleCheck (i) {
      if (this.checkes.findIndex(item => item.id === i.id) >= 0) {
        this.checkes.splice(this.checkes.findIndex(item => item.id === i.id), 1)
      } else {
        this.checkes.push(i)
      }
    }
  },
  watch: {
    // filter: {
    //   deep: true,
    //   handler (val) {
    //     console.log('....', val)
    //     this.refresh()
    //   }
    // }
    type (val) {
      this.refresh()
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
