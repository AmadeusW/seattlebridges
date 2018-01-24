class tfutils(object):
    """helper functions"""
    
    def storeData(data, path):
        """stores the array of arrays in the filesystem"""
        with open(path, 'w') as dataFile:
            for piece in data:
                row = ','.join(str(x) for x in piece)
                dataFile.write(row+'\n')


    def loadData(path):
        """loads the array of arrays from the filesystem"""
        result = []
        with open(path, 'r') as dataFile:
            for line in dataFile:
                ints = [int(x) for x in line.split(',')]
                result.append(ints)
        return result



