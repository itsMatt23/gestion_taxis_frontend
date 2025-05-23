<template>
    <div class="profile-container">
        <h2 class="text-center mb-3">Mi Perfil</h2>

        <div class="profile-icon">
            <img :src="require('@/assets/perfil.jpg')" alt="Ícono de perfil" />
        </div>

        <form @submit.prevent="actualizarUsuario" class="profile-form">
            <div class="form-group">
                <label for="cedula">Cedula:</label>
                <input type="text" id="text" v-model="perfil.cedula" placeholder="Ingrese la cedula del usaurio"
                    required disabled />
            </div>

            <div class="form-group">
                <label for="nombre">Nombre:</label>
                <input type="text" id="nombre" v-model="perfil.nombre" placeholder="Ingrese el nombre del usuario"
                    required />
            </div>
            
            <div class="form-group">
                <label for="apellido">Apellido:</label>
                <input type="text" id="apellido" v-model="perfil.apellido" placeholder="Ingrese el apellido del usuario"
                    required />
            </div>

            <div class="form-group">
                <label for="telefono">Telefono:</label>
                <input type="text" id="text" v-model="perfil.telefono"
                    placeholder="Ingrese el correo electrónico" required disabled />
            </div>

            <div class="form-group">
                <label for="email">Correo Electrónico:</label>
                <input disabled type="email" id="email" v-model="perfil.email"
                    placeholder="Ingrese el correo electrónico" required />
            </div>

            <div class="form-group">
                <label for="group" class="form-label">Rol:</label>
                <select disabled id="group" class="form-select" v-model="perfil.rol" required>
                    <option disabled value="">Seleccione el rol del usuario</option>
                    <option disabled value="Admin">Administrador</option>
                    <option disabled value="Cliente">Cliente</option>
                    <option disabled value="Conductor">Conductor</option>
                </select>
            </div>

            <div class="form-group">
                <label for="password">Nueva Contraseña:</label>
                <input type="password" id="password" v-model="perfil.password"
                    placeholder="Ingrese la nueva contraseña (opcional)" maxlength="10" />
            </div>
            <small v-if="perfil.password" class="form-text text-muted">
                    La contraseña debe tener:
                    <ul>
                        <li
                            v-bind:class="{ 'text-success': passwordValidations.length, 'text-danger': !passwordValidations.length }">
                            Entre 4 y 10 caracteres.</li>
                        <li v-bind:class="{
                            'text-success': passwordValidations.number,
                            'text-danger': !passwordValidations.number,
                        }">
                            Un número.
                        </li>
                        <li v-bind:class="{
                            'text-success': passwordValidations.uppercase,
                            'text-danger': !passwordValidations.uppercase,
                        }">
                            Una letra mayúscula.
                        </li>
                        <li v-bind:class="{
                            'text-success': passwordValidations.special,
                            'text-danger': !passwordValidations.special,
                        }">
                            Un carácter especial.
                        </li>
                    </ul>
                </small>

            <div v-if="perfil && perfil.rol == 'Conductor'">
                <div class="form-group">
                <label for="marca_vehiculo">Marca Vehiculo:</label>
                <input type="text" id="marca_vehiculo" v-model="perfil.marca_vehiculo"
                    placeholder="Ingrese el modelo del vehiculo" required />
            </div>

            <div class="form-group">
                <label for="placa">Placa del vehiculo:</label>
                <input type="text" id="placa" v-model="perfil.placa"
                    placeholder="Ingrese la placa del vehiculo"
                    maxlength="6"
                    required/>
            </div>
        </div>



            
            <button type="submit" class="btn btn-dark w-100 mt-2">Actualizar</button>
        </form>
    </div>
</template>

<script>
import apiService from "@/services/apiService";

export default {
    data() {
        return {
            perfil: "",
        };
    },
    computed:{
    passwordValidations() {
      return {
        length: this.perfil.password.length >= 4 && this.perfil.password.length <= 10,
        number: /\d/.test(this.perfil.password),
        uppercase: /[A-Z]/.test(this.perfil.password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(this.perfil.password),
      };
    },
  },

    methods: {
        async cargarPerfil() {
            const storedUser = localStorage.getItem('userConected');
            if (storedUser) {
                this.perfil = JSON.parse(storedUser); // Convertir de JSON a objeto
            }
        },

        async actualizarUsuario() {
            try {
                const usuarioActualizado = {
                    ...this.perfil, // Copia los datos actuales
                };

                if (!usuarioActualizado.password) {
                    delete usuarioActualizado.password; // Elimina el campo si está vacío o nulo
                }

                if (!this.passwordValidations.length || !this.passwordValidations.number || !this.passwordValidations.uppercase || !this.passwordValidations.special) {
                    alert("La contraseña no cumple con los requisitos.");
                    return;
                }

                const response = await apiService.updateUser(usuarioActualizado.id, usuarioActualizado);
                if (response.data) {
                    this.perfil = response.data;
                    localStorage.setItem('userConected', JSON.stringify(this.perfil));
                    alert('Usuario actualizado correctamente.');
                    location.reload();
                }
            } catch (error) {
                console.error('Error al actualizar el usuario:', error);
                alert('Ocurrió un error al actualizar el usuario.');
            }
        },

        logout() {
            localStorage.removeItem("access_token");
            localStorage.removeItem("username");
            alert("Es necesario volver a ingresar.");
            this.$router.push({ name: "Login" });
        },
    },

    mounted() {
        this.cargarPerfil();
    },
};
</script>

<style scoped>
.profile-container {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

h2 {
    text-align: center;
    color: #333;
    margin-bottom: 20px;
    font-size: 1.5rem;
}

.profile-icon {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

.profile-icon img {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 2px solid #ddd;
}

.profile-form {
    display: flex;
    flex-direction: column;
}

.form-group {
    margin-bottom: 20px;
}

label {
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 1rem;
}

input,
select {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    background-color: #f9f9f9;
}

input:disabled,
select:disabled {
    background-color: #e0e0e0;
}

.btn-update {
    width: 100%;
    padding: 12px;
    background-color: #000;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.btn-update:hover {
    background-color: #333;
}

@media (max-width: 768px) {
    .profile-container {
        padding: 15px;
        max-width: 90%;
    }

    h2 {
        font-size: 1.25rem;
    }

    .btn-update {
        font-size: 1rem;
    }
}

@media (max-width: 480px) {
    .profile-container {
        max-width: 100%;
        padding: 10px;
    }

    h2 {
        font-size: 1rem;
    }

    .btn-update {
        font-size: 0.9rem;
    }
}
</style>
