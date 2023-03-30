import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    while city not in ('chicago', 'new york city', 'washington'):
        city = str(input("Please enter a city (Chicago, New York City, Washington)").lower())
        if city not in ('chicago', 'new york city', 'washington'):
            print("Please enter a valid city")
          
    # help used: https://stackoverflow.com/questions/30267420/while-loop-to-check-for-valid-user-input
    
    # get user input for month (all, january, february, ... , june)
    month = None
    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'): 
        month = str(input("Please enter a month from January to June, or enter 'all'").lower())
        if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print("That is not a valid month from January to June. Please try again")
    
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day = str(input("Please enter a day, or enter 'all'").lower())
        if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print("That is not a valid day. Please try again")
            
    print("\nYou chose {}, {}, and {}\n".format(city, month, day))


    print('-'*40)
    return city, month, day

def display_raw_data(df):
    """Asks the user if they would like to see the raw data 5 rows at at time until user doesn't respond yes"""
    i = 5
    raw_data_input = str(input("Would you like to see the raw data? \nIf you would like to see the raw data, please enter 'yes'\n").lower())
    raw_data_input_two = None
    continue_message = "You responded with something other than 'yes', so the program will continue"
    num_rows = df.shape[0]
    
    if raw_data_input == 'yes':
        print("There are", str(num_rows), "rows \n")
        pd.set_option('display.max_columns',200)
        print(df.head(i))
        raw_data_input_two = 'yes'
        while raw_data_input_two == 'yes':
            raw_data_input_two = str(input("Would you like to see 5 more rows of data, yes or no?").lower())
            if raw_data_input_two != 'yes':
                print("\n",continue_message)
                break
            else:
                print(df[i:i+5])
                i += 5
            if i >= num_rows:
                print(df.head(num_rows))
                print("\nThere aren't any more rows to display")
                break
    else:
        print("\n",continue_message)
            
            
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
    df = pd.read_csv(CITY_DATA.get(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    if month != 'all':
        df['Start Month'] = df['Start Time'].dt.month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Start Month'] == month]
        
    if day != 'all':
        df['day_of_week'] = df['Start Time'].dt.day_name()
        
        #days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        #day = days.index(day)
        df = df[df['day_of_week'] == day.title()]
        print(day)
        
    display_raw_data(df)
    print('-'*40)


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    if 'Start Month' not in df.columns:
        df['Start Month'] = df['Start Time'].dt.month
        
    months = ['Janauary', 'February', 'March', 'April', 'May', 'June']
    print("The most common month is ", months[df['Start Month'].mode()[0]-1])


    # TO DO: display the most common day of week
    # I used https://www.statology.org/pandas-check-if-column-exists/
    if 'day_of_week' not in df.columns:
        df['day_of_week'] = df['Start Time'].dt.day_name()
    print("The most common day is ", df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    if df['hour'].mode()[0] > 12:
        print("The most popular start hour is", df['hour'].mode()[0]-12, "PM")
    else:
        print("The most popular start hour is", df['hour'].mode()[0], "AM")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most popular start station is", df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print("The most popular end station is", df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    #referenced https://stackoverflow.com/questions/39291499/how-to-concatenate-multiple-column-values-into-a-single-column-in-pandas-datafra
    df['Routes'] = df['Start Station'].astype(str) + " and " + df['End Station'].astype(str)
    print("The most popular start and end station combination was",df['Routes'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_trip_duration = df['Trip Duration'].sum()
    avg_trip_duration = df['Trip Duration'].mean()
    
    # display total travel time
    print("The total travel time is {} seconds, {} minutes, or {} hours".format(round(total_trip_duration,1),\
                                                                                 round(total_trip_duration/60,1),\
                                                                                 round((total_trip_duration/60)/60,1))) 
    
    # display mean travel time
    print("The average travel time is {} seconds, {} minutes, or {} hours".format(round(avg_trip_duration,1),\
                                                                                 round(avg_trip_duration/60,1),\
                                                                                 round((avg_trip_duration/60)/60,1))) 
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types = df['User Type'].value_counts()
    gender_counts = None
    oldest_bday = None
    newest_bday = None
    most_common_bday = None
    
    
    # Display counts of user types
    print(user_types, '\n')

    # Display counts of gender
    if city == 'washington':
        print("There isn't any gender data available for this city \n")
        print("There isn't any birth year data available for this city \n")
    else:
        gender_counts = df['Gender'].value_counts()
        print(gender_counts, '\n')
        oldest_bday = int(df['Birth Year'].min())
        newest_bday = int(df['Birth Year'].max())
        most_common_bday = int(df['Birth Year'].mode()[0])
        print("The earliest birth year is {}, the most recent birth year is {}, and the most common birth year is {}" \
              .format(oldest_bday, newest_bday, most_common_bday))

    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def main():
    restart = None
    restart_bool = True
    while restart_bool == True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        
        #Changed the conditions underwhich the program closes
        while restart != 'yes' or 'no':
            restart = str(input("\nWould you like to restart? Enter yes or no.\n").lower())
            if restart == 'yes':
                print("You have entered yes, so the program will restart!")
                restart_bool == True
                break
            elif restart == 'no':
                restart_bool = False
                print("You have entered no, so the program will close")
                break
            else:
                print('You have entered something other than yes or no. Please try again')

if __name__ == "__main__":
	main()
