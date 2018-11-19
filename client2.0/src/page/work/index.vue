<template>
  <page>
    <div class="work-wrp">
      <mt-search
        v-model="query"

        cancel-text="取消"
        placeholder="搜索">
      </mt-search>
      <div class="cell-group">
        <mt-cell title="签到状态" is-link @click.native="handleSelectStatus">
          <span>{{selectStatus.value}}</span>
        </mt-cell>
      </div>



      <div class="result-wrapper">
        <cube-scroll
          ref="scroll"
          :options="{
            scrollbar: true,
            pullUpLoad: true
          }"
          @pulling-up="onPullingUp"
          :data="items"
        >
          <div v-if="!refreshLoading" class="cell-group detail">
            <mt-cell :title="item.name" is-link v-for="item in items" :key="item.id" @click.native="handleDetail(item)">
              <span>{{item.work_state == 'rest' ? '未在班' : '在班'}}</span>
            </mt-cell>
          </div>
          <div v-else class="refresh-loading">
            <cube-loading></cube-loading>
          </div>
        </cube-scroll>
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
      query: '',
      statusOptions: [{key: '', value: '全部'}, {key: 'working', value: '在班'}, {key: 'rest', value: '未在班'}],
      selectStatus: {key: '', value: '全部'},
      refreshLoading: true,
      items: [],
      lastId: '',
      pageIndex: 0,
      pageSize: 20
    }
  },
  computed: {
    statusPicker () {
      return this.$createPicker({
        title: '签到状态',
        data: [[...this.statusOptions]],
        alias: {
          value: 'key',
          text: 'value'
        },
        onSelect: (selectedVal, selectedIndex, selectedText) => {
          console.log(this.statusOptions[selectedIndex])
          this.selectStatus = this.statusOptions[selectedIndex]
        }
      })
    }
  },
  mounted () {
    this.loadData()
  },
  methods: {
    handleSelectStatus () {
      this.statusPicker.show()
    },
    loadData () {
      this.refreshLoading = true
      this.pageIndex = 0
      console.log('query ...', this.selectStatus.key)
      this.rpc.call('repair_manage.user_api', 'query_worker', [
        this.query,
        this.selectStatus.key,
        [],
        this.pageIndex * this.pageSize,
        this.pageSize
      ], {}).then(data => {
        console.log('aaaa', data)
        this.items = data
        if (data.length) {
          this.lastId = data[data.length - 1].id
          this.pageIndex++
        }
        this.refreshLoading = false
      }).catch(e => {
        this.refreshLoading = false
        this.$createToast({
          txt: e.message,
          type: 'error',
          time: 2000
        }).show()
      })
    },
    handleDetail (item) {
      this.$router.push({name: 'work-sign', params: {worker: item.id}})
    },
    onPullingUp () {
      this.rpc.call('repair_manage.user_api', 'query_worker', [
        this.query,
        this.selectStatus.key,
        [],
        this.pageIndex * this.pageSize,
        this.pageSize
      ], {}).then(data => {
        console.log('aaaa', data)
        this.$refs.scroll.forceUpdate()
        if (data.length) {
          this.lastId = data[data.length - 1].id
          this.pageIndex++
          this.items = this.items.concat(data)
        }
        // this.items = this.items.concat(data)
      }).catch(e => {
        this.$refs.scroll.forceUpdate()
      })
    }
  },
  watch: {
    query (val) {
      this.loadData()
    },
    selectStatus (val) {
      this.loadData()
    }
  }
}
</script>

<style lang="scss">
.work-wrp{
  width: 100%;

  .mint-search{
    font-size: 12px;
    height: 50px;

    .mint-searchbar-core{
      line-height: 28px;
    }

    .mint-search-list{
      display: none;
    }
  }

  .result-wrapper{
    height: calc(100vh - 90px);
    margin-top: 2px;

    .detail{
      padding: 10px 0;
    }
  }

  .refresh-loading{
    margin-top: 16px;
    text-align: center;

    .cube-loading{
      display: inline-block;
    }
  }
}
</style>
