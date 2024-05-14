import pandas as pd
from datetime import datetime
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

def one_to_many_transformation(data):
  """
  Transforms from patient level analysis to target level analysis

  Parameters:
  data (DataFrame): dataframe from csv data

  Returns:
  df (DataFrame): dataframe from csv data
  """
  # Transformed Dataframe
  df = pd.DataFrame()


  # Unique Targets
  targets = data.loc[data['field'] == 'target-id']
  targets = targets[['mrn', 'value']]
  targets.columns = ['mrn', 'target-id']
  targets = targets.drop_duplicates().reset_index()

  # Loop Through Targets
  for index, row in targets.iterrows():
    mrn = row['mrn']
    target_id = row['target-id']

    # Select Patients Tags
    pt = data.loc[data['mrn'] == mrn]

    # Remove Tags for other targets
    other_target_ids_tag_ids = pt.loc[(pt['field'] == 'target-id') & (pt['value'] != target_id)]['tag_id'].unique().tolist()
    # Filter out Non Target-ids
    pt = pt[~pt['tag_id'].isin(other_target_ids_tag_ids)]
    # Rename mrn
    pt['mrn'] = pt['mrn'] + '-' + target_id

    # Concat
    df = pd.concat([df, pt])

  return df

def get_data_dictionary(data):
  """
  Returns data dictionary.

  Parameters:
    data (DataFrame): dataframe with csv data

    Returns:
    dictionary (DataFrame): dataframe with options
    
  """
  
  data = data[['icd10', 'tag', 'field', 'data_type']]
  # Remove Duplicates
  dictionary = data.drop_duplicates()
  # Sort
  dictionary = dictionary.sort_values(['icd10', 'tag', 'field'], ascending=[True, True, True])

  return dictionary

def get_mrns_where_filters(data, filters):
  """
  Obtains mrns where filters applies.

  Parameters:
    data (DataFrame): dataframe with csv data
    event_tag_list (list of dicts): list of possible filters. Structure of filter {'icd10':str, 'tag': str, 'field': str, 'value': [str, str,...]}

    Returns:
    mrn_list (list of str): mrns
    
  """
  
  mrn_list = []

  # Loop Through MRNs
  for mrn in data.mrn.unique(): 
    #print("mrn",mrn)
    # Select mrn specific Information
    pt = data.loc[(data['mrn'] == mrn)]

    # Loop Through Conditions
    #print(filters)
    valid = []
    for filter in filters:

      if "value" in filter and "field" in filter and "tag" in filter and "icd10" in filter:
        test = pt.loc[(pt['icd10'] == filter['icd10']) 
          & (pt['tag'] == filter['tag'])
          & (pt['field'] == filter['field'])
          & (pt['value'].isin(filter['value']))]
      elif "field" in filter and "tag" in filter and "icd10" in filter:
        test = pt.loc[(pt['icd10'] == filter['icd10']) 
          & (pt['tag'] == filter['tag'])
          & (pt['field'] == filter['field'])]
      elif "tag" in filter and "icd10" in filter:
        test = pt.loc[(pt['icd10'] == filter['icd10']) 
          & (pt['tag'] == filter['tag'])]
      elif "icd10" in filter:
        test = pt.loc[(pt['icd10'] == filter['icd10'])]
      else:
        test = pd.DataFrame()

      # Is filter apply
      if len(test.index) >= 1: valid.append(True)
      else: valid.append(False)

    #print(valid)
    # Append mrn to list if all filters apply
    if all(valid):
      mrn_list.append(str(mrn)) 

  return mrn_list


def plot_km_curves(time_list, event_list):
    """
    Creates a Kaplan-Meier plot.

    Parameters:
    time_list (list of int): time in months until censoring of data
    event_list (list of int): 1 or 0 to specify if event occurred
    """
    kmf = KaplanMeierFitter()
    kmf.fit(time_list, event_observed=event_list)

    kmf.plot()

    plt.xlabel("Time")
    plt.ylabel("Survival Probability")
    plt.title("Kaplan-Meier Curve")
    plt.show()


def kaplan_meier_data(data, mrn_list, icd10_code, start_tag, event_tag_list):
    """
    Calculate time in months until event or data censoring.

    Parameters:
    data (DataFrame): dataframe with csv data
    mrn_list (list of str): list of patient MRNs
    icd10_code (str): icd10 code
    start_tag (str): starting event
    event_tag_list (list of str): list of possible events

    Returns:
    time_list (list of int): time in months until censoring of data
    event_list (list of int): 1 or 0 to specify if event occurred
    """

    time_list = []
    event_list = []

    for pt in mrn_list:
        start, last, event = pt_dates_and_events(
            data, pt, icd10_code, start_tag, event_tag_list
        )
        if not start == None:    # checking if patient has a starting event
            time_diff = time_in_months(start, last)
            time_list.append(time_diff)
            event_list.append(event)

    return time_list, event_list


def time_in_months(start_date, end_date):
    """
    Calculate the number of months between start and end dates.

    Parameters:
    start_date (str): starting date in the format YYYY-MM-DD
    end_date (str): end date in the format YYYY-MM-DD

    Returns:
    months (int): number of months (rounded down) between start and end dates
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    months = (end.year - start.year) * 12 + end.month - start.month
    if start.day > end.day:
        months -= 1  # round down if not a full month

    return months


def pt_dates_and_events(df, mrn, icd10_code, start_tag, event_tag_list):
    """
    Determines starting date, date of event occurence or data censoring, and whether
    event occured or data was censored

    Parameters:
    data (DataFrame): dataframe with csv data
    mrn (str): patient MRN
    icd10_code (str): icd10 code
    start_tag (str): starting event
    event_tag_list (list of str): list of possible events

    Returns:
    start (str): date of starting event; None if no starting event
    end (str): earliest date of event occurence or latest known date; None if no
        starting event
    event (int): 1 if event occurred, 0 if data censored; None if no starting event
    """

    df_pt = df[[str(x) == mrn for x in df["mrn"]]]
    if not df_pt[
        [
            x == icd10_code and y == start_tag
            for x, y in zip(df_pt["icd10"], df_pt["tag"])
        ]
    ].empty:     # checking to make sure patient has a starting event
        start = df_pt[
            [
                x == icd10_code and y == start_tag and z == "date"
                for x, y, z in zip(df_pt["icd10"], df_pt["tag"], df_pt["field"])
            ]
        ]["value"].item()

        # get last known date for patient
        last = df_pt[df_pt["field"] == "date"].dropna()["value"].sort_values().iloc[-1]
        event = 0

        # check if patient has any events, update accordingly
        for event_tag in event_tag_list:
            if not df_pt[
                [
                    x == icd10_code and y == event_tag
                    for x, y in zip(df_pt["icd10"], df_pt["tag"])
                ]
            ].empty:
                event = 1
                date = df_pt[
                    [
                        x == icd10_code and y == event_tag and z == "date"
                        for x, y, z in zip(df_pt["icd10"], df_pt["tag"], df_pt["field"])
                    ]
                ]["value"].item()
                last = (
                    date
                    if datetime.strptime(last, "%Y-%m-%d")
                    > datetime.strptime(date, "%Y-%m-%d")
                    else date
                )
    else:     # if patient does not have a starting event, return Nones
        start = None
        last = None
        event = None

    return start, last, event