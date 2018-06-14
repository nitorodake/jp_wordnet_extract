import sqlite3
from collections import namedtuple

"""
============== WordNet db 登録情報 ===============

 +-----------------Table 一覧-------------------+
 | ancestor | link_def | pos_def    | sense     |
 |----------------------------------------------|
 | synlink  | synset   | synset_def | synset_ex |
 |----------------------------------------------|
 | variant  | word     | xlink      |           |
 +----------------------------------------------+

Table <word>
  wordid : 語彙のID
  lang   : 語彙の言語　jpn=日本語, eng=英語
  lemma  : 見出し語
  pron   : ? ほぼNone
  pos    : 品詞


Table <sense>
  synset  : シンセットID
  word id : 語義ID
  lang    : 言語
  others  : None

=================================
"""

class WordNet():
    def __init__(self):
        self.connection = DBConnector()
        
        self.word2id = {}
        self.id2word = {}
        
        self.wordid2synset = {}
        self.synset = {}
        
        self._get_word2id()
        self._get_wordid2synset()

    def __call__(self):
        pass

    def _get_wordid2synset(self):
        query = "select * from sense"
        result = self.connection(query)

        sense_info_conv = namedtuple('Sense', 'synset wordid lang rank lexid freq src')

        for row in result:            
            s_info = sense_info_conv(*row)

            if s_info.lang != 'jpn':
                continue

            if s_info.wordid in self.wordid2synset:             
                self.wordid2synset[s_info.wordid].append(s_info.synset)
                
            else:
                self.wordid2synset[s_info.wordid] = []
                self.wordid2synset[s_info.wordid].append(s_info.synset)

        for word, synset_list in self.wordid2synset.items():
            for synset in synset_list:
                if synset in self.synset:
                    self.synset[synset].append(word)

                else:
                    self.synset[synset] = []
                    self.synset[synset].append(word)


        for word_ids in self.synset.values():
            print('=================')
            for w_id in word_ids:
                print(self.id2word[w_id])

                
                
                
    
    def _get_word2id(self):
        query = "select * from word"
        result = self.connection(query)

        word_info_conv = namedtuple('Word', 'wordid lang lemma pron pos')
        
        for row in result:            
            w_info = word_info_conv(*row)

            if w_info.lang != 'jpn':
                continue
            
            if w_info.lemma in self.word2id:
                self.word2id[w_info.lemma].append(w_info.wordid)
            else:
                self.word2id[w_info.lemma] = []
                self.word2id[w_info.lemma].append(w_info.wordid)

        for w, ids in self.word2id.items():
            for w_id in ids:
                self.id2word[w_id] = w        

class DBConnector():
    def __init__(self):
        self.db_path = "./dict/wnjpn.db"
        
    def __call__(self, query):
        connect = sqlite3.connect(self.db_path)
        cur     = connect.execute(query)
        result  = [row for row in cur]
        connect.close()

        return result

            
    
def main():
     wordnet = WordNet()


if __name__ == '__main__':
    main()
