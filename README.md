# smartcashier-sqlite
CRUD &amp; Transaction System

---

## Project Overview

SMARTCASHIER ID is a Command Line Interface (CLI) based cashier system developed using Python and SQLite as the database engine

This project demonstrates:
- Authentication system with validation
- Relational database implementation
- Inventory CRUD management
- Transaction processing engine
- Smart discount strategy
- Tax calculation (11% VAT)
- Invoice generation
- Transaction history tracking

The system follows a modular procedural structure with clear separation of business logic.

---

## Flowchart
<img width="2351" height="1858" alt="Flowchart SMARTCHASIER" src="https://github.com/user-attachments/assets/8db5e99e-e856-404d-af19-6974fe4856bc" />

---

## Database Design

Database Name:
'''
tugas_project.db
'''

---

### Tables

- users : Stores user account data
- alamat : Stores user address information
- barang : Stores inventory items
- transaksi : Stores transaction headers
- detail_transaksi : Store transaction item details

---

### Relationship Model

- One User → Many Transactions  
- One Transaction → Many Transaction Details  
- Transaction Details → Reference Inventory Items  

Logical relational design implemented via SQLite structure.

---

## Core Features

### Authentication Module
- Strong password validation (uppercase, lowercase, number, special character)
- Email format validation
- Maximum 5 login attempts
- Unique UserID enforcement

---

### Inventory Management
- Create new items
- View all items
- Search items by code or name
- Update specific fields or full record
- Delete items with confirmation
- Duplicate prevention system

---

### Transaction Processing
- Multi-item cart system
- Stock validation before checkout
- Automatic stock deduction
- Persistent transaction storage
- Database rollback on error

---

### Smart Discount Strategy

Dual Discount Logic:

**Quantity-Based Discount**
- ≥ 5 items → 10%
- ≥ 10 items → 15%

**Price-Based Discount**
- ≥ 200,000 → 10%
- ≥ 500,000 → 20%

The system automatically selects the highest discount.

---

### Invoice Generator
- Timestamped transaction record
- Detailed item breakdown
- Subtotal calculation
- Discount application
- 11% VAT calculation
- Grand total output

---

### Transaction History
- View all past transactions
- Sorted by latest date
- View detailed transaction by ID

---

## Business Logic

### VAT Configuration

```
VAT = 11%
```

---

### Transaction Flow

1. Select items
2. Validate stock
3. Calculate subtotal
4. Apply highest discount
5. Apply VAT
6. Store transaction in database
7. Update inventory stock
8. Generate invoice

---

## Data Integrity & Controls

- Input validation
- Duplicate prevention
- Strict numeric validation
- Controlled update & delete confirmation
- Transaction rollback mechanism
- Email format verification

---

Technical Highlights

✔ Relational database structure  
✔ Persistent transaction storage  
✔ Automatic stock management  
✔ Dual discount strategy engine  
✔ Clean modular function design  
✔ Structured CLI interface  

---

## Author

Risky Adipratama  

CRUD & Transaction Processing Project

---

## Future Improvements

- Refactor into OOP architecture
- Implement foreign key constraints (PRAGMA)
- Upgrade to MySQL backend
- Add role-based access (Admin/User)
- Develop GUI version (Tkinter)
- Convert into Web App (Flask / FastAPI)
- Add PDF invoice export
- Add reporting dashboard

---

Feel free to fork, improve, and expand this project.
