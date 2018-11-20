<template>
  <div class="task-item">
    <div class="type-name" :style="{'background': color}">{{statusName}}</div>
    <div class="task-content">
       <div class="info-map">
        <div class="name">作业项目：</div>
        <div class="value row2">{{data.work_item}}</div>
      </div>
      <div class="info-map">
        <div class="name">作业地点：</div>
        <div class="value row1">{{data.work_address}}</div>
      </div>
      <div class="info-map">
        <div class="name">作业时间：</div>
        <div class="value row1">{{data.work_time}}</div>
      </div>
    </div>
     <div class="task-footer">
      <div class="code">
        执行单号：{{data.work_num}}
      </div>
      <div class="time">

      </div>
      <div class="min">
        <!-- {{data.work_num}} -->
      </div>
    </div>

    <div v-if="isCheck && active" class="checked">
      <h1>✓</h1>
    </div>
  </div>
</template>

<script>
import {getName, getColor} from './status.js'

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
    }
  },
  mounted () {
      // console.log(this.data)
  },
  computed: {
    color () {
      return getColor(this.data)
    },
    statusName () {
      return getName(this.data)
    }
  }
}
</script>

<style lang="scss">
.task-item {
  height: 110px;
  margin-top: 12px;
  background: #fff;
  position: relative;
  overflow: hidden;
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
