# Preprocessing

Nesta Etapa foi verificado a qualidade das informações até a etapa da criação das Features

Para isso foram realizados os seguintes passos sequencialmente:

* Remoção das variáveis **cd_ramo_atividade** e **cd_natureza_juridica** (Pois se tratam de códigos de outras variáveis presentes na base)

* Remoção das variáveis **de_ramo_atividade**, **nm_micro_regiao**, **nm_meso_regiao** por se tratarem de variáveis com muitos níveis, alguns com apenas uma observação.

* Remoção da variável **sg_uf_abrangencia** por ter mais de 50% de missing e muitos níveis

* Remoção das variáveis **dt_situacao_especial** por apresentar uma coluna com niveis de fator representantes da checagem ( mesmo apresentando 99% de missing).

* Remoção das variáveis  **de_validade_pgfn**, **de_validade_fgts**, **de_optante_simples** por necessitarem de separação dos nivéis categóricos e das datas da checagem em colunas distintas (através de regex)
 
* Remoção automática das variáveis com apenas um nivel de fator ( por não contribuirem para a entropia)

* Remoção automática das variáveis completamente vazias

* Preenchimento dos nivéis de fator das variáveis **de_situacao_especial** e **de_indicador_telefone** com o nivel "Unknown"

* Preenchimento das variaveis numéricas com missing acima de 50% com Zero.

* Criação das features numéricas das diferenças das das variaveis de data para a data da análise. (**dt_abertura**, **dh_ultima_atualizacao**, **dh_processamento** e **dt_situacao**)

* Preenchimento com valores 0 para evitar Leakage na coluna **renda_censitaria_2010**

* Remoção final das ultimas linhas com NA totalizando menos de 5 observações em ambas as bases devido as variaveis **dt_situacao** e **sg_uf_matriz** categóricas sem niveis

# Encode

* Foi feito Superamostragem para balancear a categoria minoritária

* Separação de Treino e Validação em 20%

# Hyper Parameter Tunning

* Feito através do método Bayesiano de atualização nos seguintes parâmetros gamma, max_depth, colsample_bytree, min_child_weight e scale_pos_weight.

# Ajuste

* Feito no Algorítmo XGBoost através da maximização da Curva ROC. 