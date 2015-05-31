.PHONY : profile clean

profile :
	python autoload/vache/profile.py

clean :
	rm -f all_names.prof family_names.prof encoded_names.prof
