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
            Inicia sesión para ver la actividad reciente
          </h1>
          <p class="fs-5 text-muted">
            Consulta viajes anteriormente, sugerencias personalizadas
          </p>
        </div>
        <!-- Formulario a la derecha -->
        <div class="col-12 col-md-6">
          <div
            class="card p-4 shadow-sm"
            style="background-color: #000; border: none; border-radius: 10px;"
          >
            <h3 class="text-light text-center fw-bold mb-4">Bienvenidos</h3>
            <form @submit.prevent="login">
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
                  Iniciar sesión
                </button>
                <button
                  class="btn btn-outline-light btn-lg fw-bold"
                  type="button"
                  @click="redirectToRegister"
                >
                  Registrarse
                </button>
              </div>
              <div class="text-center mt-3">
                <a href="#" class="text-muted text-decoration-none">¿Olvidaste tu contraseña?</a>
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
      errorMessage: "",
      usuario: "",
    };
  },
  methods: {
    redirectToRegister() {
      this.$router.push("/registro");
    },
    async login() {
      try {
        const response = await apiService.login(this.email, this.password);

        if (response && response.data && response.data.access) {
          const { access } = response.data;
          localStorage.setItem("access_token", access);

          await this.traerUsuario(this.email);
          if (this.usuario.rol === "Admin") {
            this.$router.push({ name: "Admin" });
            alert("Acceso Correcto");
          } else if (this.usuario.rol === "Cliente") {
            this.$router.push({ name: "Cliente" });
            alert("Acceso Correcto");
          } else {
            this.$router.push({ name: "Conductor" });
            alert("Acceso Correcto");
          }
        } else {
          alert("Error: No se pudo obtener el token de acceso.");
        }
      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage =
            error.response.data.detail || "Error al iniciar sesión.";
        } else {
          this.errorMessage = "Error de conexión con el servidor.";
        }
        console.error(error);
      }
    },
    async traerUsuario(user) {
      try {
        const response = await apiService.buscarUsuario(user);
        if (response.data) {
          this.usuario = response.data;
          localStorage.setItem("userConected", JSON.stringify(this.usuario));
          if (this.usuario.rol === "Cliente") {
            localStorage.setItem("cliente_id", this.usuario.id);
          } else if (this.usuario.rol === "Conductor") {
            localStorage.setItem("conductor_id", this.usuario.id);
          }
        } else {
          this.errorMessage = "Usuario no encontrado";
        }
      } catch (error) {
        console.error("Error al buscar usuario:", error);
        this.errorMessage = "Ocurrió un error al buscar el usuario";
      }
    },
  },
};
</script>

<style scoped>
/* Texto */
.text-dark {
  color: #212529 !important;
}

.text-muted {
  color: #6c757d !important;
  font-size: 1rem;
}

.card {
  background-color: #000;
}

.form-control:focus {
  border: 2px solid #000;
  box-shadow: none;
}

/* Botones */
.btn-light {
  background-color: #fff !important;
  border-color: #fff !important;
}

.btn-outline-light {
  color: #fff !important;
  border-color: #fff !important;
}

.btn-outline-light:hover {
  background-color: #fff !important;
  color: #000 !important;
}

a.text-muted:hover {
  color: #000 !important;
}

/* Responsividad */
@media (max-width: 768px) {
  .text-md-start {
    text-align: center !important;
  }
}
</style>
