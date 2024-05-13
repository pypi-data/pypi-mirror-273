import numpy as np
import pandas as pd
from .. import utils
from ..database.db_interactions import SqlHandle

#inst = SqlHandle()

def get_survey_design(column_name:str)->pd.DataFrame:
    """Getting SurveyDesign

    Examples:
        >>> from BWS.model.analysis import get_survey_design
        >>> get_survey_design("Cisco_Router")

    Args:
        column_name (str): The companie's product for which we want to create survey design

    Returns:
        pd.DataFrame: Dataframe containing the structure of the survey (how it will be conducted)
    """
    inst = SqlHandle()
    # Assuming the column name is already sanitized
    column_data = inst.get_attributes(column_name)

    if column_data:
        # Extract values from tuples and handle NaN values
        column_values = column_data
    else:
        print("No attributes found for the specified column.")
        column_values = []
        inst.close()
        return
    # Pass the column values to the design_creation function
    if column_values:
        survey_design = utils.design_creation(column_values)
    else:
        print("No attributes found for the specified column.")
        # Handle the case where no attributes are found for the specified column
        inst.close()
        return

    inst.close()
    return survey_design

def push_survey_design(column_name:str,survey_design:pd.DataFrame):
    """Pushing the Survey Design into the database

    Examples:
        >>> from BWS.model.analysis import push_survey_design, get_survey_design
        >>> push_survey_design("Cisco_Router", get_survey_design("Cisco_Router"))

    Args:
        column_name (str): The companie's product
        survey_design (pd.DataFrame): Dataframe containing the structure of the survey (how it will be conducted)
    """
    inst = SqlHandle()

    table_name = f"survey_{column_name}"
    inst.pandas_to_sql(survey_design, table_name)
    inst.close()
    return

def push_analysis1(product_name:str):
    """Analyse and push to DB 1

    Examples:
        >>> from BWS.model.analysis import push_analysis1
        >>> push_analysis1("Cisco_Router")

    Args:
        product_name (str): Name of the product, which responses are going to be analyzed
    """

    inst = SqlHandle()

    data = inst.read_table(f"response_{product_name}") 
    data.drop(columns=['id'], inplace=True) 
    result = utils.output_1_simple_demographic(data) 
    inst.pandas_to_sql(result, f"analysis1_{product_name}")
    inst.close() 
    return

def push_analysis2(product_name:str):
    """Analyse and push to DB 2

    Examples:
        >>> from BWS.model.analysis import push_analysis2
        >>> push_analysis2("Cisco_Router")

    Args:
        product_name (str): Name of the product, which responses are going to be analyzed
    """

    inst = SqlHandle()

    data = inst.read_table(f"response_{product_name}") 
    data.drop(columns=['id'], inplace=True) 
    result = utils.output_2_general_importance_plot_df(data) 
    inst.pandas_to_sql(result, f"analysis2_{product_name}") 
    inst.close()
    return
 
def push_analysis3(product_name:str):
    """Analyse and push to DB 3

    Examples:
        >>> from BWS.model.analysis import push_analysis3
        >>> push_analysis3("Cisco_Router")

    Args:
        product_name (str): Name of the product, which responses are going to be analyzed
    """

    inst = SqlHandle()
    
    data = inst.read_table(f"response_{product_name}") 
    data.drop(columns=['id'], inplace=True) 
    result = utils.output_3_4_importance_by_demographic(data) 
    inst.pandas_to_sql(result, f"analysis3_{product_name}")
    inst.close()
    return