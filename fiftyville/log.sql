-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Find description
SELECT description
FROM crime_scene_reports
WHERE year = 2023 AND month = 7 AND day = 28;

-- Check the interviews table
SELECT transcript
FROM interviews
WHERE year = 2023 AND month = 7 AND day = 28
AND transcript LIKE '%bakery%';

-- Check bakery logs for license plate (can join people table as well to find out the name of the person who owns the car)
SELECT bakery_security_logs.activity, bakery_security_logs.license_plate, people.name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year= 2023
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 15
AND bakery_security_logs.minute <= 25;

-- CHECK atm transactions on Legett Street transaction type : withdraw.  find out the account number that made the transaction and also the name of the account owner.
SELECT people.name , atm_transactions.transaction_type FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.year = 2023
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_location = 'Leggett Street'
AND atm_transactions.transaction_type = 'withdraw';

-- Check calls where duration was less than a minute
SELECT caller , caller_name ,receiver, receiver_name
FROM phone_calls
WHERE year = 2023
AND month = 7
AND day = 28
AND duration < 60;

-- Update table for caller
UPDATE phone_calls
SET caller_name = people.name
FROM people
WHERE phone_calls.caller = people.phone_number;

--Update table for receiver
UPDATE phone_calls
SET receiver_name = people.name
FROM people
WHERE phone_calls.receiver = people.phone_number;

-- Check flights table
SELECT *
FROM flights
WHERE year = 2023
AND month = 7
AND day = 29
ORDER BY hour ASC;

-- first flight id 36 destination id = 4 
SELECT *
FROM airports
WHERE id = 4;


-- Check who also went to New york from the passengers table
SELECT flights.destination_airport_id, name , phone_number, license_plate from people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON flights.id = passengers.flight_id
WHERE flights.id = 36
ORDER BY flights.hour ASC;

--find the theif
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON flights.id = passengers.flight_id
WHERE (flights.year = 2023 AND flights.month = 7 AND flights.day = 29
AND flights.id = 36)
AND name IN
(SELECT phone_calls.caller_name FROM phone_calls
WHERE year = 2023
AND month = 7
AND day = 28
AND duration < 60)
AND name in
(SELECT phone_calls.caller_name FROM phone_calls
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.year = 2023
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_location = 'Leggett Street'
AND atm_transactions.transaction_type = 'withdraw')
AND name in
(SELECT people.name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year= 2023
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 15
AND bakery_security_logs.minute <= 25);

-- Theif is Buce check call logs for to get the accomplice
SELECT caller , caller_name ,receiver, receiver_name
FROM phone_calls
WHERE year = 2023
AND month = 7
AND day = 28
AND duration < 60;
-- And the accomplice is robin




