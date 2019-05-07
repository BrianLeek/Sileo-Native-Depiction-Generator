#!/usr/bin/env python3
import os
import sys
import json
import datetime
import fileinput
import config

####################
# Thanks to everybody who has contributed!
#
# Brian Leek - Developer (https://brianleek.me/)
# Mathsh - Contributed Code (https://www.reddit.com/user/Mathsh)
#   - Helped with adding screenshot support and answered some questions I had.
# Jon Betts - Contributed Code (https://stackoverflow.com/users/3569627/jon-betts)
#   - Helped with some code and a question I had.
####################

# Put the questions to ask the user in a function to use later.
# By adding them into a function it makes it might make it easier when adding a templale to the script.
def HeaderImageQuestion():
    global headerimage
    headerimage = input("Header Image URL: ")
def PackageIDQuestion():
    # This is required to generate the depiction file and should be included in the questions on all templates.
    global packageid
    while True:
        try:
            packageid = input("Package ID (com.example.package): ")
            if packageid == '':
                print("Please enter a ID for your package.")
                continue
            else:
                break
        except ValueError:
            break
def PackageNameQuestion():
    global packagename
    while True:
        try:
            packagename = input("Package Name: ")
            if packagename == '':
                print("Please enter a name for your package.")
                continue
            else:
                break
        except ValueError:
            break
def PackageDescripionQuestion():
    global description
    while True:
        try:
            description = input("Package Description: ")
            if description == '':
                print("Please enter a description for your package.")
                continue
            else:
                break
        except ValueError:
            break
def KnownIssuesQuestion():
    global knownissues
    knownissues = input("Known Issues: ")
def FirstVersionQuestion():
    global firstversion
    while True:
        try:
            firstversion = input("First Release Version Number (Example: 1.0): ")
            if firstversion == '':
                print("Please enter the first released version number for your package.")
                continue
            elif firstversion.isalpha():
                print("Please enter a number not a string.")
                continue
            else:
                break
        except ValueError:
            break
def FirstReleaseDateQuestion():
    global firstreleasedate
    while True:
        try:
            firstreleasedate = input("First Version Release Date (YYYY/MM/DD): ")
            if firstreleasedate == '':
                print("Please enter the date your package was first released.")
                continue
            else:
                pass
            datetime.datetime.strptime(firstreleasedate, '%Y/%m/%d')
            break
        except ValueError:
            print("Incorrect date format, should be YYYY/MM/DD")
            continue
def LatestVersionQuestion():
    global latestversion
    while True:
        try:
            latestversion = input("Latest Version (Example: 1.2): ")
            if latestversion == '':
                print("Please enter the latest released version number for your package.")
                continue
            elif latestversion.isalpha():
                print("Please enter a number not a string.")
                continue
            else:
                break
        except ValueError:
            break
def LatestReleasedDateQuestion():
    global latestreleasedate
    while True:
        try:
            latestreleasedate = input("Latest Version Release Date (YYYY/MM/DD): ")
            if latestreleasedate == '':
                print("Please enter the date your latest version of your package was released.")
                continue
            else:
                pass
            datetime.datetime.strptime(latestreleasedate, '%Y/%m/%d')
            break
        except ValueError:
            print("Incorrect date format, should be YYYY/MM/DD")
            continue
def PriceQuestion():
    global price
    while True:
        try:
            price = input("Price: ")
            if price == '':
                print("Please enter a price.")
                continue
            else:
                break
        except ValueError:
            break
def DeveloperQuestion():
    global developer
    while True:
        try:
            developer = input("Developer Name: ")
            if developer == '':
                print("Please enter a name.")
                continue
            else:
                break
        except ValueError:
            break
def SupportURLQuestion():
    global supporturl
    supporturl = input("Support URL: ")

print("This script will generate/create you a native depiction file for Sileo but some information like changelog/version history will not be include because support for it has not yet been added so you will have to edit the depiction file after to add that information. This script will be able to add changelog/version history in the future just not yet.")
print("You may leave some fields blank.")
print("Pick Template")
# List all files in the templates folder.
templatepath = config.TemplatesPath
files = os.listdir(templatepath)
for name in files:
    print(name)
template = input("Template Number: ")

# Start Template 1
if template == "1":
    # This is the template file that is going to be used to create your depiction file.
    TemplateFileName = "template1.json"

    try:
        # Call the questions that are in the functions above to ask the user some information to add to the depiction file later.
        PackageIDQuestion()
        HeaderImageQuestion()
        PackageNameQuestion()
        PackageDescripionQuestion()
        FirstVersionQuestion()
        FirstReleaseDateQuestion()
        LatestVersionQuestion()
        LatestReleasedDateQuestion()
        PriceQuestion()
        DeveloperQuestion()
        SupportURLQuestion()

        # Get the placeholder text in the template file and tells the script to replace the information the user enters.
        replacements = {'Header Image URL':headerimage, 'Package Name':packagename, 'Package Description':description, 'First Released Version Number':firstversion, 'First Release Date':firstreleasedate, 'Latest Version Number':latestversion, 'Latest Release Date':latestreleasedate, 'Package Price':price, 'Package Developer':developer, 'Support URL':supporturl}
        # Remove placeholder text if input field is left blank.
        removeplaceholdertext = {'Header Image URL':'', 'Support URL':''}

        # If the folder to save the depiction file doesn't exists create it.
        try:
            if not os.path.exists(config.SaveDepictionPath):
                os.makedirs(config.SaveDepictionPath)
        except ValueError:
            print("Failed to create the folder to save your depiction file. Please check config.py.")

        # Try and create the depiction file with the name entered in the package id question.
        with open(config.TemplatesPath+TemplateFileName) as infile, open(config.SaveDepictionPath+packageid, 'w') as outfile:
            # Replace the placeholder text that was entered in "replacements" with the information the user entered.
            try:
                for createdepictionfile in infile:
                    for src, target in replacements.items():
                        createdepictionfile = createdepictionfile.replace(src, target)
                    outfile.write(createdepictionfile)
                print("Successfully created "+ packageid +" in "+ config.SaveDepictionPath+".")
            except ValueError:
                print("Failed to create "+ packageid +" in "+ config.SaveDepictionPath+".")

            # Try and remove the placeholder text that was entered in "removeplaceholdertext".
            try:
                for removeplaceholders in infile:
                    for placeholder, removeplaceholder in removeplaceholdertext.items():
                        removeplaceholders = removeplaceholders.replace(placeholder, removeplaceholder)
                    outfile.write(removeplaceholders)
                print("Successfully removed placeholder text.")
            except ValueError:
                print("Failed to remove placeholder text.")

        # Load the data
        file_name = config.SaveDepictionPath+packageid
        with open(file_name) as fh:
            full_data = json.load(fh)

        # Thanks Mathsh for the code! (https://www.reddit.com/user/Mathsh)
        screenshot_template = full_data['tabs'][0]['views'][1]['screenshots'][0]
        full_data['tabs'][0]['views'][1]['screenshots'].pop(0)
        screenshot_url = input("Please enter a screenshot url.  Enter a blank string when you are finished: ")
        while screenshot_url != "":
            modified_screenshot_template = screenshot_template
            modified_screenshot_template['url'] = screenshot_url
            modified_screenshot_template['fullSizeURL'] = screenshot_url
            full_data['tabs'][0]['views'][1]['screenshots'].append(modified_screenshot_template.copy())
            screenshot_url = input("Please enter a screenshot url.  Enter a blank string when you are finished: ")

        # Save the data
        with open(file_name, 'w') as fh:
            json.dump(full_data, fh, indent=3)

        print("Successfully generated your depiction file.")
    except ValueError:
        print("Failed to generate your depiction file.")
# End Template 1


# Start Template 2
elif template == "2":
    # The name of the template that is being used.
    TemplateFileName = "template2.json"

    try:
        # Call the questions that are in the functions above to ask the user some information to add to the depiction file later.
        PackageIDQuestion()
        HeaderImageQuestion()
        PackageDescripionQuestion()
        FirstVersionQuestion()
        LatestVersionQuestion()
        PriceQuestion()
        DeveloperQuestion()
        SupportURLQuestion()

        # Get the placeholder text in the template file and tells the script to replace the information the user enters.
        replacements = {'Header Image URL':headerimage, 'Package Description':description, 'First Released Version Number':firstversion, 'Latest Version Number':latestversion, 'Package Price':price, 'Package Developer':developer, 'Support URL':supporturl}
        # Remove placeholder text if input field is left blank.
        removeplaceholdertext = {'Header Image URL':'', 'Support URL':''}

        # If the folder to save the depiction file doesn't exists create it.
        try:
            if not os.path.exists(config.SaveDepictionPath):
                os.makedirs(config.SaveDepictionPath)
        except ValueError:
            print("Failed to create the folder to save your depiction file. Please check config.py.")

        # Try and create the depiction file with the name entered in the package id question.
        with open(config.TemplatesPath+TemplateFileName) as infile, open(config.SaveDepictionPath+packageid, 'w') as outfile:
            # Replace the placeholder text that was entered in "replacements" with the information the user entered.
            try:
                for createdepictionfile in infile:
                    for src, target in replacements.items():
                        createdepictionfile = createdepictionfile.replace(src, target)
                    outfile.write(createdepictionfile)
                print("Successfully created "+ packageid +" in "+ config.SaveDepictionPath+".")
            except ValueError:
                print("Failed to create "+ packageid +" in "+ config.SaveDepictionPath+".")

            # Try and remove the placeholder text that was entered in "removeplaceholdertext".
            try:
                for removeplaceholders in infile:
                    for placeholder, removeplaceholder in removeplaceholdertext.items():
                        removeplaceholders = removeplaceholders.replace(placeholder, removeplaceholder)
                    outfile.write(removeplaceholders)
                print("Successfully removed placeholder text.")
            except ValueError:
                print("Failed to remove placeholder text.")

        # Load the data
        file_name = config.SaveDepictionPath+packageid
        with open(file_name) as fh:
            full_data = json.load(fh)

        # Thanks Mathsh for the code! (https://www.reddit.com/user/Mathsh)
        screenshot_template = full_data['tabs'][0]['views'][3]['screenshots'][0]
        full_data['tabs'][0]['views'][3]['screenshots'].pop(0)
        screenshot_url = input("Please enter a screenshot url.  Enter a blank string when you are finished: ")
        while screenshot_url != "":
            modified_screenshot_template = screenshot_template
            modified_screenshot_template['url'] = screenshot_url
            modified_screenshot_template['fullSizeURL'] = screenshot_url
            full_data['tabs'][0]['views'][3]['screenshots'].append(modified_screenshot_template.copy())
            screenshot_url = input("Please enter a screenshot url.  Enter a blank string when you are finished: ")
        if full_data['tabs'][0]['views'][3]['screenshots'] == []:
            full_data['tabs'][0]['views'].pop(3)

        # Save the data
        with open(file_name, 'w') as fh:
            json.dump(full_data, fh, indent=4)

        print("Successfully generated your depiction file.")
    except ValueError:
        print("Failed to generate your depiction file.")
# End Template 2

# Show the user a error if they enter a number for a template that can't be found.
else:
    print("The template you are looking for can not be found!")
