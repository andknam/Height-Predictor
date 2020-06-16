import csv
from urllib import request

# getting the age index for a unique range
def get_closest(chronological_year, chronological_month):
    if chronological_month <= 3:
        return chronological_year * 12
    elif 3 < chronological_month <= 9:
        return (chronological_year * 12) + 6
    else:
        return (chronological_year * 12) + 12

# growth type based on the standard deviation
def standard_dev(chronological_in_months, skeletal_in_months, std):
    two_std_low = int(chronological_in_months - (2 * std))
    two_std_high = int(chronological_in_months + (2 * std))

    if skeletal_in_months < two_std_low:
        return 'delayed'
    elif two_std_low <= skeletal_in_months <= two_std_high:
        return 'normal'
    else:
        return 'accelerated'

# returns growth type based on standard deviations from skeletal age
def get_growth_type(chronological_year, chronological_month, skeletal_year, skeletal_month, gender):

    chronological_in_months = (chronological_year * 12) + chronological_month
    skeletal_in_months = (skeletal_year * 12) + skeletal_month

    if gender == 'male':
        # getting the age key for variablity dictionary
        if chronological_in_months <= 21:
            return 'chronological_young'
        elif 21 < chronological_in_months < 57:
            age_key = get_closest(chronological_year, chronological_month)
        elif 57 <= chronological_in_months <= 204:
            age_key = chronological_year * 12
        else:
            return 'chronological_high'

        # used to get standard deviation for specific chronological age (in months)
        # format: chronological_in_months : [standard deviation]
        boy_variability = {3:[0.69], 6:[1.13], 9:[1.43], 12:[1.97], 18:[3.52],
                            24:[3.92], 30:[4.52], 36:[5.08], 42:[5.40], 48:[6.66],
                            54:[8.36], 60:[8.79], 72:[9.17], 84:[8.91], 96:[9.10],
                            108:[9.00], 120:[9.79], 132:[10.09], 144:[10.38],
                            156:[10.44], 168:[10.72], 180:[11.32], 192:[12.86], 204:[13.05]}

        std = boy_variability[age_key][0]

        growth_type = standard_dev(chronological_in_months, skeletal_in_months, std)

    else:
        # getting the age key for variablity dictionary
        if chronological_in_months <= 21:
            return 'chronological_young'
        if 21 < chronological_in_months < 57:
            age_key = get_closest(chronological_year, chronological_month)
        if 57 <= chronological_in_months <= 192:
            age_key = chronological_year * 12
        else:
            return 'chronological_old'

        # used to get standard deviation for specific chronological age (in months)
        # format: chronological_in_months : [standard deviation]
        girl_variability = {3:[0.72], 6:[1.16], 9:[1.36], 12:[1.77], 18:[3.49],
                            24:[4.64], 30:[5.37], 36:[5.97], 42:[7.48], 48:[8.98],
                            54:[10.73], 60:[11.65], 72:[10.23], 84:[9.64], 96:[10.23],
                            108:[10.74], 120:[11.73], 132:[11.94], 144:[10.24],
                            156:[10.67], 168:[11.30], 180:[9.23], 192:[7.31]}

        std = girl_variability[age_key][0]

        growth_type = standard_dev(chronological_in_months, skeletal_in_months, std)

    return growth_type

# returns google sheet gid based on input values
def get_sheet_info(gender, growth_type, skeletal_year):
    base_sheet = 'https://docs.google.com/spreadsheets/d/1fOM_Hntn5P9DXMg4o_rzHxrWJSM_MEwCXgiosloYCqY/export?format=csv&gid='

    # in order: avg boys 7-12, avg boys 13 to maturity, acc boys 7-11, acc boys 12-17, delay boys 6-13
    boy_sheet_gids = ['1419711891', '0', '1427424453', '1271493549', '881853527']

    # avg girls 6-11, avg girls 12-18, acc girls 7-11, acc girls 12-17, delay girls 6-11, delay girls 12-17
    girl_sheet_gids = ['1579963259', '289066998', '689487051', '1179802364','148949455', '923613939']

    if gender == 'male':
        if growth_type == 'normal':
            if (skeletal_year < 13):
                sheet_gid = boy_sheet_gids[0]
            else:
                sheet_gid = boy_sheet_gids[1]
        elif growth_type == 'accelerated':
            if (skeletal_year < 12):
                sheet_gid = boy_sheet_gids[2]
            else:
                sheet_gid = boy_sheet_gids[3]
        else:
            sheet_gid = boy_sheet_gids[4]

    else:
        if growth_type == 'normal':
            if (skeletal_year < 12):
                sheet_gid = girl_sheet_gids[0]
            else:
                sheet_gid = girl_sheet_gids[1]
        elif growth_type == 'accelerated':
            if (skeletal_year < 12):
                sheet_gid = girl_sheet_gids[2]
            else:
                sheet_gid = girl_sheet_gids[3]
        else:
            if (skeletal_year < 12):
                sheet_gid = girl_sheet_gids[4]
            else:
                sheet_gid = girl_sheet_gids[5]

    sheet_url = base_sheet + sheet_gid

    return [sheet_url, sheet_gid]

# returns skeletal input (as string) by rounding to the closest value
# that is in the table
def get_skeletal_input(skeletal_year, skeletal_month, sheet_gid):

    # standard skeletal age headings
    if (skeletal_month <= 1):
        skeletal_input = str(skeletal_year) + '-0'
    elif (2 <= skeletal_month <= 4):
        skeletal_input = str(skeletal_year) + '-3'
    elif (5 <= skeletal_month <= 7):
        skeletal_input = str(skeletal_year) + '-6'
    else:
        skeletal_input = str(skeletal_year) + '-9'

    # avg girls 6-11, acc girls 7-11 and delay girls 6-11
    if sheet_gid == '1579963259' or sheet_gid == '148949455' or sheet_gid == '689487051':
        if (skeletal_year < 9 and skeletal_month >= 9):
            skeletal_input = str(skeletal_year) + '-10'
        else:
            skeletal_input = str(skeletal_year) + '-6'

    # avg girls 12-18
    if sheet_gid == '289066998':
        if (skeletal_year == 17):
            if (skeletal_month <= 3):
                skeletal_input = str(skeletal_year) + '-0'
            elif (4 <= skeletal_month <= 9):
                skeletal_input = str(skeletal_year) + '-6'
            else:
                skeletal_input = '18-0'

    # acc girls 12-17
    if sheet_gid == '1179802364':
        if (skeletal_year == 17):
            if (skeletal_month <= 3):
                skeletal_input = str(skeletal_year) + '-0'
            else:
                skeletal_input = str(skeletal_year) + '-6'

    return skeletal_input

# based on the patient gender and age, get the prediction information
def get_prediction_info(recent_height, chronological_year, chronological_month, skeletal_year, skeletal_month, gender):

    recent_height = str(recent_height)

    growth_type = get_growth_type(chronological_year, chronological_month, skeletal_year, skeletal_month, gender)

    if growth_type == 'chronological_old':
        return ['chronological_old']

    # based on gender and skeletal age, choose correct sheet_gid
    sheet_info = get_sheet_info(gender, growth_type, skeletal_year)

    response = request.urlopen(sheet_info[0]).read().decode('UTF-8')
    reader = csv.reader(response.splitlines())

    skeletal_list = []
    mature_dict = {}
    height_dict = {}

    lowest_skeletal = 0
    tallest_skeletal = 0
    lowest_height = 0
    tallest_height = 0
    keys = []

    row_num = 0
    num_of_rows = 0
    for row in reader:
        # first row holds skeletal age values
        if row_num == 0:
            skeletal_list.append(row[2:])

            lowest_skeletal = skeletal_list[0][0]
            dash_index1 = lowest_skeletal.find('-')
            lowest_skeletal_year = int(lowest_skeletal[:dash_index1])

            tallest_skeletal = skeletal_list[0][len(skeletal_list[0]) - 1]
            dash_index2 = tallest_skeletal.find('-')
            tallest_skeletal_year = int(tallest_skeletal[:dash_index2])
            tallest_skeletal_month = int(tallest_skeletal[dash_index2:])
        # second row holds percent of mature height values
        elif row_num == 1:
            key, value = row[1], row[2:]
            mature_dict[key] = value
        # other rows hold predicted height values
        else:
            key, value = row[0], row[2:]
            keys.append(key)
            height_dict[key] = value
            num_of_rows += 1
        row_num += 1

    lowest_height = int(min(keys))
    tallest_height = int(max(keys))

    # check if value is in the table
    if skeletal_year < lowest_skeletal_year:
        return ['skeletal_index_young']
    if skeletal_year > tallest_skeletal_year:
        return ['skeletal_index_old']
    if skeletal_month > tallest_skeletal_month:
        return ['skeletal_index_old']
    if int(recent_height) < lowest_height:
        return ['height_index_low']
    if int(recent_height) > tallest_height:
        return ['height_index_tall']

    # get skeletal input
    skeletal_input = get_skeletal_input(skeletal_year, skeletal_month, sheet_info[1])

    # get the predicted height value
    skeletal_index = skeletal_list[0].index(skeletal_input)
    p_height_in_inch = height_dict[recent_height][skeletal_index]

    # in the case that no value is returned (empty cell)
    if p_height_in_inch == '':
        # if the empty cell occurs in the top right portion of the sheet
        if int(recent_height) < int(recent_height) + int(num_of_rows / 2):
            return ['skeletal_high']
        # if the empty cell occurs in the bottom left portion of the sheet
        else:
            return ['skeletal_low']
    else:
        p_height_rounded = round(float(p_height_in_inch))
        p_height_ft = str(int(p_height_rounded / 12))
        p_height_in = str(int(p_height_rounded % 12))

        predicted_height = p_height_ft + ' feet and ' + p_height_in + ' inches'


        percent_of_mature_height = mature_dict['% of Mature Height'][skeletal_index]

        return [predicted_height, percent_of_mature_height]
