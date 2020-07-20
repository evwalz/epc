using Distributions
using NCDatasets
using DataStructures
using SpecialFunctions

for day in 1:365

	num = string(day)
	dsnew = Dataset("berngamma_" * num * ".nc","c")

# Define the dimension "lon" and "lat" with the size 100 and 110 resp.
	defDim(dsnew,"lon",3600)
	defDim(dsnew,"lat",800)

# Define a global attribute
	dsnew.attrib["title"] = "gamma distribution parameter of day " * num 

# Define the variables temperature with the attribute units
	v1 = defVar(dsnew,"shape",Float32,("lat","lon"), attrib = OrderedDict(
		"units" => "mm"))

	v2 = defVar(dsnew,"scale",Float32,("lat","lon"), attrib = OrderedDict(
		"units" => "mm"))

	v3 = defVar(dsnew,"prob",Float32,("lat","lon"), attrib = OrderedDict(
		"units" => "prob"))
# add additional attributes
	v1.attrib["comments"] = "this is shape parameter of gamma"
	v2.attrib["comments"] = "this is scale parameter of gamma"
	v3.attrib["comments"] = "this is prob of bernoulli gamma"


	ds = Dataset("epc15_" * num * ".nc4")
	v  = ds["precipitationCal"]
	enslen = size(v)[3]

#k = Array{Float64}(undef, 3600,2)
	for i in 1:800
		for j in 1:3600
			out = filter(x -> coalesce(x > 0, false), v[i,j,:])
			if length(unique(out)) > 1
				alpha = fit_mle(Gamma, convert(Array{Float64}, map(identity, out)))
    #k[i,:] = [shape(alpha), scale(alpha)]
				dsnew["shape"][i,j] = shape(alpha)
				dsnew["scale"][i,j] = scale(alpha)
				dsnew["prob"][i,j] = length(out)/enslen
			else
				dsnew["shape"][i,j] = 0
				dsnew["scale"][i,j] = 0
				dsnew["prob"][i,j] = 0
			end
    #p1 = cdf(Gamma(shape(alpha),scale(alpha)),obs)
    #p2 =  cdf(Gamma(shape(alpha),scale(alpha)+1),obs)
    #return(obs * (2 * p1 - 1) - scale(alpha) * (shape(alpha) * (2 * p2 - 1) + 1 / beta(0.5, shape(alpha))))
		end
	end
	close(dsnew)
end