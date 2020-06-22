import json

tp1 = 0
tp2 = 0
with open('hyp_botnet_member_time_sett27_run1.json', 'r') as file:
	data = json.load(file)
	print('len(data)', len(data))
	for key in data.keys():
		if not (data[key]['end'] is None):
			if data[key]['start'] == data[key]['end']:
				tp1 += 1
			else:
				tp2 += 1

print("tp1", tp1)
print("tp2", tp2)