labels = [{"name": "a"}]
found = false
foreach labels as label
	if label["name"] == "a" or label["name"] == "b"
		found = true
	else
		found = false
	if found
		x = 0
outside = true
