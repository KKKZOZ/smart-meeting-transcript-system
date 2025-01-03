import authService from '@/services/authService'

export default {
    namespaced: true,
    state: {
        isLoggedIn: false,
        user: null,
        token: localStorage.getItem('token') || null
    },
    mutations: {
        SET_LOGIN_STATE(state, isLoggedIn) {
            state.isLoggedIn = isLoggedIn
        },
        SET_USER(state, user) {
            state.user = user
        },
        SET_TOKEN(state, token) {
            state.token = token
            if (token) {
                localStorage.setItem('token', token)
            } else {
                localStorage.removeItem('token')
            }
        }
    },
    actions: {
        async login({ commit }, credentials) {
            try {
                const response = await authService.login(credentials)
                const token = response.access_token
                commit('SET_TOKEN', token)
                commit('SET_USER', response.user)
                commit('SET_LOGIN_STATE', true)
                return Promise.resolve(response)
            } catch (error) {
                return Promise.reject(error)
            }
        },
        
        async logout({ commit }) {
            commit('SET_TOKEN', null)
            commit('SET_USER', null)
            commit('SET_LOGIN_STATE', false)
        }
    }
} 