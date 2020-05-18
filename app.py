import request
import gunicorn
from flask import Flask, request
import pandas as pd
import sqlite3

app = Flask(__name__)
#1. (statis) top tracks berdasarkan artis dengan nilai penjualan tertinggi
@app.route('/artistsales', methods=['GET'])
def artistsales():
    conn = sqlite3.connect('data/chinook.db')
    artistsales = pd.read_sql_query('''
            SELECT art.Name, art.ArtistId, SUM(inv.Total) as Total
            FROM artists as art
            LEFT JOIN albums as alb ON alb.ArtistId = art.ArtistId
            LEFT JOIN tracks as t ON t.AlbumId = alb.AlbumId
            LEFT JOIN invoice_items as invt ON invt.TrackId = t.TrackId
            LEFT JOIN invoices as inv ON inv.InvoiceId = invt.InvoiceId
            GROUP BY art.Name
            ORDER BY Total DESC
            ''', conn)
    return (artistsales.to_json())

#2.(statis) track dengan penjualan tertinggi tiap negara
@app.route('/countrysales', methods=['GET'])
def countrysales():
    conn = sqlite3.connect('data/chinook.db')
    countriessales = pd.read_sql_query('''
            SELECT inv.*, t.Name as TrackName, t.GenreId, cust.Country, SUM(inv.Total) as TotalSales
            FROM tracks as t
            LEFT JOIN invoice_items as invt ON invt.TrackId = t.TrackId
            LEFT JOIN invoices as inv ON inv.InvoiceId = invt.InvoiceId
            LEFT JOIN customers as cust On cust.CustomerId = inv.CustomerId
            GROUP BY cust.Country
            ORDER BY TotalSales DESC
            ''', conn, parse_dates = 'InvoiceDate')
    countriessales['Year'] = countriessales['InvoiceDate'].dt.year
    countrysales = countriessales[['GenreId','TrackName','BillingCity','Country','TotalSales','Year']]
    countrysales = countrysales[countrysales['Country'].notna()].set_index('Country')
    countrysales['Year'] = countrysales['Year'].astype('int64')
    return (countrysales.to_json())

#3.(dinamis) nilai transaksi tiap bulan di tiap negara(kota) | parameter : negara/kota
@app.route('/trans/get/<country>', methods=['GET'])
def periodsales(country):
    conn = sqlite3.connect('data/chinook.db')
    trans = pd.read_sql_query('''
            SELECT *
            FROM invoices as inv
            ''', conn, parse_dates='InvoiceDate')
    trans['Month'] = trans['InvoiceDate'].dt.month_name()
    trans['Year'] = trans['InvoiceDate'].dt.to_period('Y')
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    trans['Month'] = pd.Categorical(trans['Month'],
                               categories=months,
                               ordered=True)
    periodsales = pd.pivot_table(
        data= trans,
        index= ['BillingCountry','BillingCity'],
        columns= ['Month'],
        values = 'InvoiceId',
        aggfunc = 'sum'
    )
    periodsales.melt()
    periodsales.unstack().stack()
    periodsales = periodsales[['January','February','March','April','May','June','July',\
             'August','September','October','November','December']].fillna(0)
    return (periodsales.loc[country,:].to_json())

@app.route("/docs")
def documentation():
    return '''
        <h1> Documentation </h1>
        <h2> Static Endpoints </h2>
        <ol>
            <li>
                <p> /artistsales', methods=['GET'] </p>
                <p> Menampilkan data berupa tracks yang tersusun berdasarkan artis/penyanyi dengan total penjualan tertinggi di seluruh negara. </p>
                <p> Contoh : https://algo-capstonedeployapi-wkj.herokuapp.com/artistsales </p>
            </li>
            
            <li>
                <p> /countrysales', methods=['GET'] </p>
                <p> Menampilkan data berupa daftar negara dari angka penjualan tertinggi, serta top track di masing-masing negara tersebut. </p>
                <p> Contoh : https://algo-capstonedeployapi-wkj.herokuapp.com/countrysales </p>
            </li>
        </ol>
         
        <h2> Dynamic Endpoints </h2>
        <ol>
            <li>
                <p> /trans/get/&ltcountry&gt', methods=['GET'] </p>
                <p> Menampilkan total nilai penjualan bulanan di tiap kota pada masing-masing negara. User dapat mencari informasi penjualan berdasarkan kota dan negara yang terdaftar dalam database.</p>
                <p> Contoh : https://algo-capstonedeployapi-wkj.herokuapp.com/trans/get/USA </p>
            </li>
 
        </ol>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5000)