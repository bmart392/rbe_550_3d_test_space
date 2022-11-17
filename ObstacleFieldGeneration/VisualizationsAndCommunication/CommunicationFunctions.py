import csv


# Log messages in an external text file for debugging purposes
def log_messages_in_a_log_file(log_file_location, messages):
    with open(log_file_location, 'a') as logFile:

        # If there is only one message, create an array for iteration
        if isinstance(messages, str):
            messages = [messages]

        # Append each message to the existing text in the file
        for message in messages:
            logFile.write(message)
            logFile.write('\n')


# Write array of obstacle locations to a text file
def write_obstacles_to_text_file(filename, header, data):
    with open(filename, 'w', newline='') as obstacle_file:
        obstacle_file_writer = csv.writer(obstacle_file)
        obstacle_file_writer.writerow(header)
        for row in data:
            obstacle_file_writer.writerow(row)

