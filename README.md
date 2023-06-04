# Multi-threaded-Vis-traversal
This is a simple multi-threaded vegetation index traversal method, which can simply and quickly mine hyperspectral data information, construct the best vegetation index and its combination.The source of the 30 vegetation index calculation methods used in the program is as follows:
	Index form	       Long_name	                      Formula	
	NDVI	Normalized Difference Vegetation Index	(b1 – b2) / (b1 + b2)	[1]

	TDVI	Transformed Difference Vegetation Index	1.5×((b1 – b2)/((b1 2 + b22 + 0.5) 0.5))	[2]

	NIRv	Near-Infrared Reflectance of Vegetation	((b1 - b2) / (b1 + b2)) × b1 	[3]

	MSI	Moisture Stress Index	b2/ b1	[4]

	MGRVI	Modified Green Red Vegetation Index	(b12 – b22) / (b12 + b22)	[5]

	IPVI	Infrared Percentage Vegetation Index	b2 / (b2 + b1)	[6]

	EVI2	Two-Band Enhanced Vegetation Index	2.5×(b2 – b1) / (b2 + 2.4×b1 + 6)	[7]

	DVI	Difference Vegetation Index	b2 – b1	[8]

	CIG	Chlorophyll Index Green	(b2 / b1) - 1.0	[9]

	CSI	Char Soil Index	b1/b2	[10]

	BAI	Burned Area Index	1.0 / ((0.1 – b1) 2 + (0.06 – b2) 2)	[11]

	ARI	Anthocyanin Reflectance Index	(1 / b1) - (1 / b2)	[12]

  ARI2	Anthocyanin Reflectance Index 2	b3×((1 /b1) - (1 / b2))	[12]

	ARVI	Atmospherically Resistant Vegetation Index	(b3 - (b2- 2.5×(b2 – b1))) / (b3 + (b2 -2.5×(b2 – b1)))	[13]

	SWI	Snow Water Index	(b1×(b2 – b3)) / ((b1 + b2) ×(b2 + b3))	[14]

	EBBI	Enhanced Built-Up and Bareness Index	(b2 – b1) / (10.0 ×((b3 + b2) 0.5))	[15]

	EVI	Enhanced Vegetation Index	2.5 × (b3 – b2) / (b3 + 6×b2 – 7.5×b1 + 1)	[16]

	GBNDVI	Green-Blue Normalized Difference Vegetation Index	(b3 - (b2 + b1)) / (b3+ (b2 + b1))	[17]

	GLI	Green Leaf Index	(2.0×b3 – b2 – b1) / (2.0 * b3 + b2 + b1)	[18]

	MBI	Modified Bare Soil Index	((b2 – b3 – b1) / (b2 + b3 + b1)) + 0.5	[19]

	PSRI	Plant Senescing Reflectance Index	(b2 – b1)/b3	[20]

	BaI	Bareness Index	b1+b3-b2	[21]

  BLFEI	Built-Up Land Features Extraction Index	(((b1+b2+b4)/3.0)-b3) / (((b1+b2+b4) / 3.0) + b3)	[22]

	BI	Bare Soil Index	((b4 + b2) - (b3 + b1)) / ((b4 + b2) + (b3 + b1))	[23]

	DBI	Dry Built-Up Index	((b1 – b4) / (b1 + b4)) - ((b3 - b2 ) / (b3 + b2))	[24]

	DBSI	Dry Bareness Index	((b4 – b1) / (b1 + b4)) - ((b3 – b2) / (b3 + b2))	[24]

	EMBI	Enhanced Modified Bare Soil Index	((((b3 – b4 – b2) / (b3 + b4 + b2)) + 0.5) - ((b1 – b3) / (b1 + b3)) - 0.5) / ((((b3 – b4 – b2) / (b3 + b4 + b2)) + 0.5) + ((b1 – b3) / (b1 + b3)) + 1.5)	[25]

	FCVI	Fluorescence Correction Vegetation Index	b4 - ((b1 + b2 + b3) / 3.0)	[26]

	GARI	Green Atmospherically Resistant Vegetation Index	(b4 - (b1 - (b2 – b3))) / (b4 - (b1 + (b2 – b3)))	[27]

	WRI	Water Ratio Index	(b1 + b2) / (b3 + b4)	[28]
[1]	J. W. H. Rouse, R.H.; Schell, J.A.; Deering, D.W. , "Monitoring vegetation systems in the great plains with ERTS," NASA Spéc. Pub, vol. l. 1974, 1, no. 309–317, 1974.
[2]	 A. Bannari, H. Asalhi, and P. M. Teillet, "Transformed difference vegetation index (TDVI) for vegetation cover mapping," in IEEE International Geoscience and Remote Sensing Symposium, 24-28 June 2002 2002, vol. 5, pp. 3053-3055 vol.5, doi: 10.1109/IGARSS.2002.1026867. 
[3]	G. Badgley, C. B. Field, and J. A. Berry, "Canopy near-infrared reflectance and terrestrial photosynthesis," Science advances, vol. 3, no. 3, p. e1602244, 2017.
[4]	E. R. Hunt and B. N. Rock, "Detection of changes in leaf water content using Near- and Middle-Infrared reflectances," Remote Sensing of Environment, vol. 30, no. 1, pp. 43-54, 1989/10/01/ 1989, doi: 10.1016/0034-4257(89)90046-1.
[5]	J. Bendig et al., "Combining UAV-based plant height from crop surface models, visible, and near infrared vegetation indices for biomass monitoring in barley," International Journal of Applied Earth Observation and Geoinformation, vol. 39, pp. 79-87, Jul 2015, doi: 10.1016/j.jag.2015.02.012.
[6]	R. E. Crippen, "Calculating the vegetation index faster," Remote Sensing of Environment, vol. 34, no. 1, pp. 71-73, 1990/10/01/ 1990, doi: 10.1016/0034-4257(90)90085-Z.
[7]	Z. Jiang, A. R. Huete, K. Didan, and T. Miura, "Development of a two-band enhanced vegetation index without a blue band," Remote Sensing of Environment, vol. 112, no. 10, pp. 3833-3845, 2008/10/15/ 2008, doi: 10.1016/j.rse.2008.06.006.
[8]	J.-L. Roujean and F.-M. Breon, "Estimating PAR absorbed by vegetation from bidirectional reflectance measurements," Remote Sensing of Environment, vol. 51, no. 3, pp. 375-384, 1995/03/01/ 1995, doi: 10.1016/0034-4257(94)00114-3.
[9]	A. A. Gitelson, Y. Gritz, and M. N. Merzlyak, "Relationships between leaf chlorophyll content and spectral reflectance and algorithms for non-destructive chlorophyll assessment in higher plant leaves," Journal of Plant Physiology, vol. 160, no. 3, pp. 271-282, Mar 2003, doi: 10.1078/0176-1617-00887.
[10]	A. M. S. Smith, M. J. Wooster, N. A. Drake, F. M. Dipotso, M. J. Falkowski, and A. T. Hudak, "Testing the potential of multi-spectral remote sensing for retrospectively estimating fire severity in African Savannahs," Remote Sensing of Environment, vol. 97, no. 1, pp. 92-115, 2005/07/15/ 2005, doi: 10.1016/j.rse.2005.04.014.
[11]	E. Chuvieco and M. P. Martín, "Cartografía de grandes incendios forestales en la Península Ibérica a partir de imágenes NOAA-AVHRR," 1998.
[12]	A. A. Gitelson, M. N. Merzlyak, and O. B. Chivkunova, "Optical properties and nondestructive estimation of anthocyanin content in plant leaves," Photochemistry and Photobiology, vol. 74, no. 1, pp. 38-45, Jul 2001, doi: 10.1562/0031-8655(2001)074<0038:Opaneo>2.0.Co;2.
[13]	R. N. X. Zhang Ren-hua and L. K. N, "Approach for a Vegetation Index Resistant to Atmospheric Effect," J Integr Plant Biol, vol. 38, no. 1, pp. , 1996. [Online]. Available: {https://www.jipb.net/CN/abstract/article_23925.shtml}.
[14]	A. Dixit, A. Goswami, and S. Jain, "Development and Evaluation of a New “Snow Water Index (SWI)” for Accurate Snow Cover Delineation," Remote Sensing, vol. 11, no. 23, doi: 10.3390/rs11232774.
[15]	A. R. As-syakur, I. W. S. Adnyana, I. W. Arthana, and I. W. Nuarsa, "Enhanced Built-Up and Bareness Index (EBBI) for Mapping Built-Up and Bare Land in an Urban Area," Remote Sensing, vol. 4, no. 10, pp. 2957-2970, 2012. [Online]. Available: https://www.mdpi.com/2072-4292/4/10/2957.
[16]	A. R. Huete, H. Q. Liu, K. Batchily, and W. van Leeuwen, "A comparison of vegetation indices over a global set of TM images for EOS-MODIS," Remote Sensing of Environment, vol. 59, no. 3, pp. 440-451, 1997/03/01/ 1997, doi: 10.1016/S0034-4257(96)00112-5.
[17]	F.-m. Wang, J.-f. Huang, Y.-l. Tang, and X.-z. Wang, "New Vegetation Index and Its Application in Estimating Leaf Area Index of Rice," Rice Science, vol. 14, no. 3, pp. 195-203, 2007/09/01/ 2007, doi: 10.1016/S1672-6308(07)60027-4.
[18]	M. Louhaichi, M. M. Borman, and D. E. Johnson, "Spatially located platform and aerial photography for documentation of grazing impacts on wheat," Geocarto International, vol. 16, no. 1, pp. 65-70, 2001.
[19]	C. T. Nguyen, A. Chidthaisong, P. Kieu Diem, and L.-Z. Huo, "A Modified Bare Soil Index to Identify Bare Land Features during Agricultural Fallow-Period in Southeast Asia Using Landsat 8," Land, vol. 10, no. 3, p. 231, 2021. [Online]. Available: https://www.mdpi.com/2073-445X/10/3/231.
[20]	M. N. Merzlyak, A. A. Gitelson, O. B. Chivkunova, and V. Y. Rakitin, "Non-destructive optical detection of pigment changes during leaf senescence and fruit ripening," Physiologia Plantarum, Article vol. 106, no. 1, pp. 135-141, May 1999, doi: 10.1034/j.1399-3054.1999.106119.x.
[21]	 L. Haobo, W. Jindi, L. Suhong, Q. Yonghua, and W. Huawei, "Studies on urban areas extraction from landsat TM images," in Proceedings. 2005 IEEE International Geoscience and Remote Sensing Symposium, 2005. IGARSS '05., 29-29 July 2005 2005, vol. 6, pp. 3826-3829, doi: 10.1109/IGARSS.2005.1525743. 
[22]	R. Bouhennache, T. Bouden, A. Taleb-Ahmed, and A. Cheddad, "A new spectral index for the extraction of built-up land features from Landsat 8 satellite imagery," Geocarto International, vol. 34, no. 14, pp. 1531-1551, 2019/12/06 2019, doi: 10.1080/10106049.2018.1497094.
[23]	M. An, P. Xie, W. He, B. Wang, J. Huang, and R. Khanal, "Spatiotemporal change of ecologic environment quality and human interaction factors in three gorges ecologic economic corridor, based on RSEI," Ecological Indicators, vol. 141, p. 109090, 2022/08/01/ 2022, doi: 10.1016/j.ecolind.2022.109090.
[24]	A. Rasul et al., "Applying Built-Up and Bare-Soil Indices from Landsat 8 to Cities in Dry Climates," Land, vol. 7, no. 3, p. 81, 2018. [Online]. Available: https://www.mdpi.com/2073-445X/7/3/81.
[25]	Y. Zhao and Z. Zhu, "ASI: An artificial surface Index for Landsat 8 imagery," International Journal of Applied Earth Observation and Geoinformation, vol. 107, p. 102703, 2022/03/01/ 2022, doi: 10.1016/j.jag.2022.102703.
[26]	P. Yang, C. van der Tol, P. K. E. Campbell, and E. M. Middleton, "Fluorescence Correction Vegetation Index (FCVI): A physically based reflectance index to separate physiological and non-physiological information in far-red sun-induced chlorophyll fluorescence," Remote Sensing of Environment, vol. 240, p. 111676, 2020/04/01/ 2020, doi: 10.1016/j.rse.2020.111676.
[27]	A. A. Gitelson, Y. J. Kaufman, and M. N. Merzlyak, "Use of a green channel in remote sensing of global vegetation from EOS-MODIS," Remote Sensing of Environment, vol. 58, no. 3, pp. 289-298, Dec 1996, doi: 10.1016/s0034-4257(96)00072-7.
[28]	 L. Shen and C. Li, "Water body extraction from Landsat ETM+ imagery using adaboost algorithm," in 2010 18th International Conference on Geoinformatics, 18-20 June 2010 2010, pp. 1-4, doi: 10.1109/GEOINFORMATICS.2010.5567762. 


  

