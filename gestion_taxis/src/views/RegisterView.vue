<template>
  <h2 class="title">Gestión de Usuarios</h2>
  <div class="form-container">
    <form @submit.prevent="crearUsuario">
      <div class="input-group">
        <label for="cedula">Cédula:</label>
        <input
          type="text"
          id="cedula"
          v-model="user.cedula"
          placeholder="Ingrese la cédula del usuario"
          required
        />
      </div>

      <div class="input-group">
        <label for="nombre">Nombre:</label>
        <input
          type="text"
          id="nombre"
          v-model="user.nombre"
          placeholder="Ingrese el nombre de usuario"
          required
        />
      </div>

      <div class="input-group">
        <label for="apellido">Apellido:</label>
        <input
          type="text"
          id="apellido"
          v-model="user.apellido"
          placeholder="Ingrese el apellido del usuario"
          required
        />
      </div>

      <div class="input-group">
        <label for="telefono">Teléfono:</label>
        <input
          type="text"
          id="telefono"
          v-model="user.telefono"
          placeholder="Ingrese el teléfono del usuario"
          required
        />
      </div>

      <div class="role-section">
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

      <div v-if="user.rol === 'Conductor'" class="input-group">
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

      <div class="input-group">
        <label for="email">Correo:</label>
        <input
          type="email"
          id="email"
          v-model="user.email"
          placeholder="Ingrese el correo del usuario"
          required
        />
      </div>

      <div class="input-group">
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

      <div class="button-group">
        <button type="submit" class="primary-button">Crear Usuario</button>
        <button type="button" @click="redirectToLogin()" class="secondary-button">Cancelar</button>
      </div>
    </form>
    <p v-if="usuarioCreado" class="success-message">¡Usuario creado con éxito!</p>
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
    };
  },
  methods: {
    redirectToLogin() {
      this.$router.push("/"); // Cambia la ruta según tu configuración
    },

    async crearUsuario() {
      try {
        // Validar y ajustar los campos según el rol
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
        this.limpiarFormulario();
        alert("Usuario registrado con éxito");
        this.redirectToLogin();
      } catch (error) {
        console.error("Error al crear usuario:", error);
        alert("Error al crear usuario. Por favor, verifica los datos.");
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

<style>
.form-container {
  max-width: 450px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #111;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  color: white;
}

.title {
  text-align: center;
  color: #000; /* Título en color negro */
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}

.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.input-group input[type="text"],
.input-group input[type="email"],
.input-group input[type="password"],
.input-group input[type="radio"] {
  width: calc(100% - 20px);
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: white;
  color: #333;
}

.role-section {
  margin-top: 20px;
  margin-bottom: 20px;
}

.role-section label {
  display: block;
  margin-bottom: 10px;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.primary-button {
  background-color: #000;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.secondary-button {
  background-color: #ccc;
  color: #333;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.success-message {
  color: green;
  text-align: center;
  margin-top: 20px;
}
</style>
