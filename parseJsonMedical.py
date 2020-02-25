import pandas as pd 
import json as json
import re as re
import matplotlib
import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
import itertools
import pprint

def main():

	#file must be in working dir
	# parseHouseFile("house_json.txt")
	# getDieasesfromMalacars('house',"malacards_link_house.txt")
	getDieasesfromMalacars('grey',"malacards_links_grey.txt")
def parseHouseFile(path):
	class Season:
		def __init__(self,season_num):
			self.number = season_num
			self.age_array = [0] * 120
			self.maleCount = 0
			self.femaleCount = 0

	Seasons = {}
	total_seasons_age_array = [0] * 120
	seasons_num = 0
	with open(path) as datafile:
		data = json.loads(datafile.read())
		for season in data:
			seasons_num += 1
			curr_Season = Season(season)
			Seasons[season] = curr_Season
			value_season = data[season]
			for episode in value_season:
				if "gender" in episode:
					gender = episode["gender"]
					if(gender == 'Male'):
						curr_Season.maleCount += 1
					elif(gender == 'Female'):
						curr_Season.femaleCount += 1
				if "age" in episode:
					if(episode["age"] == "Newborn"):
						curr_Season.age_array[0] += 1
						total_seasons_age_array[0] += 1
					age = re.sub('[A-Za-z()]','',episode["age"])
					if(age):
						curr_Season.age_array[int(age)] += 1
						total_seasons_age_array[int(age)] +=1
			# print('Season num =' ,curr_Season.number, 'maleCount = ',curr_Season.maleCount,'femaleCount = ',curr_Season.femaleCount)
			# print('Most Common age =',curr_Season.age_array.index(max(curr_Season.age_array)))
		total_male_count = 0
		total_female_count = 0
		# createFemaleMalebar(seasons_num,Seasons)
		createAgaBarArray(total_seasons_age_array)
		for season in Seasons.values():
			total_male_count += season.maleCount
			total_female_count += season.femaleCount
		# print('Total maleCount = ',total_male_count,'Total femaleCount = ',total_female_count)
	datafile.close()


def createAgaBarArray(age_list):
	n_groups = len(age_list)
	# create plot
	fig, ax = plt.subplots()
	index = np.arange(n_groups) +1
	bar_width = 1	
	opacity = 1

	rects1 = plt.plot(age_list,
	alpha=opacity,
	color='g',
	label='age')

	plt.xlabel('age')
	plt.yticks(np.arange(0,20))
	plt.xticks(np.arange(0,120,5))
	plt.legend()

	plt.tight_layout()
	# plt.show()


def createFemaleMalebar(seasons_num,Seasons):
	labels = ['S'+ str(i) for i in range(seasons_num+1)]
	n_groups = seasons_num
	men_means = [s.maleCount for s in Seasons.values()]
	women_means = [s.femaleCount for s in Seasons.values()]

	# create plot
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.35
	opacity = 0.8

	rects1 = plt.bar(index, men_means, bar_width,
	alpha=opacity,
	color='g',
	label='Men')

	rects2 = plt.bar(index + bar_width, women_means, bar_width,
	alpha=opacity,
	color='r',
	label='Women')

	plt.xlabel('Seasons')
	plt.yticks(np.arange(0, max(max(men_means),max(women_means)) + 5, 5))
	plt.title('Occurrences of gender by season ,Tv Show : House')
	ax.set_xticklabels(labels)
	plt.legend()

	plt.tight_layout()
	plt.savefig('gender.png', bbox_inches='tight')
	plt.cla()

def createDict_sorted_by_occurrences(Diseases_list):
	Dieases = {}
	for d in Diseases_list:
		if(d in Dieases):
			Dieases[d] +=1
		else:
			Dieases[d] = 1 
	d = {k: v for k, v in sorted(Dieases.items(), key=lambda item: item[1],reverse= True)}
	return d
def createPieChartForCatgory(tv_show,category_dict):
	values = [float(v) for v in category_dict.values()]
	labels = [str(k).replace('diseases','') for k in category_dict.keys()]
	fig = plt.gcf()
	fig.set_size_inches(6,6) 
	plt.pie(values, labels=labels,
	autopct='%1.1f%%', shadow=False, startangle=190,labeldistance = 1.1,pctdistance = 0.75,radius = 1)
	plt.axis('equal')
	plt.tight_layout()
	# plt.show()
	plt.savefig('categorychart_{}.png'.format(tv_show), bbox_inches='tight')


def createTableforDieasesOcuureances(tv_show,Dieases_dict):
	df = pd.DataFrame(data=Dieases_dict,index=[0])
	df = df.fillna(' ').T
	with open('DieasesByOccurrences_{}.html'.format(tv_show),'w') as html_file:
		html_file.write(df.to_html())
	html_file.close()

def getDiesesList(data):
	return [x['disease'] for x in data if 'link' in x and x['link'] != 'no_match']

def getCatagoryList(data):
	return [z['category'] for z in data if 'category' in z]

def getDieaseswithPrevelance_and_Age_of_onset(data):
	Dieases_prevalence_age_of_onset = [('<a href="{}">{}</a>'.format(x['link'],x['disease']),x['orpha_data']['prevalence'],x['orpha_data']['age_of_onset'])
	for x in data if 'orpha_data' in x and x['orpha_data'] != {}]
	q = Dieases_prevalence_age_of_onset[:]
	filter(lambda x: q.remove(x) is None and g.count ==0,Dieases_prevalence_age_of_onset)
	return q

def filterDieases(Dieases_table):
	r = {}
	for x in Dieases_table:
		(a,b,c) = x
		if b != '-' and b != 'Unknown' and c != '-' and c != 'Unknown' and a not in r:
			prevalence = re.sub('[<]','',b).replace(" ","").split('/')
			if '-' in prevalence[0]:
				prevalence[0] = prevalence[0].split('-')
				for i in range(len(prevalence[0])):
					prevalence[0][i] = "{:.6f}%".format(float(prevalence[0][i]) / float(prevalence[1]))
				prevalence.remove(prevalence[1])
				prevalence = '-'.join(prevalence[0])
			else:
				prevalence[0] = "{:.6f}%".format(float(prevalence[0]) / float(prevalence[1]))
				prevalence.remove(prevalence[1])
				prevalence = prevalence[0]
			r[a] = [prevalence,c]
	return r

def createTablePrevenalceandAge(tv_show,Dieases_dict):
	df = pd.DataFrame(data=Dieases_dict)
	df = df.fillna(' ').T
	with open('TablePrevenalceandAge_{}.html'.format(tv_show),'w') as html_file:
		html_file.write(df.to_html(escape =False))
	html_file.close()

def getDieasesfromMalacars(tv_show,path):
	with open(path) as datafile:
		data = json.loads(datafile.read())
		Diseases_list = getDiesesList(data)
		Catagory_list = getCatagoryList(data)
		Dieases_prevalence_age_of_onset = getDieaseswithPrevelance_and_Age_of_onset(data)
		i,j,k = 0,0,0
		pp = pprint.PrettyPrinter(indent = 4)
		Dict =(filterDieases(Dieases_prevalence_age_of_onset))
		createTablePrevenalceandAge(tv_show,Dict)
		Catagory_list_flatten = list(itertools.chain(*Catagory_list))
		Dieases_dict = createDict_sorted_by_occurrences(Diseases_list)
		category_dict = createDict_sorted_by_occurrences(Catagory_list_flatten)
		createPieChartForCatgory(tv_show,category_dict)
		createTableforDieasesOcuureances(tv_show,Dieases_dict)	
	datafile.close()



if __name__ == "__main__":
	main()