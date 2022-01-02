#!/usr/bin/env python

# script to strip a UVFITS file from the XY and YX correlations 
# designed by Tammo Jan Dijkema and Maaijke Mevius
# adopted by Thijs van der Hulst
# date: 11-11-2021

# use as "python trim_uvfits.py <input_file_name> <output_file_name>" 

from astropy.io import fits
import astropy.io.fits.hdu.base
import sys
# print (astropy.__file__)
try:
        inname = sys.argv[1]
except IndexError:
        print("input file and output file missing in command line")
        print("Usage: python trim_uvfits.py <input_file_name> <output_file_name>")
        sys.exit(1)
try:
        outname = sys.argv[2]
except IndexError:
        print("output file missing in command line")
        print("Usage: python trim_uvfits.py <input_file_name> <output_file_name>")
        sys.exit(1)
hdulist = fits.open(inname)
old_hdu = hdulist[0]
header = old_hdu.header
try:
        assert(old_hdu.data.data.shape[4] == 4)
except AssertionError:
        print("input file does not have 4 polarisations")
        sys.exit(1)
pardata = []
for parname in old_hdu.data.parnames:
        pardata.append(old_hdu.data[parname])
newdata = fits.GroupData(old_hdu.data.data[:,:,:,:,:2,:],parnames=old_hdu.data.parnames, pardata = pardata,bitpix=-32)
new_hdu = fits.GroupsHDU(header=header, data = newdata)
new_hdu.header['EXTEND']=True

hdulist[0] = new_hdu
try:
        hdulist.writeto(outname, overwrite=False)
except OSError:
        print("outfile already exists, overwrite not permitted")
        sys.exit(1)
# print input file information
print("Input file info:")
fits.open(inname).info()
# print output file information
print("Output file info:")
newfile = fits.open(outname)
newfile.info()
# print end message
print("trim_uvfits ended properly")
        
