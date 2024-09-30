This repository holds the files used in my dissertation at LJMU in 2024 to try and answer the question "Is it appropriate to use the same xG model for Women’s football and Men’s football?"

To do this I first of all scraped about 30,000 games worth of event data, condensed this to goals only, stored the data in a MongoDB, ran a number of machine learning models over the
data and selected the most appropriate.  Then ran this over WSL games and games in England to see if the variance between xG and Actual goals for men and women was significantly different.

The scripts in this repository should be run in numeric order
