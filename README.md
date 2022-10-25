# Application for interacting with a recording studio

---

![Gif](https://github.com/Vya4eslavSeleznev/MusicalRoom2/blob/master/docs/musicalRoom.gif)

---

The main purpose of this application is to enable the client to book a music hall. There are several roles: client and administrator. The administrator can easily apply the customer's booking and add various music instruments and rooms.

### Database:

![DB](/docs/db.png)

The main table in the schema is Reservation, which stores all user reservations. It is connected to the Customer table by a many-to-one relationship. User data is stored in encrypted form. Reservation is also connected by a many-to-one relationship with the Room table in which the available rooms are stored. The Room table is connected by a many-to-many relationship with the Instrument table.  
The web server was developed using Java Spring.

---

### Model-View-Presenter:

![MVP](/docs/mvp.png)

The MVP design pattern was used. Moreover, Java was used, as well as a Retrofit  framework  for interacting with the server.

---

### Login page:

![Login page](/docs/startWindow.png)

### User account:

- After successful authorization in the system, the user is greeted by the main page:

![Main page](/docs/userHome.png)

- On the next tab, which is called "Equipment", the user can view the rooms. You can also click on them and see the instruments that are in the music room:

![Equipment page1](/docs/userEquipment.png)

![Equipment page2](/docs/instrumentInRoom.png)

- On the next tab, which is called "Profile", the user can view and edit their personal data. In addition, it is possible to view the booked rooms:

![Profile page1](/docs/userProfile.png)

![Profile page2](/docs/userReservations.png)

- On the last tab, which is called "Reserve", the user can reserve a music room:

![Reserve page1](/docs/userReserve.png)

![Reserve page2](/docs/userReserve2.png)

---

### Administrator account:

- On the first tab of the administrator there is an opportunity to confirm or reject the booked rooms:

![Confirmation page](/docs/adminConfirmation.png)

- On the tab which is called "Room" you can add or view all available rooms:

![Room page1](/docs/adminRoom.png)

![Room page2](/docs/adminAllRooms.png)

- You can do the same with the instruments:

![Instrument page1](/docs/adminInstrument.png)

![Instrument page2](/docs/adminAllInstruments.png)

- On the last page you can add some instruments to the rooms. And also view all the instruments in the rooms:

![RoomsInstrument page1](/docs/adminRoomsInstrument.png)

![RoomsInstrument page2](/docs/adminEquipment.png)


















