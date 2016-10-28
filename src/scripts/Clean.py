def DataClean(file_name):
	import json
	my_file1 = open (file_name,"r+")
	my_file2 = open ("./cleaned_dataset/" + "cleaned_" + file_name ,"w+")
	
	while 1:		
		data = my_file1.readline()
		#clean
		if not data :
			break
		data_dict = json.loads(data)
		
		error = 0
		
		for key in data_dict:
			#for business:
			if key == 'city':
				pass
			if key == 'review_count':
				pass
			if key == 'name':
				pass
			if key == 'neighborhoods':
				pass
			if key == 'type':
				pass
			if key == 'business_id':
				pass
			if key == 'full_address':
				pass
			if key == 'hours':
				pass
			if key == 'state':
				pass
			if key == 'longitude':
				pass
			if key == 'stars':
				pass
			if key == 'latitude':
				pass
			if key == 'attributes':
				pass
			if key == 'open':
				pass
			if key == 'categories':
				pass

			# checkin :
			if key == 'checkin_info':
				pass
			if key == 'type':
				pass
			if key == 'business_id':
				pass

			#for review:
			if key == 'votes':
				pass
			if key == 'user_id':
				pass
			if key == 'review_id':
				if '-' in data_dict['review_id']:
					error = error + 1
			if key == 'text':
				if '\n' in data_dict['text']:
					error = error + 1	
			if key == 'business_id':
				pass
			if key == 'stars':
				pass
			if key == 'date':
				pass
			if key == 'type':
				pass

			#for tip:
			if key == 'user_id':
				pass
			if key == 'text':
				pass
			if key == 'business_id':
				pass
			if key == 'likes':
				pass
			if key == 'date':
				pass
			if key == 'type':
				pass

			#for user:
			if key == 'yelping_since':
				pass
			if key == 'votes':
				pass
			if key == 'user_id':
				pass
			if key == 'name':
				pass
			if key == 'elite':
				pass
			if key == 'type':
				pass
			if key == 'compliments':
				pass
			if key == 'fans':
				pass
			if key == 'average_stars':
				pass
			if key == 'review_count':
				pass
			if key == 'friends':
				pass
	

		data_str =  json.dumps(data_dict)
		if error == 0:
			my_file2.write(data_str)

	my_file1.close()
	my_file2.close()

