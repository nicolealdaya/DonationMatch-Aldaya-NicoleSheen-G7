DonationMatch

DonationMatch is a web-based donation management system that connects donors with organizations that need donations. It helps users share available items, submit requests, and discover potential donation opportunities.

Core Features

Donation and Request Management

Donors can create, view, edit, and delete donation posts.

Organizations can create, view, edit, and delete donation requests.

Users can manage their own posts through the My Posts page.

Users can explore available donations and requests.

Search and category filtering are available.

Role-based access and ownership protection are implemented.

Dashboard and Analytics

Unified dashboard for donors and organizations.

Donation and request statistics.

Possible donation matches based on categories.

Latest matching opportunities.

Standard Features

User registration and login.

Donor and organization accounts.

Role-based dashboards.

User profile management.

Logout functionality.

Technologies Used

Python 3.15.2

Django 6.1.3

PostgreSQL (Supabase)

HTML

CSS

JavaScript

psycopg

python-dotenv

Requirements

Python 3.15.2

Git

Supabase PostgreSQL database

pip

Installation and Setup

1\. Clone the Repository

git clone https://github.com/nicolealdaya/DonationMatch-Aldaya-NicoleSheen-G7.git

cd DonationMatch-Aldaya-NicoleSheen-G7

2\. Create a Virtual Environment

python -m venv venv

3\. Activate the Virtual Environment

.\\venv\\Scripts\\Activate

4\. Install Dependencies

pip install -r requirements.txt

5\. Configure Environment Variables

Create a .env file in the project root directory.

Add the following variables using your own credentials:

SECRET\_KEY=your-secret-key

DEBUG=True

DB\_NAME=your-database-name

DB\_USER=your-database-user

DB\_PASSWORD=your-database-password

DB\_HOST=your-database-host

DB\_PORT=5432

Use your actual Supabase PostgreSQL credentials. Never upload your .env file or expose your database password.

6\. Apply Database Migrations

python manage.py migrate

7\. Run the Development Server

python manage.py runserver

Application Pages

After starting the development server, access the following pages:

Login: http://127.0.0.1:8000/login/

Register: http://127.0.0.1:8000/register/

Dashboard: http://127.0.0.1:8000/dashboard/

Explore: http://127.0.0.1:8000/explore/

Create Post: http://127.0.0.1:8000/posts/create/

My Posts: http://127.0.0.1:8000/posts/mine/

Profile: http://127.0.0.1:8000/profile/

Application URL: http://127.0.0.1:8000/

Database

DonationMatch uses Supabase PostgreSQL for database storage. Database credentials are configured through environment variables in the .env file.

Security

Environment variables are stored in .env.

.env is excluded from Git using .gitignore.

Users are restricted to managing their own donation posts and requests.

Project

DonationMatch is developed as an academic project for Information Management 2.

