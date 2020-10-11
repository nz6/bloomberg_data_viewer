import os
import string
import _collections

dataFile = ''

class BBGFileReader:
    topSection = None

    def __init__(self, datafile):
        self.datafile = datafile
        self.nbLines = 0;

    def getFieldsList(self):
        fields = ["ID", "RETURN_CODE", "NUM FIELDS"]
        inFieldsSection = False
        inTopSection = True
        inDataSection = False
        endOfFields = False

        with open(self.datafile) as datafile:
            for line in datafile:
                if line.startswith("END-OF-FIELDS"):
                    endOfFields = True
                    #pass
                    #break
                elif line.startswith("START-OF-FIELDS"):
                    inFieldsSection = True
                    inTopSection = False

                elif line.startswith("START-OF-DATA"):
                    inDataSection = True

                if inTopSection:
                    if(self.topSection is None):
                        self.topSection = line
                    else:
                        self.topSection = self.topSection + "\n" + line

                if inFieldsSection and not(endOfFields):
                    if(not(line.startswith("START-OF-FIELDS"))):
                        fields.append(line.strip());

                if inDataSection:
                    self.nbLines = self.nbLines + 1

        datafile.close()
        return fields


    def selectLines(self, lookupvalues, outputfile):
        if self.datafile == '':
            return 'File Name is Empty';
        if lookupvalues == '':
            return 'Lookupvalues is Empty';

        startoffield = False
        startofdata = False
        values = []
        fields = []
        lc = 0;
        writer = ''
        writtenlines = 0
        with open(self.datafile) as datafile:
            for line in datafile:
                lc = lc+1
                if lc%100000==0:
                    print("Line "+str(lc))
                    print(values)
                if startoffield:
                    fields.append(line.strip())
                if line.startswith("END-OF-FIELDS"):
                    startoffield = False
                elif line.startswith("START-OF-FIELDS"):
                    startoffield = True
                elif line.startswith("START-OF-DATA"):
                    startofdata = True

                if startofdata and fields:
                    tokens = line.split("|")
                    nbfields = len(fields)
                    match = True

                    for tuple in lookupvalues:
                        fieldname = tuple[0]
                        lookupvalue = tuple[1]
                        try:
                            idx = fields.index(fieldname)+3
                        except:
                            idx = -1
                            match = False
                        if idx>=0 and idx < len(tokens):
                            val = tokens[idx]
                            if val != lookupvalue:
                                match = False
                        else:
                            match = False

                    if match == True:
                        if writer == '':
                            writer = open(outputfile, 'w')
                            for f in range (0,nbfields-1):
                                fname = fields[f]
                                writer.write(fname)
                                if f<nbfields-1:
                                    writer.write("|")
                            writer.write("\n")

                        writer.write(line)
                        writtenlines = writtenlines + 1
                        if writtenlines ==100:
                            writer.flush()
                            writtenlines = 0

        if writer != '':
            writer.flush()
            writer.close()
        datafile.close()
        return values

    def getDataRows(self, start=0, end=100):
        if self.datafile == '':
            return 'File Name is Empty';

        startoffield = False
        startofdata = False
        data = []
        fields = []
        lc = 0
        writer = ''
        writtenlines = 0
        with open(self.datafile) as datafile:
            for line in datafile:
                line = line.strip()
                if startoffield:
                    fields.append(line.strip())
                if line.startswith("END-OF-FIELDS"):
                    startoffield = False
                elif line.startswith("START-OF-FIELDS"):
                    startoffield = True
                elif line.startswith("START-OF-DATA"):
                    startofdata = True

                if startofdata and fields:
                    if not(line.startswith("START-OF-DATA")):
                        if lc>=start and lc<end:
                            datarow = line.split("|")
                            if data is None:
                                data = [datarow]
                            else:
                                data.append(datarow)
                        lc = lc + 1
                        if lc>end:
                            datafile.close()
                            return data
        datafile.close()
        return data

    def getListOfValues(self, fieldname, lookupvalue):
        if self.datafile == '':
            return 'File Name is Empty';
        if fieldname == '':
            return 'Field Name is Empty';

        startoffield = False
        startofdata = False
        values = []
        fields = []
        lc = 0;
        with open(self.datafile) as datafile:
            for line in datafile:
                lc = lc+1
                if lc%100000==0:
                    print("Line "+str(lc))
                    print(values)
                if startoffield:
                    fields.append(line.strip())
                if line.startswith("END-OF-FIELDS"):
                    startoffield = False
                elif line.startswith("START-OF-FIELDS"):
                    startoffield = True
                elif line.startswith("START-OF-DATA"):
                    startofdata = True

                if startofdata and fields:
                    tokens = line.split("|")
                    try:
                        idx = fields.index(fieldname)+3
                    except:
                        idx = -1
                    if idx>=0 and idx < len(tokens):
                        try:
                            val = tokens[idx]
                            pos = values.index(val)
                            #if pos<0:
                                #values.append(val)
                        except:
                            if lookupvalue and val:
                                if val.startswith(lookupvalue):
                                    values.append(lc);
                            elif val:
                                values.append(val)
        datafile.close()
        return values


#lk1 = ('ID_BB_ULTIMATE_PARENT_CO','4100718')
#lks = [lk1]
#reader = BBGFileReader('D:/SDH/Import/Bloomberg/datafiles/bulk/credit_risk.out.20160926')
#rows = reader.getDataRows(5, 20)
#                           lks,
#                           "D:/SDH/Import/Bloomberg/datafiles/bulk/credit_risk.out.20160926.sample")
#print(rows)


