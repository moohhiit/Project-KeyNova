
An AI-powered smart keyboard app for kids that detects inappropriate content typed on the keyboard and sends alerts to registered parents.
KeyNova is a child-safe typing companion that uses a backend Django server and an ML model to:
- Monitor and analyze typed content in real time.
- Detect **violent**, **sexual**, **abusive**, or **toxic** language using a transformer-based NLP model.
- Alert registered parents via SMS when inappropriate content is detected.

---

##  Project Structure

Project-KeyNova/
│
├── Application/KeyNova         # Android keyboard app (JavaScript/Kotlin)
├── KeyNovaWeb                  # Web UI for admin/parent control (React/HTML)
├── ML                          # Jupyter notebooks and training for content filtering
├── Server                      # Django backend + ML integration
│   ├── contentfilter/         # Main Django app
│   └── manage.py
├── ml_detector.ipynb          # Prototype for BERT-based content classification
├── README.md                   # Project documentation
└── .gitignore


##  Features

- 🔐 **User Registration/Login** using phone number.
- 🧠 **ML Model** for real-time inappropriate content detection.
- 🚨 **Parental Alerts** sent when toxic language is typed.
- 📊 **Web Dashboard** for reviewing flagged texts.
- 🔌 **API Integration** between mobile and server via HTTP endpoints.

---

## Technologies Used

- **Frontend**: Android (JavaScropt), Web (HTML/CSS/JS)
- **Backend**: Django REST Framework
- **Machine Learning**: HuggingFace Transformers (`DistilBERT`)
- **Database**: MongoDB Atlas
- **SMS Alerts**: Twilio API (mocked locally)

---

## 📦 API Endpoints (Django)

| Endpoint           | Method | Description                      |
|--------------------|--------|----------------------------------|
| `/api/register/`   | POST   | Register user (parent + child)   |
| `/api/login/`      | POST   | Login and get `uni_id`           |
| `/api/analyze/`    | POST   | Analyze text and send alerts     |

---

## 🔧 Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/moohiit/Project-KeyNova.git
   cd Project-KeyNova/Server/contentfilter
   ```

2. **Create virtual environment and install dependencies**  
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Run server**
   ```bash
   python manage.py runserver
   ```

4. **Test API in Thunder Client or Postman**

---

## 📓 Future Improvements

- Add dashboard with usage analytics for parents.
- Add fine-grained control over alert categories.
- Train a multilingual content detector.
- Real-time socket-based keyboard sync.

---

## 👨‍💻 Contributors

- [@moohiit](https://github.com/moohiit) – Android & UI/UX
- [@Sumitrathore] – ML Model
- [@annsshh] –  Backend Api and Testing
