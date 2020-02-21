import house_data
import greys_data
import disease_data
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
    #temp_table = ["Neurocysticercosis", "Small-cell lung cancer"]

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
    #temp_table = ["Excessive bleeding post-root canal"]
    diseases_table = get_diseases_table(greys_data_output, house_data_output)
    #part_table = diseases_table[1:10]
    #disease_data.get_disease_table_link(part_table)

    # getting matching disease link using malacard search
    if not path.exists("results/malacards_links.txt"):
        malacard_output = disease_data.get_disease_table_link(diseases_table)
        with open('results/malacards_links.txt', 'w') as outfile:
            json.dump(malacard_output, outfile)
    with open('results/malacards_links.txt') as json_file:
        malacard_links_list = json.load(json_file)

    #temp_part_malacard_list = malacard_links_list[40:50]

    # getting malacard disease info using malacard link
    if not path.exists("results/malacards_links_extended.txt"):
        malacard_extended_output = disease_data.get_all_malacard_data(malacard_links_list)
        with open('results/malacards_links_extended.txt', 'w') as outfile:
            json.dump(malacard_extended_output, outfile)




if __name__ == "__main__":
    main()
