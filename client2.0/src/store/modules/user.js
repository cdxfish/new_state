const state = {
  userInfo: {},
  islogin: false,
  token: null,
  uf: {}

}

const getters = {
  userInfo: state => state.userInfo,
  uf: state => state.uf
}

const actions = { changeuf ({ commit, state }, uf) {
  commit('changeuf', uf)
}
}

const mutations = {
  changeuf (state, uf) {
    state.uf = uf
  },

  changeLoginSataus (state, bool) {
    state.islogin = bool
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
