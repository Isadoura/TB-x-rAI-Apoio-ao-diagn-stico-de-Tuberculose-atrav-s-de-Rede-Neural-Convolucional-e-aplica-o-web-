document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("fileUpload");
  const overlay = document.getElementById("loadingOverlay");
  const loadingBar = document.getElementById("overlayLoadingBar");
  const loadingText = document.getElementById("overlayLoadingText");
  const form = document.getElementById("uploadForm");

  const mensagens = [
    "Iniciando a análise",
    "Processando as imagens",
    "Utilizando o modelo de Rede Neural Convolucional",
    "Gerando os resultados"
  ];

  input.addEventListener("change", () => {
    const arquivos = Array.from(input.files);

    if (arquivos.length === 0) return;

    let invalido = arquivos.some(
      (arquivo) =>
        !arquivo.name.toLowerCase().endsWith(".zip")
    );

    if (invalido) {
      alert("Apenas arquivos no formato .zip são permitidos!");
      input.value = "";
      return;
    }

    overlay.classList.remove("hidden");
    overlay.classList.add("opacity-0");

    requestAnimationFrame(() => {
      overlay.classList.add("transition-opacity", "duration-400", "opacity-100");
    });

    let progresso = 0;
    let etapa = 0;

    const intervalo = setInterval(() => {
      progresso += 2;
      loadingBar.style.width = progresso + "%";

      const novaEtapa = Math.floor(progresso / 25);
      if (novaEtapa !== etapa && novaEtapa < mensagens.length) {
        etapa = novaEtapa;
        loadingText.textContent = mensagens[etapa];
      }

      if (progresso >= 100) {
        clearInterval(intervalo);
      }
    }, 40);
  });
});

function Aviso(){
  const overlay = document.createElement("div");

    overlay.className =
      "fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50";

    overlay.innerHTML = `
      <div class="bg-white p-8 rounded-2xl shadow-2xl text-center max-w-sm">
        <h2 class="text-xl font-bold mb-4 text-blue-800">
          Atenção
        </h2>
        <p class="text-gray-700 mb-6">
          É necessário realizar o upload das imagens antes de visualizar os resultados.
        </p>
        <button class="bg-blue-800 hover:bg-blue-800 text-white px-6 py-2 rounded-lg">
          Voltar para a tela de upload
        </button>
      </div>
    `;

    document.body.appendChild(overlay);

    overlay.querySelector("button").addEventListener("click", () => {
      overlay.remove();
    });
}
