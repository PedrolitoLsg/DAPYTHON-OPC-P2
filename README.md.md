## README, Project Completed

Scraping the following website :https://books.toscrape.com/index.html

The final goal is to get several CSV (one for each category) containing the books and the following data associated :
		- title
		- url
		- category
		- universal product code
		- review rating
		- Price Excluding Tax (PET)
		- Price Including Tax (PIT)
		- stock
		- image url
		- product description

The goal is also to build an extractor that will get every image in one folder.

# PROCEDURE
For a first use on a computer please follow this procedure in order to have the correct requirements and be able to run successfully the program:

To do this you wil need to first create a virtual environment, it can be either done automatically by your IDE or by entering in the console the following code:
				 py -m venv env

install requirements.txt

# USAGE
To run the program call it, the two functions dl_images() and fill_csvs() automatically call the other functions used to extract data and structure the information to be delivered.
Just run the program (takes around 20min) and it will create a folder named img in the cwd containing all the images as well as a folder named csvs containing several files whose name will be the category of the books data contained in it



#Authors and Acknowledgemnt
I, Pierre Lesage have been developing this code under the tutorage of Alexandre Iwanovski whom i'd like to thank for his guidance and advice. I would also like to extend my appreciation to the members of the discord group whose help was critical at certain point in the project.

#License
This has been developped as a study project and with that in mind can be used freely by whomever.