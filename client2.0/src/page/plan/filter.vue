<template>
  <div style="height: 100%; width: 100%;">
    <cube-scroll
      class="query-filter"
      ref="scroll"
      :options="scrollOptions"
    >
      <div style="padding: 20px 0;">
        <div class="cell-group" v-if="route!='5'">
          <div class="cell-group time-query">
            <div class="group-title">时间段筛选</div>
            <mt-cell title="请选择" is-link @click.native="handleTimeSelect">
              <span style="font-size:1rem">{{this.startTime}} - {{this.endTime}}</span>
            </mt-cell>
          </div>
          <div class="group-title">状态筛选</div>

          <checker
            v-model="filter.status"
            default-item-class="demo5-item"
            selected-item-class="demo5-item-selected"
            radio-required
            >
              <checker-item value="all">全部状态</checker-item>
              <checker-item value="unfinished">待执行</checker-item>
              <checker-item value="finishing">执行中</checker-item>
              <checker-item value="finished">待审核</checker-item>
              <checker-item value="stopped">待复查</checker-item>
              <checker-item value="unfilled">已关闭</checker-item>
              <checker-item value="unues">无效工单</checker-item>
            <!-- </template> -->
          </checker>
        </div>

        <div class="cell-group">
          <div class="group-title">故障类型筛选</div>

          <checker
            v-model="filter.type"
            default-item-class="demo5-item"
            selected-item-class="demo5-item-selected"
            radio-required
            >
              <checker-item value="">全部</checker-item>
              <checker-item value="日检">日检</checker-item>
              <checker-item value="月检">月检</checker-item>
              <checker-item value="季检">季检</checker-item>
              <checker-item value="半年检">半年检</checker-item>
              <checker-item value="年检">年检</checker-item>


          </checker>
        </div>
      </div>
    </cube-scroll>

    <div class="query-actions">
      <cube-button primary @click="handleSubmit">确定</cube-button>
    </div>
  </div>
</template>

<script>
import Group from 'vux/src/components/group'
import {Checker, CheckerItem} from 'vux/src/components/checker'

export default {
  components: {
    Group,
    Checker,
    CheckerItem
  },
  props: ['value', 'route'],
  data () {
    return {
      scrollOptions: {
        scrollbar: true
      },
      filter: {
        type: this.route === '2' ? '重点故障' : '',
        status: this.route === '1' ? 'unfinished' : this.route === '3' ? 'unfilled' : this.route === '4' ? 'suspend' : this.route === '5' ? 'finished' : 'all',
        level: '',
        startTime: this.startTime,
        endTime: this.endTime
      },
      timeQuery: [[new Date().getFullYear() + '', new Date().getMonth() + 1 + '', new Date().getDate()], [new Date().getFullYear() + '', new Date().getMonth() + 1 + '', new Date().getDate()]],
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
    this.filter = {...this.filter, ...this.value}
    const dateSegmentData = [
      {
        is: 'cube-date-picker',
        min: new Date(2000, 0, 0),
        title: '开始时间',
        value: new Date(),
        columnCount: 3
      },
      {
        is: 'cube-date-picker',
        min: new Date(2000, 0),
        title: '结束时间',
        value: new Date(),
        columnCount: 3
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
  },
  methods: {
    handleSubmit () {
      alert(1)
      console.log(this.filter)
      this.$emit('on-filter', this.filter)
    },
    handleTimeSelect () {
      this.dateSegmentPicker.show()
    }
  },
  watch: {
    value (val) {
      this.filter = {...this.filter, ...this.value}
    }
  }
}
</script>


<style lang="scss">
.query-filter {
  width: 100%;
  height: calc(100% - 50px);

  .vux-checker-box{
    padding: 10px 15px;
  }
}
.query-actions {
  height: 50px;
  z-index: 999;
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;

  .cube-btn {
    border-radius: 0;
  }
}

.demo5-item {
  width: 65px;
  // height: 30px;
  // line-height: 30px;
  text-align: center;
  border-radius: 3px;
  border: 1px solid #ccc;
  background-color: #fff;
  margin-right: 6px;
  margin-bottom: 6px;
  padding:  10px;
  font-size: 12px;
}
.demo5-item-selected {
  background: rgba(28, 129, 210, .2);
  border-color: #1C81D2;
}
</style>
