from data.collection import SimpleDataImporter
import sys

def main():
    dataset_name = 'yelp_academic_dataset_user.json'

    try:
        dataset_name = sys.argv[1]
    except BaseException as e:
        print ('usage: main.py <inputfile>')
        #sys.exit(2)

    collection_name = SimpleDataImporter.get_collection_name(dataset_name)

    simpleImporter = SimpleDataImporter(collection_name)
    simpleImporter.run(dataset_name, True)
    simpleImporter.finish()


if __name__ == '__main__':
    main()
