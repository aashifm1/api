# Secure Mini Payment API

> Done by Aashif M (Intern Security Analyst Role)

Problem Statement: You are required to design and implement a Secure Mini Payment Backend Service. This service simulates a simplified payment system where users can register, log in, perform payments, and view transaction history.

---

## Tech Stack Used

- Python Flask
- REST API
- Supabase Database

---

## Tools Used

- Postman (for testing)

---

## Endpoints

The four endpoints implemented in the code

```bash
/register --> user registration
/login --> user login
/payment --> payment processing
/transactions --> transaction history
```

---

## My approach

- No duplication in registration as it checks the database for user email and password exist or not.
- Implemented payment authentication & session security on login
- Proper input validation is set 
- No payment can process without the autorization token which generates after successful login to make the payment secure.
- Rate limiting is implemented as more invalid login attempts (>5) will rate limited as 429.
- Can able to view the transaction history with authorization only as bearer token generated.

---

## DB Approach

- In supabase database, four tables are created. They are users, sessions, transactions, and attempts.
- The database table and output images are attached.

---