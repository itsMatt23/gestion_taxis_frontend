<template>
    <div class="profile-container">
        <h2 class="text-center mb-4">Mi Perfil</h2>

        <div class="profile-icon">
            <img :src="require('@/assets/perfil.jpg')" alt="Ícono de perfil" />
        </div>

        <form @submit.prevent="actualizarUsuario" class="profile-form">
            <div class="form-group">
                <label for="cedula">Cédula:</label>
                <input type="text" id="cedula" v-model="perfil.cedula" placeholder="Ingrese la cédula del usuario" required disabled />
            </div>

            <div class="form-group">
                <label for="nombre">Nombre:</label>
                <input type="text" id="nombre" v-model="perfil.nombre" placeholder="Ingrese el nombre del usuario" required />
            </div>
            
            <div class="form-group">
                <label for="apellido">Apellido:</label>
                <input type="text" id="apellido" v-model="perfil.apellido" placeholder="Ingrese el apellido del usuario" required />
            </div>

            <div class="form-group">
                <label for="telefono">Teléfono:</label>
                <input type="text" id="telefono" v-model="perfil.telefono" placeholder="Ingrese el teléfono del usuario" required />
            </div>

            <div class="form-group">
                <label for="email">Correo Electrónico:</label>
                <input disabled type="email" id="email" v-model="perfil.email" placeholder="Ingrese el correo electrónico" required />
            </div>

            <div class="form-group">
                <label for="group">Rol:</label>
                <select disabled id="group" v-model="perfil.rol" required>
                    <option disabled value="">Seleccione el rol del usuario</option>
                    <option disabled value="Admin">Administrador</option>
                    <option disabled value="Cliente">Cliente</option>
                    <option disabled value="Conductor">Conductor</option>
                </select>
            </div>

            <div class="form-group">
                <label for="password">Nueva Contraseña:</label>
                <input type="password" id="password" v-model="perfil.password" placeholder="Ingrese la nueva contraseña (opcional)" />
            </div>

            <div v-if="perfil && perfil.rol == 'Conductor'">
                <div class="form-group">
                    <label for="marca_vehiculo">Marca del Vehículo:</label>
                    <input type="text" id="marca_vehiculo" v-model="perfil.marca_vehiculo" placeholder="Ingrese la marca del vehículo" required />
                </div>

                <div class="form-group">
                    <label for="placa">Placa del Vehículo:</label>
                    <input type="text" id="placa" v-model="perfil.placa" placeholder="Ingrese la placa del vehículo" maxlength="6" required />
                </div>
            </div>

            <button type="submit" class="btn-update">Actualizar</button>
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
