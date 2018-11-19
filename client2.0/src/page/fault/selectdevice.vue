<template>
  <page>
    <div class="device-wrp">selectdevice

      <mt-search
        v-model="query"

        cancel-text="取消"
        placeholder="搜索">
      </mt-search>
<!-- :default-value="['一号线', '天府广场', '设备专业1', '控制室']" -->
      <md-drop-menu
        ref="dropMenu"
        :data="menuData"

        @change="handleMenuChange"
      ></md-drop-menu>

      <div class="result-wrapper">
        <cube-scroll
          ref="scroll"
          :options="{
            scrollbar: true
          }"
          :data="items"
        >
          <div v-if="!refreshLoading" class="cell-group detail">
            <mt-cell :title="i.device_name" is-link v-for="(i, $index) in items" :key="$index" @click.native="handleDetail(i)">
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
      queryDict: {},
      menuData: [
        {
          text: '线别',
          options: []
        },
        {
          text: '站点',
          options: []
        },
        {
          text: '设备专业',
          options: []
        }
      ],
      menuValue: [{id: ''}, {id: ''}, {id: ''}],
      items: [],
      refreshLoading: true
    }
  },
  mounted () {
    this.rpc.call('repair_manage.devices_api', 'get_lines_and_class', []).then(data => {
      console.log('get_lines', data)
      this.queryDict = data
      this.$set(this.menuData[0], 'options', data.lines.map(item => ({
        text: item.name,
        id: item.id
      })))
      this.$set(this.menuData[2], 'options', data.dev_class.map(item => ({
        text: item.name,
        id: item.id
      })))
      this.loadData()
    })
  },
  methods: {
    handleMenuChange (barItem, listItem) {
      console.log(barItem, listItem)

      if (barItem.text === '线别') {
        let address = this.queryDict.lines.find(item => item.id === listItem.id)

        if (address) {
          this.$set(this.menuData[1], 'options', address.addresses.map(item => ({
            id: item.id,
            text: item.name
          })))
        } else {
          this.$set(this.menuData[1], 'options', [])
        }
      }

      console.log(this.$refs.dropMenu.getSelectedValues())

      this.menuValue = [...this.$refs.dropMenu.getSelectedValues()]
    },
    handleDetail (item) {
      this.$router.push({name: 'device-detail', params: {deviceId: item.device_id}})
    },
    loadData () {
      console.log('menu query', this.menuValue)
      this.refreshLoading = true

      this.rpc.call('repair_manage.devices_api', 'query_devices', [
        this.query,
        this.menuValue[0].id,
        this.menuValue[1].id,
        this.menuValue[2].id
      ], {}).then(data => {
        this.refreshLoading = false
        this.items = data
        console.log('device list', data)
      }).catch(e => {
        this.refreshLoading = false
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })
    }
  },
  watch: {
    query (val) {
      this.loadData()
    },
    menuValue: {
      deep: true,
      handler (val) {
        this.loadData()
      }
    }
  }
}
</script>

<style lang="scss">
.device-wrp{
  .mint-search{
    font-size: 12px;
    height: 50px;
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    z-index: 10001;

    .mint-searchbar-core{
      line-height: 28px;
    }

    .mint-search-list{
      display: none;
    }
  }

  .md-drop-menu{
    position: absolute;
    top: 50px;
    height: 40px;
    font-size: 12px;
  }

  .md-radio .md-field .md-field-item{
    padding: 14px 20px;
    font-size: 12px;

    .md-radio-content{
      font-size: 12px;
    }

    .md-icon.sm{
      width: 12px;
      height: 12px;
    }
  }

  .md-drop-menu .md-drop-menu-list{
    padding-top: 40px;
  }

  .md-popup.with-mask{
    top: 50px;
  }

  .md-drop-menu .md-drop-menu-bar .bar-item span:after{
    border-width: 6px;
    top: 55%;
  }

  .result-wrapper{
    height: calc(100vh - 90px);
    // margin-top: 2px;
    position: absolute;
    top: 90px;
    left: 0;
    right: 0;

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
