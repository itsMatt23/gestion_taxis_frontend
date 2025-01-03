// src/services/api.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/usuarios/api';

// Crear una instancia de Axios
const apiClient = axios.create({
  baseURL: API_URL,
});

// Interceptor para añadir el token a las cabeceras
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
};
