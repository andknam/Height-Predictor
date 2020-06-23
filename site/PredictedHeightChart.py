from flask import Flask, render_template, request
from processing import get_prediction_info, get_brush_growth_type, get_one_year_growth_type
import responses

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET', 'POST'])
def form_page():
    errors = ''
    try:
        if request.method == 'POST':
            patient = request.form['patient_input']
            recent_height = None
            chronological_year = None
            chronological_month = None
            skeletal_year = None
            skeletal_month = None
            gender = request.form['gender-checkbox']
            selected_growth_type = request.form['growth-type-checkbox']

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

            #try-except for chronological_year_input
            try:
                chronological_year = int(request.form['chronological_year_input'])
            except:
                errors += '{!r} is not a number.\n'.format(request.form['chronological_year_input'])

            #try-except for chronological_month_input
            try:
                chronological_month = int(request.form['chronological_month_input'])
            except:
                errors += '{!r} is not a number.\n'.format(request.form['chronological_month_input'])

            if len(errors) == 0:
                if selected_growth_type == 'brush':
                    growth_type = get_brush_growth_type(chronological_year, chronological_month, skeletal_year, skeletal_month, gender)
                else:
                    growth_type = get_one_year_growth_type(chronological_year, chronological_month, skeletal_year, skeletal_month)

                prediction_info = get_prediction_info(recent_height, skeletal_year, skeletal_month, gender, growth_type[0])

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
                elif prediction_info[0] == 'chronological_young':
                    response = responses.chronological_young
                    return render_template('error_response.html', response=response)
                elif prediction_info[0] == 'chronological_old':
                    response = responses.chronological_old
                    return render_template('error_response.html', response=response)

                else:
                    ph = prediction_info[0]
                    pm = prediction_info[1]
                    gt = growth_type[0]

                    rh = recent_height
                    cy = chronological_year
                    cm = chronological_month
                    sy = skeletal_year
                    sm = skeletal_month
                    p = patient

                    if gender == 'male':
                        if selected_growth_type == 'brush':
                            sd = growth_type[1]
                            return render_template('valid_male_brush_response.html', rh=rh, cy=cy, cm=cm, sy=sy, sm=sm, gt=gt, sd=sd, p=p, ph=ph, pm=pm)
                        else:
                            return render_template('valid_male_one_year_response.html', rh=rh, cy=cy, cm=cm, sy=sy, sm=sm, gt=gt, p=p, ph=ph, pm=pm)
                    else:
                        if selected_growth_type == 'brush':
                            sd = growth_type[1]
                            return render_template('valid_female_brush_response.html', rh=rh, cy=cy, cm=cm, sy=sy, sm=sm, gt=gt, sd=sd, p=p, ph=ph, pm=pm)
                        else:
                            return render_template('valid_female_one_year_response.html', rh=rh, cy=cy, cm=cm, sy=sy, sm=sm, gt=gt, p=p, ph=ph, pm=pm)

    except:
        errors += 'Something went wrong :( Please reload the page and try again'

    return render_template('form_page.html', errors=errors)
