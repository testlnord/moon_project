import re
import urllib.request
import gzip


def unwrap_coord(coord):
    sign = '1' if coord[0] > 0 else '-1'
    deg = str(abs(coord[0]))
    min = str(int(coord[1]))
    return sign, deg, min

def get_moon(apt, log, filename=None, from_year=2004, to_year=2015, timezone=0):
    table_re = re.compile(".*<pre>(.*)</pre>.*")
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '87',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'aa.usno.navy.mil',
        'Origin': 'http://aa.usno.navy.mil',
        'Referer': 'http://aa.usno.navy.mil/data/docs/RS_OneYear.php',
        'User-Agent':
            'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
    }
    if filename is None:
        filename = "moon"+str(apt)+"_"+str(log)+".txt"
    with open(filename,"w") as outfile:
        for year in range(from_year, to_year):
            sa, da, ma = unwrap_coord(apt)
            sl, dl, ml = unwrap_coord(log)
            req = "FFX=2&xxy={0}&type=1&place=&xx0={1}&xx1={2}&xx2={3}&yy0={4}&yy1={5}&yy2={6}&zz1={8}&zz0={7}&ZZZ=END".format(
                str(year),
                sa,da,ma,
                sl,dl,ml,
                '1' if timezone > 0 else '-1',
                str(abs(timezone))
            )
            r = urllib.request.Request("http://aa.usno.navy.mil/cgi-bin/aa_rstablew.pl",
                                       data=req.encode(),
                                       headers=headers, method='POST')
            response = urllib.request.urlopen(r)
            html_raw = response.read()
            try:
                html_text = gzip.decompress(html_raw)
            except OSError:
                html_text = html_raw
            html_text = html_text.decode()
            is_text = False
            for line in html_text.splitlines():
                if line.startswith("<pre>") or line.startswith("</pre>"):
                    is_text = not is_text
                    continue
                if is_text:
                    outfile.write(line+'\n')


    pass

get_moon((51,30), (0,7), "london_moon.txt", timezone=0)