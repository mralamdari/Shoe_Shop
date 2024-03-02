import os
import pandas as pd
from flask import Flask, render_template, request
import flask
app = Flask(__name__)

type_list = ['اسپرت', 'راحتی', 'پوتون', 'طبی', 'گوندارا', 'کالج', 'مجلسی', 'دمپایی', 'پاشنه دار', 'تابستانه', 'جورابی']
color_list = ['مشکی', 'سفید', 'قهوه ای', 'کرمی', 'خاکستری', 'طوسی', 'سبز', 'آبی', 'رنگارنگ']
shoelace_list  = ['کشی', 'چسب دار', 'بند دار', 'بدون بند', 'زیپ دار']
sex_list   = ['بزرگسال', 'بزرگسال زنانه', 'بزرگسال مردانه', 'بچگانه', 'بچگانه دختر', 'بچگانه پسر']

# Define the route for the home page
@app.route('/')
def home():
    # Get unique values for each feature
    sizes = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    sexes = sex_list
    colors= color_list
    types = type_list
    shoelaces = shoelace_list
    return render_template('home.html', sizes=sizes, sexes=sexes, colors=colors, types=types, shoelaces=shoelaces)


@app.route('/show_shoes', methods=['POST'])
def show_shoes():
    # Get selected options from form submission
    selected_size = request.form.getlist('size')
    selected_sex = request.form.getlist('sex')
    selected_color = request.form.getlist('color')
    selected_type = request.form.getlist('type')
    selected_shoelace = request.form.getlist('shoelace')
    shoes = get_images(selected_size, selected_sex, selected_color, selected_type, selected_shoelace)
    if not shoes:
        shoes.append({'name': '', 'code': '', 'sizes': [], 'image_url': './static/Images/Empty.jpg'})

    return render_template('show_shoes.html', shoes=shoes)



IMAGE_DIR = 'static/Images'
root = os.path.dirname(__file__)
shoes_data = pd.read_excel(os.path.join(root, 'Book1.xlsx'))
# Read the shoe data from the Excel file
def get_images(selected_size, selected_sex, selected_color, selected_type, selected_shoelace):

    shoes_arr = []
    selection = [list(map(int, selected_size)), selected_sex, selected_color, selected_type, selected_shoelace]
    for i in range(len(shoes_data['code'].values)):
        Flag = True
        shoe_code,shoe_name,shoe_company,shoe_sizes,shoe_colors,shoe_shoelaces,shoe_sexes,shoe_types = shoes_data.iloc[i].values
        shoes =  [shoe_sizes.split('-'), shoe_sexes.split('-'), shoe_colors.split('-'), shoe_types.split('-'), shoe_shoelaces.split('-')]
        for select_details, shoe_details in zip(selection, shoes):
            if not select_details:
                continue
            for shoe_d in shoe_details:
                if shoe_d not in select_details:
                    Flag = False
                    break

            if not Flag:
                break
        if Flag:

            # shoes_arr.append({'name': shoe_name, 'code': str(shoe_code), 'sizes': shoe_sizes, 'image_url': f'/home/shoe2alamdari/mysite/static/Images/{str(shoe_code)}.jpg'})
            shoes_arr.append({'name': shoe_name, 'code': str(shoe_code), 'sizes': shoe_sizes, 'image_url': os.path.join(root,IMAGE_DIR,str(shoe_code)+'.jpg')})

    return shoes_arr