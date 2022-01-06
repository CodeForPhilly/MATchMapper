# How to Compile Frontend
1. Install NodeJS with [a package manager](https://nodejs.org/en/download/package-manager) or using [the installer](https://nodejs.org/en/download/)

2. Install dependencies from command line by running `npm install` from the `/react-frontend` directory. This may occasionally fail midway through. Usually, this will happen because of a permissions issue, in which case, you may need to run this command as the superuser using `sudo npm install` (on MacOS or Linux) or as the administrator (on Windows).

3. From the `/react-frontend` directory, run `npm run build`. It may ask you if you're sure you want to replace some files; say yes. This will compile the React code to plain HTML and place it in the `/database/bupehandler/templates` directory for Django to access.