<template>
  <div id="app" class="d-flex">
    <!-- Formulario para solicitar un viaje (lado izquierdo, más pequeño) -->
    <div id="formulario-viaje" class="form-container">
      <div v-if="!viaje || (viaje && viaje.estado !== 'en_progreso')">
        <h1 class="title">Solicitar un Viaje</h1>
        <form @submit.prevent="iniciarViaje" class="formulario">
          <div class="form-group">
            <label for="origen">Ubicación de recogida</label>
            <input
              id="origen"
              type="text"
              placeholder="Escribe la ubicación de recogida"
              ref="origenInput"
              required
              class="input"
            />
          </div>
          <div class="form-group">
            <label for="destino">Ubicación de destino</label>
            <input
              id="destino"
              type="text"
              placeholder="Escribe la ubicación de destino"
              ref="destinoInput"
              required
              class="input"
            />
          </div>
          <div class="form-group">
            <label for="tarifa">Tarifa estimada</label>
            <input
              id="tarifa"
              type="number"
              placeholder="Tarifa del viaje"
              v-model="tarifa"
              readonly
              class="input"
            />
          </div>
          <button type="submit" class="btn-submit">Solicitar Viaje</button>
        </form>
      </div>

      <!-- Detalles del viaje en progreso -->
      <div v-else>
        <h1 v-if="viaje && viaje.estado === 'en_progreso'" class="title">Viaje En Progreso</h1>
        <h1 v-else-if="viaje && viaje.estado === 'completado'" class="title">Viaje Finalizado</h1>
        <div v-if="viaje">
          <h3>Detalles del Viaje</h3>
          <p><strong>Origen:</strong> {{ viaje.origen }}</p>
          <p><strong>Destino:</strong> {{ viaje.destino }}</p>
          <p><strong>Tarifa:</strong> {{ viaje.tarifa }}</p>
          <p><strong>Estado:</strong> {{ viaje.estado }}</p>
        </div>

        <div id="map" style="height: 400px; width: 100%; margin-top: 20px;"></div>

        <div v-if="viaje && viaje.estado === 'completado'">
          <button @click="volverSolicitarViaje" class="btn-submit">Solicitar Nuevo Viaje</button>
        </div>
      </div>
    </div>

    <!-- Mapa (a la derecha del formulario, más grande) -->
    <div id="map-container" class="map-container">
      <div id="map" style="height: 100%; width: 100%;"></div>
    </div>
  </div>
</template>

<script>
/* global google */
import api from "@/services/apiService";
export default {
  data() {
    return {
      tarifa: 0,
      origen: "",
      destino: "",
      map: null,
      markerOrigen: null,
      markerDestino: null,
      autocompleteOrigen: null,
      autocompleteDestino: null,
      interval: null,
      viaje: null, // Estado del viaje
      directionsService: null, // Servicio para calcular rutas
      directionsRenderer: null, // Renderer para mostrar rutas
    };
  },

  async created() {
    const viajeId = localStorage.getItem("viaje_id");

    if (viajeId) {
      await this.cargarViaje(viajeId);

      if (this.viaje && this.viaje.estado === "en_progreso") {
        this.interval = setInterval(async () => {
          await this.cargarViaje(viajeId);
        }, 5000); // Verificar cada 5 segundos
      }
    }
  },

  beforeUnmount() {
    if (this.interval) {
      clearInterval(this.interval);
    }
  },

  methods: {
    async iniciarViaje() {
      try {
        const clienteId = localStorage.getItem("cliente_id");
        const viajeData = {
          origen: this.origen,
          destino: this.destino,
          tarifa: this.tarifa,
          cliente: clienteId,
        };
        const response = await api.createViaje(viajeData);
        alert(`Viaje iniciado con éxito. ID del viaje: ${response.data.id}`);
        localStorage.setItem("viaje_id", response.data.id);
        this.viaje = response.data;

        this.interval = setInterval(async () => {
          await this.cargarViaje(response.data.id);
        }, 5000);
      } catch (error) {
        console.error("Error al iniciar el viaje:", error);
        alert("Hubo un error al iniciar el viaje. Inténtalo nuevamente.");
      }
    },

    async cargarViaje(viajeId) {
      try {
        const response = await api.getViaje(viajeId);
        if (response.data) {
          this.viaje = response.data;
        }

        if (this.viaje.estado === "completado") {
          clearInterval(this.interval);
          localStorage.removeItem("viaje_id");
          this.viaje = null;
          this.origen = "";
          this.destino = "";
          this.tarifa = 0;
          this.initMap();
        }
      } catch (error) {
        console.error("Error al cargar el viaje:", error);
        this.viaje = null;
        clearInterval(this.interval);
      }
    },

    volverSolicitarViaje() {
      clearInterval(this.interval);
      localStorage.removeItem("viaje_id");
      this.viaje = null;
      this.origen = "";
      this.destino = "";
      this.tarifa = 0;

      this.$nextTick(() => {
        this.initMap();
      });
    },

    initMap() {
      const mapElement = document.getElementById("map");
      const defaultLocation = { lat: 40.416775, lng: -3.703790 }; // Madrid

      if (!this.map) {
        this.map = new google.maps.Map(mapElement, {
          center: defaultLocation,
          zoom: 13,
        });

        this.markerOrigen = new google.maps.Marker({
          map: this.map,
          position: defaultLocation,
          title: "Ubicación de recogida",
        });

        this.markerDestino = new google.maps.Marker({
          map: this.map,
          position: defaultLocation,
          title: "Ubicación de destino",
        });

        this.directionsService = new google.maps.DirectionsService();
        this.directionsRenderer = new google.maps.DirectionsRenderer();
        this.directionsRenderer.setMap(this.map);

        this.$nextTick(() => {
          if (this.$refs.origenInput && this.$refs.destinoInput) {
            this.autocompleteOrigen = new google.maps.places.Autocomplete(
              this.$refs.origenInput,
              { types: ["geocode"] }
            );

            this.autocompleteDestino = new google.maps.places.Autocomplete(
              this.$refs.destinoInput,
              { types: ["geocode"] }
            );

            this.autocompleteOrigen.addListener("place_changed", this.onOrigenChanged);
            this.autocompleteDestino.addListener("place_changed", this.onDestinoChanged);
          }
        });
      }
    },

    onOrigenChanged() {
      const place = this.autocompleteOrigen.getPlace();
      if (place.geometry) {
        this.origen = place.formatted_address;
        this.markerOrigen.setPosition(place.geometry.location);
        this.map.setCenter(place.geometry.location);
        this.map.setZoom(15);

        if (this.destino) {
          this.dibujarRuta();
        }
      } else {
        alert("Por favor, selecciona un lugar válido para la recogida.");
      }
    },

    onDestinoChanged() {
      const place = this.autocompleteDestino.getPlace();
      if (place.geometry) {
        this.destino = place.formatted_address;
        this.markerDestino.setPosition(place.geometry.location);
        this.map.setCenter(place.geometry.location);
        this.map.setZoom(15);

        if (this.origen) {
          this.dibujarRuta();
        }

        this.calcularTarifa();
      } else {
        alert("Por favor, selecciona un lugar válido para el destino.");
      }
    },

    dibujarRuta() {
      if (!this.origen || !this.destino) {
        alert("Por favor, asegúrate de que tanto origen como destino estén seleccionados.");
        return;
      }

      const request = {
        origin: this.markerOrigen.getPosition(),
        destination: this.markerDestino.getPosition(),
        travelMode: google.maps.TravelMode.DRIVING,
      };

      this.directionsService.route(request, (result, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
          this.directionsRenderer.setDirections(result);
        } else {
          alert("No se pudo calcular la ruta. Por favor, inténtelo nuevamente.");
        }
      });
    },

    calcularTarifa() {
      const service = new google.maps.DistanceMatrixService();
      service.getDistanceMatrix(
        {
          origins: [this.markerOrigen.getPosition()],
          destinations: [this.markerDestino.getPosition()],
          travelMode: "DRIVING",
        },
        (response, status) => {
          if (status === "OK" && response.rows[0].elements[0].status === "OK") {
            const distanceInMeters = response.rows[0].elements[0].distance.value;
            const distanceInKm = distanceInMeters / 1000;
            this.tarifa = (distanceInKm * 2).toFixed(2);
          } else {
            alert("No se pudo calcular la tarifa. Por favor, inténtelo nuevamente.");
          }
        }
      );
    },
  },

  mounted() {
    this.$nextTick(() => {
      this.initMap();
    });
  },
};
</script>

<style scoped>
#app {
  display: flex;
  justify-content: space-between;
  height: 100vh;
}

.form-container {
  width: 25%; /* Mantén el ancho del formulario pequeño */
  background-color: #f7f7f7;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: center; /* Centra el formulario verticalmente */
  align-items: center;
  height: 60%; /* Ajusta la altura del contenedor del formulario según sea necesario */
  padding: 20px; /* Agrega un poco de padding para que no esté pegado a los bordes */
}


.formulario {
  width: 90%; 
  height: auto; 
}

.map-container {
  width: 72%; 
  height: 100%; 
}

.title {
  font-family: "Helvetica Neue", sans-serif;
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.formulario .form-group {
  margin-bottom: 15px;
}

.input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-top: 5px;
}

.btn-submit {
  width: 100%;
  background-color: #1c1c1c;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.btn-submit:hover {
  background-color: #333;
}

#map {
  height: 100%; /* El mapa ocupa todo el espacio vertical */
  width: 100%;
}
</style>