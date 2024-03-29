## GEOCODER BASADO EN EL SERVICIO DE USIG GCABA
## 
## uso: USIG_geocode(direccion)
##
## Ejpemplos: 
## USIG_geocode("9 de julio y belgrano")
## 
## resultado
## 
##               address              address_normalised        lat        lng
## 9 de julio y belgrano 9 DE JULIO AV. y BELGRANO, CABA -34.613090 -58.381226
## 
## Si se trata de una dirección fuera de CABA, explicitar el municipio o partido
## USIG_geocode("9 de julio y belgrano, temperley")
## 
##  resultado
##  
##                address              address_normalised        lat        lng
## 9 de julio y belgrano 9 DE JULIO AV. y BELGRANO, CABA -34.613090 -58.381226

library(httr)

USIG_geocode <- function(address) {
  
  base_url <- "http://servicios.usig.buenosaires.gob.ar/normalizar/"
  
  make_address_query <- function(address) {
    query <- paste0(base_url, 
                    "?direccion=", 
                    address,
                    "&geocodificar=TRUE")
  }
  
  query <- URLencode(make_address_query(address))
  
  print(paste("Trying", query))
  
  results <- tryCatch(GET(query), 
                      error = function(error_message) {return(NULL)})
  
  
  
  if (!httr:::is.response(results)) {
    data.frame(address = address, lat = NA, lng = NA, stringsAsFactors = FALSE)
  } else {
    results <- content(results)
    if (length(results$direccionesNormalizadas)) {
      x <- results$direccionesNormalizadas[[1]]$coordenadas$x
      y <- results$direccionesNormalizadas[[1]]$coordenadas$y
      address_normalised <- results$direccionesNormalizadas[[1]]$direccion
    } else {
      x <- NA
      y <- NA
      address_normalised <- NA
    }
    
    
    data.frame(address = address,
               address_normalised = ifelse(is.null(address_normalised), NA, address_normalised),
               lat = ifelse(is.null(y), NA, y),
               lng = ifelse(is.null(x), NA, x),
               stringsAsFactors = FALSE)
  }
  
}
USIG_geocode("9 de julio y belgrano")
library(purr)
