<template>
  <div class="d-flex" id="color">
    <Sidebar :isVisible="isSidebarVisible" />
    <div :class="['content', { 'show-sidebar': isSidebarVisible }]">
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
      isSidebarVisible: false, // Estado para controlar si el sidebar está visible
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible; // Cambiar el estado
    },
  },
};
</script>

<style scoped>
#color {
  display: flex;
  background-color: #f0f0f0;
  height: 100vh;
  flex-direction: row; /* Asegura que en pantallas grandes, todo esté en una fila */
}

/* Estilos para el sidebar en pantallas grandes */
.sidebar {
  height: 100vh;
  border-right: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  transition: transform 0.3s ease;
  width: 250px; /* Ancho fijo del sidebar */
}

.content {
  padding: 20px;
  overflow-y: auto;
  flex-grow: 1;
  margin-left: 250px; /* Deja espacio para el sidebar en pantallas grandes */
  transition: margin-left 0.3s ease;
}

/* Estilos para pantallas pequeñas (responsivo) */
@media (max-width: 768px) {
  #color {
    flex-direction: column; /* Cambia a columna en pantallas pequeñas */
  }

  .sidebar {
    width: 250px;
    position: fixed;
    top: 0;
    left: -250px; /* Inicialmente oculto */
    transform: translateX(-100%); /* Para ocultar */
    transition: transform 0.3s ease;
  }

  .sidebar.show {
    left: 0;
    transform: translateX(0); /* Muestra el sidebar */
  }

  .content {
    padding-top: 70px; /* Para que no se oculte debajo del sidebar */
    margin-left: 0; /* No tiene margen izquierdo cuando el sidebar está oculto */
  }

  .content.show-sidebar {
    margin-left: 250px; /* Cuando el sidebar está visible en pantallas pequeñas */
  }
}
</style>
