document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("dispositivo_id");
  const modeloContainer = document.getElementById("modelo-container");

  const dispositivosConModelo = ["Notebook", "Desktop", "Celular", "Tablet"];

  function actualizarModelo() {
    const nombre = select.options[select.selectedIndex].dataset.nombre;

    if (dispositivosConModelo.includes(nombre)) {
      modeloContainer.style.display = "block";
    } else {
      modeloContainer.style.display = "none";
    }
  }

  select.addEventListener("change", actualizarModelo);
  actualizarModelo(); // Ejecutar al cargar
});
