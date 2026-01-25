-- agents
CREATE TABLE agents (
    agent_id varchar2(50) PRIMARY KEY,
    name varchar2(100),
    branch varchar2(100),
    join_date date,
    commission_rate number(5, 2)
);

-- customers
CREATE TABLE customers (
    customer_id varchar2(50) PRIMARY KEY,
    name varchar2(100),
    age number(3),
    gender varchar2(10),
    city varchar2(100),
    phone varchar2(20),
    email varchar2(100)
);

-- policies
CREATE TABLE policies (
    policy_id varchar2(50) PRIMARY KEY,
    customer_id varchar2(50),
    policy_type varchar2(50),
    start_date date,
    end_date date,
    sum_insured number(15, 2),
    premium number(15, 2),
    STATUS varchar2(20),
    agent_id varchar2(50)
);

-- claims
CREATE TABLE claims (
    claim_id varchar2(50) PRIMARY KEY,
    policy_id varchar2(50),
    claim_date date,
    claim_amount number(15, 2),
    approved_amount number(15, 2),
    STATUS varchar2(20),
    hospital_or_garage varchar2(200)
);

-- payments
CREATE TABLE payments (
    payment_id varchar2(50) PRIMARY KEY,
    policy_id varchar2(50),
    payment_date date,
    amount number(15, 2),
    payment_mode varchar2(50),
    STATUS varchar2(20)
);
