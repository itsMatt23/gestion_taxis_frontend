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

<!-- Mostrar el mapa también en los detalles -->
      <div id="map" style="height: 400px; width: 100%; margin-top: 20px;"></div>

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
       directionsService: null, // Servicio para calcular rutas
      directionsRenderer: null, // Renderer para mostrar rutas
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
         alert(`Viaje iniciado con éxito. ID del viaje: ",${response.data.id}`);
          //alert("Viaje iniciado con éxito. ID del viaje: ",${response.data.id});
          localStorage.setItem("viaje_id", response.data.id);
          this.viaje = response.data; // Actualizar el viaje actual


// Iniciar el temporizador
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
        if(response.data){
        this.viaje = response.data;

        /*

        // Dibujar la ruta en el mapa si el viaje está en progreso o completado
if (this.viaje.origen && this.viaje.destino) {
            this.origen = this.viaje.origen;
            this.destino = this.viaje.destino;
            this.dibujarRuta();
          }
*/


        if(this.viaje.estado === "completado"){
        clearInterval(this.interval);
        localStorage.removeItem("viaje_id");

         // Reiniciar formulario y mapa
            this.viaje = null;
            this.origen = "";
            this.destino = "";
            this.tarifa = 0;
        this.initMap();
        }      
        }else{ this.viaje = null;
        }

        } catch (error) {
          console.error("Error al cargar el viaje:", error);
          this.viaje=null;
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
   
    // Asegúrate de reiniciar correctamente el mapa
    this.$nextTick(() => {
      this.initMap(); // Reinicia el mapa después de que el DOM esté listo
    });
  },
    initMap() {
      const mapElement = document.getElementById("map");
      if (!mapElement) {
        console.error("No se encontró el elemento del mapa en el DOM.");
        return;
      }

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

// Inicializar el servicio y el renderer para las rutas
      this.directionsService = new google.maps.DirectionsService();
      this.directionsRenderer = new google.maps.DirectionsRenderer();
      this.directionsRenderer.setMap(this.map);

    // Inicializar Autocomplete solo si los refs están disponibles
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

// Intentar dibujar la ruta si ya hay destino
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

// Intentar dibujar la ruta si ya hay origen
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