import subprocess

def hide(datafile, infile, outfile):
    params = ['outguess', '-d', datafile, infile, outfile]
    return_value = subprocess.call(params)
    return return_value

def retrieve(stegfile, outfile):
    params = ['outguess', '-r', stegfile, outfile]
    return_value = subprocess.call(params)
    return return_value

if __name__ == '__main__':
    datafile = 'testfiles/stegin.txt'
    infile = 'testfiles/base.jpg'
    stegfile = 'testfiles/out.jpg'
    stegout = 'testfiles/stegout.txt'
    hide(datafile, infile, stegfile)
    if retrieve(stegfile, stegout) == 0:
        print "Success"
    else:
        print "Fail"
