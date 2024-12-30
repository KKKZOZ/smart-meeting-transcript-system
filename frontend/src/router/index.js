import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../views/Dashboard.vue';
import Tables from '../views/Tables.vue';
import Billing from '../views/Billing.vue';
import VirtualReality from '../views/VirtualReality.vue';
import RTL from '../views/Rtl.vue';
import Profile from '../views/Profile.vue';
import Signup from '../views/Signup.vue';
import Signin from '../views/Signin.vue';
import NewPage from '../views/NewPage.vue';
import TranscriptPage from '../views/TranscriptPage.vue';
import CreateTrans from '../views/CreateTrans.vue';
import Summary from '../views/Summary.vue';
import Tasks from '../views/Tasks.vue';
import Notifications from '../views/Notifications.vue';
// import SummaryCreate from '../views/SummaryCreate.vue';

const routes = [
    {
        path: '/',
        name: '/',
        redirect: '/dashboard-default',
    },
    {
        path: '/dashboard-default',
        name: 'Dashboard',
        component: Dashboard,
    },
    {
        path: '/tables',
        name: 'Tables',
        component: Tables,
    },
    {
        path: '/billing',
        name: 'Billing',
        component: Billing,
    },
    {
        path: '/virtual-reality',
        name: 'Virtual Reality',
        component: VirtualReality,
    },
    {
        path: '/rtl-page',
        name: 'RTL',
        component: RTL,
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile,
    },
    {
        path: '/signin',
        name: 'Signin',
        component: Signin,
    },
    {
        path: '/signup',
        name: 'Signup',
        component: Signup,
    },
    {
        path: '/new-page',
        name: 'NewPage',
        component: NewPage,
    },
    {
        path: '/transcript-page',
        name: 'TranscriptPage',
        component: TranscriptPage,
    },
    {
        path: '/create-trans',
        name: 'CreateTrans',
        component: CreateTrans,
    },
    {
        path: '/summary',
        name: 'summary',
        component: Summary,
    },
    {
        path: '/tasks',
        name: 'tasks',
        component: Tasks,
    },
    {
        path: '/notifications',
        name: 'Notifications',
        component: Notifications,
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
    linkActiveClass: 'active',
});

export default router;
