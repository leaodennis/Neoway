shinyUI(
    fluidPage(
        # theme = shinytheme("united"),
        useBs4Dash(),
        useShinyjs(),

        fluidRow(
            column(
                12,
                align = "center",
                radioButtons(
                    inputId = "doc_model",
                    label = "",
                    choices = c(
                        "Modelo" = "model",
                        "Documentação" = "doc"
                    ),
                    inline = TRUE
                )
            )
        ),

        fluidRow(
            div(
                id = "layout_model",
                class = "col-xl-12",
                # style = "padding: 5%",
                div(
                    class = "col-xl-12",
                    fluidRow(
                        bs4Dash::bs4Box(
                            title = "Ajuste do modelo",
                            width = 6,
                            plotOutput("curve_roc")
                        ),
                        bs4Dash::bs4Box(
                            title  = "Importância das variáveis",
                            width = 6,
                            plotOutput("variable_importance")
                        )
                    )
                ),
                div(
                    class = "col-xl-12",
                    fluidRow(
                        bs4Dash::bs4Box(
                            title = "Matriz de confusão",
                            width = 6,
                            verbatimTextOutput("confusion_matrix")
                        ),
                        bs4Dash::bs4Box(
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
            ),
            shinyjs::hidden(
                div(
                    id = "layout_doc",
                    class = "col-xl-12",
                    bs4Box(
                        title = "",
                        width = 12,
                        htmltools::includeMarkdown("DOC.md")
                    )
                )

            )
        )
    )
)