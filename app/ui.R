shinyUI(
    fluidPage(
        theme = shinytheme("united"),
        useShinyjs(),
        tags$head(
            shiny::tagList(useBs4Dash2())
        ),

        fluidRow(
            style = "padding: 1%",
            tabsetPanel(
                type = "pills",
                # vertical = TRUE,
                tabPanel(
                    title = "Model",
                    fluidRow(
                        div(
                            id = "layout_model",
                            class = "col-xl-12",
                            # style = "padding: 5%",
                            div(
                                class = "col-xl-12",
                                fluidRow(
                                    bs4Dash::box(
                                        title = "Ajuste do modelo",
                                        width = 6,
                                        plotOutput("curve_roc")
                                    ),
                                    bs4Dash::box(
                                        title  = "Importância das variáveis",
                                        width = 6,
                                        plotOutput("variable_importance")
                                    )
                                )
                            ),
                            div(
                                class = "col-xl-12",
                                fluidRow(
                                    bs4Dash::box(
                                        title = "Matriz de confusão",
                                        width = 6,
                                        verbatimTextOutput("confusion_matrix")
                                    ),
                                    bs4Dash::box(
                                        title = "Download dos resultados",
                                        width = 6,
                                        downloadButton("download_test")
                                    )
                                )
                            ),
                            div(
                                class = "col-xl-12",
                                htmltools::includeHTML("train_automatic_EDA.html")
                            )
                        )
                    )
                ),
                tabPanel(
                    title = "Doc",
                    uiOutput("doc") %>%
                        withSpinner()
                )
            )
        )
    )
)