const modal = document.getElementById("cameraDialog");
const abrir = document.getElementById("btnAbrir");
const fechar = document.getElementById("btnFechar");

abrir.addEventListener("click", () => {
  modal.showModal(); 
});

fechar.addEventListener("click", () => {
  modal.close(); 
});