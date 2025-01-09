<template>
  <div>
    <h1>Panel de Administración</h1>

    <!-- Tabla de Viajes en Progreso -->
    <div class="table-section">
      <h2>Viajes en Progreso</h2>
      <input
        v-model="filtroProgreso"
        @input="filtrarViajesProgreso"
        placeholder="Buscar en viajes en progreso..."
        class="filtro-input"
      />
      <table v-if="viajesEnProgresoFiltrados.length" class="table">
        <thead>
          <tr>
            <th>Origen</th>
            <th>Destino</th>
            <th>Tarifa</th>
            <th>Cédula Cliente</th>
            <th>Cédula Conductor</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="viaje in viajesEnProgresoFiltrados" :key="viaje.id">
            <td>{{ viaje.origen }}</td>
            <td>{{ viaje.destino }}</td>
            <td>${{ viaje.tarifa }}</td>
            <td>
              {{ viaje.cliente.cedula }}
              <button @click="verDatos(viaje.cliente, 'Cliente')">Ver Detalles</button>
            </td>
            <td>
              {{ viaje.conductor ? viaje.conductor.cedula : "N/A" }}
              <button
                v-if="viaje.conductor"
                @click="verDatos(viaje.conductor, 'Conductor')"
              >
                Ver Detalles
              </button>
            </td>
            <td>{{ viaje.estado }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No hay viajes en progreso.</p>
    </div>

    <!-- Tabla de Viajes Terminados -->
    <div class="table-section">
      <h2>Viajes Terminados</h2>
      <input
        v-model="filtroTerminados"
        @input="filtrarViajesTerminados"
        placeholder="Buscar en viajes terminados..."
        class="filtro-input"
      />
      <table v-if="viajesTerminadosFiltrados.length" class="table">
        <thead>
          <tr>
            <th>Origen</th>
            <th>Destino</th>
            <th>Tarifa</th>
            <th>Cédula Cliente</th>
            <th>Cédula Conductor</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="viaje in viajesTerminadosFiltrados" :key="viaje.id">
            <td>{{ viaje.origen }}</td>
            <td>{{ viaje.destino }}</td>
            <td>${{ viaje.tarifa }}</td>
            <td>
              {{ viaje.cliente.cedula }}
              <button @click="verDatos(viaje.cliente, 'Cliente')">Ver Detalles</button>
            </td>
            <td>
              {{ viaje.conductor ? viaje.conductor.cedula : "N/A" }}
              <button
                v-if="viaje.conductor"
                @click="verDatos(viaje.conductor, 'Conductor')"
              >
                Ver Detalles
              </button>
            </td>
            <td>{{ viaje.estado }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No hay viajes terminados.</p>
    </div>

    <!-- Tabla de Conductores Disponibles -->
    <div class="table-section">
      <h2>Conductores Disponibles</h2>
      <input
        v-model="filtroConductores"
        @input="filtrarConductores"
        placeholder="Buscar conductores disponibles..."
        class="filtro-input"
      />
      <table v-if="conductoresFiltrados.length" class="table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Cédula</th>
            <th>Email</th>
            <th>Teléfono</th>
            <th>Vehículo</th>
            <th>Placa</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="conductor in conductoresFiltrados" :key="conductor.id">
            <td>{{ conductor.nombre }}</td>
            <td>{{ conductor.apellido }}</td>
            <td>{{ conductor.cedula }}</td>
            <td>{{ conductor.email }}</td>
            <td>{{ conductor.telefono }}</td>
            <td>{{ conductor.marca_vehiculo || "N/A" }}</td>
            <td>{{ conductor.placa || "N/A" }}</td>
            <td>{{ conductor.estado }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No hay conductores disponibles.</p>
    </div>

    <!-- Popup -->
    <div v-if="mostrarPopup" class="popup-overlay">
      <div class="popup-content">
        <h3>Datos del {{ tipoDetalle }}</h3>
        <p><strong>Nombre:</strong> {{ datosDetalle.nombre }}</p>
        <p><strong>Apellido:</strong> {{ datosDetalle.apellido }}</p>
        <p><strong>Cédula:</strong> {{ datosDetalle.cedula }}</p>
        <p><strong>Email:</strong> {{ datosDetalle.email }}</p>
        <p><strong>Teléfono:</strong> {{ datosDetalle.telefono }}</p>
        <button @click="cerrarPopup">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/apiService";

export default {
  data() {
    return {
      viajesEnProgreso: [],
      viajesTerminados: [],
      conductores: [],
      filtroProgreso: "",
      filtroTerminados: "",
      filtroConductores: "",
      viajesEnProgresoFiltrados: [],
      viajesTerminadosFiltrados: [],
      conductoresFiltrados: [],
      mostrarPopup: false,
      datosDetalle: {},
      tipoDetalle: "",
      actualizacionIntervalo: null, // Para almacenar el temporizador
    };
  },
  methods: {
   async actualizarViajes() {
      try {
        const viajesResponse = await api.getViajes();
        this.viajesEnProgreso = viajesResponse.data.filter(
          (viaje) => viaje.estado === "en_progreso"
        );
        this.viajesTerminados = viajesResponse.data.filter(
          (viaje) => viaje.estado === "completado"
        );

        this.viajesEnProgresoFiltrados = this.viajesEnProgreso;
        this.viajesTerminadosFiltrados = this.viajesTerminados;
      } catch (error) {
        console.error("Error al actualizar los viajes:", error);
      }
    },
    filtrarViajesProgreso() {
      this.viajesEnProgresoFiltrados = this.viajesEnProgreso.filter((viaje) =>
        `${viaje.origen} ${viaje.destino} ${viaje.cliente.nombre} ${viaje.conductor?.nombre || ""}`
          .toLowerCase()
          .includes(this.filtroProgreso.toLowerCase())
      );
    },
    filtrarViajesTerminados() {
      this.viajesTerminadosFiltrados = this.viajesTerminados.filter((viaje) =>
        `${viaje.origen} ${viaje.destino} ${viaje.cliente.nombre} ${viaje.conductor?.nombre || ""}`
          .toLowerCase()
          .includes(this.filtroTerminados.toLowerCase())
      );
    },
    filtrarConductores() {
      this.conductoresFiltrados = this.conductores.filter((conductor) =>
        `${conductor.nombre} ${conductor.apellido} ${conductor.cedula}`
          .toLowerCase()
          .includes(this.filtroConductores.toLowerCase())
      );
    },
    verDatos(persona, tipo) {
      this.datosDetalle = persona;
      this.tipoDetalle = tipo;
      this.mostrarPopup = true;
    },
    cerrarPopup() {
      this.mostrarPopup = false;
      this.datosDetalle = {};
      this.tipoDetalle = "";
    },
  },
  async created() {
    try {
await this.actualizarViajes();

      const viajesResponse = await api.getViajes();
      this.viajesEnProgreso = viajesResponse.data.filter(
        (viaje) => viaje.estado === "en_progreso"
      );
      this.viajesTerminados = viajesResponse.data.filter(
        (viaje) => viaje.estado === "completado"
      );

      this.viajesEnProgresoFiltrados = this.viajesEnProgreso;
      this.viajesTerminadosFiltrados = this.viajesTerminados;

      const conductoresResponse = await api.getConductoresDisponibles();
      this.conductores = conductoresResponse.data;
      this.conductoresFiltrados = this.conductores;


      // Configura el temporizador para actualizar los viajes cada 10 segundos
      this.actualizacionIntervalo = setInterval(() => {
        this.actualizarViajes();
      }, 5000); // 10,000 ms = 10 segundos
    } catch (error) {
      console.error("Error al cargar los datos:", error);
    }
  },
};
</script>

<style scoped>
/* Mantén el estilo igual */
.table-section {
  margin-bottom: 40px;
}

.filtro-input {
  padding: 10px;
  margin-bottom: 20px;
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

.table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 300px;
}

button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
