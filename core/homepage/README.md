# Homepage

Homepage is a modern, fast, and secure application dashboard. It is highly customizable and can be configured using YAML files or Docker label discovery. The dashboard has integrations for over 100 services and is translated into multiple languages. It is a fully static and proxied application.

[Homepage Website](https://gethomepage.dev/)

## How to start

1.  Create a `.env` file based on the `.env.example` file.
2.  Set the `PATH_TO_CONFIG` variable in the `.env` file to the directory where you want to store the configuration files.
3.  Run `docker-compose up -d` to start the application.
4.  The application will be available at [http://localhost:3001](http://localhost:3001).

## Setup

After starting the application, you can configure it by editing the YAML files in the `${PATH_TO_CONFIG}` directory. The documentation for the configuration can be found on the [Homepage website](https://gethomepage.dev/en/configs/).
