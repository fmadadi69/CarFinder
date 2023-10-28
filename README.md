# CarFinder
This is the final project of ADVANCE PYTHON PROGRAMING course from Maktabkhooneh.

It is a Django web application to predict the price of your car of interest using scraped data of car sales websites (Bama.ir)

1- In Admin site a button (Insert Car) is provided. Whenever admin user clicks on the 'Insert Car' button, system scrapes data of BAMA website (checks not to be duplicated data) and insert them in database tables.

2-In Car_Prediction view, other users enter requested data (make_year_location_mileage) about their desired car and ask the system to predict the price of it.

3-In the Similar_Cars View, System displays the predicted price of the desired car. It also displays the list of similar cars that are advertised to be saled on BAMA.

4-In the Car_lists View, a list of all advertised cars on BAMA will be displayed.
