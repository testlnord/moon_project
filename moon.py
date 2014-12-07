#!/usr/bin/env python3
from moon_scripts.merge_with_moon import merge
from moon_scripts.moon_getter import get_moon
from moon_scripts.prepair_moon import prepair_moon

def main():
    get_moon((51,30), (0,7), "london", timezone=0)
    prepair_moon("london", 0)
    merge("data/GOLDAMGBD228NLBM.csv", "london")
    pass

if __name__ == "__main__":
    main()
