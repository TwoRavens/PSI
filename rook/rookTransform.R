##
## rookTransform.R
##
## 6/27/15
##
## Michael LoPiccolo
##

# After the user enters a new transformation formula, let them know whether it's valid.
# May consider returning a good name for the variable (instead of letting the user create it)

# TODO put a size limit on the formula we accept
verifyTransform.app <- function(env) {

    source("rookconfig.R") # global variables such as "IS_PRODUCTION_MODE"

    if(IS_PRODUCTION_MODE) {
        sink(file = stderr(), type = "output")
    }

    print ("Entered transformAdd app")
    # print (system2("pwd", stdout=TRUE))

    request <- Request$new(env)
    response <- Response$new(headers = list( "Access-Control-Allow-Origin"="*" ))

    warning <- FALSE
    message <- "nothing"

    print(paste("request$POST: ", request$POST(), sep=""))

    valid <- jsonlite::validate(request$POST()$tableJSON)

    if(!valid) {
        warning <- TRUE
        message = "The request is not valid json. Check for special characters."
    }

    if(!warning) {
        everything <- jsonlite::fromJSON(request$POST()$tableJSON)
        # print(everything)
    }

    if(is.null(everything$formula)) {
        warning <- TRUE
        message = "No formula found in request."
    }
    if(is.null(everything$names)) {
        warning <- TRUE
        message = "No variable names found in request."
    }
    else {
        answer <- verifyTransform(everything$formula, everything$names)
        if(!answer$success) {
            warning <- TRUE
            message <- paste("Parser error:", paste(answer$message, collapse='\n'))
        }
    }



    if(!warning) {
        toSend <- list()
    }
    else {
        toSend <- list("warning"=message)
    }

    result <- jsonlite:::toJSON(toSend)

    # print("transfromAdd: sending JSON:")
    # print(result)
    cat("\n")
    if(IS_PRODUCTION_MODE) {
        sink()
    }

    response$write(result)
    response$finish()
}
