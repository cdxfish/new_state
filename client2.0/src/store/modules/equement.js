const state = {
  equement: [],
  name: '',
  falut: {}
}

const getters = {
  equement: state => state.equement,
  name: state => state.name,
  falut: state => state.falut
}

const actions = {
  changeEuement ({ commit, state }, equement) {
    commit('changeEuement', equement)
  },
  changeName ({ commit, state }, name) {
    commit('changeName', name)
  },
  falutDetail ({ commit, state }, falut) {
    commit('falutDetail', falut)
  }
}

const mutations = {
  changeEuement (state, equement) {
    state.equement = equement
  },
  changeName (state, name) {
    state.name = name
  },
  falutDetail (state, falut) {
    state.falut = falut
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
