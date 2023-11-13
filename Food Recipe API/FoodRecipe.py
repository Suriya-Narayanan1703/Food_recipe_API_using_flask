# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 09:50:47 2023

@author: SURIYA
"""

from flask import Flask,request, jsonify
import mysql.connector as mc
import random
app=Flask(__name__)


def db_connection():
    mydb=None
    try:
        mydb=mc.connect(
            host="localhost",
            user="root",
            password="candie",
            database="foodrecipe")
    except:
        print("database error")
    return mydb

food_list=[]

def gen():
    conn=db_connection()
    mycursor=conn.cursor()
    recipes_array = []
    for recipe_id in range(1, 10):
        recipe = {
            "id": recipe_id,
            "food_name": f"Delicious_{random.choice(['Pizza', 'Pasta', 'Salad', 'Burger', 'Soup'])}_{recipe_id}",
            "steps": 
                "Prepare the ingredients. Cook the dish on medium heat.Season with salt and pepper to taste. Serve meal!"
            }
        recipes_array.append(recipe)
        sql="""INSERT INTO food VALUES (%s,%s,%s)"""
        mycursor = mycursor.execute(sql,(recipe['id'],recipe['food_name'],recipe['steps']))
        conn.commit()
    return recipes_array

food_list=gen()



@app.route('/recipe',methods=['GET','POST'])
def index():
    conn=db_connection()
    mycursor=conn.cursor()
    
    if request.method=='GET':
        mycursor.execute("select * from food")
        food=[
            dict(rid=row['id'],food_name=row['food_name'],steps=row["food_steps"])
            for row in mycursor.fetchall()]
        #ml=mycursor.fetchall()
        #for x in ml:
         #   return x
            
        if len(food_list)>0:
            return jsonify(food_list)
        else:
            return "Nothing found",404
    if request.method=='POST':
        nw_id=request.form['fid']
        nw_foodname=request.form['food_name']
        nw_steps=request.form['food_steps']
        new_obj={
            'id':nw_id,
            'food_name':nw_foodname,
            'food_steps':nw_steps
            }
        food_list.append(new_obj)
        #return jsonify(food_list),201
        sql="""INSERT INTO food VALUES (%s,%s,%s)"""
        mycursor = mycursor.execute(sql,(nw_id,nw_foodname,nw_steps))
        conn.commit()
        return "food recipe added!"

if __name__=="__main__":
    app.run(debug=True)