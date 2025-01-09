<template>
  <div>
    <NavBar />
  </div>

  <section
    class="d-flex align-items-center"
    style="width: 100%; min-height: 100vh; background-color: #F9F9F9; padding-top: 70px;"
  >
    <div class="container">
      <div class="row align-items-center justify-content-center">
        <!-- Texto a la izquierda -->
        <div
          class="col-12 col-md-6 mb-4 mb-md-0 text-center text-md-start"
          style="padding: 20px;"
        >
          <h1 class="display-4 fw-bold text-dark">
            Regístrate para empezar a usar nuestra plataforma
          </h1>
          <p class="fs-5 text-muted">
            Únete a nosotros y comienza a disfrutar de viajes personalizados y más.
          </p>
        </div>
        <!-- Formulario a la derecha -->
        <div class="col-12 col-md-6">
          <div
            class="card p-4 shadow-sm"
            style="background-color: #000; border: none; border-radius: 10px;"
          >
            <h3 class="text-light text-center fw-bold mb-4">Registro</h3>
            <form @submit.prevent="register">
              <div class="mb-3">
                <label for="email" class="form-label text-light">Correo Electrónico</label>
                <input
                  type="email"
                  class="form-control form-control-lg"
                  v-model="email"
                  id="email"
                  placeholder="name@example.com"
                  style="background-color: #fff; color: #000; border: none;"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="password" class="form-label text-light">Contraseña</label>
                <input
                  type="password"
                  class="form-control form-control-lg"
                  v-model="password"
                  id="password"
                  placeholder="Password"
                  style="background-color: #fff; color: #000; border: none;"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="confirmPassword" class="form-label text-light">Confirmar Contraseña</label>
                <input
                  type="password"
                  class="form-control form-control-lg"
                  v-model="confirmPassword"
                  id="confirmPassword"
                  placeholder="Confirm Password"
                  style="background-color: #fff; color: #000; border: none;"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="nombre" class="form-label text-light">Nombre</label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  v-model="nombre"
                  id="nombre"
                  placeholder="Tu nombre"
                  style="background-color: #fff; color: #000; border: none;"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="apellido" class="form-label text-light">Apellido</label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  v-model="apellido"
                  id="apellido"
                  placeholder="Tu apellido"
                  style="background-color: #fff; color: #000; border: none;"
                  required
                />
              </div>
              <div class="mb-3" v-if="errorMessage">
                <div class="alert alert-danger d-flex align-items-center" role="alert">
                  <span>{{ errorMessage }}</span>
                  <button
                    type="button"
                    class="btn-close ms-auto"
                    @click="errorMessage = ''"
                    aria-label="Close"
                  ></button>
                </div>
              </div>
              <div class="d-grid gap-2">
                <button
                  class="btn btn-light btn-lg fw-bold"
                  type="submit"
                  style="background-color: #fff; color: #000;"
                >
                  Registrarse
                </button>
                <button
                  class="btn btn-outline-light btn-lg fw-bold"
                  type="button"
                  @click="redirectToLogin"
                >
                  Iniciar sesión
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import apiService from "../services/apiService";
import NavBar from '../components/NavBar.vue';

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      email: "",
      password: "",
      confirmPassword: "",
      nombre: "",
      apellido: "",
      errorMessage: "",
    };
  },
  methods: {
    redirectToLogin() {
      this.$router.push("/");
    },
    // Aquí asumimos que existe un método register en apiService
    async register() {
      try {
        if (this.password !== this.confirmPassword) {
          this.errorMessage = "Las contraseñas no coinciden.";
          return;
        }
        const response = await apiService.register(this.email, this.password, this.nombre, this.apellido);

        if (response && response.data && response.data.access) {
          const { access } = response.data;
          localStorage.setItem("access_token", access);
          // Aquí deberías redirigir al usuario a una página de confirmación o inicio de sesión
          this.$router.push("/login");
        } else {
          alert("Error: No se pudo registrar el usuario.");
        }
      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage =
            error.response.data.detail || "Error al registrarse.";
        } else {
          this.errorMessage = "Error de conexión con el servidor.";
        }
        console.error(error);
      }
    },
  },
};
</script>