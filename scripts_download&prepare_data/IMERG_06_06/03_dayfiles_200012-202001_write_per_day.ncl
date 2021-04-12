begin

; Calculate 06-06 UTC daily sums and write to output files (one file per day)

	do yyyy=2000,2020
		yyyym = yyyy-1
		if (yyyy.eq.2000) then
			mm1 = 12
		else
			mm1 = 1
		end if

		do mm=mm1,12
		
			mmm = mm-1
			mo  = sprinti("%02d",mm)
			mom = sprinti("%02d",mmm)

			ldd = days_in_month(yyyy,mm)

			diri = "IMERG_025_WORLD_month_files/"
			fili = diri+"3B-HHR.MS.MRG.3IMERG."+yyyy+""+mo+".V06B.025_WORLD.nc"
			ifile = addfile(fili,"r")
			ivar  = ifile->precipitationCal
			itime = ifile->time
			idate = cd_calendar(itime,0)
			iyyyy = toint(idate(:,0))
			imm = toint(idate(:,1))
			idd = toint(idate(:,2))
			ihh = toint(idate(:,3))
			imn = toint(idate(:,4))
			lon  = ifile->lon
			lat  = ifile->lat
			dim_lon = dimsizes(lon)
			dim_lat = dimsizes(lat)


			if (yyyy.eq.2000 .and. mm.eq.6) then
				dd1 = 2
			else
				dd1 = 1
			end if

			do dd=dd1,ldd
print(yyyy+" "+mm+" "+dd)		
				time = tofloat(dd-1)+0.25
				time@units = "days since "+yyyy+"-"+mo+"-01 00:00:00"
				ovar = new((/1,dim_lon,dim_lat/),"float")
				ovar!0 = "time"
				ovar&time = time
				ovar!1 = "lon"
				ovar&lon = lon
				ovar!2 = "lat"
				ovar&lat = lat
				ovar = 9.96921e+36
				ovar@_FillValue = 9.96921e+36
				ovar@units = "mm day-1"

				if (dd.eq.1 .and. mm.eq.1) then
print("Read mom file")
					fili2 = "mom_files/3B-HHR.MS.MRG.3IMERG."+yyyym+"12.V06B.025_WORLD_t.nc"
					ifile2 = addfile(fili2,"r")
					ivar2  = ifile2->precipitationCal
					dims = dimsizes(ivar2)
					dim0 = dims(0)
					tind = ind(iyyyy.eq.yyyy .and. imm.eq.mm .and. idd.eq.dd .and. ihh.eq.0 .and. imn.eq.0)
					ts = tind
					te = tind+11
					d = day_of_year(yyyy,mm,dd)
					d = d-1
print("Calculate sums")
					ovar(0,:,:) = ((/dim_sum_n(ivar2(dim0-36:dim0-1,:,:),0)/) + (/dim_sum_n(ivar(ts:te,:,:),0)/))/2.
					delete([/fili2,ifile2,ivar2,dims,dim0,tind,ts,te,d/])
				else if (dd.eq.1 .and. mm.ge.2) then
				     	fili2 = "mom_files/3B-HHR.MS.MRG.3IMERG."+yyyy+""+mom+".V06B.025_WORLD_t.nc"
					ifile2 = addfile(fili2,"r")
					ivar2  = ifile2->precipitationCal
					dims = dimsizes(ivar2)
					dim0 = dims(0)
					tind = ind(iyyyy.eq.yyyy .and. imm.eq.mm .and. idd.eq.dd .and. ihh.eq.0 .and. imn.eq.0)
					ts = tind
					te = tind+11
					d = day_of_year(yyyy,mm,dd)
					d = d-1
					ovar(0,:,:) = ((/dim_sum_n(ivar2(dim0-36:dim0-1,:,:),0)/) + (/dim_sum_n(ivar(ts:te,:,:),0)/))/2.
					delete([/fili2,ifile2,ivar2,dims,dim0,tind,ts,te,d/])
				else
					tind = ind(iyyyy.eq.yyyy .and. imm.eq.mm .and. idd.eq.dd .and. ihh.eq.0 .and. imn.eq.0)
					ts = tind-36
					te = tind+11
					d = day_of_year(yyyy,mm,dd)
					d = d-1
					ovar(0,:,:) = (/dim_sum_n(ivar(ts:te,:,:),0)/)/2.
					delete([/tind,ts,te,d/])
				end if
				end if
			
				dstring=sprinti("%02d",dd)
			
				ofile = addfile("IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day."+yyyy+""+mo+""+dstring+".V06B.025_WORLD.nc","c")
				ofile->precipitationCal = ovar(time|:,lat|:,lon|:)
				delete([/time,ovar,ofile/])

			end do
			

			delete([/mmm,mo,mom,ldd,diri,fili,ifile,ivar,itime,idate,iyyyy,imm,idd,ihh,imn,lon,lat,dim_lon,dim_lat/])

			if (yyyy.eq.2020 .and. mm.eq.1 .and. dd.eq.31) then
			   exit
			end if

		end do
	end do
end
