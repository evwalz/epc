begin
	ifile = addfile("in.nc","r")
	ivar  = ifile->precipitationCal(:,:,{-39.95:39.95})

	ofile = addfile("out.nc","c")
	ofile->precipitationCal = ivar

end
quit