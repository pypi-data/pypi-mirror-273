from ca_vntl_helper import ErrorTrackerWithCallBacks

def send_message_to_slack(message):
    print("Message sent to slack:")
    print(message)
def save_message_to_logfile_on_s3(message):
    print("Message saved to logfile on S3:")
    print(message)

error_tracker = ErrorTrackerWithCallBacks(callback_functions=[send_message_to_slack, save_message_to_logfile_on_s3])

error_tracking_decorator_with_callbacks = error_tracker.error_tracking_decorator

def divide(a, b):
    return a / b


def second_inner_function(second_inner_a, second_inner_b):
    return divide(second_inner_a, second_inner_b)


def first_inner_function(first_inner_a, first_inner_b):
    return second_inner_function(first_inner_a, first_inner_b)


@error_tracking_decorator_with_callbacks  # Just place the decorator here
def outer_function(outer_a, outer_b):
    return first_inner_function(outer_a, outer_b)


if __name__ == "__main__":
    # The process will get an error when dividing by 0
    outer_function(1, 0)