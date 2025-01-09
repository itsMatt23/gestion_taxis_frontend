<template>
  <!-- Barra de tareas -->
  <header class="navbar">
    <nav class="container-fluid d-flex align-items-center justify-content-between">
      <div class="d-flex align-items-center">
        <router-link class="nav2" to="/">Uber</router-link>
        <!-- Menú Hamburguesa -->
        <button
          class="navbar-toggler d-lg-none"
          type="button"
          @click="toggleMenu"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div
          :class="['collapse', 'navbar-collapse', { show: isMenuOpen }]"
        >
          <ul class="nav flex-column flex-lg-row">
            <li class="nav-item">
              <a class="nav-link">Viaja</a>
            </li>
            <li class="nav-item">
              <a class="nav-link">Conduce</a>
            </li>
            <li class="nav-item">
              <a class="nav-link">Quiénes somos</a>
            </li>
          </ul>
        </div>
      </div>
      <div class="d-flex align-items-center">
        <router-link class="nav-link" to="/">Iniciar Sesión</router-link>
        <router-link to="/registro">
          <button class="btn btn-light">Regístrate</button>
        </router-link>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      isMenuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
  },
};
</script>

<style scoped>
.navbar {
  background-color: #000;
  color: #fff;
  padding: 10px 20px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

.nav-link {
  color: #fff;
  margin-right: 15px;
  font-size: 1rem;
  cursor: pointer;
}

.nav-link:hover {
  color: #aaa;
}

.nav2 {
  text-decoration: none;
  color: #fff; /* Color inicial en blanco */
  font-weight: bold;
  font-size: 1.25rem;
  margin-right: 20px;
  cursor: pointer;
}


.btn-light {
  background-color: #fff;
  color: #000;
  border: none;
}

.btn-light:hover {
  background-color: #ccc;
}

.navbar-toggler {
  font-size: 2.5rem; /* Aumenta el tamaño del ícono */
  padding: 10px 15px; /* Aumenta el área clickeable */
  background-color: transparent; /* Sin fondo */
  border: none; /* Sin borde */
}

.navbar-toggler-icon {
  width: 25px; /* Ajusta el tamaño del ícono */
  height: 3px; /* Establece el grosor de las líneas */
  background-color: white; /* Hace las líneas blancas */
  position: relative; /* Para posicionar las líneas */
}

.navbar-toggler-icon:before,
.navbar-toggler-icon:after {
  content: "";
  position: absolute;
  width: 20px; /* El mismo tamaño que el ícono principal */
  height: 3px; /* El mismo grosor que las otras líneas */
  background-color: white; /* Hacer las líneas blancas */
}

.navbar-toggler-icon:before {
  top: -8px; /* Espaciado hacia arriba */
}

.navbar-toggler-icon:after {
  bottom: -8px; /* Espaciado hacia abajo */
}

.collapse {
  display: none;
}

.collapse.show {
  display: block;
}

@media (min-width: 992px) {
  .collapse {
    display: flex !important;
  }

  .navbar-toggler {
    display: none;
  }
}
</style>
