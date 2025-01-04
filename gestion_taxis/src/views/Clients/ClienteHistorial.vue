<template>
  <div class="historial-viajes">
    <h1>Historial de Viajes</h1>

    <!-- Viajes en Proceso -->
    <h2>Viajes en Proceso</h2>
    <ul v-if="viajesEnProceso.length">
      <li v-for="viaje in viajesEnProceso" :key="viaje.id" class="viaje-item">
        <p><strong>Origen:</strong> {{ viaje.origen }}</p>
        <p><strong>Destino:</strong> {{ viaje.destino }}</p>
        <p><strong>Tarifa:</strong> ${{ viaje.tarifa }}</p>
        <p><strong>Estado:</strong> {{ viaje.estado }}</p>
        <hr />
      </li>
    </ul>
    <p v-else>No hay viajes en proceso.</p>

    <!-- Viajes Completados -->
    <h2>Viajes Completados</h2>
    <ul v-if="viajesCompletados.length">
      <li v-for="viaje in viajesCompletados" :key="viaje.id" class="viaje-item">
        <p><strong>Origen:</strong> {{ viaje.origen }}</p>
        <p><strong>Destino:</strong> {{ viaje.destino }}</p>
        <p><strong>Tarifa:</strong> ${{ viaje.tarifa }}</p>
        <p><strong>Estado:</strong> {{ viaje.estado }}</p>
        <hr />
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
      viajesEnProceso: [], // Lista de viajes en proceso
      viajesCompletados: [], // Lista de viajes completados
    };
  },
  async created() {
    try {
      // Obtener el ID del cliente desde localStorage
      const clienteId = localStorage.getItem("cliente_id");

      if (!clienteId) {
        alert("No se encontró información del cliente. Redirigiendo al inicio de sesión.");
        this.$router.push({ name: "Login" });
        return;
      }

      // Llamar al API para obtener el historial de viajes del cliente
      const response = await api.historialCliente(clienteId);

      // Filtrar los viajes por estado
      this.viajesEnProceso = response.data
      .filter((viaje) => viaje.estado === "en_progreso")
      .sort((a, b) => new Date(b.creado_en) - new Date(a.creado_en));


       this.viajesCompletados = response.data
      .filter((viaje) => viaje.estado === "completado")
      .sort((a, b) => new Date(b.creado_en) - new Date(a.creado_en));
    } catch (error) {
      console.error("Error al cargar el historial de viajes:", error);
      alert("Hubo un error al cargar el historial de viajes.");
    }
  },
};
</script>

<style scoped>
.historial-viajes {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.historial-viajes h1,
.historial-viajes h2 {
  margin-bottom: 15px;
}

.viaje-item {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
</style>
