# Jautomate
This tool automates MDM tasks on Jamf using the Jamf Pro and Jamf Classic API. For now there are only tasks focused on mobile devices. Computer versions of those tasks are in the works.

## Installation
---
A pip installation will be set up once the build has been tested. For now you can install it from the testing PyPi server with this command:

```bash
python3 -m pip install --index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple/ jautomate
```

## Setup

### Env Variables
You have to define the following environment variables in a `.env` file to connect to your Jamf Pro server.

```
JPS_USERNAME=[Username]
JPS_PASSWORD=[Password]
JPS_URL=[Url]
```

## Basic Usage

This tool runs from the command line and has basic help information built into it. To access the help functions use the command:

```bash
jautomate --help
```
## Available Commands

### Assign a device

Add student information to a device record in Jamf Pro

```bash
jautomate assign [DEVICE_TYPE] [ASSET_TAG] [SERIAL_NUMBER] [STUDENT_NAME] [HOMEROOM] [STUDENT_GRADE] [BUILDING]
```

**Required arguments**

| | |
| --- | --- |
DEVICE_TYPE | Type of device being updated. {mobile / computer}
ASSET_TAG | Asset tag should be a 6 digit number
SERIAL_NUMBER | Serial Number of device
STUDENT_NAME | Student full name  
HOMEROOM | Homeroom teachers last name
STUDENT_GRADE | Student grade as a number
BUILDING | Building names as used in Jamf Pro


### Unassign a device
Remove student information from device record in Jamf Pro.

```bash
jautomate unassign [DEVICE_TYPE] [ASSET_TAG]
```

**Required arguments**

| | |
| --- | --- |
DEVICE_TYPE | Type of device being updated. {mobile / computer}
ASSET_TAG | Asset tag should be a 6 digit number

### Sync multiple device records
Syncs data from a csv file of device records to Jamf Pro. Devices must all be of same type (mobile/computer.)

```bash
jautomate sync [DEVICE_TYPE] [FILE_PATH]
```

**Required arguments**

| | |
| --- | --- |
DEVICE_TYPE | Type of devices being updated. {mobile / computer}
FILE_PATH | The path to the csv file to be imported


# Development
References for dev/testing
```bash
# Run this line from the same directory as setup.py
python -m build 
# To test the build you can install/re-install with this line.
pip install dist/jautomate-0.0.7-py3-none-any.whl --force-reinstall 
```