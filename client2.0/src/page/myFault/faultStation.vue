<template>
  <page style="z-index: 200;">
    <div class="repair-page">
      <div class="cell-group">
        <mt-cell v-for="item in falut.falut_line_port " :key="item.id">
          <span slot="title"  >{{item.port[1]}}</span>
        </mt-cell>
      </div>
    </div>
    <flexbox :gutter="0" class="detail-actioen" >
      <flexbox-item>
        <cube-button primary  @click="goReBack">返回</cube-button>
      </flexbox-item>
    </flexbox>
  <page-view></page-view>
  </page>
</template>

<script>
import Page from '../../components/Page'
import { Flexbox, FlexboxItem } from 'vux/src/components/flexbox'
import PageView from '../../components/View'
import { mapGetters } from 'vuex'
export default {
  components: {
    Page,
    PageView,
    Flexbox,
    FlexboxItem
  },
  data () {
    return {

    }
  },
  computed: {
    ...mapGetters(['falut'])
  },
  methods: {
    goReBack () {
      this.$router.back(-1)
    }
  }
}
</script>

<style lang="scss">
.repair-page {
  padding: 16px 0;
}
.repair-action{
  margin: 30px 10px;
}
.group-detail{
  background: #fff;
  padding: 5px 15px 10px;
}
.stations_con{
  .query-filter {
    width: 100%;
    height: 100vh;
    overflow: auto;

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
    z-index:9999999;
    background: rgb(18, 71, 114);
    border-color: #1C81D2;
    color: #ccc;
  }
}
.detail-actioen{
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

</style>
