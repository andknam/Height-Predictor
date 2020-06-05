from flask import Flask, render_template, request
from processing import get_prediction_info
import responses

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET', 'POST'])
def form_page():
    errors = ''
    if request.method == 'POST':
        patient = request.form['patient_input']
        gender = request.form['gender-checkbox']
        growth_type = request.form['growth-checkbox']
        recent_height = None
        skeletal_year = None
        skeletal_month = None

        #try-except for height_input
        try:
            recent_height = int(request.form['height_input'])
        except:
            errors += '{!r} is not a number.\n'.format(request.form['height_input'])

        #try-except for skeletal_year_input
        try:
            skeletal_year = int(request.form['skeletal_year_input'])
        except:
            errors += '{!r} is not a number.\n'.format(request.form['skeletal_year_input'])

        #try-except for skeletal_month_input
        try:
            skeletal_month = int(request.form['skeletal_month_input'])
        except:
            errors += '{!r} is not a number.\n'.format(request.form['skeletal_month_input'])

        if len(errors) == 0:
            prediction_info = get_prediction_info(gender, recent_height, growth_type, skeletal_year, skeletal_month)

            #make an html for no prediction
            #add the make another height prediction button to form page
            #clean code if possible

            if prediction_info[0] == 'skeletal_low':
                response = responses.skeletal_low
                return render_template('error_response.html', response=response)
            elif prediction_info[0] == 'skeletal_high':
                response = responses.skeletal_high
                return render_template('error_response.html', response=response)
            elif prediction_info[0] == 'skeletal_index_young':
                response = responses.skeletal_index_young
                return render_template('error_response.html', response=response)
            elif prediction_info[0] == 'skeletal_index_old':
                response = responses.skeletal_index_old
                return render_template('error_response.html', response=response)
            elif prediction_info[0] == 'height_index_low':
                response = responses.height_index_low
                return render_template('error_response.html', response=response)
            elif prediction_info[0] == 'height_index_tall':
                response = responses.height_index_tall
                return render_template('error_response.html', response=response)

            else:
                predicted_height = prediction_info[0]
                percent_of_mature = prediction_info[1]
                return '''
                    <html>
                        <body>
                            <p>Height: {} inches</p>
                            <p>Skeletal Age: {} years and {} months</p>
                            <p>{}'s predicted height is about {}.</p>
                            <p>They have completed {}% of their growth!</p>
                            <img src="https://s3.amazonaws.com/lowres.cartoonstock.com/children-height-height_charts-grows-tall-measures-rbon240_low.jpg"
                            style="width:200px;height:300px;">
                            <p><a href="/">Click here to make another height prediction!</a>
                        </body>
                    </html>
                    '''.format(recent_height, skeletal_year, skeletal_month, patient, predicted_height, percent_of_mature)

    return render_template('form_page.html', errors=errors)


