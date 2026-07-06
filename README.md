# TB x-rAI: Rede Neural Convolucional e aplicação web para apoio ao auxílio do diagnóstico de Tuberculose

## Rede Neural Convolucional

Este repositório apresenta uma **arquitetura de Rede Neural Convolucional e um site desenvolvidos para a predição do diagnóstico de Tuberculose**. A arquitetura CNN utiliza 5 blocos convolucionais com a aplicação de um mecanismo de atenção *Squeeze-and-Excitation*, *Batch Normalization*, ReLU, *ensemble learning*, uma camada GAP, *dropout* para reduzir o *overfitting* da rede e *Binary Focal Cross Entropy*. A figura abaixo descreve com maiores detalhes a arquitetura proposta.

![Arquitetura da CNN proposta](https://github.com/Isadoura/TB-x-rAI-Apoio-ao-diagn-stico-de-Tuberculose-atrav-s-de-Rede-Neural-Convolucional-e-aplica-o-web-/blob/main/arquiteturaCNN.png)

Figura 1: Arquitetura da Rede Neural Convolucional proposta.

## Aplicação web TB x-rAI

O site foi construído com objetivo de facilitar a predição de imagens radiográficas por profissionais da área da saúde através de uma interface intuitiva e amigável.

Link para o site: 

Ademais, para a integração com a CNN foi utilizado o Flask.

### Módulos necessários:

```
pip install flask
```

## Base de dados
Para o treinamento da rede neural foram utilizados os datasets públicos de imagens radiográficas de Montgomery, Shenzhen e Belarus. Para baixar o de Montgomery County pode-se acessar esse link: ![Montgomery](https://openi.nlm.nih.gov/imgs/collections/NLM-MontgomeryCXRSet.zip), Shenzhen em ![Shenzhen](https://openi.nlm.nih.gov/imgs/collections/ChinaSet_AllFiles.zip).

## Resultados 
![Matriz de confusão](https://github.com/Isadoura/TB-x-rAI-Apoio-ao-diagn-stico-de-Tuberculose-atrav-s-de-Rede-Neural-Convolucional-e-aplica-o-web-/blob/main/matriz%20de%20confus%C3%A3o%20modelo%20com%20CLAHE%20treinamento%202.png)

![Curva ROC](https://github.com/Isadoura/TB-x-rAI-Apoio-ao-diagn-stico-de-Tuberculose-atrav-s-de-Rede-Neural-Convolucional-e-aplica-o-web-/blob/main/curva%20ROC%20modelo%20com%20CLAHE%20treinamento%202.png)
