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
  transition: transform 0.3s ease;
}

.content {
  padding: 20px;
  overflow-y: auto;
  flex-grow: 1;
}

/* Estilos responsivos */
@media (max-width: 768px) {
  #color {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    position: fixed;
    top: 0;
    left: -250px; /* Inicialmente oculta */
    transform: translateX(-100%); /* Para ocultar */
  }

  .sidebar.show {
    left: 0;
    transform: translateX(0); /* Mostrar la barra lateral */
  }

  .content {
    padding-top: 70px; /* Para que no se oculte debajo de la barra lateral */
  }
}
</style>

  