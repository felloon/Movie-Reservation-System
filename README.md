# Movie Reservation System
## Overview
This backend system for a movie reservation service. The service will allow users to sign up, log in, browse movies, reserve seats for specific showtimes, and manage their reservations. The system will feature user authentication, movie and showtime management, seat reservation functionality, and reporting on reservations.

# Features
1. User Authentication
    * Sign-Up and Login: Users can create accounts and log in to access the system.
    * Admins: Admins can performs all administrative operations.
2. Movie Menegement (Admins only)
    * Admins can add, update and delete movies
    * Movie have:
        - Title;
        - Description;
        - Poster image;
        - Genre;
        - Rating.
    * Movie also have showtimes
3. Reservation Management
    * Users Operations:
        - Get movies and their showtimes for a specific date;
        - Reserve seats for a showtime, see the available seats, and select the seats they want;
        - See their reservations and cancel them (only upcoming ones).
    * Admins Operations:
        - Can see all reservations, capacity and revenue.

# Requirements
* Python v3.13+
* FastAPI v0.129.0+
* Database: Postgres