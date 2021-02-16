# Neoway

Neoway POC

Três Arquivos Principais

EDA.py : Gera o relatório descritivo automático dos dados de Treino. Output: train_automatica_EDA.html

Model.py : Arquivo onde as Etapas de Préprocessamento e Ajustes são feitas. Output: validation.csv (Comparação da base de Validação) e test.csv(Submissão da base de Teste).

global.R, ui.R e server.R : Estruturas do dashboard Interativo em Framework Shiny usado para averiguar o modelo e unificar as duas etapas anteriores. Input: train_automatica_EDA.html, validation.csv, test.csv e DOC.md 

* Devido a ausência de um glossaŕio da relação dos dados não foi possivel usar pipelines automáticos e nem features complexas como as originadas do PCA.

O arquivo docker disponível integra os três arquivos e disponibiliza o Dashboard Shiny após seu Build pelos commandos na porta "5000":

sudo docker build -t shiny .
sudo docker run --rm shiny

