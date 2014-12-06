import csv
import datetime

sp_moon = []
with open("ny_moon_dates.csv") as ny_csv:
    with open("GOLDAMGBD228NLBM.csv") as sp_csv:
        sp_inp = csv.reader(sp_csv)
        next(sp_inp) # ignore header
        ny_inp = csv.reader(ny_csv)
        moon_ny = [(datetime.datetime.strptime(d, "%Y %b %d  %H:%M"),m) for d,m in ny_inp]
        fool_moon = [k.date() for k,p in moon_ny if p == '1d']
        for sd, val in sp_inp:
            sd = datetime.datetime.strptime(sd, "%Y-%m-%d").date()
            msd = None
            try:
                v = float(val)
            except ValueError:
                continue

            for md, pn in moon_ny:
                if md.date() == sd:
                    msd = pn
                    break
            if msd is not None:
                sp_moon.append((sd, val, msd, sd in fool_moon))

with open("merged_moon_sp.csv", 'w') as msp_file:
    msp_writer = csv.writer(msp_file)
    msp_writer.writerows(sp_moon)