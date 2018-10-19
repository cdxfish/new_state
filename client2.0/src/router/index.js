import Vue from 'vue'
import Router from 'vue-router'

import Home from '../page/home/index.vue'
import Sign from '../page/sign/index.vue'
import Handover from '../page/handover/index.vue'
import Task from '../page/task/index.vue'
import Detail from '../page/detail/index.vue'
import Repair from '../page/detail/repair.vue'
import Output from '../page/detail/output.vue'
import MapSign from '../page/detail/mapSign.vue'
import PhotoSign from '../page/detail/photoSign.vue'
import DeviceSign from '../page/detail/deviceSign.vue'
import Transpond from '../page/detail/transpond.vue'
import Plan from '../page/plan/index.vue'
import PlanItem from '../page/plan/planItem.vue'
import Examine from '../page/plan/examine/index.vue'
import Asgin from '../page/plan/handle/asgin.vue'
import Element from '../page/plan/examine/element.vue'
import FixDetail from '../page/plan/examine/fixDetail.vue'
import PlanDetail from '../page/plan/planDetail.vue'
import Fault from '../page/fault/index.vue'
import EquipmentSearch from '../page/fault/equipmentSearch.vue'
// import SelectDevice from '../page/fault/selectdevice.vue'
import MyFault from '../page/myFault/index.vue'
import TbDetail from '../page/myFault/tbDetail.vue'
import ShouliDteail from '../page/myFault/shouliDteail.vue'
import ReBack from '../page/myFault/reBack.vue'
import Assess from '../page/myFault/assess.vue'
import FaultEquement from '../page/myFault/faultEquement.vue'
import FaultStation from '../page/myFault/faultStation.vue'
import Work from '../page/work/index.vue'
import DeviceDetail from '../page/device/detail.vue'
import Statistics from '../page/statistics/index.vue'
import Guaqi from '../page/detail/guaqi.vue'
import DeviceInfo from '../page/device/info.vue'
import Device from '../page/device/index.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      // component: () => import('../page/home/index.vue'),
      component: Home,
      meta: {
        title: '工作'
      },
      children: [
        {
          path: 'sign/',
          name: 'sign',
          // component: () => import('../page/sign/index.vue'),
          component: Sign,
          meta: {
            title: '签到'
          },
          children: [
            {
              path: 'signhandover/',
              name: 'signhandover',
              // component: () => import('../page/handover/index.vue'),
              component: Handover,
              meta: {
                title: '交接班看板'
              }
            }
          ]
        },
        {
          path: 'task/:type',
          name: 'task',
          // component: () => import('../page/task/index.vue'),
          component: Task,
          meta: {
            title: '工单看板'
          },
          children: [
            {
              path: 'detail/:id',
              name: 'task-detail',
              // component: () => import('../page/detail/index.vue'),
              component: Detail,
              meta: {
                title: '故障详情'
              },
              children: [
                {
                  path: 'repair/:repairId',
                  name: 'repair',
                  // component: () => import('../page/detail/repair.vue'),
                  component: Repair,
                  meta: {
                    title: '维修'
                  }
                },
                {
                  path: 'output/',
                  name: 'output',
                  // component: () => import('../page/detail/output.vue'),
                  component: Output,
                  meta: {
                    title: '销项'
                  }
                },
                {
                  path: 'guaqi/',
                  name: 'guaqi',
                  component: Guaqi,
                  meta: {
                    title: '工单挂起'
                  }
                },
                {
                  path: 'mapsign',
                  name: 'map-sign',
                  // component: () => import('../page/detail/mapSign.vue'),
                  component: MapSign,
                  meta: {
                    title: '维修签到'
                  }
                },
                {
                  path: 'photosign/:address',
                  name: 'photo-sign',
                  // component: () => import('../page/detail/photoSign.vue'),
                  component: PhotoSign,
                  meta: {
                    title: '拍照签到'
                  }
                },
                {
                  path: 'devicesign',
                  name: 'device-sign',
                  // component: () => import('../page/detail/deviceSign.vue'),
                  component: DeviceSign,
                  meta: {
                    title: '设备二维码签到'
                  }
                },
                {
                  path: 'transpond/:transId',
                  name: 'transpond',
                  // component: () => import('../page/detail/transpond.vue'),
                  component: Transpond,
                  meta: {
                    title: '转发'
                  }
                }
              ]
            }
          ]
        },
        {
          path: 'plan/',
          name: 'plan',
          component: Plan,
          meta: {
            title: '维修计划'
          },
          children: [
            {
              path: 'planItem/',
              name: 'planItem',
              component: PlanItem,
              meta: {
                title: '维修项目'
              },
              children: [
                {
                  path: 'asgin/:type',
                  name: 'asgin',
                  component: Asgin,
                  meta: {
                    title: '施工登记——要点'
                  }
                }
              ]
            },
            {
              path: 'planDetail/:id',
              name: 'planDetail',
              component: PlanDetail,
              meta: {
                title: '计划详情'
              },
              children: [
                {
                  path: 'examine/',
                  name: 'examine',
                  component: Examine,
                  meta: {
                    title: '检查项目'
                  },
                  children: [
                    {
                      path: 'fixDetail/:id',
                      name: 'fixDetail',
                      component: FixDetail,
                      meta: {
                        title: '检查详情'
                      }
                    }
                  ]
                },
                {
                  path: 'element/',
                  name: 'element',
                  component: Element,
                  meta: {
                    title: '设备列表'
                  }
                }
              ]
            }
          ]
        },
        {
          path: 'fault/',
          name: 'fault',
          component: Fault,
          meta: {
            title: '问题提报'
          },
          children: [
            {
              path: 'equipmentSearch/',
              name: 'equipmentSearch',
              component: EquipmentSearch,
              meta: {
                title: '选择设备'
              }
            }
          ]
        },
        {
          path: 'myFault/:type',
          name: 'myFault',
          component: MyFault,
          meta: {
            title: '我的提报'
          },
          children: [
            {
              path: 'tbDetail/:id',
              name: 'tbDetail',
              component: TbDetail,
              meta: {
                title: '提报详情'
              },
              children: [
                {
                  path: 'reBack/:id',
                  name: 'reBack',
                  component: ReBack,
                  meta: {
                    title: '提报反馈'
                  }
                },
                {
                  path: 'shouliDteail/:id',
                  name: 'shouliDteail',
                  component: ShouliDteail,
                  meta: {
                    title: '补充提报'
                  }
                },
                {
                  path: 'assess/',
                  name: 'assess',
                  component: Assess,
                  meta: {
                    title: '提报评价'
                  }
                },
                {
                  path: 'faultEquement/',
                  name: 'faultEquement',
                  component: FaultEquement,
                  meta: {
                    title: '反馈设备'
                  }
                },
                {
                  path: 'faultStation/',
                  name: 'faultStation',
                  component: FaultStation,
                  meta: {
                    title: '反馈设备'
                  }
                }
              ]
            }
          ]
        },
        {
          path: 'handover/',
          name: 'handover',
          // component: () => import('../page/handover/index.vue'),
          component: Handover,
          meta: {
            title: '交接班看板'
          },
          children: [
            {
              path: 'transpond/:tasks',
              name: 'handover-transpond',
              // component: () => import('../page/detail/transpond.vue'),
              component: Transpond,
              meta: {
                title: '转发'
              }
            }
          ]
        },
        {
          path: 'work/',
          name: 'work',
          // component: () => import('../page/work/index.vue'),
          component: Work,
          meta: {
            title: '在班管理'
          },
          children: [
            {
              path: 'sign/:worker',
              name: 'work-sign',
              // component: () => import('../page/sign/index.vue'),
              component: Sign,
              meta: {
                // title: ''
              },
              children: [
                {
                  path: 'signhandover/',
                  name: 'work-signhandover',
                  // component: () => import('../page/handover/index.vue'),
                  component: Handover,
                  meta: {
                    title: '交接班看板'
                  }
                }
              ]
            }
          ]
        },
        {
          path: 'device/',
          name: 'device',
          // component: () => import('../page/device/index.vue'),
          component: Device,
          meta: {
            title: '设备查找'
          },
          children: [
            {
              path: 'detail/:deviceId',
              name: 'device-detail',
              // component: () => import('../page/device/detail.vue'),
              component: DeviceDetail,
              meta: {
                title: '设备详情'
              },
              children: [
                {
                  path: 'info/',
                  name: 'device-info',
                  component: DeviceInfo,
                  meta: {
                    title: '设备详情'
                  }
                },
                {
                  path: 'task/:type',
                  name: 'device-task',
                  component: Task,
                  meta: {
                    title: '历史维修记录'
                  },
                  children: [
                    {
                      path: 'detail/:id',
                      name: 'device-task-detail',
                      component: Detail,
                      meta: {
                        title: '详情'
                      }
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          path: 'statistics/',
          name: 'statistics',
          // component: () => import('../page/statistics/index.vue'),
          component: Statistics,
          meta: {
            title: '分析统计'
          }
        }
      ]
    }
  ]
})
