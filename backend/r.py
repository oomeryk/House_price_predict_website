

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.model_selection import train_test_split, GridSearchCV,cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

from xgboost import XGBRegressor







data = pd.read_excel("adverts1-2.xlsx")

data = data.drop("Unnamed: 0", axis=1)
df = data


df = pd.get_dummies(df, columns=["room"], prefix=["room"])


# Apply LabelEencoder transformation for 'city', 'district', 'neighborhood'
from sklearn.preprocessing import LabelEncoder
# Create a LabelEncoder object
le = LabelEncoder()

# Encode the string column 'city'
df['city_le'] = le.fit_transform(df['city'])

# Encode the string column 'district'
df['district_le'] = le.fit_transform(df['district'])

# Encode the string column 'neighborhood'
df['neighborhood_le'] = le.fit_transform(df['neighborhood'])


df = df.drop(["city","district","neighborhood"], axis=1)


# Define dependet and independet variables

y = df["price"]
x = df.drop("price", axis=1)


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


xgb_tuned = XGBRegressor(colsample_bytree = 0.6, 
                        learning_rate = 0.1, 
                        max_depth = 6, 
                        n_estimators = 1000) 

xgb_tuned = xgb_tuned.fit(x_train,y_train)
y_pred = xgb_tuned.predict(x_test)


#######################3
def pred_price(city, district, neighborhood, room, metrekare):


    d = data

    if metrekare=="" and room=="1+0": 
        metrekare=40
        #print(f"       m²={metrekare} olarak hesaba katıldı!")
    elif metrekare=="" and room=="1+1": 
        metrekare=65
        #print(f"       m²={metrekare} olarak hesaba katıldı!")
    elif metrekare=="" and room=="2+1": 
        metrekare=100
        #print(f"       m²={metrekare} olarak hesaba katıldı!")
    elif metrekare=="" and room=="3+1": 
        metrekare=130
        #print(f"       m²={metrekare} olarak hesaba katıldı!")
    elif metrekare=="" and room=="4+1": 
        metrekare=160
        #print(f"       m²={metrekare} olarak hesaba katıldı!")
    elif metrekare=="" and room=="": 
        metrekare=110
        #print(f"       m²={metrekare} olarak hesaba katıldı!")
    else: 
        pass
  
    new = pd.DataFrame({"city":[city], "district":[district], "neighborhood":[neighborhood], "room":[room], "m²":[metrekare]})
    new["m²"] = pd.to_numeric(new["m²"])
       
    dff = d.drop("price", axis=1)
    dff = pd.concat([dff, new], axis=0)

    dff[""] = np.arange(len(dff))
    dff = dff.set_index("")


    # Get dummies the string column"room"
    dff = pd.get_dummies(dff, columns=["room"], prefix=["room"])

    # Encode the string column'city'
    dff['city_le'] = le.fit_transform(dff['city'])
    
    # Encode the string column'district'
    dff['district_le'] = le.fit_transform(dff['district'])
    
    # Encode the string column'neighborhood'
    dff['neighborhood_le'] = le.fit_transform(dff['neighborhood'])

    dff =dff.drop(["city","district","neighborhood"], axis=1)



    if room=="":
        dff = dff.drop("room_", axis=1)
        
    if room=="1+0": room2=1
    elif room=="1+1": room2=3
    elif room=="2+1": room2=5
    elif room=="3+1": room2=7
    elif room=="4+1": room2=9
    else: pass


    # len(data) = 27118 = index of last row
    train_data = dff.iloc[27118:,:]
    pred = xgb_tuned.predict(train_data)




  ########################################################################

  #########################################################################

    # write advertising infos according to inputs entered by user
    if city=="" and room!="":
        a=d[d["room"]==room]
        return (f"\nTürkiye'de tahmini {room} kira fiyatı: {int(pred[0])} TL\n")     
        
        #print(f"\nTürkiye'de toplam {len(a)} tane {room} ilan var.\n\n----------------------------")
    
    elif district=="" and room!="":
        a=d[d["city"]==city]
        a=a[a["room"]==room]
        return (f"\n{city} şehrinde tahmini {room} kira fiyatı: {int(pred[0])} TL\n")     
        """
        if len(a)>=5: 
            last_q = a["price"].quantile(0.75) / a["m²"].quantile(0.75)
            first_q = a["price"].quantile(0.25) / a["m²"].quantile(0.25)
            print(f"\nOrtalama metrekare fiyatı {int(first_q)}TL - {int(last_q)}TL aralığında.")
        else: pass
        """
        #print(f"\nEn düşük fiyat: {a['price'].min()} \nEn yüksek fiyat: {a['price'].max()}\n")
        #print(f"{city} ilinde toplam {len(a)} tane {room} ilan var.\n\n----------------------------")
   
    elif neighborhood=="" and room!="":
        a=d[d["district"]==district]
        a=a[a["room"]==room]
        return (f"\n{district} ilçesinde tahmini {room} kira fiyatı: {int(pred[0])} TL\n")     
        """
        if len(a)>=5: 
            last_q = a["price"].quantile(0.75) / a["m²"].quantile(0.75)
            first_q = a["price"].quantile(0.25) / a["m²"].quantile(0.25)
            print(f"\nOrtalama metrekare fiyatı {int(first_q)}TL - {int(last_q)}TL aralığında.")
        else: pass
        
        print(f"\nEn düşük fiyat: {a['price'].min()} \nEn yüksek fiyat: {a['price'].max()}\n")
        print(f"{district} ilçesinde toplam {len(a)} tane {room} ilan var.\n\n----------------------------")
        a=a.sort_values(by="price", ascending=True)
        print(f"\nGirilen bilgilere göre Emlakjet sitesindeki ilanlar 'Artan fiyata göre sıralı':\n\n{a.to_string(index=False)}")
        """
    elif neighborhood != "" and room!="":
        a=d[d["district"]==district]
        a=a[a["neighborhood"]==neighborhood]
        a=a[a["room"]==room]
        return (f"\n{neighborhood} mahallesinde tahmini {room} kira fiyatı: {int(pred[0])} TL\n")     
        """
        if len(a)>=5: 
            last_q = a["price"].quantile(0.75) / a["m²"].quantile(0.75)
            first_q = a["price"].quantile(0.25) / a["m²"].quantile(0.25)
            print(f"\nOrtalama metrekare fiyatı {int(first_q)}TL - {int(last_q)}TL aralığında.")
        else: pass

        print(f"\nEn düşük fiyat: {a['price'].min()} \nEn yüksek fiyat: {a['price'].max()}\n")
        print(f"{neighborhood} mahallesinde toplam {len(a)} tane {room} ilan var.\n\n----------------------------")
        a=a.sort_values(by="price", ascending=True)
        print(f"\nGirilen bilgilere göre Emlakjet sitesindeki ilanlar 'Artan fiyata göre sıralı':\n\n{a.to_string(index=False)}")
        """
    
    elif room=="" and city=="":
        return (f"\nTürkiye'de tahmini kira fiyatı: {int(pred[0])} TL\n")     
        #print(f"Türkiye'de toplam {len(d)} tane ilan var.\n\n----------------------------")
    
    elif room == "" and district=="":
        a=d[d["city"]==city]
        return (f"\n{city} şehrinde tahmini kira fiyatı: {int(pred[0])} TL\n")     
        """
        if len(a)>=5: 
            last_q = a["price"].quantile(0.75) / a["m²"].quantile(0.75)
            first_q = a["price"].quantile(0.25) / a["m²"].quantile(0.25)
            print(f"\nOrtalama metrekare fiyatı {int(first_q)}TL - {int(last_q)}TL aralığında.")
        else: pass

        print(f"\nEn düşük fiyat: {a['price'].min()} \nEn yüksek fiyat: {a['price'].max()}\n")
        print(f"{city} ilinde toplam {len(a)} tane ilan var.\n\n----------------------------")
        """
    elif room == "" and neighborhood=="":
        a=d[d["district"]==district]
        return (f"\n{district} ilçesinde tahmini kira fiyatı: {int(pred)} TL\n")     
        """
        if len(a)>=5: 
            last_q = a["price"].quantile(0.75) / a["m²"].quantile(0.75)
            first_q = a["price"].quantile(0.25) / a["m²"].quantile(0.25)
            print(f"\nOrtalama metrekare fiyatı {int(first_q)}TL - {int(last_q)}TL aralığında.")
        else: pass

        print(f"\nEn düşük fiyat: {a['price'].min()} \nEn yüksek fiyat: {a['price'].max()}\n")
        print(f"{district} ilçesinde toplam {len(a)} tane ilan var.\n\n----------------------------")
        a=a.sort_values(by="price", ascending=True)
        print(f"\nGirilen bilgilere göre Emlakjet sitesindeki ilanlar 'Artan fiyata göre sıralı':\n\n{a.to_string(index=False)}")
        """
    elif room == "" and neighborhood!="":
        a=d[d["city"]==city]
        a=a[a["neighborhood"]==neighborhood]
        return (f"\n{neighborhood} mahallesinde tahmini kira fiyatı: {int(pred[0])} TL\n")     
        """
        if len(a)>=5: 
            last_q = a["price"].quantile(0.75) / a["m²"].quantile(0.75)
            first_q = a["price"].quantile(0.25) / a["m²"].quantile(0.25)
            print(f"\nOrtalama metrekare fiyatı {int(first_q)}TL - {int(last_q)}TL aralığında.")
        else: pass

        print(f"\nEn düşük fiyat: {a['price'].min()} \nEn yüksek fiyat: {a['price'].max()}\n")
        print(f"{neighborhood} mahallesinde toplam {len(a)} tane ilan var.\n\n----------------------------")
        a=a.sort_values(by="price", ascending=True)
        print(f"\nGirilen bilgilere göre Emlakjet sitesindeki ilanlar 'Artan fiyata göre sıralı':\n\n{a.to_string(index=False)}")
        """
    else:
        pass


  #################################################################

  #######################################################################


    return int(pred[0])

"""
city = ""
city = input("City: ")
district = ""
district = input("District: ")
neighborhood = ""
neighborhood = input("Neighborhood: ")
room = ""
room = input("Rooms: ")
metrekare = ""
metrekare = input("Meter: ")

"""
# Sent inputs to pred_price function
#print( pred_price(city,district,neighborhood,room,metrekare))
