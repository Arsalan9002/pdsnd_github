import time
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

CITIES = ['chicago', 'new york', 'washington']

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
def get_filters():    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
       city = input('Which city do you want to explore Chicago, New York or Washington? \n> ').lower()
       if city in CITIES:
           break
    
    month = input("Enter Month (Name): ")
    day = input("Enter Day (Number): ")

    print('-'*40)
    return city, month.lower(), day

def display_data(df):
    row_length = df.shape[0]

    # iterate from 0 to the number of rows in steps of 5
    for i in range(0, row_length, 5):
        
        yes = input('\nWould you like to examine the particular user trip data? Type \'yes\' or \'no\'\n> ')
        if yes.lower() != 'yes':
            break
        
        # retrieve and convert data to json format
        # split each json row data 
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            # pretty print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)
            
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_time = time.time()

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month                 # range (1-12)
    df['day_of_week'] = df['Start Time'].dt.dayofweek       # range (0-6)
    df['hour'] = df['Start Time'].dt.hour                   # range (0-23)

    init_total_rides = len(df)
    filtered_rides = init_total_rides    # initially

    # filter by month if applicable
    if month != 'all':
        # use the index of the MONTHS list to get the corresponding int
        month_i = MONTHS.index(month) + 1     # index() returns 0-based, so +1
    
        # filter by month to create the new dataframe
        df = df[df.month == month_i]
        month = month.title()



    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df["Start Time"].dt.month
    common_month = df['month'].mode()[0]
    print("Most Common Month: ",common_month)
    
    # TO DO: display the most common day of week
    df['weekday_name'] = df["Start Time"].dt.weekday_name
    common_weekday_name = df['weekday_name'].mode()[0]
    print("Most Common weekday: ",common_weekday_name)
    
    # TO DO: display the most common start hour
    df['hour'] = df["Start Time"].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print("Most Common Start Hour: ", common_start_hour)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station: ",common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("Most Common End Station: ", common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df["Start-End-Station-Combo"] = df["Start Station"] + '_' + df["End Station"]
    common_combo_station = df['Start-End-Station-Combo'].mode()[0]
    print("Most Common Combination of Start & End Station: ",common_combo_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # TO DO: display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['total travel time'] = df['End Time'] - df['Start Time']
    print("Total Travel Time: ",sum(df['total travel time'].dt.total_seconds()))

    # TO DO: display mean travel time
    print("Mean Travel Time",df['total travel time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
#     len(pd.unique(df['height']))
    print("Count of User Types:  ", len(pd.unique(df['User Type'])))
    # TO DO: Display counts of gender
    print("Count of Gender: ", len(pd.unique(df['Gender'])))

    print("\n")
    # TO DO: Display earliest, most recent, and most common year of birth
    print("Earliest Birth Year is:",min(df['Birth Year']))
    print("Most Recent Birth Year is:",max(df['Birth Year']))
    print("Most Common Birth Year is:", df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city!='washington':
            user_stats(df)
        
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    
  
        


if __name__ == "__main__":
	main()
