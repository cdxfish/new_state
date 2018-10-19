<template>
  <page title="维修计划">
    <div class="plan-header">
      <div class="plan_sele">
        <mt-search
          v-model="filter.query"
          cancel-text="取消"
          placeholder="搜索">
        </mt-search>
        <mt-cell is-link @click.native="showQuery">
          <span slot="title" >筛选</span>
          <span></span>
        </mt-cell>
      </div>
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
        <mt-cell is-link @click.native="showQuery">
        <span slot="title" >筛选</span>
        <span></span>
      </mt-cell>
      </md-popup>
    </div>

    <!-- <button @click="toDetail">detail</button> -->
    <div class="task-list">
      <task-list :filter="filter" ref="taskList"></task-list>
    </div>
    <div style="margin: 4rem auto;">
      <center>模块正在开发中。。。</center>
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
        type: this.$route.params.type === '2' ? '重点故障' : '',
        status: this.$route.params.type === '2' ? 'unfinished' : (this.$route.params.type === '1' ? 'unfinished' : this.$route.params.type === '3' ? 'unfilled' : this.$route.params.type === '4' ? 'suspend' : this.$route.params.type === '5' ? 'finished' : 'all'),
        query: ''
      }
    }
  },
  computed: {

  },
  created () {
    this.rpc.call('repair_manage.task_page', 'get_status_descript', [], {}).then(data => {
      console.log('all status', data)
    })
  },
  methods: {
    toDetail () {
      this.$router.push({name: 'planDetail', params: {id: 2}})
    },
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
      alert('发了')
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
.plan-header {

  overflow: hidden;
  .plan_sele{
    height: 100px;
  }

 .mint-search{
  font-size: 12px;
  height: 50px;
  // position: absolute;
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
