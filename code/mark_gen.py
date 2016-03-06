import string
import random

class mark_gen(object):

    def __init__(self,chain_len = 2):
        self.word_dic = {}
        self.chain_len = chain_len

    def read_words(self,fname):

        with open(fname) as f:
            text = f.read().lower()
            text = self.unicodetoascii(text) #translate all weird characters that read did not encode properly
            text = text.translate(string.maketrans("",""), string.punctuation) #delete all punctuation
            text = text.replace("\n"," ") #replace newlines with spaces for easy splitting

            words = text.split()

            for iword in range(len(words)-self.chain_len-1):

                gram = ','.join(words[iword:iword+self.chain_len])

                if gram in self.word_dic:
                    self.word_dic[gram].append(words[iword+self.chain_len+1])
                else:
                    self.word_dic[gram] = [words[iword+self.chain_len+1]]

    def get_chain(self,nwords = 10):

        thresh = nwords
        for iTrials in range(1000):

            gram = random.choice(self.word_dic.keys())
            chain = gram.split(',')

            cnt_resets = 0
            for i in range(nwords):

                gram = ','.join(chain[-2:])

                if gram in self.word_dic:
                    chain.append(random.choice(self.word_dic[gram]))
                else:
                    chain.append(random.choice(self.word_dic.keys()).split(',')[0])
                    cnt_resets += 1

            if cnt_resets < thresh:
                thresh = cnt_resets
                best_chain = chain

        return ' '.join(best_chain),thresh










    def unicodetoascii(self,text):

        uni2ascii = {
                ord('\xe2\x80\x99'.decode('utf-8')): ord("'"),
                ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
                ord('\xe2\x80\x9d'.decode('utf-8')): ord('"'),
                ord('\xe2\x80\x9e'.decode('utf-8')): ord('"'),
                ord('\xe2\x80\x9f'.decode('utf-8')): ord('"'),
                ord('\xc3\xa9'.decode('utf-8')): ord('e'),
                ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
                ord('\xe2\x80\x93'.decode('utf-8')): ord('-'),
                ord('\xe2\x80\x92'.decode('utf-8')): ord('-'),
                ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
                ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
                ord('\xe2\x80\x98'.decode('utf-8')): ord("'"),
                ord('\xe2\x80\x9b'.decode('utf-8')): ord("'"),

                ord('\xe2\x80\x90'.decode('utf-8')): ord('-'),
                ord('\xe2\x80\x91'.decode('utf-8')): ord('-'),

                ord('\xe2\x80\xb2'.decode('utf-8')): ord("'"),
                ord('\xe2\x80\xb3'.decode('utf-8')): ord("'"),
                ord('\xe2\x80\xb4'.decode('utf-8')): ord("'"),
                ord('\xe2\x80\xb5'.decode('utf-8')): ord("'"),
                ord('\xe2\x80\xb6'.decode('utf-8')): ord("'"),
                ord('\xe2\x80\xb7'.decode('utf-8')): ord("'"),

                ord('\xe2\x81\xba'.decode('utf-8')): ord("+"),
                ord('\xe2\x81\xbb'.decode('utf-8')): ord("-"),
                ord('\xe2\x81\xbc'.decode('utf-8')): ord("="),
                ord('\xe2\x81\xbd'.decode('utf-8')): ord("("),
                ord('\xe2\x81\xbe'.decode('utf-8')): ord(")"),

                            }
        return text.decode('utf-8').translate(uni2ascii).encode('ascii')
