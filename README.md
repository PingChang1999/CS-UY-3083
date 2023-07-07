# CS-UY-3083

## Objective
The objective of this project is to provide a realistic experinece in the design process of a relational database and corresponding applicatons that focusses on conceptual design, logical design, implementation, operation, and maintenance of a relational database.
An associated web-based application to communicate with the date database will be implemented (retrieve information, store information, etc.)

## Project Overview
The project is an online Air Ticket Reservation System.
Using this system, customers can search for flights (one way or round trip), purchase flights ticket, view their future flight status or see their past flights etc.
There will be three types of users of this system - Customers, Booking Agents, and Airline Staff (Administrator).
Booking Agents will book fligts for other Customers, can get a fixed commission.
They can view their monthly reports and get total commission.
Airline Staff will add new airplanes, create new flights, and update flight status.
In general, this will be similar to a simple air ticket reservation system.

## Project Description
* There are several airports (Airport), each consisting of a unique name and a city.
* There are several airlines (Ariline), each with a unique name. Each airline owns several airplanes. An airplane (Airplane) consists of the airline that owns it, a unique identification number within that airline, and the amount of seats on the airplane.
* Each airline operates flights (Flight), which consist of the airline operating the flight, a flight number, departure airport, departure date and time, arrival airport, arrival date and time, a base price, and the identification number of the airplane for the flight. Each flight is identifiable using flight number and departure date and time together within that airline.
* A ticket (Ticket) can be purchased for a flight by a Customer or Booking Agent (on behalf of customer), and will consist of the customer’s email address, the airline name, the flight number, sold_price (may be different from base price of the flight), payment information (card type - credit/debit, card number, name on card, expiration date), purchase date and time, and a booking_agent_ID. If a Booking Agent purchased the ticket then their booking_agent_ID will be used, and if a Customer purchased the ticket then the booking_agent_ID should be null. Each ticket will have a ticket ID number which is unique in this system.
* Anyone (including users not signed in) can see flights (future flights) based on the source airport, destination airport, source city, or destination city, departure date for one way (departure and return dates for round trip). Additionally, anyone can see the status (delayed/on time etc.) of the flight based on an airline and flight number combination and arrival or departure date.
* There are three types of users for this system: Customer, Booking Agent, and Airline Staff.

Customer: 

Each Customer has a name, email, password, address (composite attribute consisting of building_number, street, city, state), phone_number, passport_number, passport_expiration, passport_country, and date_of_birth. Each Customer’s email is unique, and they will sign into the system using their email address and password.

Customers must be logged in to purchase a flight ticket.

Customers can purchase a ticket for a flight as long as there is still room on the plane. This is based on the amount of tickets already booked for the flight and the seating capacity of the airplane assigned to the flight and customer needs to pay the associated price for that flight. Ticket price of a flight will be determined based on two factors – minimum/base price as set by the airline and additional price which will depend on demand of that flight. If 70% of the capacities is already booked/reserved for that flight, extra 20% will be added with the minimum/base price. Customer can buy tickets using either credit card or debit card. We want to store card information (card number and expiration date and name on the card but not the security code) along with purchased date, time. 

Customer will be able to see their future flights or previous flights taken for the airline they logged in.

Customer will be able to rate and comment on their previous flights taken for the airline they logged in.

Booking Agent:

The role of a Booking Agent is similar to that of a Customer. A Booking Agent’s purpose is to purchase a ticket on behalf of a Customer (with the same restrictions of seat availability as above), but that Booking Agent will receive a 10% commission from the ticket price.

A Booking Agent consists of a unique email, a password, and a booking_agent_ID. In order for a Booking Agent to sign into the system, they must enter all three of these items.

Once logged in, a Booking Agent will be able to see the amount of commission they received in the past 30 days, the average commission they received per ticket booked, and the total number of tickets they booked.

Airline Staff:

Each Airline Staff has a unique username, a password, a first name, a last name, a date of birth, may have more than one phone number, and the airline name that they work for. One Airline Staff works for one particular airline.

Airline Staff will be able to add new airplanes into the system for the airline they work for.

Airline Staff will set flight statuses in the system. 

Each Airline Staff can create new flights only for the particular airline that they work for by inserting all necessary information and will set the ticket base price for flight. They will also be able to see all ontime, future, and previous flights for the airline that they work for, as well as a list of passengers for the flights.

In addition, Airline Staff will be able to see a list of all flights a particular Customer has taken only on that particular airline.

Airline Staff will be able to see each flight’s average ratings and all the comments and ratings of that flight given by the customers.

Airline Staff will also be able to see the most frequent customer within the last year, see the amount of tickets sold each month, see the total amount of revenue earned etc.

Airline Staff can query for how many flights get delayed/on-time etc.

## Application Use Cases
* View Public Info: All users, whether logged in or not, can
    * Search for future flights based on source city/airport name, destination city/airport name, departure date for one way (departure and return dates for round trip).
    * Will be able to see the flights status based on airline name, flight number, arrival/departure date.
* Register: 3 types of user registrations (Customer, Booking Agent and Airline Staff) option via forms.
* Login: 3 types of user login (Customer, Booking Agent, and Airline Staff). Users enters their username (email address will be used as username), x, and password, y, via forms on login page. This data is sent as POST parameters to the login-authentication component, which checks whether there is a tuple in the corresponding user’s table with username=x and the password = md5(y).
    * If so, login is successful. A session is initiated with the member’s username stored as a session variable. Optionally, you can store other session variables. Control is redirected to a component that displays the user’s home page.
    * If not, login is unsuccessful. A message is displayed indicating this to the user.
    * Error message if the previous action was not successful.

Customer Use Cases - After logging in successfully a user(customer) may do any of the following use cases:
* View My Flights: Provide various ways for the user to see flights information which he/she purchased. The default should be showing for the future flights.
* Search for flights: Search for future flights (one way or round trip) based on source city/airport name, destination city/airport name, dates (departure or return).
* Purchase tickets: Customer chooses a flight and purchase ticket for this flight, providing all the needed data, via forms. You may find it easier to implement this along with a use case to search for flights.
* Give Ratings and Comment on previous flights: Customer will be able to rate and comment on their previous flights (for which he/she purchased tickets and already took that flight) for the airline they logged in.
* Track My Spending: Default view will be total amount of money spent in the past year and a bar chart showing month wise money spent for last 6 months. He/she will also have option to specify a range of dates to view total amount of money spent within that range and a bar chart showing month wise money spent within that range.
* Logout: The session is destroyed and a “goodbye” page or the login page is displayed.

Booking Agent Use Cases - After logging in successfully a booking agent may do any of the following use cases:
* View My flights: Provide various ways for the booking agents to see flights information for which he/she purchased on behalf of customers. The default should be showing for the future flights.
* Search for flights: Search for future flights (one way or round trip) based on source city/airport name, destination city/airport name, dates (departure or arrival).
* Purchase tickets: Booking agent chooses a flight and purchases tickets for other customers giving customer information and payment information, providing all the needed data, via forms. You may find it easier to implement this along with a use case to search for flights.
* View my commission: Default view will be total amount of commission received in the past 30 days and the average commission he/she received per ticket booked in the past 30 days and total number of tickets sold by him in the past 30 days. He/she will also have option to specify a range of dates to view total amount of commission received and total numbers of tickets sold.
* View Top Customers: Top 5 customers based on number of tickets bought from the booking agent in the past 6 months and top 5 customers based on amount of commission received in the last year. Show a bar chart showing each of these 5 customers in x-axis and number of tickets bought in y-axis. Show another bar chart showing each of these 5 customers in x-axis and amount commission received in yaxis.
* Logout: The session is destroyed and a “goodbye” page or the login page is displayed.

Airline Staff Use Cases - After logging in successfully an airline staff may do any of the following use cases:
* View flights: Defaults will be showing all the future flights operated by the airline he/she works for the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see all the customers of a particular flight.
* Create new flights: He or she creates a new flight, providing all the needed data, via forms. The application should prevent unauthorized users from doing this action. Defaults will be showing all the future flights operated by the airline he/she works for the next 30 days.
* Change Status of flights: He or she changes a flight status (from on-time to delayed or vice versa) via forms.
* Add airplane in the system: He or she adds a new airplane, providing all the needed data, via forms. The application should prevent unauthorized users from doing this action. In the confirmation page, she/he will be able to see all the airplanes owned by the airline he/she works for.
* Add new airport in the system: He or she adds a new airport, providing all the needed data, via forms. The application should prevent unauthorized users from doing this action.
* View flight ratings: Airline Staff will be able to see each flight’s average ratings and all the comments and ratings of that flight given by the customers.
* View all the booking agents: Top 5 booking agents based on number of tickets sales for the past month and past year. Top 5 booking agents based on the amount of commission received for the last year.
* View frequent customers: Airline Staff will also be able to see the most frequent customer within the last year. In addition, Airline Staff will be able to see a list of all flights a particular Customer has taken only on that particular airline.
* View reports: Total amounts of ticket sold based on range of dates/last year/last month etc. Month wise tickets sold in a bar chart.
* Comparison of Revenue earned: Draw a pie chart for showing total amount of revenue earned from direct sales (when customer bought tickets without using a booking agent) and total amount of revenue earned from indirect sales (when customer bought tickets using booking agents) in the last month and last year.
* View Top destinations: Find the top 3 most popular destinations for last 3 months and last year (based on tickets already sold).
* Logout: The session is destroyed and a “goodbye” page or the login page is displayed.

## Additional Requirements:
* The air ticket reservation system implementation should prevent users from doing actions they are not allowed to do. For example, system should prevent users who are not authorized to do so from adding flight information. This should be done by querying the database to check whether the user is an airline staff or not before allowing him to create the flight.
* When a user logs in, a session should be initiated; relevant session variables should be stored. When the member logs out, the session should be terminated. Each component executed after the login component should authenticate the session and retrieve the user’s pid from a stored session variable.
* Take measures to prevent cross-site scripting vulnerabilities, such as passing any text that comes from users through htmlspecialchars or some such function, before incorporating it into the html that air ticket reservation system produces.
* The user interface should be usable. For each type of users, different home pages should be implemented that only show relevant use cases for that type of users.
