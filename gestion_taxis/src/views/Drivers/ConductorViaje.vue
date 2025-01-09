<template>
  <div class="viaje-iniciado">
    <h1>Viaje Actual</h1>
    <div v-if="viaje" class="viaje-detalle">
      <h3>Detalles del Viaje</h3>
      <p><strong>Origen:</strong> {{ viaje.origen }}</p>
      <p><strong>Destino:</strong> {{ viaje.destino }}</p>
      <p><strong>Tarifa:</strong> ${{ viaje.tarifa }}</p>
      <p><strong>Estado:</strong> {{ viaje.estado }}</p>
      <button @click="finalizarViaje" class="btn-finalizar">Finalizar Viaje</button>
    </div>
    <div v-else class="sin-viaje">
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

      const response = await api.getViajeAsignado(conductorId); // Llamada a la API

      if (response.data.mensaje) {
        // Si no hay viajes en progreso, mostrar el mensaje
        alert(response.data.mensaje);
        this.viaje = null;
      } else {
        // Si hay un viaje, mostrar los detalles
        this.viaje = response.data;
      }
    } catch (error) {
      console.error("Error al cargar el viaje actual:", error);
      alert("Hubo un error al cargar el viaje actual.");
    }
  },
  methods: {
    async finalizarViaje() {
      try {
        await api.completarViaje(this.viaje.id); // Llama a la API para finalizar el viaje
        alert("Viaje finalizado con éxito.");
        this.viaje = null; // Limpia los datos del viaje
      } catch (error) {
        console.error("Error al finalizar el viaje:", error);
        alert("Hubo un error al finalizar el viaje.");
      }
    },
  },
};
</script>

<style scoped>
/* Estilo inspirado en Uber */
.viaje-iniciado {
  padding: 30px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 50px auto;
  font-family: 'Arial', sans-serif; /* Cambiar a Uber Move si está disponible */
  color: #333;
}

h1 {
  font-size: 24px;
  font-weight: bold;
  color: #000;
  margin-bottom: 20px;
}

.viaje-detalle h3 {
  font-size: 20px;
  font-weight: 600;
  color: #444;
  margin-bottom: 15px;
}

p {
  margin: 8px 0;
  font-size: 16px;
  line-height: 1.5;
  color: #555;
}

p strong {
  color: #000;
}

.sin-viaje {
  font-size: 16px;
  color: #888;
  text-align: center;
}

.btn-finalizar {
  display: inline-block;
  padding: 10px 20px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 20px;
}

.btn-finalizar:hover {
  background-color: #333;
}

/* Responsivo */
@media (max-width: 768px) {
  .viaje-iniciado {
    padding: 20px;
  }

  h1 {
    font-size: 20px;
  }

  p {
    font-size: 14px;
  }

  .btn-finalizar {
    font-size: 14px;
  }
}
</style>
