# 🐾 Nexus Pet Portal 🐾

Welcome to Nexus Pet Portal, your ultimate destination for managing animals in the shelter and finding them loving homes! 🏠🐶🐱

Nexus Pet Portal is a heartwarming Animal Shelter Management System designed to simplify the process of caring for and finding homes for shelter animals. Our system provides a seamless platform for shelter administrators to manage animals, update their adoption statuses, and maintain records efficiently.

# Table of Contents

- [Nexus Pet Portal 🐾](#-nexus-pet-portal-)
- [Features 🌟](#features-)
- [Installation 🚀](#installation-)
- [Setting Up MongoDB 🍃](#setting-up-mongodb-)
- [First-Time Login ⚙️](#first-time-login-)
- [System Requirements 💻](#system-requirements-)
- [Future Plans 🚀](#future-plans-)
- [Contributing 💖](#contributing-)
- [License 📝](#license-)


## Features 🌟

- **Secure Login**: 
- **Animal Management**: Add new animals to the shelter, update their information, and change adoption statuses with ease.
- **Adoption Records**: Keep track of animals' adoption statuses and manage adoption processes seamlessly.
- **Administrative Dashboard**: Access additional features for managing users, animals, and shelter operations effectively.

## Installation 🚀

1. **Clone the Repository**:

    ```
    git clone https://github.com/tylerlight071/Nexus-Pet-Portal.git
    ```

2. **Navigate to the Repository**:

    ```
    cd Nexus_Pet_Portal
    ```

3. **Install the required dependencies**
    ```
    pip install -r requirements.txt
    ```
    
4. **Run the Application**:

    ```
    python N_P_P.py
    ```  

**or download the latest release**

1. Go to **releases**
2. Click on the latest version
3. Download the exe file or the entire zip folder
4. Extract the zip file if downloaded
5. Run the exe file

## Setting Up MongoDB 🍃

To use Nexus Pet Portal, you need to have a MongoDB database. Here's how you can set it up:

1. **Create a MongoDB Account**:

   - Visit the [MongoDB website](https://www.mongodb.com/) and create an account.

2. **Create a New Project**:

   - After logging in, create a new project.
   - Give your project a name and create it.

3. **Create a New Cluster**:

   - In your project, create a deployment by clicking the '+ Create' button.
   - Choose a provider and a region.
   - Choose a cluster tier. The free tier, M0 Sandbox, is sufficient for this project but if you need/want to use another then you are free to.
   - Give your cluster a name (should you wish to) and create it.

4. **Create a Database User**:

    - In the Security Quickstart, you are prompted to authenticate your connection.
    - Click on 'Username and Password' and enter your username and click 'Autogenerate Secure Password'.
    - (They may be prefilled by MongoDB using your Cloud Registration Info in which use that)
    - Make sure you make a note of your password as you will need this in just a moment.
    - Click 'Create User' and scroll down to the 'IP Access List' and click, 'Add My Current IP Address'.
    - (Again, if this is prefilled, you can leave it.)
    - Then click 'Finish and Close'

5. **Get Your MongoDB URI**:

   - In your cluster, click on the CONNECT button.
   - Choose 'Drivers' and under 'Driver' choose Python, and use the latest version.
   - Ignore the 'Install your driver' and simply copy the provided connection string (MongoDB URI).

Remember to replace `<password>` in the MongoDB URI with the password of the database user you created.

You can now use this MongoDB URI to connect to your MongoDB database from Nexus Pet Portal! Everything else is automatically set up so you don't need to do anything past that point.

## First-Time Login ⚙️

- To access the system for the first time, use the following default credentials:
  - Username: `ADMIN`
  - Password: `ADMIN`

(You will set the password to your own on first login)

## System Requirements 💻

Nexus Pet Portal is developed using Python. To run this application from the source code, you need:

- Python 3.12 or higher
- pip (Python Package Installer)

## Future Plans 🚀

We're constantly working to improve Nexus Pet Portal and add new features. Here are some of the updates we're planning:

- User Schedules / Calendar to list upcoming events like appointments
- GUI instead of terminal-based
- Integrated Local Host Website 

Stay tuned for these exciting updates and more!

## Contributing 💖

We welcome contributions from compassionate individuals who share our mission! If you'd like to contribute to Nexus Pet Portal, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a new Pull Request filled with love and dedication!

## Issues ⚠️

Please submit any issues via the issues portal in this repo or email me at:
tylerlightwood071@gmail.com

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
