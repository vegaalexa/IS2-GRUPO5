//funcion que emitar una alerta cuando se quiere eliminar un usuario
(function () {

    const btnEliminacion = document.querySelectorAll(".btnEliminacion");

    btnEliminacion.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Seguro que quieres eliminar?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });
    
})();

function habilitarDeshabilitarCRUD(permisosPorPantalla, nombrePantalla){
    registrar(permisosPorPantalla, nombrePantalla);
    editar(permisosPorPantalla, nombrePantalla);
    eliminar(permisosPorPantalla, nombrePantalla);
    leer(permisosPorPantalla, nombrePantalla);

    if(nombrePantalla == 'BackLog' ){
        asignar(permisosPorPantalla, 'Proyecto');
    }
    else if(nombrePantalla == 'Proyecto'){
        asignar(permisosPorPantalla, 'BackLog');
    }
    else if(nombrePantalla == 'UserStory'){
        asignar(permisosPorPantalla, 'SprintBackLog');
    }
}


function asignar(permisosPorPantalla, nombrePantalla){
    //var btnGuardar = document.querySelectorAll(".btnAsignarProyecto");
    var btnAsignar = document.getElementById("btnAsignar".concat(nombrePantalla));

    //deshabilitamos la opcion de asignar
    const link = btnAsignar.href;
    btnAsignar.href = '#';
    
    //solo en caso de que tenga el permiso correspondiente
    for (let i = 0; i < permisosPorPantalla.length; i++) {
        if(permisosPorPantalla[i] == 'C'){
            btnAsignar.href = link;
            break;
        }
    }
    //lo habilitamos
    
}


function registrar(permisosPorPantalla, nombrePantalla){
    //obtenemos los campos 
    const btnGuardar = document.querySelectorAll(".btnGuardar".concat(nombrePantalla));
    var inputEmail = null;
    var inputTipo = null;
    var inputDescripcion = null;
    
    if(nombrePantalla == 'Usuario'){
        inputEmail = document.getElementById("txtEmail");
        inputEmail.disabled = true;
    }
    else{
        inputDescripcion = document.getElementById("txtDescripcion".concat(nombrePantalla));
        inputDescripcion.disabled = true;

        if(nombrePantalla == 'Permiso'){
            inputTipo = document.getElementById("txtTipoPermiso");
            inputTipo.disabled = true;
        }
    }



    const inputNombre = document.getElementById("txtNombre".concat(nombrePantalla));
    inputNombre.disabled = true;

    //deshabilitamos la opcion de registrar
    btnGuardar.forEach(btn => {
        btn.disabled = true;
    });

    
    //solo en caso de que tenga el permiso correspondiente
    //lo habilitamos
    for (let i = 0; i < permisosPorPantalla.length; i++) {
        if(permisosPorPantalla[i] == 'C'){
            inputNombre.disabled = false;

            if(nombrePantalla == 'Usuario'){
                inputEmail.disabled = false;
            }
            else{
                inputDescripcion.disabled = false;

                if(nombrePantalla == 'Permiso'){
                    inputTipo.disabled = false;
                }
            }

            btnGuardar.forEach(btn => {
                btn.disabled = false;
            });

            break;
        }
    }

}


function editar(permisosPorPantalla, nombrePantalla){
    const btnEditar = document.querySelectorAll(".btnEditar".concat(nombrePantalla));
    //deshabilitamos la opcion de editar
    btnEditar.forEach(btn => {
        btn.classList.add("disabled");
    });

    //solo en caso de que tenga el permiso correspondiente
    //lo habilitamos
    for (let i = 0; i < permisosPorPantalla.length; i++) {
        if(permisosPorPantalla[i] == 'U'){
            btnEditar.forEach(btn => {
                btn.classList.remove("disabled");
            });

            break;
        }
    }
}

function eliminar(permisosPorPantalla, nombrePantalla){
    const btnEliminacion = document.querySelectorAll(".btnEliminar".concat(nombrePantalla));
    //deshabilitamos la opcion de editar
    btnEliminacion.forEach(btn => {
        btn.classList.add("disabled");
    });

    //solo en caso de que tenga el permiso correspondiente
    //lo habilitamos
    for (let i = 0; i < permisosPorPantalla.length; i++) {
        if(permisosPorPantalla[i] == 'D'){

            btnEliminacion.forEach(btn => {
                btn.classList.remove("disabled");
            });

            break;
        }
    }
}

function leer(permisosPorPantalla, nombrePantalla){
    var permisoLectura = false;
    for (let i = 0; i < permisosPorPantalla.length; i++) {
        if(permisosPorPantalla[i] == 'R'){
            permisoLectura = true;
            break;
        }
    }

    if(permisoLectura == false){
        //no posee permiso de lectura, la pantalla se restringe
        $('#divListado'.concat(nombrePantalla)).css({"pointer-events" : "none" , "opacity" :  "0.0"}).attr("tabindex" , "-1");
    }
    
}
