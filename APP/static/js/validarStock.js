document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const dispositivoSelect = document.getElementById("dispositivo_id");
  const cantDispositivoInput = document.querySelector('input[name="cant_dispositivo"]');

  const accesorios = [
    { select: document.getElementById("accesorio1"), input: document.querySelector('input[name="cant_accesorio1"]') },
    { select: document.getElementById("accesorio2"), input: document.querySelector('input[name="cant_accesorio2"]') },
    { select: document.getElementById("accesorio3"), input: document.querySelector('input[name="cant_accesorio3"]') },
  ];

  form.addEventListener("submit", (e) => {
    let errores = [];

    // Validar dispositivo principal
    const dispositivoOpcion = dispositivoSelect.options[dispositivoSelect.selectedIndex];
    const stockDispositivo = parseInt(dispositivoOpcion.dataset.stock || "0");
    const cantidadSolicitada = parseInt(cantDispositivoInput.value || "0");

    if (cantidadSolicitada > stockDispositivo) {
      errores.push(`No hay suficiente stock de "${dispositivoOpcion.text}". Disponible: ${stockDispositivo}`);
    }

    // Validar accesorios
    accesorios.forEach(({ select, input }) => {
      const opcion = select.options[select.selectedIndex];
      const cantidad = parseInt(input.value || "0");

      if (opcion && opcion.dataset.stock && cantidad > 0) {
        const stock = parseInt(opcion.dataset.stock);
        if (cantidad > stock) {
          errores.push(`No hay suficiente stock del accesorio "${opcion.text}". Disponible: ${stock}`);
        }
      }
    });

    if (errores.length > 0) {
      e.preventDefault();
      alert("Error en el stock:\n\n" + errores.join("\n"));
    }
  });
});
