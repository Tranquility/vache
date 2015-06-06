.PHONY : profile clean lint

profile :
	python autoload/vache/profile.py

clean :
	rm -f all_names.prof family_names.prof encoded_names.prof

lint :
	flake8 --max-complexity 10 autoload/vache

ci :
	test -e test-data || git clone git://github.com/dnhgff/vache-test-data test-data
	python autoload/vache/profile.py
	time python autoload/vache/get_docsets.py --families jquery,jqueryui test-data/docsets
	time python autoload/vache/get_docsets.py test-data/docsets
