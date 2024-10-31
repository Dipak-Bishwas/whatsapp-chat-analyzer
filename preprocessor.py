import re
import pandas as pd

# Function for preprocessing chat data
def preprocess(data):
    # Pattern for date-time in chat format (e.g., 12/25/21, 5:45 PM - )
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*[AP]M\s-\s'

    # Split the data to get messages and dates
    messages = re.split(pattern, data)[1:]  # Exclude the first element which is before the first date
    dates = re.findall(pattern, data)

    # Truncate the longer list to the size of the smaller one
    min_length = min(len(messages), len(dates))
    messages = messages[:min_length]
    dates = dates[:min_length]

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')

    # Rename the column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users and messages
    users = []
    messages = []
    for msg in df['user_message']:
        entry = re.split(r'([\w\s]+?):\s', msg)
        if len(entry) > 2:
            users.append(entry[1])  # Extract the username
            messages.append(entry[2])  # Extract the message
        else:
            users.append('')  # If no user is found, append empty
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Add additional columns for date analysis
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create the period column based on the hour
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour + 1}")
        else:
            period.append(f"{hour}-{hour + 1}")
    df['period'] = period

    return df