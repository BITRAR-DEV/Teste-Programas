const modal = document.getElementById("cameraDialog");
const abrir = document.getElementById("btnAbrir");
const fechar = document.getElementById("btnFechar");
const pontos = document.getElementById("pontos");
const cameraImage = document.getElementById("cameraImage");
const modalResultado = document.getElementById("modalResultado")

let quantidade = 0;

setInterval(() => {
    quantidade++;

    if (quantidade > 3) {
        quantidade = 0;
    }

    pontos.textContent = ".".repeat(quantidade);
}, 500);

const checar = setInterval (async () => {
  if (modal.open) {
    const resultado = await fetch("/resultado");
    const dados = await resultado.json();
  
    if (dados.classe != null
    ) {
      clearInterval(checar)
      setTimeout(() => {}, 1500);
      modal.close();
      modalResultado.showModal();
    }
  
    console.log(dados);
  }
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