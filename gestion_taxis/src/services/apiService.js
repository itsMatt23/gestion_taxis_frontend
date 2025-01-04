// src/services/api.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/usuarios/api';

const API_VIAJES_URL = 'http://localhost:8000/api/viajes';

const apiViajes = axios.create({
  baseURL: API_VIAJES_URL,
});


// Crear una instancia de Axios
const apiClient = axios.create({
  baseURL: API_URL,
});


// Interceptor para añadir el token a las cabeceras
const addTokenInterceptor = (client) => {
  client.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`; // Añadir el token en las cabeceras
    }
    return config;
  }, error => {
    return Promise.reject(error);
  });
};

addTokenInterceptor(apiClient);
addTokenInterceptor(apiViajes);

// Interceptor para manejar respuestas y errores
const handleResponseError = (client, apiName) => {
  client.interceptors.response.use(
    response => response, // Dejar pasar respuestas exitosas
    error => {
      if (error.response && error.response.status === 500) {
        alert(`Error en ${apiName}: No se pudo conectar al servidor. Por favor, inténtelo más tarde.`);
      } else if (error.response && error.response.status === 401) {
        alert(`Error de autenticación en ${apiName}: Su sesión ha expirado. Por favor, vuelva a iniciar sesión.`);
        // Opcionalmente, redirige al usuario a la página de inicio de sesión
        window.location.href = '/login';
      } else {
        console.error(`Error en ${apiName}:`, error.message);
      }
      return Promise.reject(error);
    }
  );
};


handleResponseError(apiClient, 'API de Usuarios');
handleResponseError(apiViajes, 'API de Viajes');

// Interceptor para añadir el token a las cabeceras
/*
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`; // Añadir el token en las cabeceras
  }
  return config;
}, error => {
  return Promise.reject(error);
});


apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 500) {
      alert("Error de conexión: No se pudo conectar a la base de datos. Por favor, inténtelo más tarde.");
    } else {
      console.log("Error en la conexion vuelva a inicar session")
    }
    return Promise.reject(error);
  }
);

*/

export default {
  login(email, password) {
    return apiClient.post('/login/', {
      email,
      password,
    });
  },

  buscarUsuario(email) {
    return apiClient.get(`/buscar_usuario/`, {
      params: { email },
    });
  },

  /////CRUD Usuarios
  //Usuaios
  getUsers() {
    return apiClient.get('/usuarios/');
  },
  createUser(usuario) {
    return apiClient.post('/usuarios/', usuario);
  },
  updateUser(id, usuario) {
    return apiClient.put(`/usuarios/${id}/`, usuario);
  },
  deleteUser(id) {
    return apiClient.delete(`/usuarios/${id}/`);
  },

 // Funciones para Viajes
 createViaje(viaje) {
  return apiViajes.post('/', viaje);
},

getViajes() {
  return apiViajes.get('/');
},

getViaje(id) {
  return apiViajes.get(`/${id}/`);
},

completarViaje(id) {
  return apiViajes.post(`/${id}/completar/`);
},

getViajeAsignado(conductorId) {
  return apiViajes.get(`/asignado/${conductorId}/`);
},

cancelarViaje(id) {
  return apiViajes.post(`/${id}/cancelar/`);
},

asignarConductor(id) {
  return apiViajes.post(`/${id}/asignar_conductor/`);
},

historialCliente(clienteId) {
  return apiViajes.get('/historial_cliente/', { params: { cliente: clienteId } });
},

historialConductor(conductorId) {
  return apiViajes.get('/historial_conductor/', { params: { conductor: conductorId } });
},


};
