<template>
  <div class="iniciar-viaje">
    <h1>Iniciar un Viaje</h1>
    <form @submit.prevent="iniciarViaje">
      <div class="input-container">
        <label for="origen">Ubicación de recogida</label>
        <input v-model="origen" id="origen" type="text" placeholder="Escribe la ubicación de recogida" required />
      </div>
      <div class="input-container">
        <label for="destino">Ubicación de destino</label>
        <input v-model="destino" id="destino" type="text" placeholder="Escribe la ubicación de destino" required />
      </div>
      <div class="input-container">
        <label for="tarifa">Tarifa</label>
        <input v-model="tarifa" id="tarifa" type="number" placeholder="Tarifa del viaje" required />
      </div>
      <button type="submit">Solicitar Viaje</button>
    </form>
  </div>
</template>

<script>
import api from '@/services/apiService'; // Importa el servicio de API

export default {
  data() {
    return {
      origen: '',
      destino: '',
      tarifa: 0,
    };
  },
  methods: {
    async iniciarViaje() {
      try {
        // Datos del cliente (puedes obtener el ID del cliente desde la sesión o estado)
        const clienteId = localStorage.getItem('cliente_id'); // Supongamos que tienes el ID en el localStorage

        // Datos para enviar al backend
        const viajeData = {
          origen: this.origen,
          destino: this.destino,
          tarifa: this.tarifa,
          cliente: clienteId,
        };

        // Llamada a la API
        const response = await api.createViaje(viajeData);

        // Muestra un mensaje de éxito
        alert(`Viaje iniciado con éxito. ID del viaje: ${response.data.id}`);
        localStorage.setItem("viaje_id", response.data.id);

         this.$router.push({ name: "ClienteViaje" });
      } catch (error) {
        console.error('Error al iniciar el viaje:', error);
        alert('Hubo un error al iniciar el viaje. Inténtalo nuevamente.');
      }
    },
  },
};
</script>

<style scoped>
/* Estilo global: */
body {
  font-family: 'Roboto', sans-serif;
  background-color: #f7f7f7;
  margin: 0;
  padding: 0;
}

/* Contenedor principal: */
.iniciar-viaje {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 50px auto;
}

/* Estilo del encabezado: */
h1 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

/* Estilo de los inputs: */
.input-container {
  margin-bottom: 20px;
}

input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-sizing: border-box;
  background-color: #f9f9f9;
  margin-top: 5px;
}

input:focus {
  border-color: #00a8cc; /* Color azul similar al de Uber */
  background-color: #fff;
}

/* Estilo del botón: */
button {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #444;
}
</style>
