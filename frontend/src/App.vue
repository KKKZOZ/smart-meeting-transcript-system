<!--
=========================================================
* Vue Argon Dashboard 2 - v4.0.0
=========================================================

* Product Page: https://creative-tim.com/product/vue-argon-dashboard
* Copyright 2024 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
-->
<script setup>
    import { computed } from 'vue';
    import { useStore } from 'vuex';
    import Sidenav from './examples/Sidenav';
    import Navbar from '@/examples/Navbars/Navbar.vue';
    import AppFooter from '@/examples/Footer.vue';
    import { useRoute } from 'vue-router';

    const route = useRoute();
    const store = useStore();
    const isNavFixed = computed(() => store.state.isNavFixed);
    const darkMode = computed(() => store.state.darkMode);
    const isAbsolute = computed(() => store.state.isAbsolute);
    const showSidenav = computed(() => store.state.showSidenav);
    const layout = computed(() => store.state.layout);
    const showNavbar = computed(() => store.state.showNavbar);
    const showFooter = computed(() => store.state.showFooter);
    const showConfig = computed(() => store.state.showConfig);
    const hideConfigButton = computed(() => store.state.hideConfigButton);
    const toggleConfigurator = () => store.commit('toggleConfigurator');

    const navClasses = computed(() => {
        return {
            'position-sticky bg-white left-auto top-2 z-index-sticky':
                isNavFixed.value && !darkMode.value,
            'position-sticky bg-default left-auto top-2 z-index-sticky':
                isNavFixed.value && darkMode.value,
            'position-absolute px-4 mx-0 w-100 z-index-2': isAbsolute.value,
            'px-0 mx-4': !isAbsolute.value,
        };
    });
    async function initAuth() {
        await store.dispatch('auth/initAuth');
    }

    initAuth();
    const shouldShowSidenav = computed(() => {
        const authRoutes = ['/signin', '/signup'];
        return showSidenav.value && !authRoutes.includes(route.path);
    });
</script>
<template>
    <div class="wrapper">
        <div
            v-show="layout === 'landing'"
            class="landing-bg h-100 bg-gradient-primary position-fixed w-100"
        ></div>

        <sidenav v-if="shouldShowSidenav" />

        <main class="main-content position-relative border-radius-lg">
            <!-- nav -->
            <navbar :class="[navClasses]" v-if="showNavbar" />

            <div class="content-wrapper">
                <router-view />
            </div>

            <app-footer v-show="showFooter" />
        </main>
    </div>
</template>

<style>
    .wrapper {
        min-height: 100vh;
        display: flex;
    }

    .main-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    .content-wrapper {
        flex: 1;
        padding-bottom: 2rem; /* 为 footer 留出空间 */
    }

    /* 如果 app-footer 组件内还没有设置样式，需要在 app-footer 组件中添加： */
    .footer {
        margin-top: auto;
        width: 100%;
        padding: 1rem 0;
    }
</style>
