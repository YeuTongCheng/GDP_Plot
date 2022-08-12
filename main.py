import csv
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            value_of_keyfield = row[keyfield]
            table[value_of_keyfield] = row
    return table


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    gdp_data=[]
    for key, value in gdpdata.items():
        if gdpinfo['min_year']<=int(key)<=gdpinfo['max_year']:
            if value!="":
                gdp_data.append(tuple([int(key),float(value)]))
            else:
                pass
            gdp_data.sort(key=lambda tup: tup[0])
    return gdp_data


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    country_gdp={}
    country_dict=read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo["country_name"],\
                                         gdpinfo['separator'], gdpinfo['quote'])  
    for country in country_list:
        if  country_dict.get(country) is None:
            country_gdp[country]=[]
        else:
            filter_dict=dict(e for i, e in enumerate(country_dict[country].items()) if i>=4)
            country_gdp[country]=build_plot_values(gdpinfo,filter_dict)
    return country_gdp
