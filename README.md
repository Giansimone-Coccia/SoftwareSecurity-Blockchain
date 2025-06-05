# 💊 CareChain

<p align="center">
  <img src="Logo-progetto.jpg" alt="CareChain Logo">
</p>

**CareChain** is a software solution that facilitates the management and sharing of data between patients, doctors, and healthcare professionals using blockchain technology.  
It is designed to provide a solid foundation for users to manage their operations and securely share sensitive information in a transparent way.

---

## 🚀 Features

- ✅ **Data Management**  
  Allows users to securely store and access their medical data.

- 🔐 **Secure Sharing**  
  Provides a mechanism for selective data sharing between patients, doctors, and healthcare professionals.

- 🧾 **Transparency**  
  Uses blockchain to ensure traceability and immutability of data transactions.

- 💡 **User-Friendly Interface**  
  Offers a simple and intuitive user experience to make the software easy to use.

---

## 🛠️ Technologies Used

| Technology     | Description                                                                                   |
|----------------|-----------------------------------------------------------------------------------------------|
| **Blockchain** | We use the **Ganache** blockchain to ensure the security and integrity of data.               |
| **Python**     | The backend is developed in **Python** for its flexibility and ease of development.           |
| **CLI**        | We currently support a **command-line interface (CLI)** for interacting with the software.     |

---

## 📦 Installation

> ⚠️ **Note:** It is recommended to avoid using the UnivPM network when testing the program.

### 🔽 1. Clone the repository

There are several ways to do this:

- Using `git`:
  ```bash
  git clone https://github.com/Giansimone-Coccia/SoftwareSecurity-Blockchain.git

---

### 📂 2. Navigate to the project directory

Open a terminal and navigate to the project folder:

```bash
cd SoftwareSecurity-Blockchain
````
---

### 📦 3. Install the dependencies

Install the required Python packages using:

```bash
pip install -r requirements.txt
````
---

### 🔑 4. Modify the Address and Private Key

To use the Ganache blockchain correctly:

1. Open **Ganache**.
2. Choose one of the available accounts.
3. Copy the **address** and **private key**.
4. Paste them into the `Chiavi.env` file of the project in the following fields:

```env
MY_ADDRESS="your_address"
PRIVATE_KEY="your_private_key"
````
---

### ▶️ 5. Run the Software

You can run CareChain in two ways:

- **From Visual Studio Code**  
  Open the project and run the `main.py` file.

- **From the terminal**, inside the project directory:
  ```bash
  python3 main.py
