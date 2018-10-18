<template>
  <page :title="title">
    <div class="fault-header">
      <mt-cell is-link @click.native="showQuery">
        <span slot="title" >筛选</span>
        <span></span>
      </mt-cell>
      <md-popup
        v-model="popupVisible"
        position="right"
        prevent-scrollc
        transition="slide-left"
        v-if="popupShow"
      >
        <div class="md-example-popup md-example-popup-right">
          <query-filter :value="filter" @on-filter="handleFilter" :route="$route.params.type"></query-filter>
        </div>
      </md-popup>
    </div>
    <div class="task-list">
      <task-list :filter="filter" ref="taskList"></task-list>
    </div>
    <page-view></page-view>
  </page>
</template>

<script>
import Page from '../../components/Page'
import QueryFilter from './filter'
import TaskList from './list'
import PageView from '../../components/View'

export default {
  components: {
    Page,
    QueryFilter,
    TaskList,
    PageView
  },
  data () {
    return {
      popupVisible: false,
      popupShow: false,
      filter: {
        status: '',
        urgency: '',
        problem_classify: ''
      }
    }
  },
  computed: {
    title () {
      if (this.$route.params.type === '1') {
        return '我的待办'
      } else if (this.$route.params.type === '2') {
        return '重点故障'
      } else if (this.$route.params.type === '3') {
        return '未兑现任务'
      } else if (this.$route.params.type === '4') {
        return '任务挂起'
      } else if (this.$route.params.type === '5') {
        return '历史维修记录'
      } else {
        return '我的提报'
      }
    }
  },
  methods: {
    showQuery () {
      this.popupVisible = true
    },
    handleFilter (filter) {
      console.log(filter)
      this.filter = {...filter}
      this.popupVisible = false
    },
    sort (item) {
      this.filter = {...this.filter, sort: item.value}
    }
  },
  watch: {
    popupVisible (val) {
      if (val) {
        this.popupShow = val
      } else {
        setTimeout(() => {
          this.popupShow = val
        }, 300)
      }
    }
  }
}
</script>

<style lang="scss">
.fault-header {
  height: 50px;
  overflow: hidden;
}
.task-list {
  height: calc(100vh - 42px);
}

.md-example-popup-right {
  width: 330px;
  height: 100vh;
  display: flex;
}

.md-popup-box {
  background-color: #fff;
}
.md-example-popup {
  position: relative;
  box-sizing: border-box;
}
</style>
