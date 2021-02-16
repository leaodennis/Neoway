FROM rocker/r-ver:4.0.0-ubuntu18.04

RUN R -e "install.packages(c('shinythemes', 'shiny', 'bs4Dash', 'shinyWidgets', 'shinycssloaders', 'htmltools'))"
RUN R -e "install.packages(c('dplyr', 'ggplot2',  'xgboost', 'ROCR', 'Ckmeans.1d.dp', 'httr', 'caret'))"

RUN R -e "install.packages(c('e1071', 'shinyjs', 'markdown'))"

RUN apt update

RUN apt install -y libssl-dev libsasl2-dev

RUN apt-get install -y python3-pip python3-dev build-essential

RUN apt-get install -y libxtst6 libgl1-mesa-glx libxt6

WORKDIR mkdir /root/app

COPY app/ .

# RUN pip3 install -r /root/app/requirements.txt

EXPOSE 5000

CMD ["R", "-e", "shiny::runApp(port = 5000, host = '0.0.0.0')"]
