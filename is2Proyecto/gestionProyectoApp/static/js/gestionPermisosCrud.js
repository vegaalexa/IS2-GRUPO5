//funcion que emitar una alerta cuando se quiere eliminar un usuario
(function () {

    const btnEliminacion = document.querySelectorAll(".btnEliminacion");

    btnEliminacion.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Seguro de eliminar el usuario?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });
    
})();

function habilitarDeshabilitarCRUD(permisosPorPantalla){
    registrarUsuario(permisosPorPantalla)
}

function registrarUsuario(permisosPorPantalla){
    //obtenemos los campos 
    const btnGuardarUsuario = document.querySelectorAll(".btnGuardarUsuario");
    const inputEmail = document.getElementById("txtEmail");
    const inputNombre = document.getElementById("txtNombre");

    //deshabilitamos la opcion de registrar usuario
    btnGuardarUsuario.forEach(btn => {
        btn.disabled = true;
    });

    inputNombre.disabled = true;
    inputEmail.disabled = true;
    
    //solo en caso de que tenga el permiso correspondiente
    //lo habilitamos
    for (let i = 0; i < permisosPorPantalla.length; i++) {
        if(permisosPorPantalla[i] == 'C'){
            inputNombre.disabled = false;
            inputEmail.disabled = false;
            const btnGuardarUsuario = document.querySelectorAll(".btnGuardarUsuario");

            btnGuardarUsuario.forEach(btn => {
                btn.disabled = false;
            });

            break;
        }
    }
}
