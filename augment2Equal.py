from collections import defaultdict
from os.path import splitext
from os.path import basename


labelsFileNameCSV = "trainLabels.csv"
equalFileName = "trainLabelsAugm2Equal.csv"
augmentedImagesDir = "augm2_256/"


classID2ImageNames = defaultdict(list)

labelsCSV = open(labelsFileNameCSV).readlines()[:]
for line in labelsCSV:
    st = line.split(" ")
    name = st[0].split("/")[1]
    classID = int(st[1])

    classID2ImageNames[classID].append(name)


equalFile = open(equalFileName, "w")
for classID, imageNames in classID2ImageNames.items():
    length = len(imageNames)
    for i in range(100):
        imageIndex = i % length
        name = imageNames[imageIndex]
        imageBasename = splitext(basename(name))[0]
        imageExtension = splitext(basename(name))[1]

        augmentedImageName = augmentedImagesDir + imageBasename + '_' + str(i).zfill(2) + imageExtension

        equalFile.write("{0} {1}\n".format(augmentedImageName, classID))

equalFile.close()
