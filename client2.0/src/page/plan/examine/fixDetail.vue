
<template>
  <page style="z-index: 888;">
    <div class="fix_con">
      <div v-if="refreshLoading" v-for="item in items" :key="item.id" >
        <div class="title_con">
          <span>{{item.id}}:</span>
          <span>{{item.title}}</span>
        </div>
        <div class="cell-group" v-if="!item.title1">
          <div class="group-title">参数及异常记录</div>
          <mt-field placeholder="请填写现象（必填）" type="textarea" rows="4" :v-model="item.desc"></mt-field>
        </div>
        <div class="cell-group" v-if="item.title1">
          <div class="group-title">{{item.title1}}:</div>
          <mt-field placeholder="请填写现象（必填）" type="textarea" rows="1" :v-model="item.desc1"></mt-field>
        </div>
        <div class="cell-group" v-if="item.title2">
          <div class="group-title">{{item.title2}}:</div>
          <mt-field placeholder="请填写现象（必填）" type="textarea" rows="1" :v-model="item.desc2"></mt-field>
        </div>
        <div class="cell-group" v-if="item.title3">
          <div class="group-title">{{item.title3}}:</div>
          <mt-field placeholder="请填写现象（必填）" type="textarea" rows="1" :v-model="item.desc3"></mt-field>
        </div>
        <div class="desc_con">
          <div class="cell-group">
            <mt-radio
              title="完成情况"
              align="right"
              :v-model="status"
              :options="['完成', '未完成']">
            </mt-radio>
          </div>
        </div>

      </div>
      <div v-else class="refresh-loading">
        <cube-loading></cube-loading>
      </div>
      <div style="height:9rem"></div>
     <!-- <div class="detail-action"> -->
     <div class="btn_co">
        <cube-button primary @click="open" >保存</cube-button>
      </div>
    </div>


  <page-view></page-view>
  </page>
</template>
<script>
import Page from '../../../components/Page'
import PageView from '../../../components/View'

export default {
  components: {
    Page,
    PageView
  },
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
      items: [
        {
          id: 1,
          title: '地板清洁、无明显积尘',
          desc: '',
          status: '未完成'
        },
        {
          id: 2,
          title: '设备房墙体、天花无渗水、无变形；防静电地板无突起、地面无鼠迹',
          desc: '',
          status: '完成'
        },
        {
          id: 3,
          title: '设备房室内温、湿度符合要求（温度<=35℃、湿度<=80%）最高：80%  最低80%',
          title1: '温度',
          desc1: '',
          title2: '湿度',
          desc2: '',
          status: '未完成'
        },
        {
          id: 5,
          title: 'FEP、交换机水晶头未受损、松脱现象）',
          desc: '',
          status: '未完成'
        },
        {
          id: 6,
          title: '柜内各接线（含网线、电线、光纤、接地线）无破皮、松脱现象',
          desc: '',
          title1: 'A任务',
          desc1: '',
          title2: 'B任务',
          desc2: '',
          title3: 'C任务',
          desc3: '',
          status: '未完成'
        },
        {
          id: 7,
          title: '表面无锈浊、变形、缺失等现象',
          desc: '',
          status: '未完成'
        }
      ],
      refreshLoading: true,
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
.fix_con{
  height: calc(100vh - 90px);

  .title_con{
    padding: 0.5rem;
    background-color:#fff;
    margin-top: 1rem ;
    line-height: 1.2rem;
  }

}
.btn_co{
  z-index:888;
  position:sticky;
  height:50px;
  bottom: 0;
  left:0;
  right:0
}

.refresh-loading{
  margin-top: 20px;
  text-align: center;
  .cube-loading{
    display: inline-block;
  }
}
</style>

