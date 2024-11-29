import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    avatar: '',
    typevalue: '',
    roles: ''
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_TYPEVALUE(state, typevalue) {
    state.typevalue = typevalue
  },
  SET_ROLES(state, roles) {
    state.roles = roles
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const { data } = response
        console.log(data)
        const token = data.access
        commit('SET_TOKEN', token)
        commit('SET_NAME', username)
        setToken(token)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(response => {
        const { data } = response
        // console.log(data)
        if (!data) {
          return reject('Verification failed, please Login again.')
        }

        const { username, typevalue, roles } = data
        console.log('成功获取！')
        console.log(data)
        commit('SET_NAME', username)
        // commit('SET_AVATAR', avatar)
        commit('SET_ROLES', roles)
        commit('SET_TYPEVALUE', typevalue)

        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout(state.token).then(() => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // logout({ commit }) {
  //   return new Promise((resolve, reject) => {
  //     // 移除 Token
  //     removeToken()
  //     commit('RESET_STATE')
  //     // 重置路由
  //     resetRouter()
  //     resolve()
  //   })
  // },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

