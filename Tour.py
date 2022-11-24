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



@app.route('/contact')
def contact():
    return render_template("contact.html")






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
        else:
            return '''<script>alert('invalid username or password');window.location="/login"</script>'''
    else:
        return '''<script>alert('invalid username or password');window.location="/login"</script>'''

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

    return "<script>alert('Package added succesfully'); window.location='/admin_add_packages'</script>"

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

    d=Db()
    qry="UPDATE `complaints` SET `Reply`='"+Reply+"',`Status`='Done'  WHERE `Complaint_id`='"+cid+"'"
    print(qry)
    d.update(qry)
    return "ok"


@app.route('/admin_view_booking')
def admin_view_booking():

    #qry="select* from booking"

    qry = "SELECT `booking`.*,`registeration`.`Username`,`registeration`.`Phone_number`,`packages`.* FROM `booking` JOIN `registeration` ON `booking`.`User_id`=`registeration`.`login_id` JOIN `packages` ON `booking`.`Package_id`=`packages`.`Package_id` WHERE `booking`.Status='booked' order by  `booking`.`date` DESC"
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
    qry="SELECT *  FROM `complaints` INNER JOIN `registeration` ON `complaints`.`User_id`=`registeration`.`Login_id"
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
    qry="SELECT *  FROM `feedback` INNER JOIN `registeration` ON `feedback`.`User_id`=`registeration`.`login_id`"
    res=db.select(qry)
    print(res)
    return render_template("admin/view_feedback.html",data=res)


@app.route('/admin_view_feedback_post',methods=['post'])
def admin_view_feedback_post():
    Date_from=request.form['textfield']
    To = request.form['textfield2']
    return "ok"


@app.route('/admin_view_package')
def admin_view_package():
    qry = "SELECT *  FROM `destination` INNER JOIN `packages` ON `destination`.`Destination_id`=`packages`.`Destination_id`"
    db=Db()
    res =db.select(qry)
    return render_template("admin/view_package.html",data=res)

@app.route('/admin_view_package_post',methods=['post'])
def admin_view_package_post():
    db=Db()
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




@app.route('/admin_view_users')
def admin_view_users():
    db = Db()
    qry="SELECT * FROM `registeration`"
    res = db.select(qry)
    return render_template ("admin/view_users.html",val=res)



# @app.route('/admin_view_users_post', methods=['post'])
# def admin_view_users_post():
#     return redirect('/admin_view_users')







# EDIT PROFILE



@app.route('/customer_edit_profile')
def customer_edit_profile():
    db = Db()
    qry = "SELECT * FROM registeration where login_id='" + str(session["lid"]) + "'"

    res = db.selectOne(qry)
    return render_template("Customer/edit_profile.html", data=res, data1=res)



@app.route('/customer_view_profile')
def customer_view_profile():
    db = Db()
    qry = "SELECT * FROM registeration  where login_id='" + str(session["lid"]) + "'"

    res = db.select(qry)
    print(res)
    return render_template("Customer/view_profile.html", data=res)
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
    # Password = request.form['textfield9']
    d = Db()

    qry = "UPDATE registeration SET Username='" + Username + "',Gender='" + Gender + "',Place='" + Place + "',Post='" + Post + "',Pin='" + Pin + "',City='" + City + "',Email='" + Email + "',Phone_number='" + Phone_number + "'"
    res = d.update(qry)
    qry2="update login set username='"+Email+"' where loginid='"+str(session['lid'])+"'"
    res2=db.update(qry2)
    return redirect('/admin_view_package')



@app.route('/customer_view_destination')
def customer_view_destination():
    db=Db()
    qry="SELECT* FROM destination"
    res=db.select(qry)
    return render_template("Customer/view_destination.html",data=res)


@app.route('/customer_view_package/<did>')
def customer_view_package(did):
    db=Db()
    qry="SELECT `packages`.* ,`destination`.`Destination_id`,`destination`.`image` FROM `packages` INNER JOIN `destination` ON `destination`.`Destination_id`=`packages`.`Destination_id` WHERE `packages`.`Destination_id`='"+str(did)+"' AND `packages`.Date > CURDATE()"
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
    db=Db()
    qry="INSERT INTO booking (`date`,`User_id`,`Package_id`,`Status`) VALUES(curdate(),'"+str(session['lid'])+"','"+str(pid)+"','booked')"
    res=db.insert(qry)
    return "Your booking success"

@app.route('/customer_book_package_post',methods=['post'])
def customer_book_package_post():
     # Date=request.form['textfield5']
     # # qry=" selcect * from package where Date='"+Date+"'"
     qry="INSERT INTO booking(`date`,`User_id`,`Package_id`,`Status`) VALUES('"+str(session["Date"])+"','"+str(session["lid"])+"','"+str(session["pid"])+"','pending')"
     db=Db()
     res=db.insert(qry)
     return "ok"


#customer
@app.route('/customer_view_booked_package')
def customer_view_booked_package():
    qry="SELECT `destination`. *, `packages`. *, `booking`. * FROM `booking` INNER JOIN `packages` ON`booking`. `Package_id` = `packages`.`Package_id` INNER JOIN `destination` ON `destination`. `Destination_id` = `packages`. `Destination_id` WHERE`User_id` = '"+str(session["lid"])+"'and Status='approved' or Status='booked' order by  `booking`.`date` DESC"
    db=Db()
    res=db.select(qry)
    return render_template("Customer/view_booked.html", data=res)




#approve booking
@app.route('/customer_accept_booking/<cid>')
def customer_accept_booking(cid):
 qry="update booking set status='approved' where Booking_id='"+cid+"'"
 db=Db()
 res=db.update(qry)
 return "approved"



#cancel booking
@app.route('/customer_cancel_booking/<cid>')
def customer_cancel_booking(cid):
 qry="update booking set status='cancelled' where Booking_id='"+cid+"'"
 db=Db()
 res=db.update(qry)
 return redirect('/cushome')



#view cancelled
@app.route('/admin_view_cancelled_booking')
def admin_view_cancelled_booking():


    qry = "  SELECT `booking`.*,`registeration`.`login_id`,`registeration`.`Username`,`registeration`.`Phone_number`,`packages`.* FROM `booking` JOIN `registeration` ON `booking`.`User_id`=`registeration`.`login_id` JOIN `packages` ON `booking`.`Package_id`=`packages`.`Package_id` WHERE `booking`.Status='cancelled'  order by  `booking`.`date` DESC"
    db = Db()
    res = db.select(qry)
    return render_template("admin/cancelled_booking.html",val=res)



#approve booking
@app.route('/approved_booking')
def approved_booking():

    qry = "  SELECT `booking`.*,`registeration`.`Username`,`registeration`.`Phone_number`,`packages`.* FROM `booking` JOIN `registeration` ON `booking`.`User_id`=`registeration`.`login_id` JOIN `packages` ON `booking`.`Package_id`=`packages`.`Package_id` WHERE `booking`.Status='approved'"
    db = Db()
    res = db.select(qry)
    return render_template("admin/approved_booking.html",val=res)





#view cancelled
@app.route('/customer_view_cancelled_booking')
def customer_view_cancelled_booking():

    #qry="select* from booking"

    qry = "  SELECT `booking`.*,`registeration`.`Username`,`registeration`.`Phone_number`,`packages`.* FROM `booking` JOIN `registeration` ON `booking`.`User_id`=`registeration`.`login_id` JOIN `packages` ON `booking`.`Package_id`=`packages`.`Package_id` WHERE `booking`.Status='cancelled'"
    db = Db()
    res = db.select(qry)
    return render_template("admin/cancelled_booking.html",val=res)














@app.route('/customer_pay_amount/<cid>')
def customer_pay_amount(cid):
    session['bid']=cid
    qry="SELECT * FROM booking INNER JOIN packages ON packages.Package_id= Booking.Package_id WHERE Booking_id = '"+cid+"'"
    db=Db()
    res=db.selectOne(qry)
    session['amt']=res['Price']
    return render_template("Customer/payment.html",data=res)

@app.route('/customer_pay_amount_post',methods=['post'])
def customer_pay_amount_post():
    photo=request.files['file']
    from datetime import datetime
    dt=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
    photo.save("C:\\Users\\USER\\Desktop\\tourism management\\static\\payment\\"+dt)
    path="/static/payment/"+dt
    qry="INSERT INTO `users payment`(`date`,`booking id`,`amount`,`reciept`,`status`) VALUES(CURDATE(),'"+str(session['bid'])+"','"+str(session['amt'])+"','"+path+"','paid')"
    db=Db()
    db.insert(qry)
    qry="UPDATE `booking` SET `Status`='paid' WHERE `Booking_id`='"+str(session['bid'])+"'"
    db=Db()
    db.update(qry)
    return '''<script>alert('Completed');window.location='/view_paid'</script>'''
    return redirect('/cushome')



@app.route('/view_paid')
def view_paid():
    qry="SELECT `destination`. *, `packages`. *,`userspayment`. *, `booking`. * FROM `booking` INNER JOIN `packages` ON`booking`. `Package_id` = `packages`.`Package_id` INNER JOIN `destination` ON `destination`. `Destination_id` = `packages`. `Destination_id`INNER JOIN `userspayment` ON `booking`. `Booking_id` = `userspayment`. `Booking_id` WHERE`User_id` = '"+str(session["lid"])+"' order by  `booking`.`date` DESC"

    # qry="select * from userspayment WHERE`User_id` = '"+str(session["lid"])+"'and Status='paid'"
    # qry="SELECT `destination`. *, `packages`. *, `booking`. * FROM `booking` INNER JOIN `packages` ON`booking`. `Package_id` = `packages`.`Package_id` INNER JOIN `destination` ON `destination`. `Destination_id` = `packages`. `Destination_id` WHERE`User_id` = '"+str(session["lid"])+"'and Status='paid'"
    db=Db()
    res=db.select(qry)
    print(res,)
    return render_template("Customer/view_paid.html",data=res)


@app.route('/admin_view_paid')
def admin_view_paid():
    qry="SELECT `destination`. *, `packages`. *,`userspayment`. *, `booking`. * FROM `booking` INNER JOIN `packages` ON`booking`. `Package_id` = `packages`.`Package_id` INNER JOIN `destination` ON `destination`. `Destination_id` = `packages`. `Destination_id`INNER JOIN `userspayment` ON `booking`. `Booking_id` = `userspayment`. `Booking_id` order by  `booking`.`date` DESC"
    db=Db()
    res=db.select(qry)
    print(res,"============================================")
    return render_template("admin/view_paid.html",data=res)






@app.route('/customer_send_complaint')
def customer_send_complaint():
    return render_template("Customer/send_complaint.html")



@app.route('/customer_send_complaint_post',methods=['post'])
def customer_send_complaint_post():
    complaint=request.form['textarea']

    qry="INSERT INTO`complaints`(`User_id`,`Date`,`Complaint`,`Reply`,`Status`) VALUES ('"+str(session["lid"])+"',curdate(),'"+complaint+"','pending','pending')"
    db.insert(qry)
    return redirect('/cushome')

@app.route('/customer_delete_complaint/<cid>')
def customer_delete_complaint(cid):
    q="DELETE FROM complaints WHERE `User_id`='"+str(session["lid"])+"'"
    d=Db()
    d.delete(q)
    return "<script>alert('Complaint deleted succesfully');window.location='/customer_view_complaints';</script>"
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



    qry="INSERT INTO `feedback`(`User_id`,`Feedback`,`Star`,`Date`)VALUES('"+str(session['lid'])+"','"+feedback+"','',curdate())"
    db.insert(qry)
    return '''<script>alert('Thank you for your feedback');window.location='/cushome'</script>'''


@app.route('/customer_view_feedback')
def customer_view_feedback():
    db=Db()
    # qry="SELECT * FROM feedback WHERE `User_id`='"+str(session["lid"])+"'"
    qry= "SELECT `feedback`.*,registeration.Username FROM `feedback` INNER JOIN `registeration` ON `feedback`.`User_id`=`registeration`.`Login_id`"

    res=db.select(qry)
    return render_template("Customer/view_feedback.html",data=res)

@app.route('/customer_view_feedback_post',methods=['post'])
def customer_view_feedback_post():
   return "ok"












@app.route('/guest_view_package')
def guest_view_package():
    qry="select * from `destination` "
    # qry = "SELECT *  FROM `destination` INNER JOIN `packages` ON `destination`.`Destination_id`=`packages`.`Destination_id`"
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




#########



@app.route('/admin_send_notification/<logid>')
def admin_send_noti(logid):
    print(logid)
    session['loginid'] =logid

    return render_template("admin/send_notification.html")


@app.route('/admin_send_notification_post',methods=['post'])
def admin_send_notification_post():
    llid=session['loginid']
    print(llid)
    notification=request.form['textarea']
    lid=request.form['lid']
    # qry="UPDATE `notification` SET `notification`='"+notification+"',`status`='Done'"
    qry="INSERT INTO`notification`(`user_id`,`Date`,`notification`,`status`) VALUES ('"+llid+"',curdate(),'"+notification+"','pending')"
    db.insert(qry)
    return render_template("admin/send_notification.html")




@app.route('/customer_view_notification')
def customer_view_notification():
    db=Db()
    # print(str(session["lid"]))
    # qry="SELECT * FROM notification WHERE `user_id`='"+str(session["lid"])+"'"
    # qry="SELECT * FROM notification "
    qry="SELECT *  FROM `notification` INNER JOIN `registeration` ON `notification`.`user_id`=`registeration`.`Login_id` order by  `notification`.`date` DESC"

    res=db.select(qry)
    return render_template("Customer/view_notification.html",data=res)

@app.route('/customer_view_notification_post',methods=['post'])
def customer_view_notification_post():
   return "ok"


#
# #
# @app.route('/admin_monthlyreport')
# def admin_monthlyreport():
#     if session['lid']=="":
#         return '''<script>alert('please login');window.location="/"</script>'''
#     else:
#         db=Db()
#         qry="SELECT`users payment`.*,`users payment`.`amount` AS pamount,`booking`.*,`registeration`.* FROM `users payment` JOIN`booking` ON `booking`.`Booking_id`=`users payment`.`booking id` JOIN`registeration` ON`registeration`.`login_id`=`booking`.`User_id`"
#         res=db.select(qry)
#         total=0.0
#         for i in res:
#             total+=float(i['pamount'])
#             print(total)
#     return render_template('admin/view_report.html', data=res, total=total)
#
#
#  @app.route('/admin_monthlyreport_post',methods=['post'])
#
#     def admin_monthlyreport_post():
#         if session['lid'] == "":
#             return '''<script>alert('please login');window.location="/"</script>'''
#
#
#
#
# @app.route('/admin_monthlyreport2')
# def admin_monthlyreport2():
#     if session['lid']=="":
#         return '''<script>alert('please login again to continue');window.location="/"</script>'''
#     else:
#         db=Db()
#         qry="SELECT`users payment`.*,`users payment`.`amount` AS pamount,`booking`.*,`registeration`.* FROM `users payment` JOIN`booking` ON `booking`.`Booking_id`=`users payment`.`booking id` JOIN`registeration` ON`registeration`.`login_id`=`booking`.`User_id`"
#         res=db.select(qry)
#         total=0.0
#         for i in res:
#             total+=float(i['pamount'])
#             print(total)
#     return render_template('admin/view_report.html', data=res, total=total)



























app.run(debug=True,port=3000)








