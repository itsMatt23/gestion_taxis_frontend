<template>
  <div class="historial-viajes">
    <!-- Título principal -->
    <h1>Historial de Viajes</h1>

    <!-- Viajes en Proceso -->
    <div class="seccion">
      <h2 class="seccion-titulo">Viajes en Proceso</h2>
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
    </div>

    <!-- Viajes Completados -->
    <div class="seccion">
      <h2 class="seccion-titulo">Viajes Completados</h2>
      <ul v-if="viajesCompletados.length">
        <li v-for="viaje in viajesCompletados" :key="viaje.id" class="viaje-item">
          <div class="viaje-detalle">
            <p><strong>Origen:</strong> {{ viaje.origen }}</p>
            <p><strong>Destino:</strong> {{ viaje.destino }}</p>
            <p><strong>Tarifa:</strong> ${{ viaje.tarifa }}</p>
            <p><strong>Estado:</strong> {{ viaje.estado }}</p>
          </div>
          <hr />
        </li>
      </ul>
      <p v-else>No hay viajes completados.</p>
    </div>
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
/* Estilo global */
body {
  font-family: 'Roboto', sans-serif;
  background-color: #f7f7f7;
  margin: 0;
  padding: 0;
}

/* Contenedor principal */
.historial-viajes {
  padding: 30px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 900px;
  margin: 50px auto;
}

/* Título principal */
.historial-viajes h1 {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin-bottom: 30px;
  text-align: left; /* Cambié para que no esté centrado */
}

/* Sección de cada parte del historial */
.seccion {
  margin-bottom: 30px;
}

/* Títulos de cada sección */
.seccion-titulo {
  background-color: #333;
  color: white;
  padding: 15px;
  font-size: 22px;
  font-weight: 700;
  text-align: left; /* Cambié para que no esté centrado */
  border-radius: 8px;
  margin-bottom: 20px;
}

/* Estilo de cada viaje */
.viaje-item {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.viaje-item:hover {
  transform: translateY(-5px);
}

/* Detalle del viaje */
.viaje-detalle {
  margin-bottom: 15px;
}

.viaje-item p {
  margin: 10px 0;
  font-size: 18px;
  color: #555;
  text-align: left; /* Cambié para que no esté centrado */
}

.viaje-item strong {
  font-weight: 700;
  color: #333;
}

/* Línea divisoria */
hr {
  border: 0;
  border-top: 2px solid #ddd;
  margin-top: 15px;
  margin-bottom: 15px;
}

/* Mensajes cuando no hay viajes */
p {
  font-size: 18px;
  color: #777;
  text-align: left; /* Cambié para que no esté centrado */
}

/* Estilos responsivos */
@media (max-width: 768px) {
  .historial-viajes {
    padding: 15px;
  }

  .seccion-titulo {
    font-size: 20px;
  }

  .viaje-item p {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .historial-viajes {
    padding: 10px;
    margin: 20px;
  }

  .seccion-titulo {
    font-size: 18px;
    padding: 12px;
  }

  .viaje-item p {
    font-size: 14px;
  }
}
</style>
