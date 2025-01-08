<template>
  <div class="historial-viajes">
    <h1>Historial de Viajes</h1>

    <!-- Viajes en Progreso -->
    <h2>Viajes en Progreso</h2>
    <ul v-if="viajesEnProgreso.length">
      <li v-for="viaje in viajesEnProgreso" :key="viaje.id" class="viaje-item">
        <p><strong>Origen:</strong> {{ viaje.origen }}</p>
        <p><strong>Destino:</strong> {{ viaje.destino }}</p>
        <p><strong>Tarifa:</strong> ${{ viaje.tarifa }}</p>

      </li>
    </ul>
    <p v-else>No hay viajes en progreso.</p>

    <!-- Viajes Completados -->
    <h2>Viajes Completados</h2>
    <ul v-if="viajesCompletados.length">
      <li v-for="viaje in viajesCompletados" :key="viaje.id" class="viaje-item">
        <p><strong>Origen:</strong> {{ viaje.origen }}</p>
        <p><strong>Destino:</strong> {{ viaje.destino }}</p>
        <p><strong>Tarifa:</strong> ${{ viaje.tarifa }}</p>
        <p><strong>Cliente:</strong> {{ viaje.cliente.nombre }} {{ viaje.cliente.apellido }}</p>
        <p><strong>Conductor:</strong> {{ viaje.conductor.nombre }} {{ viaje.conductor.apellido }}</p>
        <p><strong>Auto:</strong> {{ viaje.conductor.marca_vehiculo }}</p>
        <p><strong>Placa:</strong> {{ viaje.conductor.placa }}</p>
      </li>
    </ul>
    <p v-else>No hay viajes completados.</p>
  </div>
</template>

<script>
import api from "@/services/apiService";

export default {
  data() {
    return {
      viajesEnProgreso: [],
      viajesCompletados: [],
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

      const response = await api.historialConductor(conductorId); // Llama a la API
      this.viajesEnProceso = response.data
      .filter((viaje) => viaje.estado === "en_progreso")
      .sort((a, b) => new Date(b.creado_en) - new Date(a.creado_en));

      this.viajesCompletados = response.data
      .filter((viaje) => viaje.estado === "completado")
      .sort((a, b) => new Date(b.creado_en) - new Date(a.creado_en));
    } catch (error) {
      console.error("Error al cargar el historial de viajes:", error);
      alert("Hubo un error al cargar el historial.");
    }
  },
};
</script>

<style scoped>
.historial-viajes {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.viaje-item {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
</style>
