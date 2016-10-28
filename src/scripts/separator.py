import os

print("Starting separator: \n" + "It's goint to take some time.... \n")

dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataset'))
new_path = "chunks"
chunk_dir = os.path.join(dataset_path, new_path)

files = [f for f in os.listdir(dataset_path) if os.path.isfile(os.path.join(dataset_path, f))]

for f in files:
    if f == 'yelp_academic_dataset_review.json':
        if not os.path.exists(chunk_dir):
            os.makedirs(chunk_dir)

        chunk_size = 1000
        smallfile = None
        fid = 0

        with open(os.path.join(dataset_path, f)) as bigfile:
            for lineno, line in enumerate(bigfile):
                if lineno % chunk_size == 0:
                    if smallfile:
                        smallfile.close()
                    fid += 1
                    small_filename = os.path.join(chunk_dir, 'review_file_{}.json'.format(fid))
                    smallfile = open(small_filename, "w")
                smallfile.write(line)
            if smallfile:
                smallfile.close()
