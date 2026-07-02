# TB x-rAI: Rede Neural Convolucional e aplicação web para apoio ao auxílio do diagnóstico de Tuberculose

## Rede Neural Convolucional

Este repositório apresenta uma **arquitetura de Rede Neural Convolucional e um site desenvolvidos para a predição do diagnóstico de Tuberculose**. A arquitetura CNN utiliza 5 blocos convolucionais com a aplicação de um mecanismo de atenção *Squeeze-and-Excitation*, *Batch Normalization*, ReLU, *ensemble learning*, uma camada GAP, *dropout* para reduzir o *overfitting* da rede e *Binary Focal Cross Entropy*. A figura abaixo descreve com maiores detalhes a arquitetura proposta.

![Arquitetura da CNN proposta](https://github.com/Isadoura/TB-x-rAI-Apoio-ao-diagn-stico-de-Tuberculose-atrav-s-de-Rede-Neural-Convolucional-e-aplica-o-web-/blob/main/arquiteturaCNN.png)

Figura 1: Arquitetura da Rede Neural Convolucional proposta.

O link do modelo de CNN está disponível em: ![Arquitetura CNN TB x-rAI]()

## Aplicação web TB x-rAI

O site foi construído com objetivo de facilitar a predição de imagens radiográficas por profissionais da área da saúde através de uma interface intuitiva e amigável.

Link para o site: 

Ademais, para a integração com a CNN foi utilizado o Flask.

###Módulos necessários:

´´´
pip install flask
´´´



