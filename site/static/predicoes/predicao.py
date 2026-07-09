# código com as predições do modelo de cnn
import tensorflow as tf
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

caminho_modelo = "sitemodelo/modelos/modelocnn.keras"

modelo = tf.keras.models.load_model(caminho_modelo)

tamanho_imagem = 256
threshold = 0.47

last_conv_layer_name = "conv2d_42"

def aplicar_clahe(img):
    img = img.astype(np.uint8)

    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    return clahe.apply(img)

def pre_processamento(img):
    img = cv.imread(img, cv.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Imagem não encontrada.")
    
    img = cv.resize(img, (tamanho_imagem, tamanho_imagem))

    img = aplicar_clahe(img)

    img = img.astype(np.float32) / 255.
    img = np.expand_dims(img, -1)
    return img

def predicao(caminho):
    img = pre_processamento(caminho)
    entrada = np.expand_dims(img,0)
    probabilidade = float(modelo.predict(entrada, verbose=0)[0][0])

    if probabilidade <= threshold:
        classe = "Sem sinais sugestivos de tuberculose"
    else: 
        classe = "Caso sugestivo de tuberculose"

    return probabilidade, classe

# função de geração do grad-CAM - igual ao do notebook colab
def get_gradcam_heatmap(modelo, image, last_conv_layer_name):
    grad_modelo = tf.keras.models.Model(
        [modelo.inputs],
        [modelo.get_layer(last_conv_layer_name).output, modelo.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_modelo(image)
        loss = predictions[:, 0]

    grads = tape.gradient(loss, conv_outputs)

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0)

    heatmap = heatmap.numpy()

    heatmap = np.nan_to_num(heatmap)

    heatmap -= heatmap.min()

    if heatmap.max() != 0:
        heatmap /= heatmap.max()

    return heatmap

def salvar_gradcam(caminho_imagem, nome_arquivo):
    img = pre_processamento(caminho_imagem)
    entrada_imagem = np.expand_dims(img, axis=0)

    heatmap = get_gradcam_heatmap(modelo, entrada_imagem, last_conv_layer_name)

    imagem_original = cv.imread(caminho_imagem, cv.IMREAD_GRAYSCALE)

    if imagem_original is None:
        raise ValueError("Erro ao carregar imagem.")
    
    imagem_original = cv.resize(imagem_original, (tamanho_imagem, tamanho_imagem))

    heatmap = cv.resize(heatmap, (tamanho_imagem, tamanho_imagem))

    heatmap = np.uint8(255 * heatmap)

    heatmap = cv.applyColorMap(heatmap, cv.COLORMAP_JET)

    imagem_original = cv.cvtColor(imagem_original, cv.COLOR_GRAY2BGR)

    gradcam = cv.addWeighted(imagem_original, 0.75, heatmap, 0.25, 0)

    pasta_saida = "sitemodelo/static/gradCAM"

    os.makedirs(pasta_saida, exist_ok=True)

    nome_saida = nome_arquivo + ".png"

    caminho_saida = os.path.join(pasta_saida, nome_saida)
    cv.imwrite(caminho_saida, gradcam)

    return nome_saida

def graficos(resultados):
    if not resultados:
        return None

    probs = [i["probabilidade"] * 100 for i in resultados]
    x = np.arange(1, len(probs)+1)

    plt.figure(figsize=(12,6))

    plt.scatter(x, probs, s=35, color="#2b7de9", edgecolors="#000080", linewidth=0.5)

    plt.axhline(threshold*100, color="red", linestyle="--", linewidth=2, label=f"Threshold ({threshold*100:.0f}%)")

    plt.title("Probabilidade prevista para cada radiografia", fontsize=16, weight="bold", color="#000080")

    plt.xlabel("Radiografias", fontsize=13)
    plt.ylabel("Probabilidade (%)", fontsize=13)
    plt.ylim(0,100)
    plt.grid(alpha=0.3)

    plt.legend()
    plt.tight_layout()

    os.makedirs("sitemodelo/static/graficos", exist_ok=True)
    nome = "grafico.png"

    plt.savefig("sitemodelo/static/graficos/"+nome, dpi=250, bbox_inches="tight")
    plt.close()

    return nome

# mudar e colocar gráfico de barras 

def grafico_pizza(resultados):
    suspeitos = sum(
        i["classe"] == "Caso sugestivo de tuberculose"
        for i in resultados    
    )

    normais = len(resultados) - suspeitos

    if not resultados:
        return None 
    
    plt.figure(figsize=(7,7), facecolor="#f5faff")

    cores = ["#0b1f8f", "#84d7ff"]

    wedges, texts, autotexts = plt.pie(
        [suspeitos, normais], 
        labels=["Suspeitos", "Normais"], 
        colors=cores, explode=(0.05,0), 
        autopct="%1.1f%%",
        startangle=90, 
        wedgeprops={
            "width":0.45, 
            "edgecolor":"white",
            "linewidth":2
        },
        textprops={
            "fontsize":13,
            "weight":"bold"
        }
    )

    plt.title("Distribuição das predições para o diagnóstico de Tuberculose", fontsize=16, weight="bold", color="#000080")

    nome = "grafico_pizza.png"

    os.makedirs("sitemodelo/static/graficos", exist_ok=True)

    plt.savefig("sitemodelo/static/graficos/" + nome, dpi=200, bbox_inches="tight")
    plt.close()

    return nome

def grafico_estatisticas(resultados):

    suspeitos = sum(
        i["classe"]=="Caso sugestivo de tuberculose"
        for i in resultados
    )

    normais = len(resultados)-suspeitos

    plt.figure(figsize=(7,2.5))

    plt.barh(
        ["Normais","Suspeitos"],
        [normais,suspeitos],
        color=["#84d7ff","#0b1f8f"]
    )

    plt.xlabel("Quantidade")

    plt.tight_layout()

    nome="estatisticas.png"

    plt.savefig(
        "sitemodelo/static/graficos/"+nome,
        dpi=250
    )

    plt.close()

    return nome

def estatisticas_modelo(resultados):
    total = len(resultados)

    casos_suspeitos = sum(
        i["classe"] == "Caso sugestivo de tuberculose" 
        for i in resultados
    )

    casos_normais = total - casos_suspeitos

    if total > 0:
        media = np.mean([i["probabilidade"] for i in resultados])
    else:
        media = 0

    return {
        "total":total,
        "suspeitos":casos_suspeitos,
        "normais":casos_normais,
        "media":media
    }

def analisar(caminho_pasta): 
    print("Pasta:", caminho_pasta)
    resultados = []

    for raiz, _, arquivos in os.walk(caminho_pasta):
        print("Raiz:", raiz)
        print("Arquivos:", arquivos)

        for arquivo in sorted(arquivos):
            if arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
                print("Imagem:", arquivo)
                caminho = os.path.join(raiz, arquivo)

                try:
                    probabilidade, classe = predicao(caminho)

                    print("Predição feita")

                    gradcam = salvar_gradcam(caminho, os.path.splitext(arquivo)[0])

                    resultados.append({
                        "arquivo": arquivo,
                        "classe": classe,
                        "probabilidade": probabilidade,
                        "gradcam": gradcam 
                    })

                except Exception as e:
                    print(f"Erro ao processar {arquivo}: {e}")

    if not resultados:
        return{
            "resultados": [],
            "grafico": None, 
            "pizza": None,
            "estatisticas": estatisticas_modelo([])
        }

    grafico = graficos(resultados)
    graf_pizza = grafico_pizza(resultados)
    estatisticas = estatisticas_modelo(resultados)

    grafico_est = grafico_estatisticas(resultados)

    return { 
        "resultados":resultados,
        "grafico": grafico,
        "pizza": graf_pizza,
        "estatisticas": estatisticas,
        "grafico_estatisticas": grafico_est
    }
