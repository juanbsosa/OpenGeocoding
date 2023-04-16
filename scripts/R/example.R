url <- get_coordinates_url(country='Argentina', state="Buenos Aires", city="Capital Federal", 
                street="Triunvirato 4331")
url

request_requests_json(url=url$url_prefix, params=url$params)

request_requests_json(url=url$url_prefix, params=url$params)[[1]]

a <- request_requests_json(url=url$url_prefix, params=url$params)[[1]]


get_coordinates(country='Argentina', state="Buenos Aires", city="Capital Federal", 
                street="Triunvirato 4331")
a <- get_coordinates(country='Argentina', state="Buenos Aires", city="Capital Federal", 
                     street="Triunvirato 4331")



df_url <- 'https://geoportal.tresdefebrero.gob.ar/geoserver/ows?service=wfs&version=1.1.0&request=GetFeature&typename=geonode%3Aparadas_municipales'

df <- sf::read_sf(df_url)

df <- sf::st_drop_geometry(df)

df2 <- geocode_df(df, country='Argentina', state='Buenos Aires', city='Tres de Febrero',
           full_address_col='direc')
