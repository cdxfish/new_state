const state = {
  people: [],
  status: '',
  plan: {}
}

const getters = {
  people: state => state.people,
  status: state => state.status,
  plan: state => state.plan
}

const actions = {
  changePeople ({ commit, state }, people) {
    commit('changePeople', people)
  },
  changeStatus ({ commit, state }, status) {
    commit('changeStatus', status)
  },
  falutPlan ({ commit, state }, plan) {
    commit('falutPlan', plan)
  }
}

const mutations = {
  changePeople (state, people) {
    state.people = people
  },
  changeStatus (state, status) {
    state.status = status
  },
  falutPlan (state, plan) {
    state.plan = plan
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
