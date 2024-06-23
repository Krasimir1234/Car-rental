## Adding a New Car
# This options are only for admins and a user is not able to acces them
To add a new car to the system, please fill in the following fields:

1. **ID**: 
   - Enter an integer ID ("101").

2. **Car Make**: 
   - Enter the car make. It doesn't matter if the letters are capitalized or not ("Toyota" or "toyota").

3. **Car Model**: 
   - Enter any car model. You can use a combination of letters and numbers ("Camry123").

4. **Car Year**: 
   - Enter the car year using only numbers ("2020").

5. **Car Price**: 
   - Enter the price per day for renting the car. This needs to be a number ("50").

6. **Status**: 
   - Enter the status of the car in FULL CAPITAL LETTERS. The options are:
     - **YES**: The car is available.
     - **NO**: The car is not available (if it needs an oil change or the car malfunctioned).

7. **Location**: 
   - Enter the location with the first letter capitalized. The available options are:
     - Sofia
     - Vienna

8. **Type**: 
   - Enter the type of car in lower case letters. They need to FULL LOWER CASE LETTERS .The available options are:
     - coupe
     - sedan
     - suv
     - kombi


## Admin and User Functions

### Admin Access
To access the admin page and manage the car listings, use the following URL:
```
/admin
```

### User Signup and Login
Users can create an account by visiting:
```
/signup
```
After signing up, they can log in by clicking the button in the top right corner, which redirects them to the login page. Once logged in, users are automatically redirected to the home page:
```
/home
```

### Car Search and Reservation
From the home page, users can search for available vehicles using the following criteria:
- Location
- Gearbox
- Type of vehicle
- Start date
- Return date
- Maximum price per day

Users can click the search button to see all available vehicles that match their specifications. They can also reserve a car. If another user searches for the same car on the same dates, it will not be available to them. However, if the dates are changed, the car will become available again.

### Important Notes
- Users must be logged in to rent cars.
- Ensure all fields are filled correctly as per the guidelines to maintain data consistency.
