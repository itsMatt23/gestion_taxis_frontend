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
                    placeholder="Ingrese el correo electrónico" required />
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
                    placeholder="Ingrese la nueva contraseña (opcional)" />
            </div>

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
    computed: {
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
                //console.log(usuarioActualizado);

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
    background: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

h2 {
    text-align: center;
    color: #333;
    margin-bottom: 20px;
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
    margin-bottom: 15px;
}

label {
    margin-bottom: 5px;
}

input,
select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 14px;
    background: #fff;
}

input:disabled,
select:disabled {
    background: #f0f0f0;
}

.btn-update {
    width: 100%;
    padding: 10px;
    background: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    transition: background 0.3s ease;
}

.btn-update:hover {
    background: #0056b3;
}
</style>
