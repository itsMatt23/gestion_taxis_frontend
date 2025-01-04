import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";

//Vistas del admin
import AdminView from "@/views/Admin/AdminView.vue";
import AdminRegistro from "../views/Admin/AdminRegistro.vue";
import PerfilView from "../views/PerfilView.vue";

//Vistas del cliente
import ClientsViews from "@/views/Clients/ClientsViews.vue";

//Vistas del Conductor
import DriversView from "@/views/Drivers/DriversView.vue";
//import holaView from "@/views/Drivers/holaView.vue";

import ClientsRegistro from "@/views/Clients/ClientsRegistro.vue";
//import DriversRegistro from "@/views/Drivers/DriversRegistro.vue";

// Vistas del viaje
import ClienteViaje from "@/views/Clients/ClienteViaje.vue";
import ConductorViaje from "@/views/Drivers/ConductorViaje.vue";

import ClienteHistorial from "@/views/Clients/ClienteHistorial.vue";
import ConductorHistorial from "@/views/Drivers/ConductorHistorial.vue";

const routes = [
  {
    path: "/",
    name: "Login",
    component: LoginView,
  },
  {
    path: "/registro",
    name: "Registro",
    component: RegisterView,
  },

  //ADMIN
  {
    path: "/Admin",
    name: "Admin",
    component: AdminView,
    meta: { requiresAuth: true, role: 'Admin' },
    redirect: "/AdminRegistro",
    children: [ 
      {
        path: "/AdminRegistro",
        name: "AdminRegistro",
        component: AdminRegistro,
        meta: { requiresAuth: true },
      },
      {
        path: "/AdminPerfil",
        name: "AdminPerfil",
        component: PerfilView,
        meta: { requiresAuth: true },
      }  
    ]  
  },

  //CLIENTE
  {
    path: "/Cliente",
    name: "Cliente",
    component: ClientsViews,
    meta: { requiresAuth: true, role: 'Cliente' }, // Ruta protegida para Cliente
    redirect: "/ClienteViaje",
    children:[
      {
        path: "/ClienteRegistro",
        name: "ClienteRegistro",
        component: ClientsRegistro,
        meta: { requiresAuth: true },
      },
      {
        path: "/ClientePerfil",
        name: "ClientePerfil",
        component: PerfilView,
        meta: { requiresAuth: true },
      },
      {
        path:"/ClienteViaje",
        name:"ClienteViaje",
        component:ClienteViaje,
        meta:{requiresAuth:true},
      },
      {
        path: "/ClienteHistorial",
        name: "ClienteHistorial",
        component: ClienteHistorial,
        meta: { requiresAuth: true },
      },
    ],
  },

  //CONDUCTOR
  {
    path: "/Conductor",
    name: "Conductor",
    component: DriversView,
    meta: { requiresAuth: true, role: 'Conductor' }, // Ruta protegida para Conductor
    redirect: "/ConductorViaje",
    children:[
      {
        path: "/ConductorPerfil",
        name: "ConductorPerfil",
        component: PerfilView,
        meta: { requiresAuth: true },
      } ,
      {
        path: "/ConductorViaje",
        name: "ConductorViaje",
        component: ConductorViaje,
        meta: { requiresAuth: true },
      },
      {
        path: "/ConductorHistorial",
        name: "ConductorHistorial",
        component: ConductorHistorial,
        meta: { requiresAuth: true },
      },

    ]
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Proteger rutas
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("access_token"); // Verificar si el token existe
  const user = JSON.parse(localStorage.getItem("userConected")); // Obtener el usuario conectado

  if (to.matched.some((record) => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: "Login" }); // Redirigir al login si no está autenticado
  } else if (to.matched.some((record) => record.meta.requiresAuth) && isAuthenticated) {
    if (to.matched.some((record) => record.meta.role && record.meta.role !== user.rol)) {
      // Redirigir a la pantalla destinada a su rol
      if (user.rol === 'Admin') {
        next({ name: "Admin" });
      } else if (user.rol === 'Cliente') {
        next({ name: "Cliente" });
      } else if (user.rol === 'Conductor') {
        next({ name: "Conductor" });
      } else {
        next({ name: "Login" }); // Redirigir al login si el rol no coincide con ninguno
      }
    } else {
      next(); // Permitir el acceso a la ruta
    }
  } else {
    next(); // Permitir el acceso a la ruta
  }
});

export default router;