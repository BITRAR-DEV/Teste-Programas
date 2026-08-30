const modal = document.getElementById("cameraDialog");
const abrir = document.getElementById("btnAbrir");
const fechar = document.getElementById("btnFechar");
const pontos = document.getElementById("pontos");
const cameraImage = document.getElementById("cameraImage");

let quantidade = 0;

setInterval(() => {
    quantidade++;

    if (quantidade > 3) {
        quantidade = 0;
    }

    pontos.textContent = ".".repeat(quantidade);
}, 500);

abrir.addEventListener("click", async () => {
  await fetch("/iniciar-camera");
  cameraImage.src = "/foto?t=" + Date.now();
  modal.showModal(); 
});

fechar.addEventListener("click", async () => {
  cameraImage.src = "";
  await fetch("/parar-camera");
  modal.close(); 
});