.PHONY : profile clean lint

profile :
	python autoload/vache/profile.py

clean :
	rm -f all_names.prof family_names.prof encoded_names.prof

lint :
	flake8 --max-complexity 10 autoload/vache

ci :
	git clone git://github.com/dnhgff/vache-test-data test-data
	python autoload/vache/profile.py ./test-data
