<template>
  <div class="sidebar-container">
    <!-- Barra lateral que se muestra siempre en pantallas grandes -->
    <div :class="{'sidebar': true, 'sidebar-visible': isSidebarVisible}">
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
              <i class="fas fa-user-plus"></i> Registro
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

      <!-- Cerrar sesión (visible solo en pantallas grandes) -->
      <div class="mt-auto">
        <button v-if="isDesktop" @click="logout" class="btn btn-dark w-100 mt-4">Cerrar Sesión</button>
      </div>
    </div>

    <!-- Botón para abrir la barra lateral solo en pantallas pequeñas -->
    <button v-if="!isDesktop" @click="toggleSidebar" class="btn btn-dark d-block d-md-none w-100 mt-4">
      <i class="fas fa-bars"></i> <!-- Icono de menú -->
    </button>
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
      }
    },

    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible; // Alternar la visibilidad en pantallas pequeñas
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

/* Barra lateral que solo se muestra en dispositivos de escritorio */
.sidebar {
  display: block;
}

.sidebar-header {
  margin-bottom: 20px;
}

.sidebar-title {
  font-size: 1.3rem;
  color: #333;
  font-weight: 500;
}

.sidebar-title2 {
  font-size: 1.0rem;
  color: #666;
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
  color: #333;
  font-size: 1rem;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.nav-link:hover {
  background-color: #f1f1f1;
  color: #007bff;
}

.nav-item .nav-link i {
  font-size: 1.2rem;
}

.nav-link.active {
  background-color: #007bff;
  color: white;
}

.btn {
  font-size: 1.1rem;
  padding: 12px;
  border-radius: 6px;
  background-color: #333;
  color: white;
}

.btn:hover {
  background-color: #555;
}

.mt-auto {
  margin-top: auto;
}

/* Barra lateral visible solo en pantallas grandes */
@media (min-width: 769px) {
  .sidebar {
    display: block; /* Barra lateral visible siempre en pantallas grandes */
  }

  .btn {
    display: block; /* Mostrar el botón solo en pantallas grandes */
  }

  .btn.d-block {
    display: none; /* El botón de menú se oculta en pantallas grandes */
  }
}

@media (max-width: 768px) {
  /* En pantallas pequeñas, la barra lateral se muestra solo cuando se hace clic */
  .sidebar {
    display: none; /* Oculta la barra lateral por defecto en móviles */
  }

  .sidebar-visible {
    display: block; /* Muestra la barra lateral cuando isSidebarVisible es verdadero */
  }

  .btn {
    display: none; /* Ocultar el botón de "Cerrar sesión" en pantallas pequeñas */
  }
}
</style>
