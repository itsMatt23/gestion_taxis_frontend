<template>
  <div class="d-flex" id="app-container">
    <!-- Barra lateral -->
    <Sidebar v-if="isSidebarVisible" class="sidebar" />

    <!-- Contenido principal -->
    <div class="content flex-grow-1 overflow-auto">
      <!-- Botón para mostrar/ocultar la barra lateral -->
      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=menu" />
      <button 
        class="btn btn-toggle-sidebar d-md-none" 
        @click="toggleSidebar">
        <i class="fas fa-bars"></i>
      </button>

      <!-- Vista dinámica (contenido) -->
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
  data() {
    return {
      isSidebarVisible: true, // Controla si la barra lateral es visible
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible;
    },
  },
};
</script>


<style scoped>
#app-container {
  display: flex;
  background-color: #f0f0f0;
  height: 100vh;
}

.content {
  padding: 20px;
  flex-grow: 1;
  overflow-y: auto;
}

/* Botón de menú */
.btn-toggle-sidebar {
  position: absolute;
  top: 15px;
  left: 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Asegura que el botón esté encima */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-toggle-sidebar:hover {
  background-color: #0056b3;
}

/* Esconde el botón en pantallas grandes */
@media (min-width: 768px) {
  .btn-toggle-sidebar {
    display: none;
  }
}
</style>
