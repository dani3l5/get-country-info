#! /usr/bin/python3
# -*- coding: utf-8 -*-

#Requests is used for accessing the data from the API
import requests
#JSON is used to add lines in the data so it is more easily separated
import json
#Time is used to measure computation time
import time
#Decimal is used for rounding the total time elapsed
from decimal import Decimal
import sys

#Code
def print_data():
    #Asks user for country
    country = input("Country: ")
    #If a space is in the country's name, it will be replaced with '%20' so
    #it can be used in the url
    country.replace(" ", "%20")

    #Records the start time of the process
    start_time = time.time()

    #Creates a variable called 'url' which is used to access the data with the Requests Module
    #It adds the country to the url and asks only for the name, capital, region, population,
    #demonym and area of the country

    url = 'https://www.restcountries.eu/rest/v2/name/' + country + '?fields=name;capital;region;population;demonym;area;' \
                                                                   '&fullText=true'

    #'Source' is used to gather the country's raw data from the API
    try:
        source = requests.get(url).json()
        if time.time() - start_time > 15:
            raise requests.Timeout
    except requests.ConnectionError as e:
        print("ERROR: " + str(e))
        sys.exit(1)
    except requests.Timeout as timeout:
        print("Request Timed Out, Try Again.")
        sys.exit(1)
    except requests.RequestException as e:
        print("ERROR: " + str(e))
        sys.exit(1)
    except KeyboardInterrupt as ki:
        print("Program Stopped!")
        sys.exit(0)
    except requests.HTTPError as e:
        print("ERROR: " + str(e))
        sys.exit()

    #'Lined_source' is 'source', however is formatted to have separated line
    lined_source = json.dumps(source, indent=4)

    #'Currency_req' requests the country's currency info
    try:
        currency_req = requests.get('https://www.restcountries.eu/rest/v2/name/' + country + '?fields=currencies' \
                                                                                       '&fullText=true').json()
    except requests.ConnectionError as e:
        print("ERROR: " + e)
        sys.exit(1)
    except requests.Timeout as timeout:
        print("Request Timed Out, Try Again.")
        sys.exit(1)
    except requests.RequestException as e:
        print("ERROR: " + e)
        sys.exit(1)
    except KeyboardInterrupt as ki:
        print("Program Stopped!")
        sys.exit(0)
    except requests.HTTPError as e:
        print("ERROR: " + str(e))
        sys.exit()
    #'Lined_currency' is 'currency_req' but formatted
    lined_currency = json.dumps(currency_req, indent=4)

    #'Split_source' is a list that holds each line of 'lined_source' as an item
    split_source = lined_source.split('\n')
    #'Split_currency' is a list that holds each line of 'lined_currency' as an item
    split_currency = lined_currency.split('\n')

    #'Colon' and 'quote' are used to keep track of where the later for loops are in the lines
    colon = 0
    quote = 0

    #These variables are used to store the extracted data
    name = ''
    capital = ''
    region = ''
    population = ''
    demonym = ''
    area = ''
    currency = ''

    #This for loop goes through 'split_source'
    for line in split_source:
        #Checks if "name" is in the line
        if "name" in line:
            #Extracts that line's data
            for char in line:
                if quote == 1 and char != '"' and char != ',':
                    name += char
                elif char == ":":
                    colon = 1
                elif colon == 1 and char == '"':
                    quote = 1
                    colon = 0
                else:
                    quote = 0
        #Checks if "capital" is in the line
        elif "capital" in line:
            #Extracts that line's data
            for char in line:
                if quote == 1 and char != '"' and char != ',':
                    capital += char
                elif char == ":":
                    colon = 1
                elif colon == 1 and char == '"':
                    quote = 1
                    colon = 0
                else:
                    quote = 0
        #Checks if "region" is in the line
        elif "region" in line:
            #Extracts that line's data
            for char in line:
                if quote == 1 and char != '"' and char != ',':
                    region += char
                elif char == ":":
                    colon = 1
                elif colon == 1 and char == '"':
                    quote = 1
                    colon = 0
                else:
                    quote = 0
        #Checks if "population" is in the line
        elif "population" in line:
            #Extracts that line's data
            for char in line:
                if colon == 1 and char != ',' and char != ' ':
                    population += char
                elif char == ":":
                    colon = 1
                else:
                    pass
            colon = 0
        #Checks if "demonym" is in the line
        elif "demonym" in line:
            #Extracts that line's data
            for char in line:
                if quote == 1 and char != '"' and char != ',':
                    demonym += char
                elif char == ":":
                    colon = 1
                elif colon == 1 and char == '"':
                    quote = 1
                    colon = 0
                else:
                    quote = 0
        #Checks if "area" is in the line
        elif "area" in line:
            #Extracts that line's data
            for char in line:
                if colon == 1 and char != ',' and char != ' ':
                    area += char
                elif char == ":":
                    colon = 1
                else:
                    pass
            colon = 0
        else:
            pass

    #Goes through 'split_currency'
    for line in split_currency:
        #Checks if "name" is in that line
        if "name" in line:
            #If it is, it goes through that line's characters and extracts the data
            for char in line:
                if quote == 1 and char != '"' and char != ',':
                    currency += char
                elif char == ":":
                    colon = 1
                elif colon == 1 and char == '"':
                    quote = 1
                    colon = 0
                else:
                    quote = 0
            currency += ' '
        else:
            pass

    #If the user entered a valid country and the program has extracted data,
    #it prints out the data
    if name != '':
        data =  "Data:" \
                "\nCountry Name: " + name + \
                "\nCapital City: " + capital + \
                "\nRegion: " + region + \
                "\nPopulation: " + population + \
                "\nCurrency: " + currency + \
                "\nDemonym: " + demonym + \
                "\nArea: " + area + " sq. km"
        print(data)
    #Otherwise, it gives: "Country Not Recognised"
    else:
        print("Country Not Recognised!")

    #'End_time' is used to store the finishing time
    end_time = time.time()
    #'Total_time' subtracts 'start_time' from 'end_time' to calculate the total time elapsed
    total_time = end_time - start_time
    #'Decimal_total_time' is the decimal version of 'total_time'
    decimal_total_time = Decimal(total_time)

    print("Total Time Elapsed: " + str(round(decimal_total_time, 2)) + " seconds.")

#Begins the Process
print_data()
