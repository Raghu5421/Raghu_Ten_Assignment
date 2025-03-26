

A Django REST framework-based API for managing inventory, member bookings, and cancellations. This project allows members to book items from the inventory with booking limits and cancellation capabilities.

---

## 🚀 Features

- ✅ Book items from the inventory.
- ✅ Cancel bookings using a booking reference.
- ✅ Limit each member to **MAX_BOOKINGS = 2**.
- ✅ Prevent overbooking if inventory is depleted.
- ✅ Upload inventory and member data via CSV files.
- ✅ RESTful endpoints for CRUD operations.

---

## ⚙️ Tech Stack

- **Backend:** Python, Django REST Framework  
- **Database:** PostgreSQL/MySQL (configurable in `settings.py`)  
- **Libraries:** Pandas (CSV handling), UUID (booking reference)  
- **Tools:** Git, Django Admin  

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone <repository-url>
cd inventory-management
```

### 2️⃣ Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate      # For Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a superuser
```bash
python manage.py createsuperuser
```

### 6️⃣ Run the server
```bash
python manage.py runserver
```
API will be available at:  
`http://127.0.0.1:8000`

---

## ⚡ API Endpoints

### 🏠 Home
- `GET /`
- Displays available API endpoints.

### 🔥 Booking Endpoints

#### ➡️ Book an item
- `POST /book/`
- **Payload:**
```json
{
    "member_id": 1,
    "inventory_id": 3
}
```
- **Response:**
```json
{
    "message": "Booking successful",
    "booking_reference": "b68d59a0-1234-5678-9101-abcdef123456"
}
```

#### 🔥 Cancel a booking
- `POST /cancel_booking/`
- **Payload:**
```json
{
    "reference": "b68d59a0-1234-5678-9101-abcdef123456"
}
```
- **Response:**
```json
{
    "message": "Booking cancelled successfully"
}
```



### 📑 CSV Upload Endpoints
- `POST /upload-inventory/` → Upload inventory CSV  
- `POST /upload-members/` → Upload member CSV  

---

## ✅ Database Migrations
If you make any changes to the models, run:
```bash
python manage.py makemigrations
python manage.py migrate
```

---


## 🎯 Future Improvements
- ✅ Add pagination and filtering for large datasets.  
- ✅ Implement JWT authentication for secure access.  
- ✅ Use Redis caching to improve performance.  

✅ Enjoy using the Inventory Management API!
