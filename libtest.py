from fuzzywuzzy import process, fuzz


names = ["bariq", "isfar", "fareq", "mannan", "hamed", "bar"]


while True:

    typo = input("write a name here:" )
    print(process.extract(typo, names, limit=2))

