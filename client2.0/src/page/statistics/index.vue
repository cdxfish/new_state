<template>
  <page>
    <div class="ss-wrp">
      <div class="cell-group time-query">
        <mt-cell title="日期" is-link @click.native="handleTimeSelect">
          <span>{{this.startTime}} - {{this.endTime}}</span>
        </mt-cell>
      </div>

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
        >
          <div class="ss-detail">
            <div id="chart1">
              <div v-if="!chart1Loaded" class="refresh-loading">
                <cube-loading></cube-loading>
              </div>
            </div>

            <div id="chart2">
              <div v-if="!chart2Loaded" class="refresh-loading">
                <cube-loading></cube-loading>
              </div>
            </div>
          </div>
        </cube-scroll>
      </div>
    </div>
  </page>
</template>

<script>
import Page from '../../components/Page'
import echarts from 'echarts'

export default {
  components: {
    Page
  },
  data () {
    return {
      menuData: [
        {
          text: '车间筛选',
          options: []
        },
        {
          text: '工班筛选',
          options: []
        }
      ],
      menuValue: [{id: ''}, {id: ''}],
      chart1: null,
      chart2: null,
      chartOption1: {
        color: ['#1C81D2'],
        title: {
          text: '故障统计'
        },
        xAxis: {
          type: 'category',
          data: ['aaa', 'bb', 'cc', 'dd', 'f', 'e', 'g', 't', 'rr', 'ddf', 'fff', 'lll']
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          name: '故障数',
          data: [2, 5, 7, 8, 9, 2, 5, 7, 8, 9, 10, 4],
          type: 'line'
        }],
        tooltip: {
          trigger: 'axis',
          position: function (pt) {
            return [pt[0], '10%']
          }
        },
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 50
          }
        ]
      },
      chartOption2: {
        color: ['#39c7c8', '#c9b4f2', '#5eb2ed', '#faba84'],
        title: {
          text: '故障等级'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },

        series: [
          {
            name: '故障等级',
            type: 'pie',
            radius: '45%',
            center: ['50%', '50%'],
            data: [],
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              },
              normal: {
                label: {
                  show: true,
                  formatter: '{b} \n{c} ({d}%)'
                }
              }
            }
          }
        ]
      },
      timeQuery: [[new Date().getFullYear() + '', new Date().getMonth() + 1 + ''], [new Date().getFullYear() + '', new Date().getMonth() + 1 + '']],
      menuDict: [],
      chart1Loaded: false,
      chart2Loaded: false
    }
  },
  computed: {
    startTime () {
      return this.timeQuery[0].join('/')
    },
    endTime () {
      return this.timeQuery[1].join('/')
    }
  },
  mounted () {
    const dateSegmentData = [
      {
        is: 'cube-date-picker',
        min: new Date(2000, 0),
        title: '开始时间',
        value: new Date(),
        columnCount: 2
      },
      {
        is: 'cube-date-picker',
        min: new Date(2000, 0),
        title: '结束时间',
        value: new Date(),
        columnCount: 2
      }
    ]

    this.dateSegmentPicker = this.$createSegmentPicker({
      data: dateSegmentData,
      onSelect: (selectedDates, selectedVals, selectedTexts) => {
        console.log(selectedTexts)
        this.timeQuery = [...selectedTexts]
      },
      onNext: (i, selectedDate, selectedValue, selectedText) => {
        dateSegmentData[1].min = selectedDate
        if (i === 0) {
          this.dateSegmentPicker.$updateProps({
            data: dateSegmentData
          })
        }
      }
    })

    this.chart1 = echarts.init(document.getElementById('chart1'))
    this.chart2 = echarts.init(document.getElementById('chart2'))

    this.rpc.call('repair_manage.statics', 'getWorkShops', []).then(data => {
      console.log('...ddd', data)
      this.menuDict = data
      this.$set(this.menuData[0], 'options', data.map(item => ({
        id: item.id,
        text: item.name
      })))
      this.loadChart()
    }).catch(e => {
      this.$createToast({
        txt: e.message,
        type: 'error'
      }).show()
    })
  },
  methods: {
    handleMenuChange (barItem, listItem) {
      if (barItem.text === '车间筛选') {
        let works = this.menuDict.find(item => item.id === listItem.id)

        if (works) {
          this.$set(this.menuData[1], 'options', works.repair_manage_working_class.map(item => ({
            id: item.id,
            text: item.name + (item.type === 'inner' ? '（内部）' : '（外部）'),
            type: item.type
          })))
        } else {
          this.$set(this.menuData[1], 'options', [])
        }
      }

      this.menuValue = [...this.$refs.dropMenu.getSelectedValues()]
    },
    loadChart () {
      console.log('----', this.menuValue)
      this.chart1Loaded = false
      this.chart2Loaded = false

      this.rpc.call('repair_manage.statics', 'getWorkerShopStatic', [
        this.menuValue[0].id,
        this.menuValue[1].id,
        this.menuValue[1].type,
        this.timeQuery[0][0] + '-' + (this.timeQuery[0][1] > 9 ? this.timeQuery[0][1] : '0' + this.timeQuery[0][1]),
        this.timeQuery[1][0] + '-' + (this.timeQuery[1][1] > 9 ? this.timeQuery[1][1] : '0' + this.timeQuery[1][1])
      ]).then(data => {
        console.log('chart data', data)

        this.chart1Loaded = true
        this.chart2Loaded = true

        this.$set(this.chartOption1.series[0], 'data', Object.values(data.month_static))
        this.$set(this.chartOption1.xAxis, 'data', Object.keys(data.month_static).map(i => i + '月'))

        let data2 = []

        Object.keys(data.abc).forEach(i => {
          data2.push({
            name: i + '类',
            value: data.abc[i]
          })
        })

        this.$set(this.chartOption2.series[0], 'data', data2)

        this.chart1.setOption(this.chartOption1)
        this.chart2.setOption(this.chartOption2)
      }).catch(e => {
        this.$createToast({
          txt: e.message,
          type: 'error'
        }).show()
      })
    },
    handleTimeSelect () {
      this.dateSegmentPicker.show()
    }
  },
  watch: {
    menuValue (val) {
      console.log(val)
      this.loadChart()
    },
    timeQuery (val) {
      this.loadChart()
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
.ss-wrp{
  .md-drop-menu{
    position: absolute;
    top: 40px;
    height: 40px;
    font-size: 12px;

    z-index: 10001;
  }

  .time-query{
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    z-index: 10002;
    border-bottom: 1px solid #eee;
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
    height: calc(100vh - 80px);
    // margin-top: 2px;
    position: absolute;
    top: 80px;
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

  .ss-detail{
    padding: 10px 0;
    #chart1,#chart2{
      height: 300px;
      background: #fff;
      padding: 10px 15px;
      margin-bottom: 15px;
    }
  }
}
</style>
