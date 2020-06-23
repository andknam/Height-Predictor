# HeightPredictor!

One of the things done frequently in pediatrics is to predict a patient's height based on their growth. This is to determine whether or not a patient's current illness will impact their final growth. However, figuring out predicted height is a cumbersome process involving looking up a value from a dense table. 

This is where the HeightPredictor! Alexa skill comes in to play. Users ask Alexa to 'make a height prediction' and Alexa will ask users to fill out some information. Currently, the Alexa skill takes six input values: patient name, patient gender, recent height of the patient, growth type of the patient, the year value of the skeletal age, and the month value of the skeletal age. Using these values, Alexa parses a google sheet that holds the height prediction table (converted to csv format) to return the predicted height. Attributes are then stored using Amazon DynamoDB.

The web application takes this a step further, taking in the following inputs: patient name, gender, recent height, chronological age, skeletal age, and a choice between using brush foundation means or one year from the chronological age for the skeletal growth type calculation.

The prediction tables can be found [here!](https://docs.google.com/spreadsheets/d/1fOM_Hntn5P9DXMg4o_rzHxrWJSM_MEwCXgiosloYCqY/edit#gid=1419711891)

The accompanying proof-of-concept web application can be found [here!](http://andrew22124.pythonanywhere.com)

**Alexa Skill Features:**
- [ ] option to ask for the information of a previously documented patient
- [x] (added 5/25/2020) add patient gender and age as variables
- [x] (added 5/25/2020) parse different height prediction tables based on the gender and age variables
- [x] (v1 added 5/25/2020) parse out the input values from a single utterance, rather than asking the user for input values one by one
- [x] (added 6/5/2020) store patient information in database 
- [x] (added 6/5/2020) make sure parsing values are in the table

**Web App Features:**
- [x] (added 6/9/2020) automatically unchecks checkbox when a different checkbox is selected
- [x] (added 6/9/2020) fixed some processing problems
- [x] (added 6/19/2020) added chronological age for automatic skeletal growth type calculation
- [x] (added 6/23/2020) added choice between brush foundations means and one year from chronological age 
