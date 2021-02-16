shinyServer(function(input, output, session) {
    observe({
        if (input$doc_model == "doc") {
            shinyjs::show("layout_doc")
            shinyjs::hide("layout_model")
        } else {
            shinyjs::hide("layout_doc")
            shinyjs::show("layout_model")
        }
    })

    output$confusion_matrix <- renderPrint({
        caret::confusionMatrix(table(validation$pred, validation$truth))
    })

    output$curve_roc  <- renderPlot({
        
        xgb.pred <- prediction(validation$pred, validation$truth)
        xgb.perf <- performance(xgb.pred, "tpr", "fpr")

        plot(xgb.perf,
            avg="threshold",
            colorize=TRUE,
            lwd=1,
            main="ROC Curve w/ Thresholds",
            print.cutoffs.at=seq(0, 1, by=0.05),
            text.adj=c(-0.5, 0.5),
            text.cex=0.5)
        grid(col="lightgray")
        axis(1, at=seq(0, 1, by=0.1))
        axis(2, at=seq(0, 1, by=0.1))
        abline(v=c(0.1, 0.3, 0.5, 0.7, 0.9), col="lightgray", lty="dotted")
        abline(h=c(0.1, 0.3, 0.5, 0.7, 0.9), col="lightgray", lty="dotted")
        lines(x=c(0, 1), y=c(0, 1), col="black", lty="dotted")

    })

    output$variable_importance <- renderPlot({
        xgboost::xgb.importance(model = model) %>%
            xgboost::xgb.ggplot.importance(top_n = 6, measure = NULL, rel_to_first = F) +
            theme_classic()
    })

    output$download_test <- downloadHandler(
        filename = function() {
            paste("data-", Sys.Date(), ".csv", sep = "")
        },
        content = function(file) {
            write.csv(teste, file)
        }
    )
})