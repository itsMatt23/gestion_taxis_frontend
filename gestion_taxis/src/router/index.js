import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import AdminView from "../views/Admin/AdminView.vue";
import AdminRegistro from "../views/Admin/AdminRegistro.vue";

import ClientsViews from "@/views/Clients/ClientsViews.vue";

import DriversView from "@/views/Drivers/DriversView.vue";
import RegisterView from "@/views/RegisterView.vue";


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

  {
    path: "/Admin",
    name: "Admin",
    component: AdminView,
    meta: { requiresAuth: true, role: 'Admin' }, // Ruta protegida para Admin
    redirect: "/AdminRegistro",
    children: [ 
      {
        path: "/AdminRegistro",
        name: "AdminRegistro",
        component: AdminRegistro,
        meta: { requiresAuth: true },
      }   
    ]  

  },
  {
    path: "/Cliente",
    name: "Cliente",
    component: ClientsViews,
    meta: { requiresAuth: true, role: 'Cliente' }, // Ruta protegida para Cliente
  },
  {
    path: "/Conductor",
    name: "Conductor",
    component: DriversView,
    meta: { requiresAuth: true, role: 'Conductor' }, // Ruta protegida para Conductor
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