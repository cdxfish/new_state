<template>
  <div class="fault-item">
    <div class="type-name" :style="{'background': color}">{{statusName}}</div>
    <div class="task-content">
      <div class="info-map" v-if="data.failure">
        <div class="name">故障现象：</div>
        <div class="value row2">{{data.failure}}</div>
      </div>
      <div class="info-map" v-if="data.failure">
        <div class="name">故障地点：</div>
        <div class="value row1">{{data.falut_line_port[0].port[1]}}...</div>
      </div>
      <div class="info-map-row">
        <div class="info-map">
          <div class="name">故障分类：</div>
          <div class="value">{{problem_classify}}</div>
        </div>
        <div class="info-map">
          <div class="name">紧急程度：</div>
          <div class="value">{{urgency}}</div>
        </div>
      </div>
    </div>
    <div class="task-footer">
      <!-- <div class="code">
        {{data.data.no}}
      </div> -->
      <div class="time">
        提报时间：{{data.report_tm}}
      </div>
      <div class="min1" v-if="data.is_feedback">
        <span style="border: 2px solid red;background:red;color:#fff;font-weight:900;border-radius:3px">待反馈</span>
      </div>
      <div class="min1" v-if="data.feedback_user">
        <span style="border: 2px solid red;background:red;color:#fff;font-weight:900;border-radius:3px">已反馈</span>
      </div>
      <div class="min" v-if="data.is_evaluate">
        <span style="border: 2px solid red;background:red;color:#fff;font-weight:900;border-radius:3px">待评价</span>
      </div>
    </div>

    <div v-if="isCheck && active" class="checked">
      <h1>✓</h1>
    </div>
    <div v-if="data.service_evaluation" class="qqqweiwai">
      <img src="../../assets/ypj.png">
    </div>
  </div>
</template>

<script>
import {getName, getColor, getClssify, getUrgency} from './status.js'

export default {
  props: {
    active: {
      type: Boolean,
      default: false
    },
    isCheck: {
      type: Boolean,
      default: false
    },
    data: {
      type: Object,
      default: () => {}
    },
    isWeiwai: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    color () {
      return getColor(this.data.state)
    },
    statusName () {
      return getName(this.data.state)
    },
    urgency () {
      return getUrgency(this.data.urgency)
    },
    problem_classify () {
      return getClssify(this.data.problem_classify)
    }
  },
  mounted () {
    // console.log(this.data.falut_line_port[0].lines[1], this.data.falut_line_port[0].port[1])
  }
}
</script>

<style lang="scss">
.fault-item {
  height: 110px;
  margin-top: 12px;
  background: #fff;
  position: relative;
  overflow: hidden;

  .qqqweiwai{
    position: absolute;
    width: 60px;
    height: 60px;
    top: 3px;
    right: 20px;
    img{
      width: 100%;
      height: 100%;
    }
  }

  .checked{
    position: absolute;

    background: #1C81D2;
    width: 100px;
    height: 100px;
    top: -50px;
    right: -50px;
    transform: rotate(45deg);
    opacity: 0.8;

    h1{
      font-size: 40px;
      color: #fff;
      transform: rotate(-45deg);
      padding-left: 5px;
      padding-top: 50px;
    }
  }

  .type-name {
    width: 35px;
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    font-size: 18px;
    color: #fff;
    text-align: center;
    line-height: 25px;
    padding-top: 17px;
  }

  .task-content,
  .task-footer {
    margin-left: 35px;
    .min1{
      margin: 0 -12px;
    }
    .min{
      margin-left: -45px;
    }


  }

  .task-content {
    height: 85px;
    padding: 0 15px 0 8px;

    .info-map {
      display: flex;
      line-height: 16px;
      padding-top: 5px;
      justify-content: flex-start;
      .name {
        font-size: 10px;
        color: rgb(127, 127, 127);
        width: 55px;
      }

      .value {
        font-size: 12px;
        color: rgb(59, 59, 59);
        flex: 1;

        &.row1 {
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        &.row2 {
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 2;
          overflow: hidden;
          height: 32px;
        }
      }
    }

    .info-map-row {
      display: flex;
      justify-content: space-between;
    }
  }

  .task-footer {
    padding: 0 15px 0 8px;
    height: 25px;
    line-height: 25px;
    display: flex;
    font-size: 9px;
    color: rgb(127, 127, 127);
    justify-content: space-between;
    border-top: 1px solid #eee;
  }
}
</style>
