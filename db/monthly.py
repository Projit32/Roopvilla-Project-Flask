from db.client import MongoDBClient
import math

class MonthlyFunctions:

    _members_collection=MongoDBClient.members_details
    _ms_collection=MongoDBClient.monthly_stats
    _ef_collection=MongoDBClient.emergency_funds
    _ledger_collection=MongoDBClient.ledger_data
    _electricity_collection=MongoDBClient.electricity_data

    def get_unique_months_of_years(self):
        years= MonthlyFunctions._ms_collection.find({}).distinct('YEAR')
        data=[]
        for year in years:
            months=MonthlyFunctions._ms_collection.find({"YEAR": year}).distinct('MONTH')
            data.append({
                "year": year,
                "months":months
            })
        return data
    
    def get_estimation_categories(self):
        return MonthlyFunctions._ledger_collection.find({}).distinct("ITEM_CATEGORY")
    
    def get_defaulter_status(self,month,year):
        results=MonthlyFunctions._ms_collection.find_one({"MONTH": month,"YEAR": year})
        data=[]
        for flat in results["MONTHLY_DIST"]['FLATWISE_DIST']:
            if not (flat["COMMENT"]=="UNSOLD" or flat["COMMENT"]=="NOT PAYING"):
                data.append({"flat":flat['FLAT_NUM'], "defaulter":True if flat["COMMENT"]=="DEFAULTER" else False})
        return data
    
    def get_payment_status(self,month,year):
        data=MonthlyFunctions._ms_collection.find_one({"MONTH": month,"YEAR": year})
        payment_status=[]
        for owner in data["MONTHLY_DIST"]['OWNERWISE_DIST']:
            for flat in owner['FLATS']:
                payment_status.append({"flat":flat,"payment":owner["PAYMENT_RECEIVED"]})
        return payment_status

    def update_payment_status(self, month,year,flats=[], status="NO"):
        if(flats):
            result=MonthlyFunctions._ms_collection.update_one(filter={"MONTH": month,"YEAR": year},
                                            update={"$set": {"MONTHLY_DIST.OWNERWISE_DIST.$[flat].PAYMENT_RECEIVED" :status}},
                                            array_filters=[{"flat.FLATS": {"$in": flats}}],upsert=False)
            print("PAYMENT UPDATE - Matched :",result.matched_count)
            print("PAYMENT UPDATE - Modified :",result.modified_count)
            
    def populate_unsold(self,month,year,flats=[]):
        for flat in flats:
            flat_data = {
                    "FLAT_NUM":flat,
                    "AMOUNT": 0,
                    "COMMENT":"UNSOLD"
                }
            result=MonthlyFunctions._ms_collection.update_one(filter={"MONTH": month,"YEAR": year},
                                                update={"$push": {"MONTHLY_DIST.FLATWISE_DIST" :flat_data}})
            print("UNSOLD- Flatwise Matched :",result.matched_count)
            print("UNSOLD- Flatwise Modified :",result.modified_count)
            
        
        """if flats:
            owner_data={
                    "OWNER": "OMKARA DEV",
                    "FLATS": flats,
                    "RATE": 0,
                    "TOT_RATE": 0,
                    "EMERGENCY_FUND": 0,
                    "TOTAL" : 0,
                    "PAYMENT_RECEIVED": "NA",
                    "COMMENTS":""
                }
            result=MonthlyFunctions._ms_collection.update_one(filter={"MONTH": month,"YEAR": year},
                                            update={"$push": {"MONTHLY_DIST.OWNERWISE_DIST" :owner_data}})
            print("UNSOLD- Ownerwise Matched :",result.matched_count)
            print("UNSOLD- Ownerwise Modified :",result.modified_count)"""

    def set_defaulter_status(self,month,year,apply,flats=[]):
        if(flats):
            result=MonthlyFunctions._ms_collection.update_one(filter={"MONTH": month,"YEAR": year},
                                    update={"$set": {"MONTHLY_DIST.FLATWISE_DIST.$[elem].COMMENT" :"DEFAULTER" if apply else ""}},
                                            array_filters=[{"elem.FLAT_NUM": {"$in":flats}}],upsert=False)
            print("Defaulter Matched :",result.matched_count)
            print("Defaulter Modified :",result.modified_count)

    def create_monthly_dist(self,month,year,est=[], flats=[]):
        #calculations
        total_amount =0
        for item in est:
            total_amount+= item["Price"]
        
        rate_amt=math.ceil(total_amount/len(flats))    
        
        #update flat wise distribution
        flat_dist =list()
        for flat in flats:
            ef_data = MonthlyFunctions._ef_collection.find_one({"FLT_NUM":flat})
            rate = rate_amt
            overall = rate + ef_data["RND_OFF_AMNT"]
            print(flat, rate, ef_data ,overall)
            flat_data = {
                "FLAT_NUM":flat,
                "AMOUNT": overall,
                "COMMENT":""
            }
            flat_dist.append(flat_data)
        
        
        
        #update owner wise dist
        member_dist =list()
        for owner in MonthlyFunctions._members_collection.find({}):
            ef_total =0
            paying_for=[]
            for flat in owner['FLT_NUMS']:
                if(flat in flats):
                    paying_for.append(flat)
                    ef_total += MonthlyFunctions._ef_collection.find_one({"FLT_NUM":flat})['RND_OFF_AMNT']
                    print(owner['OWNER_NAME'], rate_amt*owner['QNT'], ef_total ,(rate_amt*owner['QNT'])+ef_total)
            
            if(paying_for):
                owner_data={
                "OWNER": owner['OWNER_NAME'],
                "FLATS": paying_for,
                "RATE": rate_amt,
                "TOT_RATE": rate_amt*owner['QNT'],
                "EMERGENCY_FUND": ef_total,
                "TOTAL" : (rate_amt*owner['QNT'])+ef_total,
                "PAYMENT_RECEIVED": "NO",
                "COMMENTS":""
                }
                member_dist.append(owner_data)

        #created Monthly structure
        result = MonthlyFunctions._ms_collection.insert_one({
            "MONTH": month,
            "YEAR": year,
            "MONTHLY_EST": est,
            "MONTHLY_EXP": {},
            "MONTHLY_DIST":{
                "DIVIDING_MEMBERS": len(flats),
                "FLATWISE_DIST" : flat_dist,
                "OWNERWISE_DIST": member_dist
            },
        })
        print("New Inserted Acknowledged : ",result.acknowledged)

    def idiot_box(self,month,year,flats=[]):
        for flat in flats:
            flat_data = {
                    "FLAT_NUM":flat,
                    "AMOUNT": 0,
                    "COMMENT":"NOT PAYING"
                }
            result=MonthlyFunctions._ms_collection.update_one(filter={"MONTH": month,"YEAR": year},
                                                update={"$push": {"MONTHLY_DIST.FLATWISE_DIST" :flat_data}})
            print("Idiot Flatwise Matched :",result.matched_count)
            print("Idiot Flatwise Modified :",result.modified_count)
            
            """# name finding 
            name = MonthlyFunctions._members_collection.find_one({"FLT_NUMS":flat})["OWNER_NAME"]
            # make a dict to match names
            owner_data={
                    "OWNER": name,
                    "FLATS": [flat],
                    "RATE": 0,
                    "TOT_RATE": 0,
                    "EMERGENCY_FUND": 0,
                    "TOTAL" : 0,
                    "PAYMENT_RECEIVED": "NO",
                    "COMMENTS":""
                }
            result=MonthlyFunctions._ms_collection.update_one(filter={"MONTH": month,"YEAR": year},
                                            update={"$push": {"MONTHLY_DIST.OWNERWISE_DIST" :owner_data}})
            print("Idiot Ownerwise Matched :",result.matched_count)
            print("Idiot Ownerwise Modified :",result.modified_count)"""

    def delete_monthly_data(self, month, year):
        monthly_results = MonthlyFunctions._ms_collection.delete_one({"MONTH": month, "YEAR": year})
        print("Acknowledged:",monthly_results.acknowledged)

        ledger_results= MonthlyFunctions._ledger_collection.delete_many({"MONTH": month, "YEAR": year})
        print("Items Deleted:", ledger_results.deleted_count)

        electricity_results=MonthlyFunctions._electricity_collection.delete_one({"PAID_MON":month, "PAID_YR":year})
        print("Acknowledged:", electricity_results.acknowledged)
    
    def update_expenses(self,month,prev_month,year,prev_year,el_month,el_year,el_unit,el_amount,exp=[]):
        total_acc=sum([owner_data["TOTAL"] for owner_data in MonthlyFunctions._ms_collection.find_one({"MONTH": month, "YEAR": year})["MONTHLY_DIST"]["OWNERWISE_DIST"] if owner_data["PAYMENT_RECEIVED"]=="YES"])
        last_month_exp=list(MonthlyFunctions._ms_collection.find({"MONTH": prev_month, "YEAR": prev_year}))
        last_month_bal = last_month_exp[0]["MONTHLY_EXP"]["BALANCE"] if last_month_exp else 0
        
        print(total_acc, last_month_bal)
        
        # calculations
        ledger_list=list()
        ledger_list.append({
                "ITEM_NAME":"Monthly Maintenance",
                "ITEM_CATEGORY": "ACC",
                "MONTH": month,
                "YEAR": year,
                "CREDIT":total_acc,
                "DEBIT":0,
                "BALANCE": total_acc+last_month_bal})
            
        total_exp=0
        temp_acc=total_acc+last_month_bal
        exp.append({"NAME": "Electricity Bill","CATEGORY": "VAR","COST" :el_amount})
        for item in exp:
            ledger_data={
                "ITEM_NAME": item["NAME"],
                "ITEM_CATEGORY": item["CATEGORY"],
                "MONTH": month,
                "YEAR": year,
                "CREDIT":0,
                "DEBIT":item['COST'],
                "BALANCE": temp_acc-item["COST"]
            }
            temp_acc -=item["COST"]
            total_exp += item['COST']
            ledger_list.append(ledger_data)

        ledger_list.append({
                "ITEM_NAME":"Closing Balance for the month",
                "ITEM_CATEGORY": "BAL",
                "MONTH": month,
                "YEAR": year,
                "CREDIT":0,
                "DEBIT":0,
                "BALANCE": total_acc-total_exp+last_month_bal})
        
        result=MonthlyFunctions._ledger_collection.insert_many(ledger_list)
        print("Leger Insertion acknowledgement :",result.acknowledged)

        result=MonthlyFunctions._electricity_collection.insert_one({
            "BILLED_MON":el_month,
            "BILLED_YR": el_year,
            "PAID_MON":month,
            "PAID_YR":year,
            "AMOUNT":el_amount,
            "UNITS": el_unit
        })
        
        
        monthly_exp={
            "TOTAL_INCOME":total_acc,
            "TOTAL_EXPENSES": total_exp,
            "BALANCE": total_acc-total_exp+last_month_bal,
        }
        print(total_exp, total_acc-total_exp+last_month_bal)
        
        result =MonthlyFunctions._ms_collection.update_one({"MONTH": month, "YEAR":year},{
            "$set":{
                "MONTHLY_EXP":monthly_exp
            }
        })
