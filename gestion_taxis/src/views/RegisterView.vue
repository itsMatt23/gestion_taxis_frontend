<template>
  <div>
    <NavBar />
  </div>

  <section class="d-flex align-items-center"
    style="width: 100%; min-height: 100vh; background-color: #F9F9F9; padding-top: 70px;">
    <div class="container">
      <div class="row align-items-center justify-content-center">
        <!-- Texto a la izquierda -->
        <div class="col-12 col-md-6 mb-4 mb-md-0 text-center text-md-start" style="padding: 20px;">
          <h1 class="display-4 fw-bold text-dark">
            Regístrate para empezar a usar nuestra plataforma
          </h1>
          <p class="fs-5 text-muted">
            Únete a nosotros y comienza a disfrutar de viajes personalizados y más.
          </p>
        </div>
        <!-- Formulario a la derecha -->
        <div class="col-12 col-md-6">
          <div class="card p-4 shadow-sm" style="background-color: #000; border: none; border-radius: 10px;">
            <h3 class="text-light text-center fw-bold mb-4">Registro</h3>
            <form @submit.prevent="crearUsuario">
              <div class="mb-3">
                <label for="cedula" class="form-label text-light">Cédula:</label>
                <input type="text" class="form-control form-control-lg" id="cedula" v-model="user.cedula"
                  placeholder="Ingrese la cédula del usuario" @input="validateCedula" maxlength="10" required />
              </div>
              <div v-if="cedulaError" class="text-danger mt-1">
                {{ cedulaError }}
              </div>

              <div class="mb-3">
                <label for="nombre" class="form-label text-light">Nombre:</label>
                <input type="text" class="form-control form-control-lg" id="nombre" v-model="user.nombre"
                  placeholder="Ingrese el nombre de usuario" required />
              </div>

              <div class="mb-3">
                <label for="apellido" class="form-label text-light">Apellido:</label>
                <input type="text" class="form-control form-control-lg" id="apellido" v-model="user.apellido"
                  placeholder="Ingrese el apellido del usuario" required />
              </div>

              <div class="mb-3">
                <label for="telefono" class="form-label text-light">Teléfono:</label>
                <input type="text" class="form-control form-control-lg" id="telefono" v-model="user.telefono"
                  placeholder="Ingrese el teléfono del usuario" @input="validateNumero" required />
              </div>

              <div class="mb-3">
                <label for="rol" class="form-label text-light">Tipo de usuario:</label>
                <div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" id="cliente" v-model="user.rol" value="Cliente"
                      required />
                    <label class="form-check-label text-light" for="cliente">Cliente</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" id="conductor" v-model="user.rol" value="Conductor"
                      required />
                    <label class="form-check-label text-light" for="conductor">Conductor</label>
                  </div>
                </div>
              </div>

              <div v-if="user.rol === 'Conductor'" class="mb-3">
                <div>
                  <label for="marcaVehiculo" class="form-label text-light">Marca del vehículo:</label>
                  <input type="text" class="form-control form-control-lg" id="marcaVehiculo"
                    v-model="user.marca_vehiculo" placeholder="Ingrese la marca del vehículo" required />
                </div>

                <div class="mb-3">
                  <label for="placa" class="form-label text-light">Placa del vehículo:</label>
                  <input type="text" class="form-control form-control-lg" id="placa" v-model="user.placa"
                    placeholder="Ingrese la placa del vehículo" maxlength="6" required />
                </div>
              </div>

              <div class="mb-3">
                <label for="email" class="form-label text-light">Correo:</label>
                <input type="email" class="form-control form-control-lg" id="email" v-model="user.email"
                  placeholder="Ingrese el correo del usuario" required />
              </div>

              <div class="mb-3">
                <label for="password" class="form-label text-light">Contraseña:</label>
                <input type="password" class="form-control form-control-lg" id="password" v-model="user.password"
                  placeholder="Ingrese la contraseña del usuario" required maxlength="10" />
              </div>

              <small v-if="user.password" class="form-text text-muted text-light">
                La contraseña debe tener:
                <ul class="text-light">
                  <li :class="{ 'text-success': passwordValidations.length, 'text-danger': !passwordValidations.length }">
                    Entre 4 y 10 caracteres.
                  </li>
                  <li :class="{ 'text-success': passwordValidations.number, 'text-danger': !passwordValidations.number }">
                    Un número.
                  </li>
                  <li
                    :class="{ 'text-success': passwordValidations.uppercase, 'text-danger': !passwordValidations.uppercase }">
                    Una letra mayúscula.
                  </li>
                  <li
                    :class="{ 'text-success': passwordValidations.special, 'text-danger': !passwordValidations.special }">
                    Un carácter especial.
                  </li>
                </ul>
              </small>

              <div class="d-grid gap-2 mt-3">
                <button type="submit" class="btn btn-light btn-lg fw-bold"
                  style="background-color: #fff; color: #000;">Crear Usuario</button>
                <button type="button" @click="redirectToLogin"
                  class="btn btn-outline-light btn-lg fw-bold">Cancelar</button>
              </div>
            </form>
            <p v-if="usuarioCreado" class="text-light text-center mt-3">¡Usuario creado con éxito!</p>
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
      user: {
        email: "",
        cedula: "",
        nombre: "",
        apellido: "",
        telefono: "",
        rol: "",
        marca_vehiculo: null,
        placa: null,
        estado: null,
        password: "",
      },
      usuarioCreado: false,
      cedulaError: "",
    };
  },

  computed: {
    passwordValidations() {
      return {
        length: this.user.password.length >= 4 && this.user.password.length <= 10,
        number: /\d/.test(this.user.password),
        uppercase: /[A-Z]/.test(this.user.password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(this.user.password),
      };
    },
  },

  methods: {
    redirectToLogin() {
      this.$router.push("/"); // Cambia la ruta según tu configuración
    },

    validateCedula() {
      this.user.cedula = this.user.cedula.replace(/\D/g, "");
      if (this.user.cedula.length > 10) {
        this.user.cedula = this.user.cedula.slice(0, 10);
      }

      if (this.user.cedula.length === 10) {
        if (!this.isValidCedula(this.user.cedula)) {
          this.cedulaError = "La cédula ingresada no es válida.";
        } else {
          this.cedulaError = "";
        }
      } else {
        this.cedulaError = "La cédula debe tener exactamente 10 dígitos.";
      }
    },

    isValidCedula(cedula) {
      let total = 0;
      const longitud = 10;
      const digitoRegion = parseInt(cedula.substring(0, 2));

      if (digitoRegion >= 1 && digitoRegion <= 24 && cedula.length === longitud) {
        for (let i = 0; i < longitud - 1; i++) {
          let numero = parseInt(cedula.charAt(i));
          if (i % 2 === 0) {
            numero *= 2;
            if (numero > 9) numero -= 9;
          }
          total += numero;
        }
        const digitoVerificador = parseInt(cedula.charAt(longitud - 1));
        const residuo = total % 10;
        return residuo === 0 ? digitoVerificador === 0 : 10 - residuo === digitoVerificador;
      }
      return false;
    },

    validateNumero() {
      this.user.telefono = this.user.telefono.replace(/\D/g, "");
      if (this.user.telefono.length > 10) {
        this.user.telefono = this.user.telefono.slice(0, 10);
      }
    },

    async crearUsuario() {
      try {
        if (!this.user.rol) {
          alert("Debe seleccionar un tipo de usuario.")
          return;
        }

        if (!this.passwordValidations.length || !this.passwordValidations.number || !this.passwordValidations.uppercase || !this.passwordValidations.special) {
          alert("La contraseña no cumple con los requisitos.");
          return;
        }

        if (this.user.rol === "Cliente") {
          this.user.marca_vehiculo = null;
          this.user.placa = null;
          this.user.estado = null;
        } else if (this.user.rol === "Conductor") {
          this.user.estado = "Libre";
        }

        // Enviar la solicitud de creación de usuario
        await apiService.createUser(this.user);
        // Mensaje de éxito y limpieza del formulario
        this.usuarioCreado = true;
        alert("Usuario registrado con éxito");
        this.limpiarFormulario();
        this.redirectToLogin();
      } catch (error) {
        if (error.response && error.response.data) {
          this.errors = error.response.data;
          this.showErrorsAsAlerts();
        } else {
          alert("Hubo un error al crear el usuario. Intenta de nuevo más tarde.")
        }
      }
    },

    showErrorsAsAlerts() {
      // Recorremos los errores y mostramos cada mensaje como una alerta
      for (const [field, messages] of Object.entries(this.errors)) {
        messages.forEach((message) => {
          alert(`${field}: ${message}`); // Mostrar el error en una alerta
        });
      }
    },

    limpiarFormulario() {
      this.user = {
        email: "",
        cedula: "",
        nombre: "",
        apellido: "",
        telefono: "",
        rol: "",
        marca_vehiculo: null,
        placa: null,
        estado: null,
        password: "",
      };
      this.usuarioCreado = false;
    },
  },
};
</script>
<style scoped>
/* Los estilos ya están definidos en el diseño original, pero aquí puedes agregar estilos específicos si es necesario */
</style>