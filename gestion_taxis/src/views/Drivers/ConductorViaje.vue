<template>
  <div class="viaje-iniciado">
    <h1>Viaje Actual</h1>
    <div v-if="viaje">
      <h3>Detalles del Viaje</h3>
      <p><strong>Origen:</strong> {{ viaje.origen }}</p>
      <p><strong>Destino:</strong> {{ viaje.destino }}</p>
      <p><strong>Tarifa:</strong> ${{ viaje.tarifa }}</p>
      <p><strong>Estado:</strong> {{ viaje.estado }}</p>
      <button @click="finalizarViaje" class="btn btn-danger mt-3">Finalizar Viaje</button>
    </div>
    <div v-else>
      <p>No tienes un viaje asignado actualmente.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/apiService";

export default {
  data() {
    return {
      viaje: null, // Detalles del viaje actual
      intervaloActualizacion: null, // Referencia al intervalo
    };
  },
  async created() {
    try {
      const conductorId = localStorage.getItem("conductor_id");
      if (!conductorId) {
        alert("No se encontró el ID del conductor. Redirigiendo al inicio de sesión.");
        this.$router.push({ name: "Login" });
        return;
      }

      // Llama a la API para cargar el viaje inicial
      await this.cargarViaje(conductorId);

      // Configura el intervalo para verificar el estado del viaje cada 5 segundos
      this.intervaloActualizacion = setInterval(async () => {
        await this.cargarViaje(conductorId);
      }, 5000); // 5000 ms = 5 segundos
    } catch (error) {
      console.error("Error al cargar el viaje actual:", error);
      alert("Hubo un error al cargar el viaje actual.");
    }
  },
  beforeUnmount() {
    if (this.intervaloActualizacion) {
      clearInterval(this.intervaloActualizacion);
    }
  },
  methods: {
    async cargarViaje(conductorId) {
      try {
        const response = await api.getViajeAsignado(conductorId); // Llamada a la API

        if (response.data.mensaje) {
          // Si no hay viajes en progreso, limpiar los datos del viaje
          this.viaje = null;
        } else {
          // Si hay un viaje, actualizar los detalles
          this.viaje = response.data;
        }
      } catch (error) {
        console.error("Error al cargar el viaje actual:", error);
        alert("Hubo un error al cargar el viaje actual.");
      }
    },
    async finalizarViaje() {
      try {
        await api.completarViaje(this.viaje.id); // Llama a la API para finalizar el viaje
        alert("Viaje finalizado con éxito.");
        this.viaje = null; // Limpia los datos del viaje
        clearInterval(this.intervaloActualizacion); // Limpia el intervalo
      } catch (error) {
        console.error("Error al finalizar el viaje:", error);
        alert("Hubo un error al finalizar el viaje.");
      }
    },
  },
};
</script>

<style scoped>
.viaje-iniciado {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>
