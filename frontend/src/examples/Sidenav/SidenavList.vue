<script setup>
    import { computed, onMounted } from 'vue';
    import { useRoute } from 'vue-router';
    import { useStore } from 'vuex';

    import SidenavItem from './SidenavItem.vue';

    const store = useStore();
    const isRTL = computed(() => store.state.isRTL);

    const getRoute = () => {
        const route = useRoute();
        const routeArr = route.path.split('/');
        return routeArr[1];
    };

    const unreadCount = computed(() => store.state.notifications.unreadCount);
    const userRoot = computed(() => store.state.auth?.user?.root || false);

    onMounted(() => {
        const publicPages = ['signin', 'signup'];
        if (!publicPages.includes(getRoute())) {
            store.dispatch('fetchUnreadCount');
        }
    });
</script>
<template>
    <div class="collapse navbar-collapse w-auto h-auto h-100" id="sidenav-collapse-main">
        <ul class="navbar-nav">
            <li class="nav-item">
                <sidenav-item
                    to="/dashboard-default"
                    :class="getRoute() === 'dashboard-default' ? 'active' : ''"
                    :navText="isRTL ? 'لوحة القيادة' : 'Dashboard'"
                >
                    <template v-slot:icon>
                        <i class="ni ni-tv-2 text-primary text-sm opacity-10"></i>
                    </template>
                </sidenav-item>
            </li>

            <li class="nav-item">
                <sidenav-item
                    to="/meetings"
                    :class="getRoute() === 'meetings' ? 'active' : ''"
                    :navText="isRTL ? 'صفحة جديدة' : 'Meetings'"
                >
                    <template v-slot:icon>
                        <i class="ni ni-calendar-grid-58 text-warning text-sm opacity-10"></i>
                    </template>
                </sidenav-item>
            </li>

            <!-- <li class="nav-item">
                <sidenav-item
                    to="/create-trans"
                    :class="getRoute() === 'create-trans' ? 'active' : ''"
                    :navText="isRTL ? 'صفحة جديدة' : 'Transcript'"
                >
                    <template v-slot:icon>
                        <i class="ni ni-calendar-grid-58 text-warning text-sm opacity-10"></i>
                    </template>
                </sidenav-item>
            </li> -->

            <li class="nav-item">
                <sidenav-item
                    to="/summary"
                    :class="getRoute() === 'summary' ? 'active' : ''"
                    :navText="isRTL ? 'صفحة جديدة' : 'Summary'"
                >
                    <template v-slot:icon>
                        <i class="ni ni-calendar-grid-58 text-warning text-sm opacity-10"></i>
                    </template>
                </sidenav-item>
            </li>

            <li class="nav-item">
                <sidenav-item
                    to="/tasks"
                    :class="getRoute() === 'tasks' ? 'active' : ''"
                    :navText="isRTL ? 'صفحة جديدة' : 'Tasks'"
                >
                    <template v-slot:icon>
                        <i class="ni ni-calendar-grid-58 text-warning text-sm opacity-10"></i>
                    </template>
                </sidenav-item>
            </li>

            <li class="nav-item">
                <sidenav-item
                    to="/notifications"
                    :class="getRoute() === 'notifications' ? 'active' : ''"
                    :navText="isRTL ? 'صفحة جديدة' : 'Notifications'"
                >
                    <template v-slot:icon>
                        <div class="position-relative">
                            <i class="ni ni-calendar-grid-58 text-warning text-sm opacity-10"></i>
                            <span
                                v-if="unreadCount > 0"
                                class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                            >
                                {{ unreadCount > 99 ? '99+' : unreadCount }}
                            </span>
                        </div>
                    </template>
                </sidenav-item>
            </li>

            <li v-if="userRoot" class="nav-item">
                <sidenav-item
                    to="/manage"
                    :class="getRoute() === 'manage' ? 'active' : ''"
                    :navText="isRTL ? 'إدارة' : 'Manage'"
                >
                    <template v-slot:icon>
                        <i class="ni ni-settings text-info text-sm opacity-10"></i>
                    </template>
                </sidenav-item>
            </li>

            <li class="mt-3 nav-item">
                <h6
                    v-if="isRTL"
                    class="text-xs ps-4 text-uppercase font-weight-bolder opacity-6"
                    :class="isRTL ? 'me-4' : 'ms-2'"
                >
                    صفحات المرافق
                </h6>

                <h6
                    v-else
                    class="text-xs ps-4 text-uppercase font-weight-bolder opacity-6"
                    :class="isRTL ? 'me-4' : 'ms-2'"
                >
                    ACCOUNT PAGES
                </h6>
            </li>
            <!-- 
            <li class="nav-item">
                <sidenav-item
                    to="/profile"
                    :class="getRoute() === 'profile' ? 'active' : ''"
                    :navText="isRTL ? 'حساب تعريفي' : 'Profile'"
                >
                    <template v-slot:icon>
                        <i class="ni ni-single-02 text-dark text-sm opacity-10"></i>
                    </template>
                </sidenav-item>
            </li>

            <li class="nav-item">
                <sidenav-item
                    to="/signin"
                    :class="getRoute() === 'signin' ? 'active' : ''"
                    :navText="isRTL ? 'تسجيل الدخول' : 'Sign In'"
                >
                    <template v-slot:icon>
                        <i class="ni ni-single-copy-04 text-danger text-sm opacity-10"></i>
                    </template>
                </sidenav-item>
            </li>

            <li class="nav-item">
                <sidenav-item
                    to="/signup"
                    :class="getRoute() === 'signup' ? 'active' : ''"
                    :navText="isRTL ? 'اشتراك' : 'Sign Up'"
                >
                    <template v-slot:icon>
                        <i class="ni ni-collection text-info text-sm opacity-10"></i>
                    </template>
                </sidenav-item>
            </li>
            -->
        </ul>
    </div>
</template>

<style scoped>
    .badge {
        font-size: 0.65rem;
        padding: 0.25em 0.4em;
        transform: translate(-50%, -50%);
    }
</style>
