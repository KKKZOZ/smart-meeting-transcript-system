<script setup>
    import { ref, onBeforeMount, onBeforeUnmount } from 'vue';
    import { useRouter } from 'vue-router';
    import { useStore } from 'vuex';
    import { authService } from '@/services/authService';
    import Navbar from '@/examples/PageLayout/Navbar.vue';
    import AppFooter from '@/examples/PageLayout/Footer.vue';
    import ArgonInput from '@/components/ArgonInput.vue';
    import ArgonCheckbox from '@/components/ArgonCheckbox.vue';
    import ArgonButton from '@/components/ArgonButton.vue';
    import backgroundImage from '@/assets/img/background.jpeg'; // 导入背景图片

    const body = document.getElementsByTagName('body')[0];

    const router = useRouter();
    const store = useStore();

    // 表单数据
    const formData = ref({
        username: '',
        email: '',
        password: '',
        nickname: '',
        confirmPassword: '',
    });

    // 错误信息
    const error = ref('');

    // 登录方法
    const handleRegister = async () => {
        try {
            if (formData.value.password !== formData.value.confirmPassword) {
                error.value = '两次输入的密码不一致';
                return;
            }

            console.log('提交的表单数据：', formData.value);
            error.value = '';
            const response = await authService.register({
                username: formData.value.username,
                email: formData.value.email,
                password: formData.value.password,
                nickname: formData.value.nickname,
            });

            console.log('Register Response:', response);

            if (response.access_token) {
                alert('注册成功，已为您自动登录');
                router.push('/dashboard-default');
            }
        } catch (err) {
            error.value = err.message || '注册失败，请重试';
        }
    };

    onBeforeMount(() => {
        store.state.hideConfigButton = true;
        store.state.showNavbar = false;
        store.state.showSidenav = false;
        store.state.showFooter = false;
        body.classList.remove('bg-gray-100');
    });
    onBeforeUnmount(() => {
        store.state.hideConfigButton = false;
        store.state.showNavbar = true;
        store.state.showSidenav = true;
        store.state.showFooter = true;
        body.classList.add('bg-gray-100');
    });
</script>
<template>
    <div class="container top-0 position-sticky z-index-sticky">
        <div class="row">
            <div class="col-12">
                <navbar isBtn="bg-gradient-light" />
            </div>
        </div>
    </div>
    <main class="main-content mt-0">
        <div
            class="page-header align-items-start min-vh-50 pt-5 pb-11 m-3 border-radius-lg"
            :style="{
                backgroundImage: `url(${backgroundImage})`,
                backgroundPosition: 'bottom',
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat',
                minHeight: '800px',
            }"
        >
            <span class="mask bg-gradient-dark opacity-6"></span>
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-5 text-center mx-auto">
                        <h1 class="text-white mb-2 mt-5">Welcome!</h1>
                        <p class="text-lead text-white"> 欢迎使用智能会议转录系统 </p>
                    </div>
                </div>
            </div>
        </div>
        <div class="container">
            <div class="row mt-lg-n10 mt-md-n11 mt-n10 justify-content-center">
                <div class="col-xl-4 col-lg-5 col-md-7 mx-auto">
                    <div class="card z-index-0">
                        <div class="card-header text-center pt-4">
                            <h5>Register with</h5>
                        </div>

                        <div class="card-body">
                            <form role="form" @submit.prevent="handleRegister">
                                <argon-input
                                    id="name"
                                    type="text"
                                    placeholder="Name"
                                    aria-label="Name"
                                    v-model="formData.username"
                                />
                                <argon-input
                                    id="nickname"
                                    type="text"
                                    placeholder="Nickname"
                                    aria-label="Nickname"
                                    v-model="formData.nickname"
                                />
                                <argon-input
                                    id="email"
                                    type="email"
                                    placeholder="Email"
                                    aria-label="Email"
                                    v-model="formData.email"
                                />
                                <argon-input
                                    id="password"
                                    type="password"
                                    placeholder="Password"
                                    aria-label="Password"
                                    v-model="formData.password"
                                />
                                <argon-input
                                    id="confirmPassword"
                                    type="password"
                                    placeholder="Confirm Password"
                                    aria-label="Confirm Password"
                                    v-model="formData.confirmPassword"
                                />
                                <argon-checkbox checked>
                                    <label class="form-check-label" for="flexCheckDefault">
                                        I agree the
                                        <a href="javascript:;" class="text-dark font-weight-bolder"
                                            >Terms and Conditions</a
                                        >
                                    </label>
                                </argon-checkbox>

                                <p v-if="error" class="text-danger text-sm mt-2">{{ error }}</p>

                                <div class="text-center">
                                    <argon-button
                                        fullWidth
                                        type="submit"
                                        color="dark"
                                        variant="gradient"
                                        class="my-4 mb-2"
                                        >Sign up</argon-button
                                    >
                                </div>
                                <p class="text-sm mt-3 mb-0">
                                    Already have an account?
                                    <a href="javascript:;" class="text-dark font-weight-bolder"
                                        >Sign in</a
                                    >
                                </p>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    <app-footer />
</template>
