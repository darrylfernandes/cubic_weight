from flask import Flask, request, render_template, redirect, url_for
from app.services.weight_calculator import calculate_average_cubic_weight

rester_app = Flask(__name__, static_folder='static')
rester_app.secret_key = '@123koganinterviewquestions@321'


@rester_app.route('/', methods=['GET'])
def index():
    return redirect(url_for('home_page'))


@rester_app.route('/home_page', methods=['GET', 'POST'])
def home_page():
    category_choices = ["Air Conditioners", "Gadgets", "Batteries", "Cables & Adapters", "Oral Care",
                        "Food Preparation", "Scooters, Bicycles & Tricycles", "Fitness Equipment",
                        "Automotive Accessories", "LED Televisions", "Carpet & Steam Cleaners",
                        "Vacuum Cleaners", "Holders & Stands", "SIM Cards", "Prepaid Plans", "Wall Mounts",
                        "Networking & Wireless", "Travel Adapters", "Travel Accessories", "Automotive Accessories",
                        "Pest Control", "Android Phones", "Shoes"]
    category_choice_preselect = {'choice': 'Air Conditioners'}
    if request.method == 'POST':
        category_choice_selected = request.form['category']
        avg_cubic_weight = calculate_average_cubic_weight(category_choice_selected)
        category_choice_preselect = {'choice': category_choice_selected, 'avg_cubic_weight': avg_cubic_weight}
        return render_template('home_page.html', form=request.form, category_choices=category_choices,
                               category_choice_preselect=category_choice_preselect)
    return render_template('home_page.html', category_choices=category_choices,
                           category_choice_preselect=category_choice_preselect)


if __name__ == '__main__':
    rester_app.run()


