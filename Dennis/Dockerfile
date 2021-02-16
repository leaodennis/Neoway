# BASE IMAGE TO APPS
FROM rocker/r-ver:4.0.0-ubuntu18.04

RUN R -e "install.packages('remotes')"

RUN R -e "remotes::install_github('r-lib/rlang@v0.4.10')"
RUN R -e "remotes::install_github('r-lib/vctrs@v0.3.6')"

RUN R -e "remotes::install_github('tidyverse/dplyr@v1.0.2')"
RUN R -e "remotes::install_github('tidyverse/ggplot2@v3.3.3')"
RUN R -e "remotes::install_github('tidyverse/lubridate@v1.7.9')"
RUN R -e "remotes::install_github('tidyverse/stringr@v1.4.0')"

RUN apt update
RUN apt install -y libmariadbclient-dev

RUN R -e 'remotes::install_github("rstudio/htmltools@v0.5.1")'

RUN R -e 'remotes::install_github("rstudio/sass@v0.3.1")'
RUN R -e 'remotes::install_github("rstudio/jquerylib@v0.1.3")'
RUN R -e 'remotes::install_github("rstudio/bslib@v0.2.4")'
RUN R -e 'remotes::install_github("r-lib/cachem@v1.0.3")'
RUN R -e 'remotes::install_github("rstudio/shiny@v1.6.0")'

RUN R -e "remotes::install_github('daattali/shinyjs@v1.1')"
RUN R -e "remotes::install_github('rstudio/shinythemes@v1.1.2')"

RUN R -e "remotes::install_github('RinteRface/bs4Dash@v2.0.0')"
RUN R -e "remotes::install_github('dreamRs/shinyWidgets@v0.5.7')"
RUN R -e "remotes::install_github('daattali/shinycssloaders@1.0.0')"

# # Graphics and tables
RUN R -e "remotes::install_github('r-lib/httr@v1.4.2')"  

RUN R -e "remotes::install_github('dmlc/xgboost@v1.3.3')"  
RUN R -e "install.packages(c('ROCR', 'Ckmeans.1d.dp'))"

RUN apt install -y libssl-dev libsasl2-dev

RUN apt-get install -y python3-pip python3-dev build-essential

RUN mkdir /root/app

COPY app /root/app

COPY requirements.txt /root/requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["R", "-e", "shiny::runApp('/root/app', port = 5000)"]