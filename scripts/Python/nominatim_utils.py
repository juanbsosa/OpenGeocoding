import asyncio
from typing import Any, Dict, Optional
import requests
import pandas as pd
from tqdm.auto import tqdm

DOMAIN_URL = 'http://localhost:8080'


def request_requests_json(url: str) -> Dict[str, Any]:
    """
    Sends an HTTP GET request to the specified URL and returns the JSON response as a Python dictionary.

    Args:
        url (str): A string representing the URL to send the HTTP GET request to.

    Returns:
        Dict[str, Any]: A dictionary containing the JSON data from the HTTP response. The keys of the dictionary
                       are strings, and the values can be of any data type.

    Raises:
        requests.RequestException: If there is an issue with the HTTP request (e.g., network error, timeout).
    """
    res = requests.get(url)
    return res.json()


def get_coordinates_url(country: Optional[str] = None, state: Optional[str] = None, city: Optional[str] = None,
                        street: Optional[str] = None, postalcode: Optional[str] = None) -> str:
    """
    Constructs a URL for querying geocoding information using the provided location parameters.

    Args:
        country (Optional[str], default=None): The country name to include in the query.
        state (Optional[str], default=None): The state name to include in the query.
        city (Optional[str], default=None): The city name to include in the query.
        street (Optional[str], default=None): The street address to include in the query.
        postalcode (Optional[str], default=None): The postal code to include in the query.

    Returns:
        str: The complete URL for querying the geocoding service with the specified location parameters.

    Note:
        The function assumes that the DOMAIN_URL variable is defined elsewhere in the code, and
        that it contains the base URL for the geocoding service.
    """
    params = []
    if country:
        params.append(f'country={country}')
    if state:
        params.append(f'state={state}')
    if city:
        params.append(f'city={city}')
    if street:
        params.append(f'street={street}')
    if postalcode:
        params.append(f'postalcode={postalcode}')
    params.append('format=json')
    params = '&'.join(params)
    return f'{DOMAIN_URL}/search?{params}'


def get_coordinates(country: Optional[str] = None, state: Optional[str] = None, city: Optional[str] = None,
                    street: Optional[str] = None, postalcode: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Retrieves geocoding information for the specified location parameters using the geocoding service.

    Args:
        country (Optional[str], default=None): The country name to include in the query.
        state (Optional[str], default=None): The state name to include in the query.
        city (Optional[str], default=None): The city name to include in the query.
        street (Optional[str], default=None): The street address to include in the query.
        postalcode (Optional[str], default=None): The postal code to include in the query.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the geocoding data for the first result of the query,
                                  or None if no results are found or an error occurs.

    Note:
        This function relies on the get_coordinates_url() and request_requests_json() functions to
        construct the query URL and retrieve the JSON data from the geocoding service.
    """
    url = get_coordinates_url(
        country=country, state=state, city=city, street=street, postalcode=postalcode)
    coordinates = request_requests_json(url)
    try:
        return coordinates[0]
    except:
        return None
    

def geocode_df(df, 
               country: Optional[str] = None, country_col: Optional[str] = None, 
               state: Optional[str] = None, state_col: Optional[str] = None, 
               city: Optional[str] = None, city_col: Optional[str] = None, 
               postalcode: Optional[str] = None, postalcode_col: Optional[str] = None, 
               full_address_col: Optional[str] = None, street_name_col: Optional[str] = None, 
               street_number_col: Optional[str] = None):
    """
    Geocodes a DataFrame using the specified location parameters and adds geocoding data as new columns.

    Args:
        df (pd.DataFrame): The input DataFrame to be geocoded.
        country (str, optional): A fixed country name to use for all rows, if not using 'country_col'.
        country_col (str, optional): The column containing country names in the DataFrame.
        state (str, optional): A fixed state name to use for all rows, if not using 'state_col'.
        state_col (str, optional): The column containing state names in the DataFrame.
        city (str, optional): A fixed city name to use for all rows, if not using 'city_col'.
        city_col (str, optional): The column containing city names in the DataFrame.
        postalcode (str, optional): A fixed postal code to use for all rows, if not using 'postalcode_col'.
        postalcode_col (str, optional): The column containing postal codes in the DataFrame.
        full_address_col (str, optional): The column containing full street addresses in the DataFrame.
        street_name_col (str, optional): The column containing street names in the DataFrame.
        street_number_col (str, optional): The column containing street numbers in the DataFrame.

    Returns:
        pd.DataFrame: The georeferenced DataFrame with added columns for latitude, longitude, type, and category (as
        obtained from the Nominatim API).

    Raises:
        ValueError: If invalid combinations of arguments are provided.

    Note:
        This function relies on the get_coordinates() function to retrieve geocoding data for each row in the DataFrame.
    """
    
    if country is not None and country_col is not None:
        raise ValueError("Only one of 'country' and 'country_col' should be provided.")
    if state is not None and state_col is not None:
        raise ValueError("Only one of 'state' and 'state_col' should be provided.")
    if city is not None and city_col is not None:
        raise ValueError("Only one of 'city' and 'city_col' should be provided.")
    if postalcode is not None and postalcode_col is not None:
        raise ValueError("Only one of 'postalcode' and 'postalcode_col' should be provided.")
    
    if (full_address_col is not None) and (street_name_col is not None or street_number_col is not None):
        raise ValueError(
            "If 'full_address_col' is provided, 'street_name_col' and 'street_number_col' should not be provided.")
    
    if (street_name_col is not None and street_number_col is None) or (street_name_col is None and street_number_col is not None):
        raise ValueError("Both 'street_name_col' and 'street_number_col' should be provided together, or not provided at all.")
    
    df['latitude'] = ''
    df['longitude'] = ''
    df['nomi_type'] = ''
    df['nomi_category'] = ''

    successful_geocodes = 0
    
    for idx in tqdm(df.index, desc='Georeferenciando', leave=True):
        street = None
        if full_address_col is not None:
            street = df[full_address_col].at[idx]
        elif street_name_col is not None and street_number_col is not None:
            street = f"{df[street_name_col].at[idx]} {df[street_number_col].at[idx]}"

        data = get_coordinates(
            country=country if country_col is None else df[country_col].at[idx],
            state=state if state_col is None else df[state_col].at[idx],
            city=city if city_col is None else df[city_col].at[idx],
            street=street,
            postalcode=postalcode if postalcode_col is None else df[postalcode_col].at[idx],
        )
        
        if street == '':
            df['latitude'].at[idx] = None
            df['longitude'].at[idx] = None
            df['nomi_type'].at[idx] = None
            df['nomi_category'].at[idx] = None
            continue
        
        try:
            df['latitude'].at[idx] = data['lat']
            df['longitude'].at[idx] = data['lon']
            df['nomi_type'].at[idx] = data['type']
            df['nomi_category'].at[idx] = data['class']
            successful_geocodes += 1
        except:
            df['latitude'].at[idx] = None
            df['longitude'].at[idx] = None
            df['nomi_type'].at[idx] = None
            df['nomi_category'].at[idx] = None
    
    success_percentage = round((successful_geocodes / len(df)) * 100)
    print(f"Geocoding success rate: {success_percentage}%")

    return df

# data = get_coordinates(country='Argentina', state="Buenos Aires", city="Capital Federal", street="Triunvirato 4331", postalcode="")
# print(data)

# data = get_coordinates(country='Argentina', postalcode='6660')
# print(data)