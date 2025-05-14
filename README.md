# 🌱 OneEarthFormWEB - Waste Management System

**OneEarthFormWEB** is a Django-based Waste Management System aimed at promoting sustainability by enabling users to **buy and sell organic products and manures**. It provides a user-friendly interface for buyers and sellers, along with an admin panel for managing users, orders, and products. The platform integrates with **Twilio** to send SMS alerts regarding waste collection schedules.

---

## 🚀 Features

### 👥 For Buyers
- Browse and purchase organic products and manures.
- View product details (price, stock, description).
- Place orders with delivery and payment options.
- Receive SMS notifications when an order is placed.

### 🛒 For Sellers
- List organic products and manures for sale.
- Manage inventory and pricing.
- Receive SMS notifications about waste collection schedules.

### 🔧 Admin Panel
- Manage buyers, sellers, orders, and product listings.
- Send SMS updates to sellers via Twilio.
- Filter/search orders by date, product type, and payment status.

### 📲 Twilio Integration
- Automatically send SMS notifications to sellers.
- **Example SMS:**
OneEarthFarm - Dear [Seller Name], we are collecting your waste on [Date and Time].



---

## 🛠️ Technologies Used

### Backend
- **Django**: Python web framework.
- **Django ORM**: For database operations.

### Frontend
- **HTML/CSS/JavaScript**: Basic UI structure and behavior.
- **Bootstrap**: For responsive design.

### Third-Party Libraries
- **Twilio API**: For sending SMS messages.

---

## ⚙️ How to Run the Project

### ✅ Prerequisites
- Python 3.x  
- Django 4.x  
- A Twilio account (for SMS features)

### 🔧 Setup Instructions

1. **Clone the repository**
 ```bash
 git clone https://github.com/Teju-ks/OneEarthFormWEB.git
 cd OneEarthFormWEB
```
2.**Install dependencies**

```bash
pip install -r requirements.txt
```
3.**Set up the database***

```bash
python manage.py makemigrations
python manage.py migrate
```

4.**Create a superuser**

```bash
python manage.py createsuperuser
```
5.**Replace the twilio ids**
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```
6.**Run the development server**

```bash
python manage.py runserver
```
7.**Access the app**

```
Frontend: http://127.0.0.1:8000/
Admin Panel: http://127.0.0.1:8000/admin/
```

## 📁 Project Structure
```
waste_management/
├── landing/
│   ├── admin.py
│   ├── models.py
│   ├── sms_service.py
│   ├── templates/
│   │   └── landing/
│   │       ├── index.html
│   │       ├── organic_manures.html
│   │       ├── organic_products.html
│   │       ├── buynow.html
│   │       ├── signup.html
│   │       ├── login.html
│   │       ├── success.html
│   ├── views.py
├── waste_management/
│   ├── settings.py
│   ├── urls.py
├── manage.py
├── .env
 
```


### 🌱 Future Enhancements
Integrate payment gateway for online payments.

Add dashboards for buyers and sellers.

Include advanced analytics for waste tracking.

Integrate OneEarthForm, an ML-based nutrient predictor and crop recommender.
