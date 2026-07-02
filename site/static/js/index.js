document.addEventListener("DOMContentLoaded", () => {
  sessionStorage.removeItem('uploadRealizado');
  
  const botaoResultados = document.getElementById("menuResultados");

  if (!botaoResultados) return;

  botaoResultados.addEventListener("click", (event) => {
    event.preventDefault();

    const uploadRealizado = sessionStorage.getItem("uploadRealizado");

    if (!uploadRealizado) {
      Aviso();
    } else{
        window.location.href = 'resultados'
    }
  });

  function Aviso() {
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
          Voltar a tela principal
        </button>
      </div>
    `;

    document.body.appendChild(overlay);

    overlay.querySelector("button").addEventListener("click", () => {
      overlay.remove();
    });
  }
});
