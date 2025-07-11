//No muestra el check leasing cuando el dispositivo no es una notebook

document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("dispositivo_id");
  const leasingContainer = document.getElementById("leasing-container");
  const leasingCheckbox = leasingContainer.querySelector('input[type="checkbox"]');

  function actualizarLeasing() {
    const nombre = select.options[select.selectedIndex].dataset.nombre;

    if (nombre === "Notebook") {
      leasingContainer.style.display = "block";
    } else {
      leasingContainer.style.display = "none";
      leasingCheckbox.checked = false;
    }
  }

  select.addEventListener("change", actualizarLeasing);
  actualizarLeasing(); 
});
