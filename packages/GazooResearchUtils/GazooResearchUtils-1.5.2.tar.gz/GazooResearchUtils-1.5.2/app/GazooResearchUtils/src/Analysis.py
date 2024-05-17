import numpy as np
import pandas as pd
from datetime import datetime
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

def multilesion_transforation(data):
  """
  Transforms from patient level analysis to multi-target level analysis

  Parameters:
  data (DataFrame): dataframe from csv data

  Returns:
  df (DataFrame): dataframe from csv data
  """
  # Transformed Dataframe
  df = pd.DataFrame()

  # Unique Targets
  targets = data.loc[data['field'] == 'target-id']
  targets = targets[['id', 'value']]
  targets.columns = ['id', 'target-id']
  targets = targets.drop_duplicates().reset_index()

  # Loop Through Targets
  for index, row in targets.iterrows():
    id = row['id']
    target_id = row['target-id']
    print(target_id)
    # Select Patients Tags
    pt = data.loc[data['id'] == id]
    # Remove Tags for other targets
    other_target_ids_tag_ids = pt.loc[(pt['field'] == 'target-id') & (pt['value'] != target_id)]['tag_id'].unique().tolist()
    # Filter out Non Target-ids
    pt = pt[~pt['tag_id'].isin(other_target_ids_tag_ids)]
    # Rename id
    pt['id'] = pt['id'].astype(str) + '-' + str(target_id)

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



def pt_dates_and_events(df, start_tag, event_tags, occurance=0):
  """
  Determines starting date, date of event occurence or data censoring, and whether
  event occured or data was censored

  Parameters:
  data (DataFrame): dataframe for patient
  start_tag (dict): Structure of filter {'icd10':str, 'tag': str, 'field': str, 'exact': [str, str,...], 'between': [float, float]}
  event_tags (list of dicts): list of possible filters. Structure of filter {'icd10':str, 'tag': str, 'field': str, 'exact': [str, str,...], 'between': [float, float]}
  occurance (int): index of occurance of the start tag

  Returns:
  start (str): date of starting event; None if no starting event
  end (str): earliest date of event occurence or latest known date; None if no
      starting event
  event (int): 1 if event occurred, 0 if data censored; None if no starting event
  """
  # Convert String to Date
  convert_date = lambda date: datetime.strptime(date, '%Y-%m-%d')

  # Get Start Dates
  test = get_data_filter(df, start_tag)
  start_dates = test.loc[(test['field']=='date')]['value'].to_numpy()
  start_dates = np.array(list(map(convert_date, start_dates)))
  start_dates = np.unique(start_dates)  # Remove Duplicates
  start_dates = np.sort(start_dates)  # Sort

  # Set Start Date
  if len(start_dates) >=1:
    start = start_dates[occurance]
  else:
    # Return None if no start date
    return None, None, None

  # Get Event Dates
  event_dates = []
  for event_tag in event_tags:
    test = get_data_filter(df, event_tag)
    events = test.loc[(test['field']=='date')]['value'].to_numpy()
    events = list(map(convert_date, events))
    # Append Dates
    event_dates = event_dates + events

  # Event Dates
  event_dates = np.asarray(event_dates)
  event_dates = np.sort(event_dates)

  # Only Keep Event Dates after Start Date
  event_dates = np.where(event_dates > start, event_dates, None)
  event_dates = event_dates[event_dates != np.array(None)]

  # Events 
  if len(event_dates) >= 1:
    last = event_dates[-1]
    event = 1
    return start, last, event

  # Return Censor
  censor_dates = df.loc[(df['field']=='date')].value.to_numpy()
  censor_dates = list(map(convert_date, censor_dates))
  censor_dates = np.sort(censor_dates) # sort
  last = censor_dates[-1]
  event = 0

  return start, last, event

def get_data_filter(pt, filter):
  """
  Get filter if exists in dataframe

  Parameters:
  data (DataFrame): dataframe
  filter (list of dicts): Structure of filter {'icd10':str, 'tag': str, 'field': str, 'exact': [str, str,...], 'between': [float, float]}

  Returns:
  data (DataFrame): dataframe with filters

  """
  if "value" in filter and "field" in filter and "tag" in filter and "icd10" in filter:
    test = pt.loc[(pt['icd10'] == filter['icd10'])
      & (pt['tag'] == filter['tag'])
      & (pt['field'] == filter['field'])
      & (pt['value'].isin(filter['value']))]
  elif "between" in filter and "field" in filter and "tag" in filter and "icd10" in filter:
    test = pt.loc[(pt['icd10'] == filter['icd10'])
      & (pt['tag'] == filter['tag'])
      & (pt['field'] == filter['field'])]
    test = pd.to_numeric(test['value']).between(filter['between'][0], filter['between'][1])
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

  return test


def filter(data, filters):
  """
  Only include patients that matches the filter

  Parameters:
  data (DataFrame): dataframe with csv data
  filters (list of dicts): list of possible filters. Structure of filter {'icd10':str, 'tag': str, 'field': str, 'exact': [str, str,...], 'between': [float, float]}

  Returns:
  data (DataFrame): dataframe with filters
  """

  df = pd.DataFrame()

  # Loop Through MRNs
  for mrn in data.id.unique():
    #print("mrn",mrn)
    # Select mrn specific Information
    pt = data.loc[(data['id'] == mrn)]

    # Loop Through Conditions
    #print(filters)
    valid = []
    for filter in filters:
      # Get filter
      test = get_data_filter(pt, filter)

      # Is filter apply
      if len(test.index) >= 1: valid.append(True)
      else: valid.append(False)

    # Append mrn to list if all filters apply
    if all(valid):
      df = pd.concat([df, pt])

  return df

def kaplan_meier(data, start_tag, event_tags):
  """
  Calculate kaplan-meier dataframe.

  Parameters:
  data (DataFrame): dataframe with csv data
  start_tag (dict): Structure of filter {'icd10':str, 'tag': str, 'field': str, 'exact': [str, str,...], 'between': [float, float]}
  event_tags (list of dicts): list of possible filters. Structure of filter {'icd10':str, 'tag': str, 'field': str, 'exact': [str, str,...], 'between': [float, float]}

  Returns:
  km (DataFrame): dataframe for kaplan meier calculation
  """
  km = pd.DataFrame(columns=['id', 'start-date', 'end-date', 'event'])

  # Loop id
  for id in data.id.unique():
    # Patient Data
    pt = data.loc[(data['id'] == id)]
    # Get Event/Censored
    start, last, event = pt_dates_and_events(pt, start_tag, event_tags)

    if not start == None:    # checking if patient has a starting event
      km.loc[len(km)] = [id, start, last, event]
  
  return km

def time_in_months(start, end):
    """
    Calculate the number of months between start and end dates.

    Parameters:
    start_date (datetime.datetime): starting date in the format YYYY-MM-DD
    end_date (datetime.datetime): end date in the format YYYY-MM-DD

    Returns:
    months (int): number of months (rounded down) between start and end dates
    """
    months = (end.year - start.year) * 12 + end.month - start.month
    if start.day > end.day:
        months -= 1  # round down if not a full month

    return months

def plot_km_curves(km):
    """
    Creates a Kaplan-Meier plot.

    Parameters:
    km (DataFrame): dataframe for kaplan meier
    """

    durations = km.apply(lambda row: time_in_months(row['start-date'], row['end-date']), axis = 1).to_numpy();
    events = km['event'].to_numpy()

    kmf = KaplanMeierFitter()
    kmf.fit(durations, event_observed=events)

    kmf.plot()

    plt.xlabel("Time (months)")
    plt.ylabel("Event Probability")
    plt.title("Kaplan-Meier Curve")
    plt.show()