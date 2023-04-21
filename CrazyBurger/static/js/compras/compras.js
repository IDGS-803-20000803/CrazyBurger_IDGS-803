$(document).ready(function () {
    $('#tblCompra').DataTable({
        language: {
            "decimal": "",
            "emptyTable": "No hay información",
            "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
            "infoEmpty": "Mostrando 0 de 0 de 0 Entradas",
            "infoFiltered": "(Filtrado de _MAX_ total entradas)",
            "infoPostFix": "",
            "thousands": ",",
            "lengthMenu": "Mostrar _MENU_ Entradas",
            "loadingRecords": "Cargando...",
            "processing": "Procesando...",
            "search": "Buscar:",
            "zeroRecords": "Sin resultados encontrados",
            "paginate": {
                "first": "Primero",
                "last": "Ultimo",
                "next": "Siguiente",
                "previous": "Anterior"
            }
        },
        columnDefs: [{
            "targets": [4],
            "searchable": true,
            "orderable": false
        }]
    });
});

// Generar evento que se ejecuta cuando se selecciona un valor del select
document.getElementById("compra").addEventListener("change", obtenerValorSelect);

function obtenerValorSelect() {

    let valor = document.getElementById("compra").value;

    if (valor == "Other") {

        // Mostrar un input
        document.getElementById("otherCompra").style.display = "block";

        document.getElementById("nombreCompra").style.display = "none";
        document.getElementById("nombreCompra").removeAttribute("required");

        // Agregar un atributo required
        document.getElementById("otherCompra").setAttribute("required", "required");

        // Agregar que solo acepte numeros enteros en el input
        document.getElementById("cantidadCompra").setAttribute("step", "1");
        document.getElementById("cantidadCompra").setAttribute("min", "1");

    }else if (valor == "Ingrediente") {
        
        // Ocultar el input
        document.getElementById("otherCompra").style.display = "none";

        // Opciones de NombreCompra
        document.getElementById("nombreCompra").style.display = "block";
        document.getElementById("nombreCompra").setAttribute("required", "required");

        // Remover el atributo required
        document.getElementById("otherCompra").removeAttribute("required");

        // Agregar que acepte numeros con decimales en el input con 2 decimales con step
        document.getElementById("cantidadCompra").setAttribute("step", "0.1");
        document.getElementById("cantidadCompra").setAttribute("min", "1");

        document.getElementById("unidadMedida").style.display = "block";
        document.getElementById("sltUnidadMedida").setAttribute("required", "required");
    }
}

function eliminarCompra(id) {

    var csrf_token = document.getElementsByName("csrf-token")[0].content;

    Swal.fire({
        title: '¿Estás seguro?',
        text: "¡No podrás revertir esto!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar!',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: "/compras/eliminarCompra?id=" + id,
                type: "GET",
                headers: {
                    "X-CSRFToken": csrf_token
                }
            }).done(function (data) {
        
                console.log(data);
        
                if (data.status == "success") {
                    
                    Swal.fire({
                        title: 'Compra eliminada',
                        text: 'La compra se ha eliminado correctamente',
                        icon: 'success',
                        confirmButtonText: 'Aceptar'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            location.reload();
                        }
                    });
        
                } else {
                    alert("Error al eliminar");
                }
            });
        }
    });
}