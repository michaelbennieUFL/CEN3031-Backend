generate_requirements:
	pip install pipreqs
	pipreqs ./ --force

upgradeDatabase:
	flask db migrate
	flask db upgrade

generatePhonemeList:
	find Data/phoneticData -type f -name "phone.txt"  -exec cat {} \; > allPhones.txt
	sort allPhones.txt | uniq > allUniquePhones.txt
