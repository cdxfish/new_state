<template>
  <div>
    <div class="cell-group" v-for="(item, index) in items" :key="index">
      <div class="group-title">{{index + 1}}</div>
      <div class="record-item">
        <div class="item-header">
          <div class="left">
            {{item.task_deal_tm}} &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: rgb(28, 129, 210);">{{item.name}}</span>
          </div>
          <div class="right">
            处理人：{{item.assignee}}
          </div>
        </div>
        <div class="item-content" v-if="item.content || item.remark">
          <div class="title" v-if="item.content">
            内容：
          </div>
          <div class="text" v-if="item.content">
            {{item.content}}
          </div>
          <div class="title" v-if="item.remark">
            备注：
          </div>
          <div class="text" v-if="item.remark">
            {{item.remark}}
          </div>
        </div>
        <div class="item-imgs" v-if="item.pics && item.pics.length > 0">
          <div class="image-wrp" v-for="(item, i) in item.pics" @click="showViewer(index, i, $event)" :key="i">
            <div class="img"
              :style="`background: url(${item.url}) center no-repeat;background-size:cover;`">
            </div>
          </div>
        </div>
        <div class="item-imgs" v-if="item.videos && item.videos.length > 0">
          <div class="image-wrp" v-for="(item, i) in item.videos" :key="i">
            <div class="img"
              :style="`background: url(${item.url}?vframe/png/offset/0) center no-repeat;background-size:cover;`">
            </div>
            <icon @click.native="showVideoViewer(index, i, $event)" name="regular/play-circle" class="item-video-icon" ></icon>
          </div>
        </div>
      </div>
    </div>


  </div>
</template>

<script>

export default {
  components: {
    // VideoViewer
  },
  props: ['imgs', 'items'],
  data () {
    return {
      currentImgs: [],
      videoVisible: false,
      videoSrc: '',
      videoPic: ''
    }
  },
  methods: {
    showViewer (index, i) {
      // this.$emit('on-viewer', index, i)
      this.currentImgs = this.items[index].pics

      this.$emit('on-viewer', this.currentImgs, i)

      // this.$refs.imageViewerRecord.show(i)
    },

    showVideoViewer (index, i) {
      this.$emit('on-video', this.items[index].videos[i].url)
    }
  }
}
</script>

<style lang="scss">
.record-item{
  background: #fff;
  color: rgb(127,127,127);
  font-size: 10px;

  .item-header{
    height: 32px;
    line-height: 32px;
    border-bottom: 1px solid #eee;
    padding: 0 15px;

    .left{
      float: left;
    }
    .right{
      float: right;
    }
  }

  .item-content{
    border-bottom: 1px solid #eee;
    padding: 10px 15px 0;

    .text{
      color: #595959;
      font-size: 12px;
      line-height: 20px;
      padding: 10px 0;
    }
  }

  .item-imgs{
    padding: 10px 15px;

  }

  .item-video-icon{
    position: absolute;font-size: 30px; color: #fff;
    top: 5px;
    left: 5px;
  }
}

.image-wrp{
  position:relative;
  display: inline-block;
  width:40px;
  height: 40px;
  margin-right: 8px;
  margin-bottom: 8px;
  // border-sizing: border-box;
  border-radius: 2px;
  // overflow: hidden;

  .img{
    position: absolute;
    width: 100%;
    height: 100%;
  }
}
</style>
