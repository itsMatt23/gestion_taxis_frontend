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
            required
          />
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
