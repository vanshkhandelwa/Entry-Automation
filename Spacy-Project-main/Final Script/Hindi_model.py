#!/usr/bin/env python
# coding: utf-8

# In[1]:



import stanza
import spacy_stanza
import regex

stanza.download("hi")
nlp = spacy_stanza.load_pipeline("hi")



CashoutMainSet={'पोषित', 'लौट', 'कटौती', 'खर्च', 'स्थानांतरित', 'बुक', 'जा', 'दे', 'प्रतिपूर्ति', 'अधिग्रहित', 'भुगतान', ' ', 'प्राप्त', 'दान', 'पुरस्कार', 'बना', 'डाल', 'आदेश', 'वापसी', 'खो', 'निवेश', 'रिचार्ज', 'बिल', 'वित्त', 'पारिश्रमिक', 'कर', 'किराया', 'योगदान', 'खरीद', 'साफ'}




CashInMainSet={'लौट', 'बेच', 'आ', 'उधार', 'बिकी', 'गॉट', 'इकट्ठी', 'रद्द', 'ब्याज', 'प्राप्त', 'जमा', 'बना', 'अर्जित', 'वापसी', 'कमाई', 'जोडी', 'वाला', 'जोड', 'बरामद', 'जीत', 'एकत्रित'}




def Hindi_Prediction(text):
    if (len(text) > 0):
        AllVerbs=[]
        CombinedMoneyTerms=[]
        Date=[]
        remark=[]
        statement=text

        doc = nlp(statement)
        tas=[]
        Statuschecker=0;

        for token in doc:


            if( token.pos_=="VERB" or token.pos_=="AUX"):
                tas.append(token.text)
             #  if(token.pos_=="PRON"):
            if(token.text=="मुझे" or token.text=='खिलाफ'):
                    tas.append(token.text)
            if(token.text in CashoutMainSet or token.text in CashInMainSet):
                Statuschecker=1;
                tas.append(token.text)

        AllVerbs.append(tas)


        money=[]
        newstatement=nlp(statement)


        for i in range(0,len(newstatement)-1):
            if(newstatement[i].pos_=='NUM'):

                money.append(newstatement[i].text)
                if(newstatement[i+1].pos_!='NUM'):
                    money.append('Gap')


        if(newstatement[-1].pos_=='NUM'):
            money.append(newstatement[-1].text)

        Gapcount=0;


        for items in money:
            if(items=='Gap'):
                Gapcount=Gapcount+1

        if(len(money)!=0 and money[-1]=='Gap'):
            Gapcount=Gapcount-1
        teststr=' '.join(money)


        doc=nlp(teststr)
        combined=teststr.split('Gap')
        combined=''.join(combined)
        CombinedMoneyTerms.append(combined)

        cnt=0
        removestr=""
        nlptokens=nlp(statement)
        datetokens=[]
        Monthlis=regex.findall("जनवरी|फरवरी|मार्च|अप्रैल|मई|जून|जुलाई|अगस्त|सितंबर|अक्टूबर|नवंबर|दिसंबर|सोमवार|मंगलवार|बुधवार|गुरुवार|शुक्रवार|शनिवार|रविवार|कल",statement)
        Monthchecker=0;
        if(len(Monthlis)!=0):
            Monthchecker=1
            for tokens in nlptokens:
                cnt=cnt+1
                if(tokens.text==Monthlis[0]):
                    Numbertokens=nlp(nlptokens[cnt-2].text)
                    if(Numbertokens[0].pos_=='NUM'):
                         # if(int(Numbertokens[0].text)>=1 and int(Numbertokens[0].text)<=31):

                        datetokens.append(Numbertokens[0].text)
                    Numbertokenafter=nlp(nlptokens[cnt].text)
                    datetokens.append(Monthlis[0])
                    if(Numbertokenafter[0].pos_=='NUM'):
                        datetokens.append(Numbertokenafter[0].text)
        remarkstatement=""
        removestr=' '.join(datetokens)
        newstatement=statement.replace(removestr,'')
        Date.append(datetokens)
        nlptoken=nlp(newstatement)
        remar=[]
        for items in nlptoken:
            if(items.pos_!='NUM' and items.pos_!='ADJ' and items.text!='रुपये' and items.text!='का'):
                remar.append(items.text)
                remarkstatement=remarkstatement+items.text
            if(items.text=='को ' and items.text=='ने' and items.text=='मुझे'):
                remar.append(items.text)

        remark.append(remar)




        # In[21]:
        Status="Verb Not found"
        Confidence_score = "No"
        if(len(AllVerbs[-1])>0):

            result=[]
            result=[0]*len(AllVerbs)


            # In[22]:


            for z,item in enumerate(AllVerbs):
                itemstr='  '.join(item)
                doc=nlp(itemstr)
                for item in doc:

                    word=item.lemma_
                    if(word in CashoutMainSet):
                        result[z]=1


            # In[23]:


            for z,item in enumerate(AllVerbs):
                itemstr='  '.join(item)
                doc=nlp(itemstr)
                for item in doc:
                    word=item.lemma_
                    if(word in CashInMainSet):
                        result[z]=0


            # In[24]:


            for z,item in enumerate(AllVerbs):
                itemstr='  '.join(item)
                doc=nlp(itemstr)
                for item in doc:
                    word=item.lemma_
                    if(word=='मैं' or word=='खिलाफ'):
                        if(result[z]==1):

                            result[z]=0
                        else:
                            result[z]=1


    # In[25]:


            if(result[-1]==1):
                Status="Cash-Out"
            else:
                Status="Cash-In"
            Confidence_score="No"
            if(Statuschecker==1):
                Confidence_score="YES"

        Confidence_score_Money="No"
        if(Gapcount==0 and len(money)!=0):
            Confidence_score_Money="YES"

        Confidence_score_Date="No"
        if(Monthchecker==1):
            Confidence_score_Date="YES"

        Dict={'Status': Status,'Confident_On_Status':Confidence_score,'Date': Date[-1],'Confident_On_Date': Confidence_score_Date,'Money Involved is': CombinedMoneyTerms[-1],'Confident_On_Money':Confidence_score_Money,'Remark':remark}
        print(Dict)
        return Dict





