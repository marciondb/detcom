__author__ = 'marcio'


class Etp4():

    def __init__(self):
        pass

    #treat the original output file
    def treatRecordsFile(self, fname, fileWithTreatedRecords):

        file = open( fileWithTreatedRecords, "w")

        with open(fname) as f:
            content = f.read().splitlines()
            for line in content:
                partition = line.split('|')
                file.write(partition[1]+ '\n')

        file.close()

    def run(self, fileWithTreatedRecords, fileWithOriginalRecords, categorical, isHomogeneousNetwork):

        import time
        strings = time.strftime("%Y,%m,%d,%H,%M,%S")
        t = strings.split(',')
        numbers = [int(x) for x in t]
        print 'INICIO{}'.format(numbers)

        #first treat the original output file
        self.treatRecordsFile( fileWithOriginalRecords, fileWithTreatedRecords)

        #list of algorithm to choose
        algorithm = {}

        algorithm[0] = ['Affinity Propagation']

        #user choice
        algorithmChoose = 0

        print "Algorithm selected to clustring records was {}".format( algorithm[algorithmChoose][0] )

        if algorithmChoose == 0:
            import ap
            ap.ap( fileWithTreatedRecords, categorical, isHomogeneousNetwork )

        print "Step4 done!"
        strings = time.strftime("%Y,%m,%d,%H,%M,%S")
        t = strings.split(',')
        numbers = [int(x) for x in t]
        print 'FIM{}'.format(numbers)

