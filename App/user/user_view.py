from flask import Flask, render_template, request, jsonify
from App.user.user_model import get_user_model, UserModel
from App import app


# Initialize the user model
status, user_model_or_message = get_user_model()
if not status:
    print(user_model_or_message)
    raise Exception("Failed to initialize user model.")
UserModel = user_model_or_message


# Route to render the registration form
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('user/user_register.html')


# Route to handle user registration (POST request)
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    # Validate input
    if not username or not password or role not in ['admin', 'site_engineer']:
        return jsonify({"success": False, "message": "Invalid input."}), 400

    # Register the user
    success, message = UserModel.register_user(username, password, role)
    return jsonify({"success": success, "message": message})

#==============================================
#Login route
@app.route('/')
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('user/user_login.html')

@app.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        # Validate input
        if not username or not password or role not in ['admin', 'site_engineer']:
            return jsonify({"success": False, "message": "Invalid input."}), 400

        # Authenticate user
        success, message = UserModel.authenticate_user(username, password, role)
        if success:
            if role == "admin":
                return jsonify({"success": True, "redirect_url": "/admin/dashboard"})
            elif role == "site_engineer":
                return jsonify({"success": True, "redirect_url": "/site/dashboard"})
        else:
            return jsonify({"success": False, "message": message})

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"success": False, "message": "An internal error occurred."}), 400

@app.route('/users')
def users():
    """Fetch all users and display them in a DataTable."""
    success, user_model_or_message = get_user_model()
    if not success:
        return f"Error initializing user model: {user_model_or_message}", 500

    user_model = user_model_or_message
    success, result = user_model.get_all_users()

    if success:
        user_model.close_connection()
        return render_template('users.html', users=result)
    else:
        user_model.close_connection()
        return f"Error fetching users: {result}", 500


@app.route('/admin/dashboard')
def dashboard():
    return render_template('/admin/adminDashboard.html')

@app.route('/site')
def Site():
    return render_template('/admin/siteForm.html')

