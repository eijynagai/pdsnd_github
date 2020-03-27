import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = None
    while city not in CITY_DATA.keys():
        city = input("Please insert a valid city (Chicago, New York City, Washington): ").lower()
        if city not in CITY_DATA.keys():
            print('Please type again, something was wrong.')

    month = None
    valid_months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    while month not in valid_months:
        month = input("Please insert a month within January-June or all: ").lower()
        if month not in valid_months:
            print('Please type again, something was wrong.')

    day = None
    valid_weekdays = ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')
    while day not in valid_weekdays:
        day = input("Please insert a specific weekday or all: ").lower()
        if day not in valid_weekdays:
            print('Please type again, something was wrong.')

    print('-'*40)
    return city, month, day



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
    # Load file for chosen city
    df = pd.read_csv(CITY_DATA[city])

    # Create Month and Weekday columns
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # Returns filtered dataframe
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #print(df.info())

    # TO DO: display the most common month
    months_map = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    print('Most common month is {}.'.format(months_map[df['month'].value_counts().idxmax()]))

    # TO DO: display the most common day of week
    print('Most common day of week is {}.'.format(df['day_of_week'].value_counts().idxmax()))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('Most common start hour is {}.'.format(df['hour'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #print(df.head())
    # TO DO: display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print('Most common start station is {}.'.format(start_station))

    # TO DO: display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print('Most common end station is {}.'.format(end_station))

    # TO DO: display most frequent combination of start station and end station trip
    print('Most common combination is {}.'.format(df.groupby(['Start Station','End Station']).size().idxmax()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    print('Total trip duration is {} seconds.'.format(total_duration))

    # TO DO: display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('Mean trip duration is {} seconds.'.format(mean_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts().to_frame())

    if city != 'washington':

        # TO DO: Display counts of gender
        print('\n', df['Gender'].value_counts().to_frame())

        # TO DO: Display earliest, most recent, and most common year of birth
        print('\nThe eldest client was born in {}.'.format(str(int(df['Birth Year'].min()))))
        print('Most younger client was born in {}.'.format(str(int(df['Birth Year'].max()))))
        print('Most popular year is {}.'.format(str(int(df['Birth Year'].value_counts().idxmax()))))
    else:
        print('Ops, no information of gender and birth for Washington, sorry!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
