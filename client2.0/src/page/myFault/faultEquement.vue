<template>
  <page style="z-index: 200;">
    <div v-if='falut.fault_equipment.length > 0' class="repair-page">
      <div class="cell-group">
        <mt-cell v-for="item in falut.fault_equipment" :key="item.id">
          <span slot="title"  >{{item.name}}</span>
        </mt-cell>
      </div>

    </div>
    <div v-else style="margin: 5rem auto;color:red">
        <center>
          该记录没有报修设备。。。
        </center>
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
