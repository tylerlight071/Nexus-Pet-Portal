# 🐾 FurEver Friends 🐾

Welcome to FurEver Friends, your ultimate destination for managing animals in the shelter and finding them loving homes! 🏠🐶🐱

FurEver Friends is a heartwarming Animal Shelter Management System designed to simplify the process of caring for and finding homes for shelter animals. Our system provides a seamless platform for shelter administrators to manage animals, update their adoption statuses, and maintain records efficiently.

# Table of Contents

- [FurEver Friends 🐾](#-furever-friends-)
- [Features 🌟](#features-)
- [Installation 🚀](#installation-)
- [Setting Up MongoDB 🍃](#setting-up-mongodb-)
- [First-Time Login ⚙️](#first-time-login-)
- [System Requirements 💻](#system-requirements-)
- [Future Plans 🚀](#future-plans-)
- [Contributing 💖](#contributing-)
- [License 📝](#license-)


## Features 🌟

- **Secure Login**: Administrators can log in securely with the username `ADMIN` and password `ADMIN` on first start to access the system.
- **Animal Management**: Add new animals to the shelter, update their information, and change adoption statuses with ease.
- **Adoption Records**: Keep track of animals' adoption statuses and manage adoption processes seamlessly.
- **Administrative Dashboard**: Access additional features for managing users, animals, and shelter operations effectively.

## Installation 🚀

1. **Clone the Repository**:

    ```
    git clone https://github.com/tylerlight071/FurEver-Friends.git
    ```

2. **Navigate to the Repository**:

    ```
    cd FurEver_Friends
    ```

3. **Install the required dependancies**
    '''
    pip install -r requirements.txt
    '''
    
4. **Run the Application**:

    ```
    python FurEver_Friends.py
    ```

## Setting Up MongoDB 🍃

To use FurEver Friends, you need to have a MongoDB database. Here's how you can set it up:

1. **Create a MongoDB Account**:

   - Visit the [MongoDB website](https://www.mongodb.com/) and create an account.

2. **Create a New Project**:

   - After logging in, create a new project.
   - Give your project a name and create it.

3. **Create a New Cluster**:

   - In your project, create a new cluster.
   - Choose a provider and a region.
   - Choose a cluster tier. The free tier, M0 Sandbox, is sufficient for this project.
   - Give your cluster a name and create it.

4. **Create a Database User**:

   - In the Database Access tab, add a new database user.
   - Choose a username and a password. Remember these credentials as you'll need them to connect to your database.

5. **Get Your MongoDB URI**:

   - In your cluster, click on the CONNECT button.
   - Choose "Connect your application".
   - Copy the provided connection string (MongoDB URI).

Remember to replace `<password>` in the MongoDB URI with the password of the database user you created.

You can now use this MongoDB URI to connect to your MongoDB database from FurEver Friends! Everything else is automatically set up so you don't need to do anything past that point.

## First-Time Login ⚙️

- To access the system for the first time, use the following credentials:
  - Username: `ADMIN`
  - Password: `ADMIN`

## System Requirements 💻

FurEver Friends is developed using Python. To run this application from the source code, you need:

- Python 3.12 or higher
- pip (Python Package Installer)

## Future Plans 🚀

We're constantly working to improve FurEver Friends and add new features. Here are some of the updates we're planning:

- Animal medical records
- User schedule for hours and events
- Notifications in app
- Website intergration

Stay tuned for these exciting updates and more!

## Contributing 💖

We welcome contributions from compassionate individuals who share our mission! If you'd like to contribute to FurEver Friends, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a new Pull Request filled with love and dedication!


## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Together, let's make a difference in the lives of shelter animals and help them find their FurEver homes! 🐾✨
