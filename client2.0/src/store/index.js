import Vue from 'vue'
import Vuex from 'vuex'
import user from './modules/user'
import equement from './modules/equement'
import plan from './modules/plan'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  modules: {
    equement,
    user,
    plan
  },
  strict: debug
})
