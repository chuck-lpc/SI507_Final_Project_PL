# Steam Account Analyzer

## Introduction
Steam is a video game digital distribution service by Valve. Users may purchase games or other software with steam. The purchased items will be under the users’ “library”. As time goes by, the prices may change. Because Steam does not explicitly show the prices of an item once the item is already in a user’s library (already purchased), the user may be wondering about “What is the total value of my account?” or “What is the sum of the current prices of the items in my library?” Though the Steam does not show the current prices once a user is logged in and already has the items in the user’s library, the prices are still available without logging in. This project aims at automating the process of retrieving all non-free items in a user’s library, present it in a readable way, and sum up the current prices of all the retrieved items and display it to the user. As an additional bonus feature, it can convert the price to different currencies based on the latest rate. A demo video is available at https://drive.google.com/file/d/1AZRKh2EEeQ2L1AM1nuJ-OZugjy0I5f9A/view?usp=sharing

## Install Requirements
The code is tested with Python 3.7.5 and the packages listed in requirements.txt. It is advisiable to make a new virtual environment and install the dependencies. 

The provided requirements.txt can be used to install all the required packages. Use the following commands to install dependencies:

for linux:
```
pip install –r requirements.txt
```
for windows:
```
py -3 -m pip install -r requirements.txt
```

## Run the Program

Run app.py as the top module, and then open a web browser and open the url: http://localhost:5000/

The welcome page should show up. Then enter a valid Steam ID and choose the options on the page, then click "Get Value" button. The program will retrive, cache, and display the data in a new page.