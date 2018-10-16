<template>
  <page :title="title">
    <div class="task-header">
    <mt-search
        v-model="filter.query"
        cancel-text="取消"
        placeholder="搜索">
      </mt-search>
      <cube-toolbar :actions="actions" @click="clickHandler"></cube-toolbar>

      <md-popup
        v-model="popupVisible"
        position="right"
        prevent-scroll
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

      actions: [
        {
          text: '通报时间 ⇅',
          type: 'checkbox',
          checked: false,
          index: 1,
          value: 'order_tm'
          // icon: 'cubeic-pulldown'
        },
        {
          text: '截止时间 ⇅',
          checked: false,
          type: 'checkbox',
          index: 2,
          value: 'end_tm'
          // icon: 'cubeic-pulldown'
        },
        {
          text: '已耗时 ⇅',
          checked: false,
          type: 'checkbox',
          index: 3,
          value: 'ellapse'
          // icon: 'cubeic-pulldown'
        },
        {
          text: '筛选',
          action: 'showQuery',
          type: 'checkbox',
          checked: false
        }
      ],
      popupVisible: false,
      popupShow: false,
      filter: {
        type: this.$route.params.type === '2' ? '重点故障' : '',
        status: this.$route.params.type === '2' ? 'unfinished' : (this.$route.params.type === '1' ? 'unfinished' : this.$route.params.type === '3' ? 'unfilled' : this.$route.params.type === '4' ? 'suspend' : this.$route.params.type === '5' ? 'finished' : this.$route.params.type === '6' ? 'outside_order' : 'all'),
        query: ''
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
        return '工单看板'
      }
    }
  },
  created () {
    this.rpc.call('repair_manage.task_page', 'get_status_descript', [], {}).then(data => {
      console.log('all status', data)
    })
  },
  methods: {
    clickHandler (item) {
      console.log(item)

      if (item.action) {
        this[item.action](item)
      } else {
        this.actions[0].checked = false
        this.actions[1].checked = false
        this.actions[2].checked = false
        this.actions[item.index - 1].checked = true

        this.sort(item)
      }
    },
    showQuery () {
      this.popupVisible = true
    },
    handleFilter (filter) {
      this.filter = {...filter}
      this.popupVisible = false
    },
    sort (item) {
      console.log('sort...', item)
      if (this.filter.sort === item.value) {
        this.filter = {...this.filter, sort: item.value + ' desc'}
      } else {
        this.filter = {...this.filter, sort: item.value}
      }
    }
  },
  watch: {
    popupVisible (val) {
      if (val) {
        this.popupShow = val
      } else {
        setTimeout(() => {
          this.popupShow = val
        }, 200)
      }
      this.actions[3].checked = true
    }
  },
  beforeRouteUpdate (to, from, next) {
    console.log('....', to)
    if (to.name === 'task') {
      // alert('....')
      this.$refs.taskList.refresh()
    }

    next()
  }
}
</script>

<style lang="scss">
.task-header {
  height: 90px;
  overflow: hidden;

 .mint-search{
  font-size: 12px;
  height: 50px;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  z-index: 12;
  .mint-searchbar-core{
    line-height: 28px;
  }
  .mint-search-list{
    display: none;
  }
}

  .cube-toolbar {
    position: absolute;
    left: 0;
    right: 0;
    top: 50px;
    height: 40px;
    z-index: 12;

    .cube-checkbox-ui.cubeic-round-border {
      display: none;
    }
    .cube-checkbox_checked {
      color: #1c81d2;
    }
  }

  .cube-toolbar-group {
    box-shadow: 0 0.5px 1px rgba(0, 0, 0, 0.1);

    .cube-btn {
      position: relative;

      i {
        position: absolute;
        right: 5 px;
        top: 17px;
      }
    }
  }
}
.task-list {
  height: calc(100vh - 90px);
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
