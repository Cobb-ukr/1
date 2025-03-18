# Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```
MONGO_URI=mongodb+srv://dentist:host@cluster0.l6uus.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
JWT_SECRET=your_jwt_secret
EMAIL=
EMAIL_PASSWORD=
RECIPIENT_EMAIL=
PORT=5000
```

---

## Running the Main Website

### Steps:

1. Run the server:
   ```sh
   node server.js
   ```

2. Open the website in your browser:
   ```
   http://localhost:5000
   ```

---

## Running the Admin Page

### Steps:

1. Create new CLI/terminal instance and navigate to the `admin` directory:
   ```sh
   cd admin
   ```

2. Remove the existing virtual environment (if any):
   ```sh
   Remove-Item -Recurse -Force venv
   ```

3. Create a new virtual environment:
   ```sh
   python -m venv venv
   ```

4. Set the execution policy (required for Windows users):
   ```sh
   Set-ExecutionPolicy Unrestricted -Scope Process
   ```

5. Activate the virtual environment:
   ```sh
   .\venv\Scripts\activate
   ```

6. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

7. Run the application:
   ```sh
   python app.py
   ```

8. Open the admin panel in your browser:
   ```
   http://127.0.0.1:5000
   ```

