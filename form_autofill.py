# Program to autofill google form using selenium
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import numpy as np

# Load firefox webdriver
driver = webdriver.Firefox()

url = "https://docs.google.com/forms/d/e/1FAIpQLSevfLzzh81zhuwO51r2wmWvRacpPBa94y41R8NzSDtB-E-cqw/viewform"

driver.get(url)

CONTAINER_CLASS = "geS5n"
QUESTION_CLASS = "M7eMe"
INPUT_CLASS = "KHxj8b"
RADIO_BUTTON_CLASS = "docssharedWizToggleLabeledContainer"
SUBMIT_BUTTON_CLASS = "NPEfkd"

# Responses to exclude to manipulate the data
EXCLUDE_RESPONSES = [
    "Other:",
    "Above 50",
    "35-50",
    "Under 18",
    "Doctorate",
    "Not at all familiar",
    "Encryption",
    "I'm not familiar with any of these terms",
    "Yes",
    "High School or less",
    "Some College or Associate's Degree",
    "Master's Degree",
    "High School or less",
]


def fillForm():
    question_containers = driver.find_elements(By.CLASS_NAME, CONTAINER_CLASS)

    # Dictionary to store input fields and radio buttons for each question container
    input_fields_stored = []
    radio_buttons_stored = []

    for question_container in question_containers:
        # To get question name
        # question_name = question_container.find_element(By.CLASS_NAME, "M7eMe").text

        # Store all input fields in a list
        # For input fields
        input_fields = question_container.find_elements(By.CLASS_NAME, INPUT_CLASS)
        if len(input_fields) > 0:
            input_fields_stored.extend(input_fields)

        # For radio buttons
        radio_buttons = question_container.find_elements(
            By.CLASS_NAME, RADIO_BUTTON_CLASS
        )

        required_buttons = []
        for radio_button in radio_buttons:
            if radio_button.text not in EXCLUDE_RESPONSES:
                required_buttons.append(radio_button)

        if len(radio_buttons) > 0:
            radio_buttons_stored.append(required_buttons)

    for rbs in radio_buttons_stored:
        print("[", end="")
        for rb in rbs:
            print(rb.text)
        print("]")

    for radio_buttons in radio_buttons_stored:
        # Select random radio button
        random_radio_button = np.random.choice(radio_buttons)
        random_radio_button.click()

    for input_field in input_fields_stored:
        input_field.send_keys("Random answer")

    # Submit form
    submit = driver.find_element(By.CLASS_NAME, SUBMIT_BUTTON_CLASS)
    submit.click()

    another_response = driver.find_element(By.LINK_TEXT, "Submit another response")
    another_response.click()


for i in range(50):
    time.sleep(0.5)
    fillForm()

driver.close()
