// Agregar un evento 'click' al botón de conversión
document.getElementById('convert-btn').addEventListener('click', async function () {
    // Obtener el elemento de entrada de archivo
    var fileInput = document.getElementById('pdf-file');
    // Obtener el archivo seleccionado
    var file = fileInput.files[0];
    // Verificar si se seleccionó un archivo
    if (file) {
        // Mostrar un loading para indicar que se está procesando la solicitud
        showOverlay();
        // Deshabilitar el botón de conversión mientras se procesa la solicitud
        disableButtonSave(true, "convert-btn");
         // Crear un objeto FormData para enviar el archivo al servidor
        var formData = new FormData();
        formData.append('pdf_file', file);
         // Configuración de la solicitud HTTP
        const requestOptions = {
            method: 'POST',
            body: formData
        };

        try {
            // Enviar la solicitud al servidor y esperar la respuesta
            const response = await fetch('/extract-table-pdf/', requestOptions);
            // Verificar si la respuesta es exitosa
            if (!response.ok) {
                // Si la respuesta no es exitosa, lanzar un error con el mensaje de error proporcionado
                const errorMessage = await response.text();
                throw new Error(errorMessage);
            }
            // Obtener el contenido de la respuesta como un blob
            const blob = await response.blob();
            // Habilitar el botón de conversión después de recibir la respuesta
            disableButtonSave(false, "convert-btn");
            // Crear un objeto URL para el blob
            const url = window.URL.createObjectURL(blob);
            // Crear un enlace <a> para descargar el archivo
            const a = document.createElement('a');
            a.href = url;
            a.download = 'documento.xlsx';
             // Agregar el enlace al DOM
            document.body.appendChild(a);
            // Simular el clic en el enlace
            a.click(); 
            // Liberar el objeto URL
            window.URL.revokeObjectURL(url);
        } catch (error) {
            // Manejar cualquier error que ocurra durante el proceso de conversión
            swalValidateInputFile(error);
        } finally {
             // Ocultar el overlay después de completar el proceso
            hideOverlay();
            // Restablecer el valor del elemento de entrada de archivo
            fileInput.value = '';
             // Restablecer el texto del label del elemento de entrada de archivo
            setTextLabelInputFile("Seleccionar archivo");
            // Habilitar nuevamente el botón de conversión
            disableButtonSave(false, "convert-btn");
        }
    } else {
        // Si no se selecciona ningún archivo, mostrar un mensaje de error
        swalValidateInputFile("Debe seleccionar un archivo PDF");
    }
});

// Función para manejar la selección de archivos
function handleFileSelect() {
    const selectedFile = document.getElementById('pdf-file').files[0];
    const textMessage = "Archivo seleccionado: " + selectedFile.name;
    setTextLabelInputFile(textMessage);
}
// Función para establecer el mensaje en el elemento de etiqueta de archivo
function setTextLabelInputFile(msg) {
    const spanText = document.getElementById('file-span');
    spanText.textContent = msg;
}
// Función para deshabilitar o habilitar un botón
function disableButtonSave(val, id) {
    var btnGuardar = document.getElementById(id);
    btnGuardar.disabled = val;
    if (val === true) {
        btnGuardar.style.opacity = "0.5";
        btnGuardar.style.cursor = "not-allowed";
    } else if (val === false) {
        btnGuardar.style.opacity = "";
        btnGuardar.style.cursor = "";
    }
}
// Función para mostrar un mensaje de validación utilizando SweetAlert
function swalValidateInputFile(msg) {
    Swal.fire({
        html: "<h4>" + msg + "</h4>",
        icon: "info",
        width: "300px",
        confirmButtonText: "Aceptar",
        confirmButtonColor: "#3085d6"
    });
}
// Función para mostrar el loading
function showOverlay() {
    const overlay = document.querySelector('.loader-overlay');
    overlay.style.opacity = '1';
    overlay.style.visibility = 'visible';
}
// Función para ocultar el loading
function hideOverlay() {
    const overlay = document.querySelector('.loader-overlay');
    overlay.style.opacity = '0';
    overlay.style.visibility = 'hidden';
}
