import os
import glob
import pandas as pd
import gradio as gr

type_list = ['اسپرت', 'راحتی', 'پوتون', 'طبی', 'گوندارا', 'کالج', 'مجلسی', 'دمپایی', 'پاشنه دار', 'تابستانه', 'جورابی']
color_list = ['مشکی', 'سفید', 'قهوه ای', 'کرمی', 'خاکستری', 'طوسی', 'سبز', 'آبی', 'رنگارنگ']
shoelace_list  = ['کشی', 'چسب دار', 'بند دار', 'بدون بند', 'زیپ دار']
sex_list   = ['بزرگسال', 'بزرگسال زنانه', 'بزرگسال مردانه', 'بچگانه', 'بچگانه دختر', 'بچگانه پسر']
sizes = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

shoes_data = pd.read_excel('Book1.xlsx')

def show_shoes(types, genders, colors, shoelaces, sizes):
    shoes_arr = []
    selection = [types, genders, colors, shoelaces, sizes]
    for i in range(len(shoes_data)):
        Flag = True
        shoe_code,shoe_name,_,shoe_sizes,shoe_colors,shoe_shoelaces,shoe_sexes,shoe_types = shoes_data.iloc[i].values
        shoes =  [shoe_types.split('-'), shoe_sexes.split('-'), shoe_colors.split('-'), shoe_shoelaces.split('-'), shoe_sizes.split('-')]
        
        for select_details, shoe_details in zip(selection, shoes):
            if not select_details:
                continue
            for shoe_d in select_details:
                if shoe_d not in shoe_details:
                    Flag = False
                    break

            if not Flag:
                break
        if Flag:
            shoes_arr.append((f'./Img/{shoe_code}.jpg', f'Name: {shoe_name} ***** Code: {shoe_code} ***** Sizes: {shoe_sizes}'))

    if len(shoes_arr)==0:
        shoes_arr.append(('./Img/Empty.png', 'این کالا موجود نمی باشد'))
    return shoes_arr

demo = gr.Interface(
    fn=show_shoes,
    inputs=[
      gr.CheckboxGroup(type_list, label="types", info="لطفا نوع کفش دلخواه را انتخاب کنید"),
      gr.CheckboxGroup(sex_list, label="genders", info="لطفا جنسیت خود را انتخاب کنید"),
      gr.CheckboxGroup(color_list, label="colors", info="لطفا رنگ کفش دلخواه را انتخاب کنید"),
      gr.CheckboxGroup(shoelace_list, label="shoelaces", info="لطفا نوع بند کفش دلخواه را انتخاب کنید"),
      gr.Dropdown(sizes, multiselect=True, label="sizes", info="لطفا اندازه پای خود را انتخاب کنید"),
    ],
    outputs=gr.Gallery(label="Selected Shoes", allow_preview=True, preview=True, show_label=True, elem_id="gallery", columns=[3], rows=[1], object_fit="fill", height="auto")
)

demo.launch(share=True)
