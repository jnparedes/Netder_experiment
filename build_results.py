import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import csv
import json
target_loc = 'final_results.csv'
csv_source_base = 'result_netder_experiment_sett_'
#settings = [4, 12, 19, 24, 36]
settings = [36]
#programs = ['alpha', 'beta', 'gamma']
programs = ['alpha']
cant_prog = len(programs)
target_data = ['fnA_prec', 'fnA_rec', 'fnB_prec', 'fnB_rec', 'fnC_prec', 'fnC_rec', 'resp_prec', 'resp_rec', 'mal_prec', 'mal_rec', 'memb_prec', 'memb_rec']
#target_data = ['fnA_prec']

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
	for prog in range(cant_prog):
		for setting in settings:
			final_result = {}
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
				for item in reader:
					for tg in target_data:
						if not item[tg] == '' and not item[tg] == tg:
							final_result[tg]['value'] += float(item[tg])
							print('float(item[tg])', float(item[tg]))
							final_result[tg]['counter'] += 1
							final_result['dev_' + tg].append(float(item[tg]))

			for tg in target_data:
				counter = final_result[tg]['counter']
				final_result[tg] = final_result[tg]['value'] / final_result[tg]['counter']
				dev = 0
				print('tg', tg)
				for value in final_result['dev_' + tg]:
					print('value', value)
					print('final_result tg', final_result[tg])
					dev += (value - final_result[tg])**2
				print('dev', dev)
				print('counter', counter)
				final_result['dev_' + tg] = (dev / counter) ** 0.5

			save_csv(target_loc, final_result)

def get_time_detection():
	time_sim = 15
	cant_runs = 100
	detection_base = 'time_detection_results/'
	detection_task = ['hyp_botnet_member', 'hyp_is_mal', 'hyp_is_resp']
	task_name = ['memb', 'mal', 'resp']
	for prog in range(cant_prog):
		for setting in settings:
			result = {}
			result['prog'] = programs[prog]
			result['sett'] = setting
			for task in task_name:
				result[task] = {'value': 0, 'counter': 0}
			for run in range(cant_runs):
				for task in range(len(detection_task)):
					json_source = detection_base + detection_task[task] + '_time_sett' + str(setting) + '_run' + str(run + 1) + '_prog' + str(prog + 1) + '.json'
					with open(json_source, 'r') as jsonfile:
						data = json.load(jsonfile)
						for key in data.keys():
							if not data[key]['start'] is None and not data[key]['end'] is None:
								result[task_name[task]]['value'] += data[key]['end'] - data[key]['start']
								result[task_name[task]]['counter'] += 1
			for task in task_name:
				result[task] = result[task]['value'] / result[task]['counter']

			save_csv('detection_time.csv', result)

#get_time_detection()
summary()
