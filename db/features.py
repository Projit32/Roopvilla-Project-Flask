from db.client import MongoDBClient
from bson import ObjectId


class FeaturesFunctions:

    __features_collection=MongoDBClient.features

    def add_features(self, heading, description, image_link, date, focused_word=None, button_link=None)->None:
        feature_data={
            "HEADING":heading,
            "DESCRIPTION": description,
            "IMG_LINK":image_link,
            "DATE": date,
        }

        if focused_word is not None:
            feature_data['FOCUSED_WORD']=focused_word
        if button_link is not None:
            feature_data['BTN_LINK']=button_link
        
        result=self.__features_collection.insert_one(feature_data)
        print("Feature Inserted:", result.acknowledged,result.inserted_id)
    
    def replace_features(self, id, heading, description, image_link, date, focused_word=None, button_link=None)->None:
        feature_data={
            "HEADING":heading,
            "DESCRIPTION": description,
            "IMG_LINK":image_link,
            "DATE": date,
        }

        if focused_word is not None:
            feature_data['FOCUSED_WORD']=focused_word
        if button_link is not None:
            feature_data['BTN_LINK']=button_link
        
        result=self.__features_collection.replace_one({"_id":ObjectId(id)},feature_data)
        print("Feature Replced:", result.acknowledged)
        print("Features Matched", result.matched_count)
        print("Features Modified", result.modified_count)
    
    def get_features(self)->list:
        results=self.__features_collection.find({}).sort("DATE", -1)
        output=[]
        for item in results:
            feature={
                "id":str(item['_id']),
                "heading":item['HEADING'],
                "desc":item['DESCRIPTION'],
                "date":item['DATE'],
                "img":item['IMG_LINK'],
            }

            if 'FOCUSED_WORD' in item.keys():
                feature['focused']=item['FOCUSED_WORD']
            if 'BTN_LINK' in item.keys():
                feature['btn']=item['BTN_LINK']
            
            output.append(feature)
        
        return output
    
    def delete_feature(self, id):
        result=self.__features_collection.delete_one({"_id":ObjectId(id)})
        print("Feature Deleted: ",result.acknowledged)
        print("Feature delete count: ",result.deleted_count)
