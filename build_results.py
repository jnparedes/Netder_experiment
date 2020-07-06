import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import csv
import json
target_loc = 'final_results.csv'
avg_values_loc = 'avg_values'
csv_source_base = 'result_netder_experiment_sett_'
settings = [4, 12, 19, 24, 28, 36]
#settings = [4]
programs = ['alpha', 'beta', 'alpha*']
#programs = ['alpha']
cant_prog = len(programs)
target_data = ['fnA_prec', 'fnA_rec', 'fnB_prec', 'fnB_rec', 'fnC_prec', 'fnC_rec', 'resp_prec', 'resp_rec', 'mal_prec', 'mal_rec', 'memb_prec', 'memb_rec']
#target_data = ['memb_prec']
time_sim = 15

def get_csv_headers(csv_source):
	with open(csv_source, 'r', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		headers = reader.fieldnames

	return headers

def save_csv(csv_source, data):
	fieldnames = {}
	for key in data.keys():
		fieldnames[key] = key
	fieldnames = list(data.keys())
	with open(csv_source, 'a+', newline='') as csvfile:
		read_data = []
		writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
		if os.stat(csv_source).st_size > 0:
			reader = csv.DictReader(csvfile, fieldnames = fieldnames)
			read_data = list(reader)
		else:
			writer.writeheader()
		writer.writerows(read_data)
		writer.writerow(data)

def summary():
	total_final_result = []
	total_avg_values = {}
	for prog in range(cant_prog):
		for setting in settings:
			final_result = {}
			avg_values = []
			total_avg_values['prog' + str(prog) + '_sett' + str(setting)] = avg_values
			final_result['prog'] = programs[prog]
			final_result['sett'] = setting
			counter = 0
			acum = 0
			csv_source = csv_source_base + str(setting) + '_prog'+ str(prog + 1) + '.csv'
			fieldnames = get_csv_headers(csv_source)
			for tg in target_data:
				final_result[tg] = {'value': 0, 'counter': 0}
				final_result['dev_' + tg] = []
				
			with open(csv_source, 'r', newline='') as csvfile:
				reader = csv.DictReader(csvfile, fieldnames = fieldnames)
				index = 0
				for item in reader:
					row_to_add = {}
					for tg in target_data:
						if ((index) % time_sim) == 0 and index != 0:
							if not item[tg] == '':
								final_result[tg]['value'] += float(item[tg])
								final_result[tg]['counter'] += 1
								final_result['dev_' + tg].append(float(item[tg]))
							row_to_add[tg] = item[tg]
					if not row_to_add == {}:
						avg_values.append(row_to_add)
					index += 1

			
			for tg in target_data:
				counter = final_result[tg]['counter']
				
				final_result[tg] = final_result[tg]['value'] / final_result[tg]['counter']
				dev = 0
				for value in final_result['dev_' + tg]:
					dev += (value - final_result[tg])**2
				
				final_result['dev_' + tg] = (dev / counter) ** 0.5
				

			total_final_result.append(final_result)

	return {'total_final_result': total_final_result, 'total_avg_values': total_avg_values}

def get_time_detection():
	time_sim = 15
	cant_runs = 100
	detection_base = 'time_detection_results/'
	detection_task = ['hyp_is_resp', 'hyp_is_mal', 'hyp_botnet_member']
	task_name = ['resp', 'mal', 'memb']
	for prog in range(cant_prog):
		for setting in settings:
			result = {}
			result['prog'] = programs[prog]
			result['sett'] = setting
			for task in task_name:
				result[task] = {'value': 0, 'counter': 0, 'data': []}
			for run in range(cant_runs):
				for task in range(len(detection_task)):
					json_source = detection_base + detection_task[task] + '_time_sett' + str(setting) + '_run' + str(run + 1) + '_prog' + str(prog + 1) + '.json'
					with open(json_source, 'r') as jsonfile:
						data = json.load(jsonfile)
						for key in data.keys():
							if not data[key]['start'] is None and not data[key]['end'] is None:
								result[task_name[task]]['value'] += data[key]['end'] - data[key]['start']
								result[task_name[task]]['data'].append(data[key]['end'] - data[key]['start'])
								result[task_name[task]]['counter'] += 1
			
			for task in task_name:
				data = result[task]['data']
				counter = result[task]['counter']
				result[task] = result[task]['value'] / result[task]['counter']
				dev = 0
				for item in data:
					dev += (item - result[task])**2
				result['dev_' + task] = (dev / counter) ** 0.5
			save_csv('detection_time.csv', result)

def time_to_csv():
	time_sim = 15
	cant_runs = 100
	detection_base = 'time_detection_results/'
	detection_task = ['hyp_is_resp', 'hyp_is_mal', 'hyp_botnet_member']
	task_name = ['resp', 'mal', 'memb']
	for prog in range(cant_prog):
		index = 0
		for setting in settings:
			for run in range(cant_runs):
				for task in range(len(detection_task)):
					result = []
					json_source = detection_base + detection_task[task] + '_time_sett' + str(setting) + '_run' + str(run + 1) + '_prog' + str(prog + 1) + '.json'
					with open(json_source, 'r') as jsonfile:
						data = json.load(jsonfile)
						for key in data.keys():
							if not data[key]['start'] is None and not data[key]['end'] is None:
								to_save = {}
								to_save['sett'] = setting
								to_save['task'] = detection_task[task]
								to_save['time'] = data[key]['end'] - data[key]['start']
								result.append(to_save)
								print('index', index)
								index += 1
					for item in result:
						save_csv('detection_time_prog_'+ str(prog + 1) +'.csv', item)
#summary = summary()


'''
for key in summary['total_avg_values'].keys():
	values = summary['total_avg_values'][key]
	for item in values:
		save_csv(avg_values_loc + '_' + str(key) + '.csv', item)'''


#for item in summary['total_final_result']:
#	save_csv(target_loc, item)
#get_time_detection()
#summary()
time_to_csv()

