<template>
  <div class="repair-progress">
    <steps direction="vertical" :active="items.length">
      <step v-for="(item, index) in items" :key="index" >
        <span slot="title">{{item.name}}</span>
        <span slot="icon">
        </span>
        <span slot="description">
          <div>{{item.task_deal_tm}}</div>
          <div>{{item.working_class}}一{{item.assignee}}处理</div>
        </span>
      </step>
    </steps>
  </div>
</template>

<script>
import Steps from 'element-ui/packages/steps'
import Step from 'element-ui/packages/step'
import 'element-ui/lib/theme-chalk/step.css'
import 'element-ui/lib/theme-chalk/steps.css'

export default {
  components: {
    Step,
    Steps
  },
  props: ['items']
}
</script>

<style lang="scss">
.repair-progress {
  background: #fff;
  padding: 10px 15px;
  margin-top: 16px;
}
</style>
