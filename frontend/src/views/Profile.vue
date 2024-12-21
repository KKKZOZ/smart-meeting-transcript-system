<script setup>
import { onBeforeMount, onMounted, onBeforeUnmount, ref } from "vue";
import { useStore } from "vuex";
import * as bootstrap from 'bootstrap';
import axios from '@/axios';  

import setNavPills from "@/assets/js/nav-pills.js";
import setTooltip from "@/assets/js/tooltip.js";
import ArgonInput from "@/components/ArgonInput.vue";
import ArgonButton from "@/components/ArgonButton.vue";

const body = document.getElementsByTagName("body")[0];

const store = useStore();

const userData = ref({
  username: '',
  email: '',
  notification_type: '',
  frequency: '',
  password: ''
});

const handlePasswordFocus = () => {
  userData.value.password = '';
  console.log("password cleared");
};

const fetchUserData = async () => {
  try {
    const response = await axios.get('/api/me');
    console.log(response.data);
    userData.value = response.data;
    userData.value.password = '********';
  } catch (error) {
    console.error('获取用户数据失败:', error);
  }
};

const handleSubmit = async () => {
  try {
    // 创建要提交的数据对象
    const updateData = {
      username: userData.value.username,
      email: userData.value.email,
      notification_type: userData.value.notification_type,
      frequency: userData.value.frequency
    };

    // 如果密码不是 8 个 * 且不为空，则添加到提交数据中
    if (userData.value.password && userData.value.password !== '********') {
      updateData.password = userData.value.password;
    }

    const response = await axios.put('/api/update-profile', updateData);
    console.log('更新成功:', response.data);
    
    // 重新获取用户数据
    await fetchUserData();
    
    // TODO: 可以添加一个成功提示
    alert('个人资料更新成功！');
  } catch (error) {
    console.error('更新用户数据失败:', error);
    // TODO: 可以添加一个错误提示
    alert('更新失败：' + (error.response?.data?.message || error.message));
  }
};

onMounted(() => {
  store.state.isAbsolute = true;
  setNavPills();
  setTooltip();
  fetchUserData();
  
  // 初始化 Bootstrap 标签页
  const tabList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tab"]'))
  tabList.forEach(function (tab) {
    new bootstrap.Tab(tab)
  })
});
onBeforeMount(() => {
  store.state.imageLayout = "profile-overview";
  store.state.showNavbar = false;
  store.state.showFooter = true;
  store.state.hideConfigButton = true;
  body.classList.add("profile-overview");
});
onBeforeUnmount(() => {
  store.state.isAbsolute = false;
  store.state.imageLayout = "default";
  store.state.showNavbar = true;
  store.state.showFooter = true;
  store.state.hideConfigButton = false;
  body.classList.remove("profile-overview");
});
</script>
<template>
  <main>
    <div class="container-fluid">
      <div
        class="page-header min-height-300"
        style="
          background-image: url(&quot;https://images.unsplash.com/photo-1531512073830-ba890ca4eba2?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80&quot;);
          margin-right: -24px;
          margin-left: -34%;
        "
      >
        <span class="mask bg-gradient-success opacity-6"></span>
      </div>
      <div class="card shadow-lg mt-n6">
        <div class="card-body p-3">
          <div class="row gx-4">
            <div class="col-auto">
              <div class="avatar avatar-xl position-relative" style="width: 150px; height: 150px; overflow: hidden; border-radius: 50%;">
                <img
                  src="../assets/img/profile.jpg"
                  alt="profile_image"
                  class="shadow-sm w-100 border-radius-lg"
                />
              </div>
            </div>
            <div class="col-auto my-auto">
              <div class="h-100">
                <h5 class="mb-1">Sayo Kravits</h5>
                <p class="mb-0 font-weight-bold text-sm">Public Relations</p>
              </div>
            </div>
            <div
              class="mx-auto mt-3 col-lg-4 col-md-6 my-sm-auto ms-sm-auto me-sm-0"
            >
              <div class="nav-wrapper position-relative end-0">
                <ul
                  class="p-1 bg-transparent nav nav-pills nav-fill"
                  role="tablist"
                >
                  <li class="nav-item">
                    <a
                      class="px-0 py-1 mb-0 nav-link active"
                      data-bs-toggle="tab"
                      href="#profile-tab"
                      role="tab"
                      aria-selected="true"
                    >
                      <span class="ms-1">用户资料</span>
                    </a>
                  </li>
                  <li class="nav-item">
                    <a
                      class="px-0 py-1 mb-0 nav-link"
                      data-bs-toggle="tab"
                      href="#meetings-tab"
                      role="tab"
                      aria-selected="false"
                    >
                      <span class="ms-1">我的会议</span>
                    </a>
                  </li>
                  
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="tab-content">
      <div class="tab-pane fade show active" id="profile-tab" role="tabpanel">
        <div class="py-4 container-fluid">
          <div class="row">
            <div class="col-md-12">
              <div class="card">
                <div class="card-header pb-0">
                  <div class="d-flex align-items-center">
                    <p class="mb-0">Edit Profile</p>
                    <argon-button 
                      color="success" 
                      size="sm" 
                      class="ms-auto"
                      @click="handleSubmit"
                    >确认修改</argon-button>
                  </div>
                </div>
                <div class="card-body">
                  <p class="text-uppercase text-sm">User Information</p>
                  <div class="row">
                    <div class="col-md-4">
                      <label for="example-text-input" class="form-control-label"
                        >Username</label
                      >
                      <argon-input type="text" v-model="userData.username" />
                    </div>
                    <div class="col-md-4">
                      <label for="example-text-input" class="form-control-label"
                        >Email address</label
                      >
                      <argon-input type="email" v-model="userData.email" />
                    </div>
                    <div class="col-md-4">
                      <label for="example-text-input" class="form-control-label"
                        >password</label
                      >
                      <argon-input 
                        type="password" 
                        v-model="userData.password"
                        @focus="handlePasswordFocus"
                      />
                    </div>
                  </div>
                  
                </div>
                <div class="card-body">
                  <p class="text-uppercase text-sm">User Settings</p>
                  <div class="row">
                    <div class="col-md-6">
                      <label for="example-text-input" class="form-control-label"
                        >通知类型</label
                      >
                      <argon-input type="notification-type" v-model="userData.notification_type" />
                    </div>
                    <div class="col-md-6">
                      <label for="example-text-input" class="form-control-label"
                        >频率</label
                      >
                      <argon-input type="frequency" v-model="userData.frequency" />
                    </div>
                    
                  </div>
                  
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="tab-pane fade" id="meetings-tab" role="tabpanel">
        <div class="py-4 container-fluid">
          <div class="row">
            <div class="col-md-12">
              <div class="card">
                <div class="card-header pb-0">
                  <h6>我的会议列表</h6>
                </div>
                <div class="card-body px-0 pt-0 pb-2">
                  <div class="table-responsive p-0">
                    <table class="table align-items-center mb-0">
                      <thead>
                        <tr>
                          <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">会议名称</th>
                          <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">日期时间</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">状态</th>
                          <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">操作</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>
                            <div class="d-flex px-2 py-1">
                              <div class="d-flex flex-column justify-content-center">
                                <h6 class="mb-0 text-sm">项目周会</h6>
                              </div>
                            </div>
                          </td>
                          <td>
                            <p class="text-xs font-weight-bold mb-0">2024-03-20 14:30</p>
                          </td>
                          <td class="align-middle text-center text-sm">
                            <span class="badge badge-sm bg-gradient-success">进行中</span>
                          </td>
                          <td class="align-middle text-center">
                            <a href="javascript:;" class="text-secondary font-weight-bold text-xs" data-toggle="tooltip" data-original-title="Edit user">
                              查看详情
                            </a>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
