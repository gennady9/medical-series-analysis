import house_data
import greys_data
import disease_data
import results
import json
import os.path
from os import path

def get_diseases_table(greys_output, house_ouput):
    diseases_table = []
    # greys diseases

    for season in range(len(greys_output)):
        season_index = str(season + 1)
        for episode_index in range(len(greys_output[season_index])):
            patients_table = greys_output[season_index][episode_index]['patients']
            for patient in range(len(patients_table)):
                diseases_table.extend(patients_table[patient]['diagnose'])

    # house diseases
    for season in range(len(house_ouput)):
        season_index = str(season + 1)
        for patient_index in range(len(house_ouput[season_index])):
            disease_to_add = house_ouput[season_index][patient_index]['diagnose']
            correct_cut = disease_to_add.replace(' and ', ',').split(',')
            diseases_table.extend(correct_cut)
    return diseases_table


def main():
    temp_table = ["Neurocysticercosis", "Small-cell lung cancer"]
    if not path.exists("results/greys_json.txt"):
        greys_json = greys_data.greys_data()
        with open('results/greys_json.txt', 'w') as outfile:
            json.dump(greys_json, outfile)
    if not path.exists("results/house_json.txt"):
        house_json = house_data.house_data()
        with open('results/house_json.txt', 'w') as outfile:
            json.dump(house_json, outfile)
    with open('results/greys_json.txt') as json_file:
        greys_data_output = json.load(json_file)
    with open('results/house_json.txt') as json_file:
        house_data_output = json.load(json_file)

    diseases_table = get_diseases_table(greys_data_output, house_data_output)
    print(disease_data.get_all_disease_data(temp_table))


if __name__ == "__main__":
    main()
