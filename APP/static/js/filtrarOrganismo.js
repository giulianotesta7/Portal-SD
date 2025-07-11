document.addEventListener("DOMContentLoaded", () => {
  const organismoSelect = document.getElementById("organismo");
  const dispositivoSelect = document.getElementById("dispositivo_id");

  // Guardar una copia completa de las opciones originales
  const todasLasOpciones = Array.from(dispositivoSelect.options).map(opt => opt.cloneNode(true));
  
  console.log("Opciones cargadas:", todasLasOpciones.map(opt => ({
  nombre: opt.textContent,
  organismo: opt.dataset.organismo
})));

  function filtrarDispositivos() {
    const organismoSeleccionado = organismoSelect.value;

    // Vaciar el select actual
    dispositivoSelect.innerHTML = "";

    // Filtrar por el data-organismo
    const opcionesFiltradas = todasLasOpciones.filter(opt =>
      opt.dataset.organismo === organismoSeleccionado
    );

    if (opcionesFiltradas.length > 0) {
      opcionesFiltradas.forEach(opt => dispositivoSelect.appendChild(opt));
    } else {
      const opt = document.createElement("option");
      opt.textContent = "Sin dispositivos disponibles";
      opt.disabled = true;
      dispositivoSelect.appendChild(opt);
    }
  }

  organismoSelect.addEventListener("change", filtrarDispositivos);
  filtrarDispositivos(); // Ejecutar al cargar
});
