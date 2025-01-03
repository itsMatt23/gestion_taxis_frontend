<template>
    <div class="d-flex" id="color">
      <Sidebar />
      <div class="content flex-grow-1 overflow-auto">
        <router-view />
      </div>
    </div>
  </template>
  
  <script>
  import Sidebar from '@/components/AppSidebar.vue';
  
  export default {
    components: {
      Sidebar,
    },
  };
  </script>
  
  <style scoped>
  #color {
    display: flex;
    background-color: #f0f0f0;
    height: 100vh;
  }
  
  .sidebar {
    height: 100vh;
    border-right: 1px solid #ddd;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }
  
  .content {
    padding: 20px;
    overflow-y: auto;
    flex-grow: 1;
  }
  </style>
  