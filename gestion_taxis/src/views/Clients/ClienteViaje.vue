<template>
  <div>
    <!-- Formulario para solicitar un viaje -->
    <div v-if="!viaje || (viaje && viaje.estado !== 'en_progreso')">
      <h1>Solicitar un Viaje</h1>
      <form @submit.prevent="iniciarViaje">
        <div>
          <label for="origen">Ubicación de recogida</label>
          <input
            id="origen"
            type="text"
            placeholder="Escribe la ubicación de recogida"
            ref="origenInput"
            required
          />
        </div>
        <div>
          <label for="destino">Ubicación de destino</label>
          <input
            id="destino"
            type="text"
            placeholder="Escribe la ubicación de destino"
            ref="destinoInput"
            required
          />
        </div>
        <div>
          <label for="tarifa">Tarifa estimada</label>
          <input
            id="tarifa"
            type="number"
            placeholder="Tarifa del viaje"
            v-model="tarifa"
            readonly
          />
        </div>
        <button type="submit" class="btn btn-primary mt-3">Solicitar Viaje</button>
      </form>
      <div id="map" style="height: 400px; width: 100%; margin-top: 20px;"></div>
    </div>

    <!-- Detalles del viaje en progreso -->
    <div v-else>
      <h1 v-if="viaje && viaje.estado === 'en_progreso'">Viaje En Progreso</h1>
      <h1 v-else-if="viaje && viaje.estado === 'completado'">Viaje Finalizado</h1>
      <div v-if="viaje">
        <h3>Detalles del Viaje</h3>
        <p><strong>Origen:</strong> {{ viaje.origen }}</p>
        <p><strong>Destino:</strong> {{ viaje.destino }}</p>
        <p><strong>Tarifa:</strong> {{ viaje.tarifa }}</p>
        <p><strong>Estado:</strong> {{ viaje.estado }}</p>
      </div>
      <div v-if="viaje && viaje.estado === 'completado'">
        <button @click="volverSolicitarViaje" class="btn btn-primary mt-3">Solicitar Nuevo Viaje</button>
      </div>
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
    };
  },

async created() {
      const viajeId = localStorage.getItem("viaje_id");
  
      if (viajeId) {
        await this.cargarViaje(viajeId);
  
        if (this.viaje && this.viaje.estado === "en_progreso") {
          // Configura un temporizador para verificar el estado del viaje
          this.interval = setInterval(async () => {
            await this.cargarViaje(viajeId);
            if (this.viaje.estado === "completado") {
              clearInterval(this.interval); // Detén el temporizador
            }
          }, 2000); // Verificar cada 5 segundos
        } else {
          this.viaje = null; // No hay viaje en progreso
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
         alert(`Viaje iniciado con éxito. ID del viaje: ",${response.data.id}`);
          //alert("Viaje iniciado con éxito. ID del viaje: ",${response.data.id});
          localStorage.setItem("viaje_id", response.data.id);
          this.viaje = response.data; // Actualizar el viaje actual
        } catch (error) {
          console.error("Error al iniciar el viaje:", error);
          alert("Hubo un error al iniciar el viaje. Inténtalo nuevamente.");
        }
    
    },
     async cargarViaje(viajeId) {
        try {
          const response = await api.getViaje(viajeId);
          this.viaje = response.data;

if (this.viaje && this.viaje.estado === "completado") {
        clearInterval(this.interval); // Detén el temporizador
        this.viaje = null; // Reinicia el estado del viaje
        localStorage.removeItem("viaje_id");
        this.initMap(); // Reinicializa el mapa
      }



        } catch (error) {
          console.error("Error al cargar el viaje:", error);
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
    this.initMap(); // Reinicializa el mapa
  },
    initMap() {
      const mapElement = document.getElementById("map");
      if (!mapElement) {
        console.error("No se encontró el elemento del mapa en el DOM.");
        return;
      }

      const defaultLocation = { lat: 40.416775, lng: -3.703790 }; // Madrid
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
    },
    onOrigenChanged() {
      const place = this.autocompleteOrigen.getPlace();
      if (place.geometry) {
        this.origen = place.formatted_address;
        this.markerOrigen.setPosition(place.geometry.location);
        this.map.setCenter(place.geometry.location);
        this.map.setZoom(15);
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
        this.calcularTarifa();
      } else {
        alert("Por favor, selecciona un lugar válido para el destino.");
      }
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

            // Fórmula de tarifa personalizada
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
