import pandas as pd
import logging

class RecSysHeandler:

    def __init__ (self):
        """
        Класс RecSysHeandler иницаализирует файлы рекомендаций
        """
        self._stats = {
            "personal_count": 0,
            "top_popular_count": 0,
            "similar_count": 0,
        }
        self._recs = {
            "als_data": None, 
            "similar_item_data": None,
            "top_popular_data": None
            }
        
        self.load_rec_file(hendler='als_data',file_path='recommendations.parquet',index="user_id")
        self.load_rec_file(hendler='similar_item_data',file_path='similar.parquet',index="main_item_id")
        self.load_rec_file(hendler='top_popular_data',file_path='top_popular.parquet',index="item_id")
        
        self._recs['top_popular_data'] = self._recs['top_popular_data'].sort_values(by='popularity_weighted')[0:100].copy()

        logging.info(msg='Class ' + __name__ + ' init')
    
    def load_rec_file(self,hendler: str,file_path: str,index: str,**kwargs):
        self._recs[hendler] = self.load_df(file_path=file_path,**kwargs)
        self._recs[hendler] = self._recs[hendler].set_index(index)

    
    def load_df(self,file_path: str, **kwargs) -> pd.DataFrame:
        """
        Загрузчик данных из файла
        """
        try: 
            data = pd.read_parquet(path=file_path, **kwargs)
            logging.info(msg='Loaded seccessful from file: ' + file_path)
        except Exception as e:
            logging.error(msg=f"{file_path} {e}")

        return data
    
    def personal_rec(self,user_id: int, k: int = 100):
        """
        Персональные рекомендации для пользователя user_id
        возвращает К позиций
        """
        try:
            recs = self._recs['als_data'].loc[user_id]
            recs = recs["item_id"].to_list()[:k]
            self._stats["personal_count"] += 1 
            logging.info(f"personal")
        except KeyError:
            recs =  self.popular_rec(k)
        except Exception as e:
            logging.error("Error with recs for user " + user_id)
            recs = []

        return recs
    
    def items_rec(self,item_id: int, k: int = 100):
        """
        Возвращает K наиболее похожих треков для item_id
        """
        try:
            recs = self._recs['similar_item_data'].loc[item_id]
            recs = recs['item_id'].to_list()[:k]
            self._stats["similar_count"] += 1
            logging.info(f"item2item")
        except Exception as e:
            logging.error("Error with recs for item " + item_id)
            recs = []
            
        return recs
    
    def popular_rec(self,k: int = 100):
        """
        Возвращает K треков из подборки популярных
        """
        recs = self._recs['top_popular_data'].sample(k)
        recs = recs.index.to_list()

        self._stats["top_popular_count"] += 1
        logging.info(f"top_popular")

        return recs
    
    def stats(self):
        """
        Возвращает стстистику выданных рекомендаций
        """
        logging.info("Stats for recommendations")
        for name, value in self._stats.items():
            logging.info(f"{name:<30} {value} ")