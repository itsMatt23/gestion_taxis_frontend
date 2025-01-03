<template>
  <!-- Login 13 - Bootstrap Brain Component -->
  <section class="bg-light py-4 py-md-5" style="width: 100%; min-height: 100vh;">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-12 col-sm-10 col-md-8 col-lg-6 col-xl-5 col-xxl-4">
          <div class="card border border-light-subtle rounded-3 shadow-sm">
            <div class="card-body p-3 p-md-4 p-xl-5">
              <div class="text-center mb-3">
                <h1>Iniciar sesion</h1>
              </div>
              <h2 class="fs-6 fw-normal text-center text-secondary mb-4">Ingresa tus credenciales!</h2>
              <form @submit.prevent="login">
                <div class="row gy-2 overflow-hidden">
                  <div class="col-12">
                    <div class="form-floating mb-3">
                      <input type="email" class="form-control" v-model="email" id="email" placeholder="name@example.com"
                        required>
                      <label for="email" class="form-label">Correo Electronico</label>
                    </div>
                  </div>
                  <div class="col-12">
                    <div class="form-floating mb-3">
                      <input type="password" class="form-control" v-model="password" id="password"
                        placeholder="Password" required>
                      <label for="password" class="form-label">Contraseña</label>
                    </div>

                    <div class="form-floating">
                      <div v-if="errorMessage" class="alert alert-danger mt-2 d-flex align-items-center" role="alert"
                        style="font-size: 0.9em; padding: 0.75em; color: #721c24; background-color: #f8d7da; border-color: #f5c6cb;">
                        <span>{{ errorMessage }}</span>
                        <button type="button" class="btn-close ms-auto" @click="errorMessage = ''" aria-label="Close"
                          style="color: #721c24;"></button>
                      </div>
                    </div>
                  </div>
                  <div class="col-12">
                    <div class="d-grid my-1">
                      <button class="btn btn-dark btn-lg" type="submit">Log in</button>
                    </div>

                    <div class="d-grid my-1">
                      <button class="btn btn-secondary btn-lg" type="button" @click="redirectToRegister">Register</button>
                    </div>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import apiService from '../services/apiService';
export default {
  data() {
    return {
      email: '', // Cambiado de username a email
      password: '',
      errorMessage: '',
      usuario: ""
    };
  },
  methods: {
    redirectToRegister() {
      this.$router.push('/registro'); // Cambia '/registro' por la ruta a la que quieras redirigir
    },

    async login() {
      try {
        // Llamada al servicio de login
        const response = await apiService.login(this.email, this.password);

        if (response && response.data && response.data.access) {
          const { access } = response.data;
          localStorage.setItem('access_token', access); // Guardar el token en el localStorage
          alert('Acceso Correcto');

          // Obtener la información del usuario y mandarlo a su pantalla respectiva
          await this.traerUsuario(this.email);
          if (this.usuario.rol === "Admin") {
              this.$router.push({ name: 'Admin' });
            } else if (this.usuario.rol === "Cliente") {
              this.$router.push({ name: 'Cliente' });
            } else {
              this.$router.push({ name: 'Conductor' });
            }
        } else {
          alert('Error: No se pudo obtener el token de acceso.');
        }

      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.detail || 'Error al iniciar sesión.';
        } else {
          this.errorMessage = 'Error de conexión con el servidor.';
        }
        console.error(error); // Mejor manejo de errores
      }
    },


    async traerUsuario(user) {
      try {
        const response = await apiService.buscarUsuario(user);
        if (response.data) {
          this.usuario = response.data;
          localStorage.setItem('userConected', JSON.stringify(this.usuario));
        } else {
          this.errorMessage = 'Usuario no encontrado';
        }
      } catch (error) {
        console.error("Error al buscar usuario:", error);
        this.errorMessage = 'Ocurrió un error al buscar el usuario';
      }
    },
  }
};
</script>

<style scoped></style>
