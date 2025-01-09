<template>
  <div class="sidebar-container">
    <!-- Barra lateral que se muestra siempre en pantallas grandes y se puede togglear en pequeñas -->
    <div :class="{'sidebar': true, 'sidebar-visible': isSidebarVisible, 'd-md-block': isDesktop, 'd-none': !isSidebarVisible && !isDesktop}">
      <div class="sidebar-header d-flex flex-column align-items-start mb-4">
        <h5 class="sidebar-title mt-1">Bienvenido</h5>
        <h6 v-if="usuario" class="sidebar-title2 text-muted">
          {{ usuario.nombre }} | {{ usuario.rol }}
        </h6>
      </div>

      <!-- Sección de enlaces -->
      <ul class="nav flex-column">
        <!-- Pantallas del Admin -->
        <div v-if="usuario && usuario.rol == 'Admin'" class="mb-4">
          <li class="nav-item">
            <router-link to="/AdminRegistro" class="nav-link">
              <i class="fas fa-user-plus"></i> Registro de viajes
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/AdminPerfil" class="nav-link">
              <i class="fas fa-user-cog"></i> Perfil
            </router-link>
          </li>
        </div>

        <!-- Pantallas del Cliente -->
        <div v-if="usuario && usuario.rol == 'Cliente'" class="mb-4">
          <li class="nav-item">
            <router-link to="/ClienteViaje" class="nav-link">
              <i class="fas fa-car"></i> Viaje
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/ClienteHistorial" class="nav-link">
              <i class="fas fa-history"></i> Historial de Viajes
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/ClientePerfil" class="nav-link">
              <i class="fas fa-user"></i> Perfil
            </router-link>
          </li>
        </div>

        <!-- Pantallas del Conductor -->
        <div v-if="usuario && usuario.rol == 'Conductor'" class="mb-4">
          <li class="nav-item">
            <router-link to="/ConductorViaje" class="nav-link">
              <i class="fas fa-road"></i> Viaje
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/ConductorHistorial" class="nav-link">
              <i class="fas fa-history"></i> Historial de Viajes
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/ConductorPerfil" class="nav-link">
              <i class="fas fa-user"></i> Perfil
            </router-link>
          </li>
        </div>
      </ul>

      <!-- Cerrar sesión -->
      <div class="d-flex flex-column" style="height: 55vh;">
      <div class="mt-auto">
        <button @click="logout" class="btn btn-dark w-100 mt-3">Cerrar Sesión</button>
      </div>
    </div>
    </div>

    <nav class="navbar navbar-dark d-md-none" style="background-color: #000;" ref="navbar">
  <div class="container-fluid d-flex justify-content-center align-items-center">
    <!-- Botón para abrir la barra lateral -->
    <button @click="toggleSidebar" class="btn btn-dark ms-1">
      <i class="fas fa-bars"></i>
    </button>
    <!-- Nombre de Uber centrado -->
    <span class="navbar-brand">Uber</span>
  </div>
</nav>

    
  </div>
</template>


<script>
export default {
  data() {
    return {
      usuario: "",
      isDesktop: false,
      isSidebarVisible: false // Controlar la visibilidad de la barra lateral solo en móviles
    };
  },

  mounted() {
    this.cargarPerfil();
    this.checkScreenSize(); // Llama a este método al montar el componente
    window.addEventListener('resize', this.checkScreenSize); // Asegura que el cambio de tamaño se maneje correctamente
    document.addEventListener('click', this.handleClickOutside);
  },

  // Cambia `beforeDestroy` a `beforeUnmount`
  beforeUnmount() {
    window.removeEventListener('resize', this.checkScreenSize);
  },

  methods: {
    async cargarPerfil() {
      const storedUser = localStorage.getItem('userConected');
      if (storedUser) {
        this.usuario = JSON.parse(storedUser); // Convertir de JSON a objeto
      }
    },

    checkScreenSize() {
      this.isDesktop = window.innerWidth > 768; // 768px es el límite para móvil
      if (this.isDesktop) {
        this.isSidebarVisible = true; // Asegura que la barra lateral esté visible en pantallas grandes
      } else {
        this.isSidebarVisible = false; // Oculta la barra lateral en pantallas pequeñas por defecto
      }
    },

    toggleSidebar() {
      event.stopPropagation();
      this.isSidebarVisible = !this.isSidebarVisible; // Alternar la visibilidad en pantallas pequeñas
    },

    handleClickOutside(event) {
      // Verificar si el clic fue fuera del AppBar
      const navbar = this.$refs.navbar;
      if (navbar && !navbar.contains(event.target)) {
        this.isSidebarVisible = false; // Cerrar el sidebar si se hace clic fuera
      }
    },

    logout() {
      const confirmed = confirm("¿Estás seguro de que deseas cerrar la sesión?");
      if (confirmed) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("userConected");
        alert("Sesión cerrada correctamente");
        this.$router.push({ name: "Login" });
      }
    }
  }
};
</script>

<style scoped>
.sidebar-container {
  display: flex;
  flex-direction: column;
}

.sidebar {
  background-color: #F9F9F9; /* Fondo de la barra lateral */
  padding: 20px;
  height: 100vh; /* Asegura que la barra lateral ocupe toda la altura de la pantalla */
  overflow-y: auto; /* Agrega scroll si es necesario */
  position: fixed; /* Fija la barra lateral */
  top: 0;
  left: 0;
  z-index: 1000; /* Asegura que esté por encima de otros elementos */
  transition: all 0.3s ease; /* Transición suave al mostrar/ocultar */
}

.sidebar-header {
  margin-bottom: 20px;
}

.sidebar-title {
  font-size: 1.3rem;
  color: #212529; /* Color del texto del título */
  font-weight: 500;
}

.sidebar-title2 {
  font-size: 1.0rem;
  color: #6c757d; /* Color del texto secundario */
}

.nav-section-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 10px;
  color: #1f1f1f;
}

.nav-link {
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #212529; /* Color del texto de los enlaces */
  font-size: 1rem;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.nav-link:hover {
  background-color: #f1f1f1;
  color: #000;
}

.nav-item .nav-link i {
  font-size: 1.2rem;
}

.nav-link.active {
  color: white;
}

.btn {
  font-size: 1.1rem;
  padding: 12px;
  border-radius: 6px;
  background-color: #000; /* Color del botón */
  color: white;
  border: none;
}

.btn:hover {
  background-color: #333; /* Color al pasar el ratón sobre el botón */
}

.mt-auto {
  margin-top: auto;
}

/* Ajustes para pantallas pequeñas */
@media (max-width: 768px) {
  .sidebar {
    width: 250px; /* Ancho de la barra lateral en móviles */
    transform: translateX(-100%);
  }

  .sidebar-visible {
    transform: translateX(0);
  }
}
</style>