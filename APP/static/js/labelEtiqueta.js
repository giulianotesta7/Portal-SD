document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("dispositivo_id");
  const etiquetaContainer = document.getElementById("etiqueta-container");

  const dispositivosConEtiqueta = ["Notebook", "Desktop", "Celular", "Tablet"];

  function actualizarEtiqueta() {
    const nombre = select.options[select.selectedIndex].dataset.nombre;

    if (dispositivosConEtiqueta.includes(nombre)) {
      etiquetaContainer.style.display = "block";
    } else {
      etiquetaContainer.style.display = "none";
    }
  }

  select.addEventListener("change", actualizarEtiqueta);
  actualizarEtiqueta(); // Ejecutar al cargar
});
