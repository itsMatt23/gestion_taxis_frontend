<template>
  <div class="sidebar bg-light text-dark p-4 d-flex flex-column">
    <!-- Header de la sidebar -->
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
        <h6 class="nav-section-title">Administración</h6>
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
        <h6 class="nav-section-title">Cliente</h6>
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
        <h6 class="nav-section-title">Conductor</h6>
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
    <div class="mt-auto">
      <button @click="logout" class="btn btn-dark w-100 mt-4">Cerrar Sesión</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      usuario: "",
    };
  },

  mounted() {
    this.cargarPerfil();
  },

  methods: {
    async cargarPerfil() {
      const storedUser = localStorage.getItem('userConected');
      if (storedUser) {
        this.usuario = JSON.parse(storedUser); // Convertir de JSON a objeto
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
.sidebar {
  height: 100vh;
  width: 250px;
  border-right: 1px solid #eaeaea;
  background-color: #f9f9f9;
  font-family: 'Roboto', sans-serif;
  transition: transform 0.3s ease;
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

@media (max-width: 768px) {
  .sidebar {
    width: 220px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    position: absolute;
    z-index: 1000;
  }

  .sidebar.show {
    transform: translateX(0);
  }
}
</style>
