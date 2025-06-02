# 🦷 SignalWire Dental Office Management System

A comprehensive web-based dental office management system powered by **SignalWire** for voice, SMS, and MMS communications.

## 🚀 Features

- **Patient Management**: Complete patient records and profiles
- **Treatment History**: Track all dental procedures and notes
- **Billing System**: 6-digit bill numbers, insurance tracking, and payment processing
- **Mobile Responsive**: Full mobile interface with 51x40px logo sizing
- **SMS/MMS Integration**: Send bills, reminders, and notifications via SignalWire
- **Multi-Factor Authentication**: SMS-based verification for secure access
- **Voice AI Integration**: SWAIG endpoints for phone-based interactions
- **PDF Generation**: Bill generation and document management

## 📋 Requirements

- Python 3.8+
- SignalWire Account (for SMS/MMS/Voice features)
- Modern web browser

## 🛠️ Installation & Setup

You have **two options** for setting up the SignalWire Dental Office Management System:

### Option 1: Web-Based Setup (Recommended)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Application**
   ```bash
   python app.py
   ```

3. **Complete Setup in Browser**
   - Visit: http://127.0.0.1:8080
   - The system will automatically redirect to the setup page
   - Fill in all required configuration fields
   - Click "Save Configuration" to create your `.env` file
   - Application will restart automatically

### Option 2: Command-Line Setup

1. **Run the Setup Script**
   ```bash
   python setup.py
   ```
   This will:
   - Check Python version compatibility
   - Install all dependencies
   - Guide you through configuration
   - Create the `.env` file
   - Initialize the database

2. **Start the Application**
   ```bash
   python app.py
   ```

### Quick Start Scripts

**Windows:**
```cmd
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

## 🔧 Environment Configuration

Create a `.env` file in the project root with your SignalWire credentials:

```bash
# SignalWire Configuration
SIGNALWIRE_PROJECT_ID=your_project_id
SIGNALWIRE_TOKEN=your_auth_token
SIGNALWIRE_SPACE=your_space_subdomain
FROM_NUMBER=+1234567890

# Application Configuration
SECRET_KEY=your_secret_key_here
PROJECT_URL=http://localhost:8080
HTTP_USERNAME=your_api_username
HTTP_PASSWORD=your_api_password

# Optional: Call-to-Call API
C2C_API_KEY=your_c2c_api_key
C2C_ADDRESS=your_c2c_address
```

**Reference**: See `environment_variables.txt` for detailed descriptions of each variable.

### 3. Database Setup

The application will automatically create the SQLite database on first run. If you need to manually initialize:

```bash
python -c "
from app import app, init_db_if_needed
with app.app_context():
    init_db_if_needed()
"
```

**Alternative initialization methods:**

```bash
# Using the dedicated initialization script
python init_db.py

# Add sample test data for development/testing
python init_test_data.py
```

### 4. Add Bill Numbers (For Existing Databases)

If upgrading from an older version without bill numbers:

```bash
sqlite3 dental_office.db < migrate_add_bill_number.sql
```

## 🚀 Running the Application

```bash
python app.py
```

The application will be available at:
- **Local**: http://127.0.0.1:8080
- **Network**: http://[your-ip]:8080

## 👥 Default Login Credentials

**Patient Account:**
- Email: `jane.doe@email.com`
- Password: `patient123`
- Patient ID: `8675309`

**Dentist Account:**
- Email: `dr.smith@dentaloffice.com`
- Password: `dentist123`

## 🎯 Key Features

### Mobile Responsive Design
- **Logo Sizing**: Exactly 51x40 pixels on mobile as specified
- **Full-Width Usage**: No padding/margin issues on mobile
- **Dual Hamburger Menus**: Left and right navigation options
- **Badge Containment**: IDs display completely without truncation

### SignalWire Integration
- **Fixed URL Construction**: Properly handles both full URLs and subdomains
- **MMS Image Support**: 30-second delayed cleanup for image delivery
- **SMS Notifications**: Bill summaries, appointment reminders
- **Voice AI**: 13 SWAIG endpoints for phone interactions

### Bill Management
- **6-Digit Bill Numbers**: User-friendly bill references (e.g., 536394)
- **Proper Display**: Shows actual bill numbers instead of database IDs
- **MMS Bill Images**: Generate and send bill images via MMS
- **Payment Tracking**: Complete payment history and balances

## 📱 Mobile Features

- **Responsive Navigation**: Works on all screen sizes
- **Touch-Optimized**: 44px minimum touch targets
- **Mobile Header**: Custom header with hamburger menu
- **Sidebar Overlay**: Smooth mobile navigation experience

## 🔐 Security Features

- **MFA Authentication**: SMS-based two-factor authentication
- **Challenge Tokens**: Secure session management
- **Password Hashing**: SHA-256 with salt
- **Session Management**: Secure user sessions

## 🔧 Configuration Notes

1. **SignalWire Space**: Use only the subdomain (e.g., `myspace` not `https://myspace.signalwire.com`)
2. **Phone Numbers**: Must be in E.164 format (e.g., `+14155551234`)
3. **Project URL**: Should match your server's public URL for webhooks
4. **HTTP Auth**: Used for SWAIG API endpoints
5. **First Run**: Application automatically redirects to setup page if no `.env` file exists

## 🗂️ File Structure

```
final_project/
├── app.py                       # Main Flask application
├── mfa_util.py                 # Multi-factor authentication utilities
├── schema.sql                  # Database schema
├── migrate_add_bill_number.sql # Bill number migration
├── environment_variables.txt   # Environment variable reference
├── requirements.txt            # Python dependencies
├── setup.py                    # Command-line setup script
├── start.bat                   # Windows startup script
├── start.sh                    # Linux/Mac startup script
├── README.md                   # This file
├── init_db.py                  # Database initialization script
├── init_test_data.py           # Test data population script
├── templates/                  # HTML templates
│   ├── base.html              # Base template with mobile support
│   ├── first_run.html         # Web-based setup interface
│   ├── sidebar_*.html         # Navigation sidebars
│   ├── top_menu.html          # Top navigation
│   └── *.html                 # Page templates
└── static/                    # Static assets
    ├── css/                   # Stylesheets and images
    └── js/                    # JavaScript files
```

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm dental_office.db
python app.py
```

### SignalWire Connection Issues
- Verify credentials in `.env` file
- Check space name format (subdomain only)
- Ensure phone number is in E.164 format

### Mobile Display Issues
- Hard refresh browser (Ctrl+F5)
- Check CSS cache busting parameter
- Verify viewport meta tag

### Setup Issues
- Use web-based setup if command-line setup fails
- Ensure all required fields are filled in setup form
- Check Python version compatibility (3.8+ required)

## 📞 Support

For SignalWire-specific features:
- [SignalWire Documentation](https://docs.signalwire.com)
- [SWAIG Documentation](https://docs.signalwire.com/swaig)

---

**Powered by SignalWire** - Advanced Communications Platform