# Neoway

Neoway POC


Três Arquivos Principais

EDA.py : Gera o relatório descritivo automático dos dados de Treino. Output: train_automatica_EDA.html

Model.py : Arquivo onde as Etapas de Préprocessamento e Ajustes são feitas. Output: validation.csv (Comparação da base de Validação) e test.csv(Submissão da base de Teste).

global.R, ui.R e server.R : Estruturas do dashboard Interativo em Framework Shiny usado para averiguar o modelo e unificar as duas etapas anteriores. Input: train_automatica_EDA.html, validation.csv, test.csv e DOC.md 

O arquivo docker disponível integra os três arquivos e disponibiliza o Dashboard Shiny após seu Build pelos commandos na porta "5000":

e 




