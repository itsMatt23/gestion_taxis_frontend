<template>
    <div class="sidebar bg-white text-dark p-3 d-flex flex-column">
      <div class="sidebar-header d-flex flex-column align-items-start">
        <h5 class="sidebar-title mt-1">Bienvenido</h5>
        <h5 v-if="usuario" class="sidebar-title2">
          {{ usuario.nombre }} | {{ usuario.rol }}
        </h5>
      </div>
  
      <ul class="nav flex-column mt-3">  
        <div v-if="usuario && usuario.rol == 'Admin'">
        <li class="nav-item">
          <router-link to="/AdminRegistro" class="nav-link text-dark">
            <i class="fas fa-tachometer-alt"></i> Registro
          </router-link>
        </li>
  
        <li class="nav-item">
          <router-link to="/perfil_admin" class="nav-link text-dark">
            <i class="fas fa-tachometer-alt"></i> Perfil
          </router-link>
        </li>
      </div>
      </ul>
  
      <div class="mt-auto">
        <button @click="logout" class="btn btn-dark w-100 mt-2">Cerrar Sesión</button>
      </div>
    </div>
  </template>
  
  <script>
  
  export default {
    data() {
      return {
        usuario: "",
        errorMessage: ''
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
    border-right: 1px solid #ddd;
    box-sizing: border-box;
  }
  
  .sidebar-header {
    font-weight: bold;
  }
  
  .sidebar-title {
    margin: 0;
    font-size: 1.2em;
  }
  
  .sidebar-title2 {
    margin: 0;
    font-size: 1.0em;
  }
  
  .nav-link {
    padding: 8px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: background-color 0.3s;
    border-radius: 5px;
  }
  
  .nav-link.active {
    background-color: #343a40;
    color: white;
  }
  
  .nav-link:hover {
    background-color: #f0f0f0;
  }
  </style>
  