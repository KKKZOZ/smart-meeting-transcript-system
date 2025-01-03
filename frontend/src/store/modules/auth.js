import authService from '@/services/authService'

export default {
    namespaced: true,
    state: {
        isLoggedIn: !!localStorage.getItem('token'),
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
        async initAuth({ commit }) {
            console.log('initAuth');
            const token = localStorage.getItem('token');
            console.log('token',token);
            if (token) {
                try {
                    commit('SET_TOKEN', token);
                    const user = await authService.getUserInfo()
                    commit('SET_USER', user)
                    commit('SET_LOGIN_STATE', true)
                } catch (error) {
                    localStorage.removeItem('token')
                    commit('SET_TOKEN', null)
                    commit('SET_USER', null)
                    commit('SET_LOGIN_STATE', false)
                }
            }
        },
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
            localStorage.removeItem('token')
            commit('SET_TOKEN', null)
            commit('SET_USER', null)
            commit('SET_LOGIN_STATE', false)
        }
    }
} 