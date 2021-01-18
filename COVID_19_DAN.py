#%% Header
import urllib.request
from pathlib import Path


# source = 'json'
source = 'csv'

id_dan = 354
id_lg = 355
id_filter = (id_dan, id_lg)

filedir = Path(__file__).parent

lg_path=filedir.joinpath("covid19_lg.txt")
dan_path=filedir.joinpath("covid19_dan.txt")

path_dict={id_dan: dan_path, id_lg: lg_path}

url_json = "https://www.apps.nlga.niedersachsen.de/corona/download.php?json"
url_csv =  "https://www.apps.nlga.niedersachsen.de/corona/download.php?csv"

url_csv_historie = "https://www.apps.nlga.niedersachsen.de/corona/download.php?csv_tag_region"


dateformate2="(%Y, %m, %d)"
dateformate="%Y-%m-%d %H:%M:%S"

import datetime as dt


print(f"File Path: {__file__}")
print(f"CWD: {Path('').cwd()}")
# Ich habe diesmal eine Klasse probiert, in der fast alle Funktionen definiert sind.
class landkreis_covid_datensatz:
    """Covid 19 Daten eines Landkreises."""
    def __init__(self, id):

        # self.properties={"id":int(0), "gkz":"", "name":"", "value":int(0), "incedence" : float(0), "diff":int(0)}
        self.now = None
        self.lastupdate = None
        self.update_ref_time = dt.time(13,30)
        self.properties={}
        self.database_updated_at=0
        self.id = id
        self.name = ""
        self.anzahl = 0
        self.differenz = 0
        self.inzidenz = 0
        self.deceased = 0
        self.deceased_diff = 0
        self.anzahl_flaeche = 0
        self.anzahl_7tage = 0
        self.inzidenz_7tage = 0
        self.pfad = path_dict[id]
        
    def get_items(self, itemlist):
        self.name = itemlist[0]
        self.anzahl = int(itemlist[1])
        self.differenz = int(itemlist[2])
        self.inzidenz = float(itemlist[3])
        self.deceased = int(itemlist[4])
        self.deceased_diff = int(itemlist[5])
        self.anzahl_flaeche = float(itemlist[6])
        self.anzahl_7tage = float(itemlist[7])
        self.inzidenz_7tage = float(itemlist[8])
        
    def read_last_line(self):
        if covid.pfad.exists():
            with self.pfad.open(mode='r') as f:
                for last_line in f.readlines():
                    pass
                return last_line
        else:
            return ""
        
    def check_if_update(self):
        ## CSV

        
        # self.lastupdate = dt.datetime.fromtimestamp(self.pfad.stat().st_mtime)
        last_line_str=self.read_last_line()
        list_last_line=last_line_str.strip()[1:-1].split(',')
        self.lastupdate=dt.datetime.strptime(list_last_line[0].strip('\''),dateformate)
        
        
        lastupdate = self.lastupdate
        now = self.now
        update_ref_time = self.update_ref_time
        
        date_delta = now.date() - lastupdate.date()
        


        if source == 'csv':
            heute=dt.date.today()
            rev_zeit = dt.time(13,30)
            rev_zeit = dt.datetime.combine(heute, rev_zeit)
            print(f'Rev_Zeit: {self.update_ref_time}')
            print(f'Last_Update Zeit: {self.lastupdate}')
            print(f'Now: {self.now}')
            print(f'Delta: {date_delta}')
            if date_delta > dt.timedelta(days=1) : # Vorgestern letztes Update (immerr update)
                return True
            
            if date_delta == dt.timedelta(days=1) : #Gestern letztes Update
                if now.time() > update_ref_time: # Wenn heute die Referenzzeit schon überschritten ist.
                    return True 
                if lastupdate.time() < update_ref_time:
                    return True
                    
            if date_delta == dt.timedelta(days=0) : #Heute letztes Update 
                # Nur Update, wenn heute einmal vor und einmal nach der RefZeit aufgerufen wurde.
                if now.time() > update_ref_time and lastupdate.time() < update_ref_time:
                    return True
                
            return False
            
            # print(self.updated_at)
            # if rev_zeit > lastupdate:
            #     if self.updated_at > rev_zeit:
            #         return True
            # return False
        
        # if source == 'json':
        #     ## JSON
        #     if self.updated_at == 0:
        #         if self.read_last_line() == self.get_filestr():
        #             return False
        #         else:
        #             return True
        #     else:
        #         if self.updated_at > lastupdate:
        #             return True
        #         else:
        #             return False

    def return_last_5_lines(self):
        text = self.pfad.read_text()
        # list_of_lines = text.splitlines(keepends=True)
        list_of_lines = text.splitlines()
        # print(*list_of_lines[-5:])
        print(*list_of_lines[-5:], sep = '\n')
        print('\n' * 2)


    def get_filestr(self):
        # import datetime as dt
        list=[  self.database_updated_at.strftime(dateformate),
                self.anzahl,
                self.differenz, 
                self.inzidenz, 
                self.name, 
                self.deceased, 
                self.deceased_diff,
                self.anzahl_flaeche,
                self.anzahl_7tage,
                self.inzidenz_7tage
                ]
        return str(list)+"\n"

    def apend_to_file(self):
        with self.pfad.open(mode='a') as f:
            f.write(self.get_filestr())
            
    def do_it(self):
        print("#"*80)
        if self.check_if_update() == True:
            # self.datum=self.updated_at
            print(f"Es gibt neue Daten aus {self.name}:")
            print("#"*80)
            print(f"Es sind {self.differenz} neue Fälle, also insgesamt {self.anzahl} Fälle und {self.inzidenz} pro 100.000 Einwohner.\n")
            self.apend_to_file()
        else:
            print(f"Es gibt keine neuen Daten aus {self.name}:")
            print("#"*80)
            print(f"Weiterhin sind es {self.anzahl} Fälle bei {self.inzidenz} Fällen pro 100.000 Einwohner.\n")
            
        self.return_last_5_lines()


#%% Fill list every day
###############################################################################
# Erstelle ein dict mit den IDs als Key und einer Liste der restlichen Einträge als Value.
        
        
if __name__ == "__main__":       
            
    dict_items={}
    
    now = dt.datetime.now()
    
    if source == 'csv':
        ###############################################################################
        # Das ist die CSV Variante
        with urllib.request.urlopen(url_csv) as url_handler:
            import csv
            # CSV Liste von der Website laden und einlesen.
            # Wichtig, splitlines zu verwenden, da mit csv.reader() keine Datei 
            # eingelsen wird, sondern ein str Objekt.
            csv_data=url_handler.read().decode()
            csv_data = csv_data.strip().splitlines()
            # update_time=datetime.datetime.strptime(json_data["updated_at"],dateformate_json)
            update_time=now
            csv_reader = csv.reader(csv_data, delimiter=';', quotechar='"')
            # csv_dict = csv.DictReader(csv_data, delimiter=';', quotechar='"')
            # dict_items2 = {}
            # for line in csv_dict:
                # dict_items2[line["id"]] = line
            # print(dict_items2.keys())
            for nb, line in enumerate(csv_reader):
                if nb == 0:
                    id_pos = line.index("id")
                    gkz_pos = line.index("GKZ")
                    name_pos = line.index("Landkreis")
                    faelle_pos = line.index("bestätigte Fälle")
                    dif_pos = line.index("Änderung zum Vortag")
                    inzidenz_pos = line.index("Fälle pro 100.000 Einwohner")
                    deceased_pos = line.index("verstorbene Fälle")
                    deceased_diff_pos = line.index("verstorbene Fälle Änderung zum Vortag")
                    anzahl_flaeche_pos = line.index("Fälle pro Fläche (pro 100 km²)")
                    anzahl_7tage_pos = line.index("Fälle vergangene 7 Tage")
                    inzidenz_7tage_pos = line.index("Fälle vergangene 7 Tage pro 100.000 Einwohner")
                    
                    
                else:
                    dict_items[ int(line[id_pos])]=[    line[name_pos], 
                                                        int(line[faelle_pos]), 
                                                        int(line[dif_pos]), 
                                                        float(line[inzidenz_pos]), 
                                                        int(line[deceased_pos]), 
                                                        int(line[deceased_diff_pos]), 
                                                        float(line[anzahl_flaeche_pos]),
                                                        float(line[anzahl_7tage_pos]),
                                                        float(line[inzidenz_7tage_pos])
                                                    ]
    
    if source == 'json':
    ###############################################################################
    # Das ist die JSON Variante mit dem JSON Modul
        dateformate_json="%Y-%m-%dT%H:%M:%S%z"
        json_lk_dict={}
        with urllib.request.urlopen(url_json) as url_handler:
            import json
            import datetime as dt
            json_data=json.load(url_handler)
            update_time=dt.datetime.strptime(json_data["updated_at"],dateformate_json)
            for entry in json_data["features"]:
                json_lk_dict[entry["properties"]["id"]]=entry["properties"]
                dict_items[entry["properties"]["id"]]=[entry["properties"]["name"],
                                                       int(entry["properties"]["value"]),
                                                       int(entry["properties"]["diff"]),
                                                       float(entry["properties"]["incidence"]),
                                                       int(entry["properties"]["deceased"]),
                                                       int(entry["properties"]["deceased_diff"])]
    
    
    
    ###############################################################################
    # Für alle gewünschten Landkreise die Liste aktualisieren.
    for id in id_filter:
        covid = landkreis_covid_datensatz(id)
        covid.get_items(dict_items[id])
        # covid.properties=json_lk_dict[id]
        covid.now = now.replace(tzinfo=None)
        covid.database_updated_at=update_time.replace(tzinfo=None)
        covid.do_it()
    
    
    #%% Plot Inzdenz Verlauf
    
    ###############################################################################
    # Erstelle list mit der Inzidenz über alle Wochen
    
    verlauf_dict = {}
    with urllib.request.urlopen(url_csv_historie) as url_handler:
        import csv
        import datetime as dt
        # CSV Liste von der Website laden und einlesen.
        # Wichtig, splitlines zu verwenden, da mit csv.reader() keine Datei 
        # eingelsen wird, sondern ein str Objekt.
        csv_data=url_handler.read().decode()
        csv_data = csv_data.strip().splitlines()
        # update_time=datetime.datetime.strptime(json_data["updated_at"],dateformate_json)
        update_time=dt.datetime.now()
        csv_dict = csv.DictReader(csv_data, delimiter=';', quotechar='"')
        for line in csv_dict:
            if int(line['id']) in id_filter :
                try:
                    d = [int(x) for x in line["Meldedatum"].split('.')]
                    datum = dt.datetime(d[2], d[1], d[0])
                    data = line
                    verlauf_dict[line["id"]].update({datum : data})
                except KeyError:
                    verlauf_dict[line["id"]] = {datum : data}
    

    
    
    dan_verlauf = verlauf_dict[str(id_dan)]
    lg_verlauf = verlauf_dict[str(id_lg)]
    
    # for keys in sorted(dan_verlauf):
        # print(keys)
        
    from bokeh.plotting import figure, output_file, show
    from bokeh.models import BoxAnnotation
    
    # output to static HTML file
    output_file("COVID_INZIDENZ.html")
    
    low_box = BoxAnnotation(top=35, fill_alpha=0.1, fill_color='green')
    mid_box = BoxAnnotation(bottom=35, top=50, fill_alpha=0.1, fill_color='yellow')
    high_box = BoxAnnotation(bottom=50, top=100, fill_alpha=0.1, fill_color='red')
    ver_high_box = BoxAnnotation(bottom=100, fill_alpha=0.1, fill_color='purple')
    
    
    x = list([i   for i, val in enumerate(sorted(dan_verlauf))])
    key = list([val   for i, val in enumerate(sorted(dan_verlauf))])
    y_dan = list([float(dan_verlauf[i]["7-Tagesinzidenz pro 100.000 Einwohner"]) for i in key])
    y_lg = list([float(lg_verlauf[i]["7-Tagesinzidenz pro 100.000 Einwohner"]) for i in key])
    y_faelle_lg = list([float(lg_verlauf[i]["bestätigte Fälle"]) for i in key])
    y_faelle_dan = list([float(dan_verlauf[i]["bestätigte Fälle"]) for i in key])

    # create a new plot with a title and axis labels
    p = figure(plot_width=1500, plot_height=700, title="COVID_INZIDENZ",x_axis_type='datetime', x_axis_label='x', y_axis_label='y', y_range= (0, int(max(y_dan+y_lg))+10))
    
    

    # add a line renderer with legend and line thickness
    p.step(x=key, y=y_dan, legend_label="DAN Inzidenz", line_width=2, color='green')
    p.step(x=key, y=y_lg, legend_label="LG Inzidenz",  line_width=2, color='red')
    p.vbar(x=key, top=y_faelle_lg, bottom=0, width=0.5, legend_label="LG new cases", color='yellow')
    p.vbar(x=key, top=y_faelle_dan, bottom=0, width=0.5, legend_label="DAN new cases", color='orange')
    

    p.add_layout(low_box)
    p.add_layout(mid_box)
    p.add_layout(high_box)
    p.add_layout(ver_high_box)
    
    # x_2 = [{'days':1},{'days':2},{'days':3}]
    # y_2 = [1,2,3]    
    # p.step(x=x_2, y=y_2)
    p.legend.location  = 'top_left'
    
    
    # show the results
    show(p)
    
    
    # import pandas as pd
    # data_csv = pd.read_csv(url_csv, sep=";")
    # data_csv.describe()
    # print(data_csv)
    
    # data_json = pd.read_json(url_json)
    
    # print(data_json)

