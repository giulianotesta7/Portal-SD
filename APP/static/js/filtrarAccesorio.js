document.addEventListener("DOMContentLoaded", () => {
  const organismoSelect = document.getElementById("organismo");

  const accesorioSelects = [
    document.getElementById("accesorio1"),
    document.getElementById("accesorio2"),
    document.getElementById("accesorio3")
  ];

  // Guardamos copia de TODAS las opciones originales de cada accesorio
  const opcionesOriginales = accesorioSelects.map(select =>
    Array.from(select.options).map(opt => opt.cloneNode(true))
  );

  function filtrarAccesorios() {
    const orgSeleccionado = organismoSelect.value;

    accesorioSelects.forEach((select, i) => {
      const opciones = opcionesOriginales[i];
      select.innerHTML = "";

      opciones.forEach(opt => {
        if (!opt.dataset.organismo || opt.dataset.organismo === orgSeleccionado || opt.value === "") {
          select.appendChild(opt.cloneNode(true));
        }
      });
    });
  }

  organismoSelect.addEventListener("change", filtrarAccesorios);
  filtrarAccesorios(); // ejecutar al inicio
});
