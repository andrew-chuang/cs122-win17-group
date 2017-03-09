from django.shortcuts import render
from django.http import HttpResponse
import datetime 
from scraping.scraping import find_intended_restaurant
import final_project


def parse_search_inputs(request):
	'''
	Reads the inputs from the search form and parses them into a 
		usable dictionary. 
	Returns: dictionary containing the search terms (n1, l1, ..., n4, l4)
	'''
	terms = {}
	if request.GET:
		q = request.GET
		if q['n1']:
			terms['r1'] = (str(q['n1']), str(q['l1']))
		if q['n2']:
			terms['r2'] = (str(q['n2']), str(q['l2']))
		if q['n3']:
			terms['r3'] = (str(q['n3']), str(q['l3']))
		if q['n4']:
			terms['r4'] = (str(q['n4']), str(q['l4']))
	return terms


def search(request):
	missingError = False
	now = current_datetime(request)
	terms = parse_search_inputs(request)
	matches = {}
	if not terms:
		return render(request, 'search_form.html', 
			{'time': now, 'blankError': True})

	else:
		for rest in terms:
			if not (terms[rest][0] and terms[rest][1]):
				return render(request, 'search_form.html', 
					{'time': now, 'missingError': True})
			else:
				matches[rest] = find_intended_restaurant(terms[rest][0], 
					terms[rest][1])

		return render(request, 'page2.html', 
			{'inputs': terms, 'matches': matches})


def recs(request):
	q = request.GET
	user_input = []
	if not q:
		return render(request, 'search_form.html')
	
	for key in q:
		user_input.append(str(q[key]))


	print(user_input)
	out = final_project.go(user_input, 'asdf.db')
	
	return render(request, 'recs.html', {'d': out})
	


def current_datetime(request):
	now = datetime.datetime.now()
	return now
