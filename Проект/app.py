from flask import Flask, request, render_template_string, redirect, url_for, render_template, send_from_directory, jsonify
import hashlib
import sqlite3
app = Flask(__name__)

# Простая "база данных" пользователей: username -> password_hash
# Создадим одного пользователя: admin / password123
users_db = {
    'admin': hashlib.sha256('123'.encode()).hexdigest()
}

@app.route('/send_feedback', methods=['POST'])
def send_feedback():
    data = request.json
    message = data.get('message')
    
    # Сохранение в базу данных
    try:
        conn = sqlite3.connect('feedback.db')
        c = conn.cursor()
        c.execute("INSERT INTO messages (message) VALUES (?)", (message,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# HTML шаблон для страницы входа
login_html = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Вход на сайт</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background-color: #fff;
            padding: 30px 40px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }
        h2 {
            text-align: center;
            margin-bottom: 20px;
            color: #333;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px 12px;
            margin-bottom: 15px;
            border-radius: 6px;
            border: 1px solid #ccc;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #0056b3;
        }
        .error {
            color: red;
            text-align: center;
            margin-bottom: 10px;
        }
        .register-link {
            display:block; text-align:center; margin-top:15px; font-size:14px;}
        .register-link a { color:#007bff; text-decoration:none;}
        .register-link a:hover { text-decoration:none; }
    </style>
</head>
<body>
<div class="login-container">
    <h2>Войти на сайт</h2>
    {% if error %}
      <div class="error">{{ error }}</div>
    {% endif %}
    <form action="/login" method="POST">
        <label for="username">Имя пользователя</label>
        <input type="text" id="username" name="username" required />

        <label for="password">Пароль</label>
        <input type="password" id="password" name="password" required />

        <button type="submit">Войти</button>
    </form>
    <div class="register-link">
       Нет аккаунта? <a href="/register">Зарегистрироваться</a>
    </div>
</div>
</body>
</html>
'''

# HTML шаблон для страницы регистрации
register_html = '''
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Регистрация</title>
<style>
    body {
        font-family:'Arial', sans-serif;
        background:#74ebd5; /* градиент можно оставить или изменить */
        display:flex; justify-content:center; align-items:center; min-height:100vh; margin:0;}
    .register-container {
        background:#fff; padding:40px 30px; border-radius:15px; box-shadow:
         0 8px 20px rgba(0,0,0,0.2); max-width:400px; width:
         90%; box-sizing:border-box; transition:
           transform .3s ease, box-shadow .3s ease;}
    .register-container:hover {transform:
     translateY(-5px); box-shadow:
      0 12px 24px rgba(0,0,0,0.3);}
    h2 {text-align:center; margin-bottom:
    20px; color:#333; font-size:
     24px;}
    label {display:block; margin-bottom:
    8px; font-weight:bold; color:#555;}
    input[type=text], input[type=password] {width:
    100%; padding:12px 15px; margin-bottom:
     20px; border-radius:
      8px; border:1px solid #ccc; font-size:
      16px; box-sizing:border-box;}
    input[type=text]:focus,
     input[type=password]:focus {border-color:#007bff; box-shadow:
      inset 0 0 5px rgba(0,123,255,0.5); outline:none;}
    button {width:
    100%; padding:
     14px; background-color:#28a745; color:#fff; border:none;border-radius:
      8px;font-size:
      16px; cursor:pointer; transition:bg-color .3s ease,color .3s ease;}
    button:hover {background-color:#218838;}
    .message {text-align:center;margin-top:-10px;font-size:
    14px;}
</style>
</head>
<body>
<div class='register-container'>
<h2>Регистрация</h2>
{% if message %}
<div class='message' style='color:{% if success %}green{% else %}red{% endif %};'>{{ message }}</div>
{% endif %}
<form action="/register" method="POST">
    <label for='new_username'>Имя пользователя</label>
    <input type='text' id='new_username' name='new_username' required />

    <label for='new_password'>Пароль</label>
    <input type='password' id='new_password' name='new_password' required />

    <button type='submit'>Зарегистрироваться</button>
</form>
<a href="/login" style='display:block;text-align:center;margin-top:15px;font-size:14px;color:#007bff;text-decoration:none;'>Вернуться к входу</a>
</div></body></html>
'''

# Страница после успешного входа (здесь вставляем содержимое файла index(1).html)
# Для примера вставляю простое содержание.
# Если хотите вставить содержимое файла - нужно его прочитать и вставить сюда.
# Предположим что содержимое файла очень большое - лучше разместить его как отдельный шаблон.
# Для этого я сделаю отдельный route и рендеринг.

@app.route('/welcome')
def welcome():

    # Можно динамически получить список изображений из папки
    import os
    images_dir = os.path.join(app.root_path, 'LangFlowandMain/фото')
    try:
        images = os.listdir(images_dir)
        # Формируем список путей к изображениям
        image_paths = [f'/static/{img}' for img in images]
        
    except Exception as e:
        image_paths = []
    
    # Вставляем HTML с изображениями
    images_html = ''.join([f'<img src="{path}" style="max-width:200px; margin:10px;">' for path in image_paths])
    
    page_content = f'''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Добро пожаловать</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 20px;
            }}
            h1 {{
                color: #333;
            }}
            .images-container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }}
        </style>
    </head>
    <body>
        <h1>Добро пожаловать!</h1>
        <div class="images-container">
            {images_html}
        </div>
        <a href="/logout" style="margin-top:20px; font-size:16px;">Выйти</a>
    </body>
    </html>
    '''
    return render_template("index.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db:
            hashed_input_password = hashlib.sha256(password.encode()).hexdigest()
            
            if users_db[username] == hashed_input_password:
                return redirect(url_for('welcome'))
                # Можно добавить сессию для запоминания авторизации
            else:
                error = "Неверный пароль"
        else:
            error = "Пользователь не найден"
    
    return render_template_string(login_html, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['new_username']
        password = request.form['new_password']
        
        if username in users_db:
            message = "Такой пользователь уже существует."
            return render_template_string(register_html,
                                          message=message,
                                          success=False)
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        users_db[username] = hashed_password
        message = "Регистрация прошла успешно!"
        
        return render_template_string(register_html,
                                      message=message,
                                      success=True)
    
    return render_template_string(register_html)

@app.route("/rtx3050", methods= ['GET'])
def rtx3050():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "RTX 3050.html")

@app.route("/rtx3060", methods= ['GET'])
def rtx3060():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "RTX 3060.html")

@app.route("/rtx3070", methods= ['GET'])
def rtx3070():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "RTX 3070.html")

@app.route("/rtx3080", methods= ['GET'])
def rtx3080():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "RTX 3080.html")

@app.route("/rtx3090", methods= ['GET'])
def rtx3090():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "RTX 3090.html")

@app.route("/rtx4060", methods= ['GET'])
def rtx4060():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "RTX 4060.html")

@app.route("/rtx4070", methods= ['GET'])
def rtx4070():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "RTX 4070.html")

@app.route("/rtx4080", methods= ['GET'])
def rtx4080():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "RTX 4080.html")

@app.route("/rtx4090", methods= ['GET'])
def rtx4090():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "RTX 4090.html")

@app.route("/rtx5070", methods= ['GET'])
def rtx5070():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "RTX 5070.html")


@app.route("/rtx5080", methods= ['GET'])
def rtx5080():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "RTX 5080.html")


@app.route("/rtx5090", methods= ['GET'])
def rtx5090():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "RTX 5090.html")




#процессоры

@app.route("/i514600", methods= ['GET'])
def i514600():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "i5 14600.html")

@app.route("/i513400", methods= ['GET'])
def i513400():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "i5 13400.html")

@app.route("/i512400", methods= ['GET'])
def i512400():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "i5 12400.html")

#оперативки

@app.route("/kingstonfury16", methods= ['GET'])
def kingston16():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "kingston16.html")

@app.route("/kingstonfury32", methods= ['GET'])
def kingston32():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "kingston32.html")

@app.route("/kingstonfury64", methods= ['GET'])
def kingston64():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "kingston64.html")

@app.route("/kingstonfury96", methods= ['GET'])
def kingston96():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "kingston96.html")

@app.route("/kingstonfury128", methods= ['GET'])
def kingston128():
    # file = open("Product/RTX 3050.html")
    return send_from_directory('Product', "kingston128.html")




@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)