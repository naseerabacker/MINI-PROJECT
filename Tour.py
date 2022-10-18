from flask import *

import datetime

from DBConnection import *
app = Flask(__name__)

app.secret_key="hifdgdfgdfgfdg"
db=Db()

@app.route('/')
def home():
    return render_template("intropage.html")


@app.route('/myhome')
def mhome():


  return render_template("myhome2.html")

@app.route('/home_post')
def home_post():


  return render_template("intropage.html")
#     return render_template()






@app.route('/login')
def login():
    return render_template("index.html")


@app.route('/login_post',methods=['post'])
def login_post():
    username=request.form['textfield']
    password=request.form['textfield2']
    d=Db()
    qry="select * from login where username='"+username+"' and password='"+password+"'"
    res=d.selectOne(qry)
    if res is not None:
        if res['usertype']=='admin':
            session['lid']=res['loginid']
            return redirect('/ahome')
        elif res['usertype']=='customer':
            session['lid'] = res['loginid']
            return redirect('/cushome')

@app.route('/admin_add_destination')
def admin_ad_destination():
    return render_template("admin/ADD_DESTINATION.html")
@app.route('/admin_add_destination_post',methods=['post'])
def admin_add_destination_post():
    Destination=request.form['jumpMenu']
    description=request.form['textarea']
    image=request.files['fileField']
    date=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    image.save(r"C:/Users/USER/Desktop/tourism management/static/photo/"+date+".jpg")
    path="/static/photo/"+date+".jpg"
    qry="INSERT INTO destination(Destination,Description,image)VALUES('"+Destination+"','"+description+"','"+path+"')"
    res=db.insert(qry)
    return redirect('/admin_view_destination')

@app.route('/cushome')
def cushome():
    return render_template("myhome2.html")


@app.route('/ahome')
def ahome():
    return  render_template('admin/adminindex.html')





@app.route('/admin_edit_destination/<did>')
def admin_edit_destination(did):
    d=Db()
    qry="select* from destination where Destination_id='"+did+"'"
    res=d.selectOne(qry)
    return render_template('admin/edit_destination.html',data=res)

@app.route('/admin_edit_destination_post',methods=['post'])
def admin_edit_destination_post():
    idr=request.form['did']
    Destination = request.form['jumpMenu']
    description = request.form['textarea']
    image = request.files['fileField']
    date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    if image:
        image.save(r"C:/Users/USER/Desktop/tourism management/static/photo/" + date + ".jpg")
        path = "/static/photo/" + date + ".jpg"
        qry = " UPDATE `destination` SET `Destination` = '" + Destination + "', `Image` = '" + path + "', `Description` = '" + description + "'WHERE Destination_id = '" + idr + "'"
        d = Db()
        res = d.update(qry)
        return redirect('/admin_view_destination')
    else:
        image.save(r"C:/Users/USER/Desktop/tourism management/static/photo/" + date + ".jpg")
        path = "/static/photo/" + date + ".jpg"
        qry = " UPDATE `destination` SET `Destination` = '" + Destination + "', `Description` = '" + description + "'WHERE Destination_id = '" + idr + "'"
        d = Db()
        res = d.update(qry)
        return redirect('/admin_view_destination')



@app.route('/admin_add_packages')
def admin_add_packages():
    qry = "SELECT* FROM destination"
    res = db.select(qry)
    print(res)
    return render_template("admin/ADD_PACKAGE.html",data=res)

@app.route('/admin_add_packages_post',methods=['post'])
def admin_add_packages_post():
    Destination=request.form['jumpMenu']
    Price = request.form['textfield2']
    Description=request.form['textarea']
    Date = request.form['textarea5']
    qry= "INSERT INTO packages(Destination_id,Price,Description,Date)VALUES('"+Destination+"', '"+Price+"', '"+Description+"','"+Date+"')"
    res=db.insert(qry)

    return "ok"

@app.route('/admin_edit_package/<pid>')
def admin_edit_package(pid):
    qry = "SELECT* FROM destination"
    res = db.select(qry)
    qry1="select * from packages where Package_id='"+pid+"'"
    res1=db.selectOne(qry1)
    return render_template("admin/edit_package.html",data=res,data1=res1)


@app.route('/admin_edit_package_post',methods=['post'])
def admin_edit_package_post():
    Destination=request.form['jumpMenu']
    Price = request.form['textfield2']
    Description=request.form['textarea']
    Date = request.form['textarea5']
    idr=request.form['id']
    d=Db()
    qry="UPDATE `packages` SET `Destination_id`='"+Destination+"',`Price`='"+Price+"',`Description`='"+Description+"' WHERE Package_id='"+idr+"'"
    res=d.update(qry)
    return redirect('/admin_view_package')


@app.route('/admin_send_reply/<cid>')
def admin_send_reply(cid):
    return render_template("admin/send_reply.html",cid=cid)
@app.route('/admin_send_reply_post',methods=['post'])
def admin_send_reply_post():
    Reply=request.form['textarea']
    cid=request.form['cid']

    qry="UPDATE `complaints` SET `Reply`='"+Reply+"',`Status`='Done'  WHERE `Complaint_id`='"+cid+"'"
    db.update(qry)
    return "ok"


@app.route('/admin_view_booking')
def admin_view_booking():

    #qry="select* from booking"

    qry = "SELECT `booking`.*,`registeration`.`Username`,`registeration`.`Phone_number`,`packages`.* FROM `booking` JOIN `registeration` ON `booking`.`User_id`=`registeration`.`User_id` JOIN `packages` ON `booking`.`Package_id`=`packages`.`Package_id`"
    db = Db()
    res = db.select(qry)
    return render_template("admin/view_booking.html",val=res)

@app.route('/admin_view_booking_post',methods=['post'])
def admin_view_booking_post():
    From= request.form['textfield']
    To= request.form['textfield2']

    return render_template("admin/view_booking.html")




@app.route('/admin_view_complaints')
def admin_view_complaints():
    db=Db()
    qry="SELECT *  FROM `complaints` INNER JOIN `registeration` ON `complaints`.`User_id`=`registeration`.`User_id"
    res=db.select(qry)
    return render_template("admin/view_complaints.html",data=res)
@app.route('/admin_view_complaints_post',methods=['post'])
def admin_view_complaints_post():

   Date_from=request.form['textfield']
   to= request.form['textfield2']
   db = Db()
   qry = "SELECT *  FROM `complaints` INNER JOIN `registeration` ON `complaints`.`User_id`=`registeration`.`Login_id` where Date between '"+Date_from+"' and '"+to+"'"
   res = db.select(qry)
   return render_template("admin/view_complaints.html", data=res)


@app.route('/admin_view_destination')
def admin_view_destination():
    db=Db()
    qry="SELECT* FROM destination"
    res=db.select(qry)
    return render_template("admin/view_destination.html",data=res)

@app.route('/admin_view_destination_post',methods=['post'])
def admin_view_destination_post():
   Name=request.form['textfield2']
   qry = "SELECT* FROM destination where Destination like '"+Name+"'"
   res = db.select(qry)
   return render_template("admin/view_destination.html",data=res)
@app.route('/admin_view_feedback')
def admin_view_feedback():
    db=Db()
    qry="SELECT *  FROM `feedback` INNER JOIN `registeration` ON `feedback`.`User_id`=`registeration`.`User_id`"
    res=db.select(qry)
    return render_template("admin/view_feedback.html",data=res)
@app.route('/admin_view_feedback_post',methods=['post'])
def admin_view_feedback_post():
    Date_from=request.form['textfield']
    To = request.form['textfield2']
    return "ok"


@app.route('/admin_view_package')
def admin_view_package():
    qry = "SELECT *  FROM `destination` INNER JOIN `packages` ON `destination`.`Destination_id`=`packages`.`Destination_id`"
    D=Db()
    res = db.select(qry)
    return render_template("admin/view_package.html",data=res)

@app.route('/admin_view_package_post',methods=['post'])
def admin_view_package_post():
    Destination_Name=request.form['textfield']
    qry = "SELECT *  FROM `destination` INNER JOIN `packages` ON `destination`.`Destination_id`=`packages`.`Destination_id` WHERE Destination LIKE '%"+Destination_Name+"%'"
    res = db.select(qry)
    return render_template("admin/view_package.html", data=res)


@app.route('/admin_delete_package/<pid>')
def admin_delete_package(pid):
    q="DELETE FROM packages WHERE `Package_id`='"+pid+"'"
    d=Db()
    d.delete(q)
    return "<script>alert('Package deleted succesfully');window.location='/admin_view_package';</script>"

@app.route('/admin_delete_destination/<pid>')
def admin_delete_destination(pid):
    q = "DELETE FROM destination WHERE `Destination_id`='" + pid + "'"
    d=Db()
    d.delete(q)
    return "<script>alert('Destination deleted succesfully');window.location='/admin_view_destination';</script>"

@app.route('/registeration')
def registeration():
    return render_template("register.html")


@app.route('/customer_add_registeration')
def customer_add_registeration():
    return render_template("/register.html")

@app.route('/customer_add_registeration_post',methods=['post'])
def customer_add_registeration_post():
    Username=request.form['textfield']
    Gender=request.form['radio']
    Place=request.form['textfield3']
    Post=request.form['textfield4']
    Pin = request.form['textfield2']
    City = request.form['textfield5']

    Email = request.form['textfield6']
    Phone_number = request.form['textfield7']
    Password = request.form['textfield8']

    qry="INSERT INTO login(`username`,`password`,`usertype`)  VALUES ('"+Email+"','"+Password+"','customer')"
    d=Db()
    lid=d.insert(qry)


    qry1="INSERT INTO registeration(`Username`,`Gender`,`Place`,`Post`,`Pin`,`City`,`Email`,`Phone_number`,`login_id`)VALUES('"+Username+"','"+Gender+"','"+Place+"','"+Post+"','"+Pin+"','"+City+"','"+Email+"','"+Phone_number+"','"+str(lid)+"')"
    db.insert(qry1)


    return redirect('/')





# EDIT PROFILE



@app.route('/customer_edit_profile')
def customer_edit_profile():
    db = Db()
    qry = "SELECT * FROM registeration where login_id='" + str(session["lid"]) + "'"

    res = db.selectOne(qry)
    return render_template("Customer/edit_profile.html", data=res, data1=res)


@app.route('/customer_edit_profile_post', methods=['post'])
def customer_edit_profile_post():
    lid = request.form['textfield']
    Username = request.form['textfield']
    Gender = request.form['Radio']
    Place = request.form['textfield3']
    Post = request.form['textfield4']
    Pin = request.form['textfield2']
    City = request.form['textfield5']

    Email = request.form['textfield7']
    Phone_number = request.form['textfield8']
    Password = request.form['textfield9']
    d = Db()

    qry = "UPDATE registeration SET Username='" + Username + "',Gender='" + Gender + "',Place='" + Place + "',Post='" + Place + "',Pin='" + Pin + "',City='" + City + "',Email='" + Email + "',Phone_number='" + Phone_number + "'"
    res = d.update(qry)
    return redirect('/admin_view_package')



# VIEW DESTINATION



@app.route('/customer_view_destination')
def customer_view_destination():
    db=Db()
    qry="SELECT* FROM destination"
    res=db.select(qry)
    return render_template("Customer/view_destination.html",data=res)

@app.route('/customer_view_package/<did>')
def customer_view_package(did):

    qry = "SELECT *  FROM `packages` JOIN `destination` ON `destination`.`Destination_id`=`packages`.`Destination_id` WHERE `packages`.`Destination_id`='"+did+"'"
    db=Db()
    res = db.select(qry)
    print(did)
    return render_template("Customer/view_package.html",data=res)

@app.route('/customer_view_package_post',methods=['post'])
def customer_view_package_post():
    Destination_Name=request.form['textfield']
    qry = "SELECT *  FROM `destination` INNER JOIN `packages` ON `destination`.`Destination_id`=`packages`.`Destination_id` WHERE Destination LIKE '%"+Destination_Name+"%'"
    res = db.select(qry)
    return render_template("Customer/view_package.html", data=res)

@app.route('/customer_book_package/<pid>')
def customer_book_package(pid):
    session["pid"]=pid
    return "ok"
    # return render_template("Customer/booking.html")

@app.route('/customer_book_package_post',methods=['post'])
def customer_book_package_post():
     # Date=request.form['textfield5']
     # # qry=" selcect * from package where Date='"+Date+"'"
     qry="INSERT INTO booking(`Date`,`User_id`,`Package_id`,`Status`) VALUES('"+str(session["Date"])+"','"+str(session["lid"])+"','"+str(session["pid"])+"','pendng')"
     db=Db()
     res=db.insert(qry)
     return "ok"


#customer
@app.route('/customer_view_booked_package')
def customer_view_booked_package():
    qry="SELECT `destination`. *, `packages`. *, `booking`. * FROM `booking` INNER JOIN `packages` ON`booking`. `Package_id` = `packages`.`Package_id` INNER JOIN `destination` ON `destination`. `Destination_id` = `packages`. `Destination_id` WHERE`User_id` = '"+str(session["lid"])+"'"
    db=Db()
    res=db.select(qry)

    return render_template("Customer/view_booked.html", data=res)



@app.route('/customer_send_complaint')
def customer_send_complaint():
    return render_template("Customer/send_complaint.html")



@app.route('/customer_send_complaint_post',methods=['post'])
def customer_send_complaint_post():
    complaint=request.form['textarea']



    qry="INSERT INTO`complaints`(`User_id`,`Date`,`Complaint`,`Reply`,`Status`) VALUES ('"+str(session["lid"])+"',curdate(),'"+complaint+"','pending','pending')"
    db.insert(qry)
    return redirect('/cushome')



@app.route('/customer_view_complaints')
def customer_view_complaints():
    db=Db()
    qry="SELECT * FROM complaints WHERE `User_id`='"+str(session["lid"])+"'"
    res=db.select(qry)
    return render_template("Customer/view_complaints.html",data=res)

@app.route('/customer_view_complaints_post',methods=['post'])
def customer_view_complaints_post():
   return "ok"



@app.route('/customer_send_feedback')
def customer_send_feedback():
    return render_template("Customer/send_feedback.html")



@app.route('/customer_send_feedback_post',methods=['post'])
def customer_send_feedback_post():
    feedback=request.form['textarea']



    qry="INSERT INTO `feedback`(`User_id`,`Feedback`,`Star`,`Date`)VALUES('"+str(session['lid'])+"','"+feedback+"','','curdate()')"
    db.insert(qry)
    return "Thank you for your feedback"



@app.route('/customer_view_feedback')
def customer_view_feedback():
    db=Db()
    qry="SELECT * FROM feedback WHERE `User_id`='"+str(session["lid"])+"'"
    res=db.select(qry)
    return render_template("Customer/view_feedback.html",data=res)

@app.route('/customer_view_feedback_post',methods=['post'])
def customer_view_feedback_post():
   return "ok"













    # qry = "UPDATE registeration SET Username='" + Username + "',Gender='" + Gender + "',Place='" + Place + "',Post='" + Place + "',Pin='" + Pin + "',City='" + City + "',Email='" + Email + "',Phone_number='" + Phone_number + "'"
    # res = d.update(qry)
    # return redirect('/admin_view_package')
    #


    # qry = "UPDATE login SET (`username`,`password`,`usertype`)  VALUES ('" + Email + "','" + Password + "','customer')"
 #    d = Db()
 #    db.UPDATE(qry )


# @app.route('/admin_edit_destination/<did>')
# def admin_edit_destination(did):
#     d=Db()
#     qry="select* from destination where Destination_id='"+did+"'"
#     res=d.selectOne(qry)
#     return render_template('admin/edit_destination.html',data=res)
#
# @app.route('/admin_edit_destination_post',methods=['post'])
# def admin_edit_destination_post():
#     idr=request.form['did']
#     Destination = request.form['jumpMenu']
#     description = request.form['textarea']
#     image = request.files['fileField']
#     date = datetime.datetime.now().strftime('%y&m&d-%H%M%S')
#     if image:
#         image.save(r"C:/Users/USER/Desktop/tourism management/static/photo/" + date + ".jpg")
#         path = "static/photo/" + date + ".jpg"
#         qry = " UPDATE `destination` SET `Destination` = '" + Destination + "', `Image` = '" + path + "', `Description` = '" + description + "'WHERE Destination_id = '" + idr + "'"
#         d = Db()
#         res = d.update(qry)
#         return redirect('/admin_view_destination')
#     else:
#         image.save(r"C:/Users/USER/Desktop/tourism management/static/photo/" + date + ".jpg")
#         path = "static/photo/" + date + ".jpg"
#         qry = " UPDATE `destination` SET `Destination` = '" + Destination + "', `Description` = '" + description + "'WHERE Destination_id = '" + idr + "'"
#         d = Db()
#         res = d.update(qry)
#         return redirect('/admin_view_destination')
#
#



@app.route('/guest_view_package')
def guest_view_package():
    qry = "SELECT *  FROM `destination` INNER JOIN `packages` ON `destination`.`Destination_id`=`packages`.`Destination_id`"
    D=Db()
    res = db.select(qry)
    return render_template("guest/view_packages.html",data=res)

@app.route('/guest_view_package_post',methods=['post'])
def guest_view_package_post():
    Destination_Name=request.form['textfield']
    qry = "SELECT *  FROM `destination` INNER JOIN `packages` ON `destination`.`Destination_id`=`packages`.`Destination_id` WHERE Destination LIKE '%"+Destination_Name+"%'"
    res = db.select(qry)
    return render_template("guest/view_packages.html", data=res)






@app.route('/customer_view_destination_post',methods=['post'])
def customer_view_destination_post():
   Search_your_destination=request.form['textfield2']
   qry = "SELECT* FROM destination where Destination like '"+ Search_your_destination+"'"
   res = db.select(qry)
   return render_template("Customer/view_destination.html",data=res)





app.run(debug=True,port=3000)


