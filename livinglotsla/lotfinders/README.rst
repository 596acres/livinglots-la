Living Lots LA: Lot Finders
===========================

Original data documentation from C-Lab
--------------------------------------

1. Using the County Assessor's data as our base, we added 3 columns: 
    * Surplus Vacant (YES/NO),
    * Side Lots (YES/NO)
    * and Easement (YES/NO).

    Using the data sets from all three sources we labelled whether these
    categories were YES or NO.

    a. NOTE: The Surplus Data had been reduced previous to this addition
        because it contained parcels with and without structures on the site.
        This was done by filtering whether the given parcel was simply 
        "Surplus" or "Surplus Vacant"; only those labelled as "Surplus Vacant"
        were noted in our new column in the County Assessor Data
2. We filtered the data based on the Land Use column. We searched for any row
    with a private vacant land use code (100V, 010V, 300V, 200V) or with a 
    public vacant land use code (880V)
3. A column was added based upon the Weed Abatement (2012) data – no new
    parcels were added in. We simply stated whether a given parcel with a
    vacant use code was part of the 2012 Weed Abatement program or not. (i.e. 
    if a parcel was labelled as part of the Weed Abatement program but wasn't 
    categorized as vacant based on its use code, it is not in the data set)
4. We clipped a parcel shapefile which comprised the entire county to the
    shape of the city of LA based upon the boundaries in the Council
    District shapefile.
5. We then erased all parcels that overlapped with the park shapefile.
6. We joined the County Assessor data to the parcel shapefile, eliminating
    all parcels that were not in the modified County Assessor data set.
7. We visualized the building footprint data and highlighted all vacant parcels
    that contained a building (Select by Location). All parcels that contained
    a building on them were deleted from the data set.
8. Using the Join function we added the zoning data to the attribute table of
    the modified County Assessor data

How lot finders match this documentation
----------------------------------------

**VacantParcelFinder**:
* Filter by use code (step 2)
* Parcels are already clipped to the city (step 4)
* Parcels are compared with ProtectedAreas (step 5), not added as lots if they
  are present
