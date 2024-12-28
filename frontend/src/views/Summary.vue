<template>
    <div>
        <input type="text" v-model="searchQuery" placeholder="搜索历史会议..." />
        <button @click="search">
            <img src="@/assets/img/magnifier.png" alt="Search" />
        </button>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                searchQuery: '',
            };
        },
        methods: {
            search() {
                console.log('Searching for:', this.searchQuery);
            },
        },
    };
</script>

<style scoped>
    input {
        width: calc(100% - 500px);
        position: relative;
        left: 40px;
        padding: 10px 20px;
        margin: 10px 0;
        box-sizing: border-box;
        border-radius: 20px;
    }
    button {
        width: 40px;
        height: 40px;
        background: none;
        border: none;
        cursor: pointer;
        position: relative;
        left: 40px;
        padding: 0;
        margin-left: 10px;
    }

    button img {
        width: 100%;
        height: 100%;
    }
</style>
