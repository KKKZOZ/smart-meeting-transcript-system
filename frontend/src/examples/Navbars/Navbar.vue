<script setup>
    import { computed, ref } from 'vue';
    import { useStore } from 'vuex';
    import { useRoute, useRouter } from 'vue-router';
    import Breadcrumbs from '../Breadcrumbs.vue';

    const showMenu = ref(false);
    const store = useStore();
    const router = useRouter();
    const isRTL = computed(() => store.state.isRTL);
    const isLoggedIn = computed(() => store.state.auth?.isLoggedIn || false);
    const username = computed(() => {
        console.log('auth state:', store.state.auth?.user?.username);
        console.log('auth state:', store.state.auth);
        return store.state.auth?.user?.username || '未登录';
    });

    const route = useRoute();

    const currentRouteName = computed(() => {
        return route.name;
    });
    const currentDirectory = computed(() => {
        let dir = route.path.split('/')[1];
        return dir.charAt(0).toUpperCase() + dir.slice(1);
    });

    const handleUsernameClick = () => {
        if (username.value !== '未登录') {
            router.push('/profile');
        }
    };

    const handleLogoutAction = () => {
        if (isLoggedIn.value) {
            store.dispatch('auth/logout');
            router.push({ name: 'Signin' });
        }
    };
</script>

<template>
    <nav
        class="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl"
        :class="isRTL ? 'top-0 position-sticky z-index-sticky' : ''"
        v-bind="$attrs"
        id="navbarBlur"
        data-scroll="true"
    >
        <div class="px-3 py-1 container-fluid">
            <breadcrumbs :current-page="currentRouteName" :current-directory="currentDirectory" />

            <div
                class="mt-2 collapse navbar-collapse mt-sm-0 me-md-0 me-sm-4"
                :class="isRTL ? 'px-0' : 'me-sm-4'"
                id="navbar"
            >
                <div
                    class="pe-md-3 d-flex align-items-center"
                    :class="isRTL ? 'me-md-auto' : 'ms-md-auto'"
                >
                </div>

                <ul class="navbar-nav justify-content-end">
                    <li class="nav-item d-flex align-items-center me-3">
                        <span
                            class="nav-link font-weight-bold text-white cursor-pointer"
                            @click="handleUsernameClick"
                            :style="{ cursor: username !== '未登录' ? 'pointer' : 'default' }"
                        >
                            {{ username }}
                        </span>
                    </li>
                    <li class="nav-item d-flex align-items-center">
                        <a
                            v-if="isLoggedIn"
                            @click="handleLogoutAction"
                            class="px-0 nav-link font-weight-bold text-white cursor-pointer"
                        >
                            <i class="fa fa-user" :class="isRTL ? 'ms-sm-2' : 'me-sm-2'"></i>
                            <span v-if="isRTL" class="d-sm-inline d-none">تسجيل خروج</span>
                            <span v-else class="d-sm-inline d-none">Log Out</span>
                        </a>
                        <router-link
                            v-else
                            :to="{ name: 'Signin' }"
                            class="px-0 nav-link font-weight-bold text-white"
                        >
                            <i class="fa fa-user" :class="isRTL ? 'ms-sm-2' : 'me-sm-2'"></i>
                            <span v-if="isRTL" class="d-sm-inline d-none">يسجل دخول</span>
                            <span v-else class="d-sm-inline d-none">Sign In</span>
                        </router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<style scoped>
    .cursor-pointer {
        cursor: pointer;
    }
</style>
