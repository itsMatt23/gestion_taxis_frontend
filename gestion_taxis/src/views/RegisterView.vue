<template>
    <h2>Gestión de Usuarios</h2>
    <div>
      <form @submit.prevent="crearUsuario">
        <div>
          <label for="cedula">Cédula:</label>
          <input
            type="text"
            id="cedula"
            v-model="user.cedula"
            placeholder="Ingrese la cédula del usuario"
            @input="validateCedula"
            required
          />
        </div>
        <div v-if="cedulaError" class="text-danger mt-1">
                    {{ cedulaError }}
                </div>
  
        <div>
          <label for="nombre">Nombre:</label>
          <input
            type="text"
            id="nombre"
            v-model="user.nombre"
            placeholder="Ingrese el nombre de usuario"
            required
          />
        </div>
  
        <div>
          <label for="apellido">Apellido:</label>
          <input
            type="text"
            id="apellido"
            v-model="user.apellido"
            placeholder="Ingrese el apellido del usuario"
            required
          />
        </div>
  
        <div>
          <label for="telefono">Teléfono:</label>
          <input
            type="text"
            id="telefono"
            v-model="user.telefono"
            placeholder="Ingrese el teléfono del usuario"
            @input="validateNumero"
            required
          />
        </div>
  
        <div>
          <label for="rol">Tipo de usuario:</label>
          <br />
          <label for="cliente">
            <input type="radio" id="cliente" v-model="user.rol" value="Cliente" />
            Cliente
          </label>
  
          <label for="conductor">
            <input
              type="radio"
              id="conductor"
              v-model="user.rol"
              value="Conductor"
            />
            Conductor
          </label>
        </div>
  
        <div v-if="user.rol === 'Conductor'">
          <div>
            <label for="marcaVehiculo">Marca del vehículo:</label>
            <input
              type="text"
              id="marcaVehiculo"
              v-model="user.marca_vehiculo"
              placeholder="Ingrese la marca del vehículo"
              required
            />
          </div>
  
          <div>
            <label for="placa">Placa del vehículo:</label>
            <input
              type="text"
              id="placa"
              v-model="user.placa"
              placeholder="Ingrese la placa del vehículo"
              maxlength="6"
              required
            />
          </div>
        </div>
  
        <div>
          <label for="email">Correo:</label>
          <input
            type="email"
            id="email"
            v-model="user.email"
            placeholder="Ingrese el correo del usuario"
            required
          />
        </div>
  
        <div>
          <label for="password">Contraseña:</label>
          <input
            type="password"
            id="password"
            v-model="user.password"
            placeholder="Ingrese la contraseña del usuario"
            required
            maxlength="10"
          />
        </div>

        <small v-if="user.password" class="form-text text-muted">
                    La contraseña debe tener:
                    <ul>
                        <li
                            v-bind:class="{ 'text-success': passwordValidations.length, 'text-danger': !passwordValidations.length }">
                            Entre 4 y 10 caracteres.</li>


                        <li v-bind:class="{
                            'text-success': passwordValidations.number,
                            'text-danger': !passwordValidations.number,
                        }">
                            Un número.
                        </li>
                        <li v-bind:class="{
                            'text-success': passwordValidations.uppercase,
                            'text-danger': !passwordValidations.uppercase,
                        }">
                            Una letra mayúscula.
                        </li>
                        <li v-bind:class="{
                            'text-success': passwordValidations.special,
                            'text-danger': !passwordValidations.special,
                        }">
                            Un carácter especial.
                        </li>
                    </ul>
                </small>
        
        <div>
          <button type="submit">Crear Usuario</button>
          <button type="button" @click="redirectToLogin()">Cancelar</button>
        </div>
      </form>
      <p v-if="usuarioCreado">¡Usuario creado con éxito!</p>
    </div>
  </template>
  
  <script>
import apiService from "../services/apiService";

export default {
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
      errors: {},
      cedulaCliente: "",

    };
  },

  computed:{
    passwordValidations() {
            return {
                length:
                    this.user.password.length >= 4 && this.user.password.length <= 10, // Validación de longitud
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
            // Filtrar entrada para que solo contenga números
            this.user.telefono = this.user.telefono.replace(/\D/g, "");

            // Limitar a 10 dígitos
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
