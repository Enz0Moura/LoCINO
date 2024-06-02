# LoCINO Project

This project consists of two main modules: a Python module for message structuring and a C++ module for sending messages via the physical LoRa network.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
  - [Python Module](#python-module)
  - [C++ Module](#c-module)
- [Installation](#installation)
  - [Python Module Installation](#python-module-installation)
  - [C++ Module Installation](#c-module-installation)
- [Usage](#usage)
  - [C++ Module](#c-module-1)
  - [Python Module](#python-module-1)
  

## Overview

The LoCINO project allows the creation and sending of structured messages via the LoRa network. It is divided into two main modules:
1. **Python Module**: Responsible for creating and structuring messages.
2. **C++ Module**: Responsible for sending the messages via the LoRa network.

## Requirements

### Python Module 
- Python 3.x
- Libraries: `pyserial`, `construct`, `pydantic`

### C++ Module
- Arduino IDE
- Library: `RH_RF95`
- `LoRaLibrary` (included in the repository)

## Installation

### Python Module

1. Clone the repository:
   ```sh
   git clone https://github.com/Enz0Moura/LoCINO.git
   cd LoCINO/PYBackEnd
2. Create a virtual environment and install the dependencies:
    ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt

### C++ Module Installation
1. Add the LoRaLibrary:

    - In the cloned repository, navigate to the LoRaLibrary directory.
    - Copy the LoRaLibrary folder to the Arduino IDE libraries directory. Typically, this directory is located at:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt

2. Install the RH_RF95 Library:

    - Open the Arduino IDE.
    - Go to Sketch > Include Library > Manage Libraries.
    - Search for RH_RF95 and install it.
3. Upload the transmitter.ino and receiver.ino files to your Arduinos with the LoRa module.

# Usage
### C++ Module
- The C++ module runs on the Arduino to send the structured messages via the LoRa network.

### Python Module
- The Python module is used to structure messages that will be sent via LoRa.


