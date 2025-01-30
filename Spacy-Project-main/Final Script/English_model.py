#!/usr/bin/env python
# coding: utf-8

# In[1]:



import spacy


nlp = spacy.load("en_core_web_lg")


def Assign_New_Word_Status(Word):
    CashOutCmpareset = ['pay', 'gave', 'receive', 'buy', 'purchase', 'lose', 'spend', 'clear', 'deposit', 'deduct']
    CashinCmpareset = ['receive', 'got', 'earn', 'sell', 'refund', 'borrow', 'recover', 'obtain', 'gain']

    SIMS = []

    token1 = nlp(Word)
    for text in CashOutCmpareset:
        token2 = nlp(text)
        sims = token1.similarity(token2)

        SIMS.append(sims)

    mx1 = sum(abs(number) for number in SIMS) / len(SIMS)


    SIMS1 = []

    for text in CashinCmpareset:
        token2 = nlp(text)
        sims = token1.similarity(token2)

        SIMS1.append(sims)

    mx2 = sum(abs(number) for number in SIMS1) / len(SIMS1)

    if (mx1 >= mx2):
        return "Cash-Out"
    else:
        return "Cash-In"

def English_Prediction(Statement):
    if(len(Statement)==0):
        Y="Please Input a valid statement"
        return Y
    else:
        CashoutMainSet={'purchase', 'transfer', 'book', 'spend', 'contribute', 'reimburse', 'pay', 'gain', 'give', 'lose', 'make', 'put', 'buy', 'acquire', 'invest', 'return', 'recharge', 'fund', 'clear', 'deposit', 'yield', 'reward', 'donate', 'deduct', 'order', 'remunerate', 'gave'}
        CashInMainSet={'Incoming', 'obtain', 'receive', 'gain', 'win', 'get', 'add', 'cancel', 'make', 'gather', 'have', 'acquire', 'got', 'incur', 'earn', 'sell', 'refund', 'borrow', 'collect', 'catch'}
        AllVerbs=[]
        Date=[]

        CombinedMoneyTerms=[]
        remark_final=[]
        statement=Statement

        statement=statement.lower()

        doc = nlp(statement)

        tas=[]

        for token in doc:

            if( token.pos_=="VERB" or token.pos_=="AUX"):
                tas.append(token.text)
            if(token.pos_=="PRON"):
                if(token.text=="me"):
                    tas.append(token.text)

        status = ""
        AllVerbs.append(tas)
        if(len(AllVerbs[0])==0):
            status="Verb Not found"


        rupeevariable=""
        statement=statement.lower()
        nlptokens=nlp(statement)
        date=[]
        removestr=""
        for y in nlptokens.ents:
            if(y.label_=='DATE'):
                date.append(y.text)
                removestr=y.text

        newitem=statement.replace(removestr,'')
        Date.append(date)
        money=[]
        newstatement=nlp(newitem)

        for i in range(0,len(newstatement)-1):
            if(newstatement[i].pos_=='NUM'):

                money.append(newstatement[i].text)
                if(newstatement[i+1].pos_!='NUM'):
                    money.append('Gap')
                if(newstatement[i+1].text=='rs' or newstatement[i+1].text=='rupees'):
                    rupeevariable='rupees'
                if((newstatement[i-1].text=='rs' or newstatement[i-1].text=='rupees' or newstatement[i-1].text=='.')):
                    rupeevariable='rupees'

        if(newstatement[-1].pos_=='NUM'):
            money.append(newstatement[-1].text)

        money.append(rupeevariable)
        Gapcount=0
        for items in money:
            if(items=='Gap'):
                Gapcount=Gapcount+1
        if(len(money)!=0 and money[-1]=='Gap'):
            Gapcount=Gapcount-1

        teststr=' '.join(money)

        combined=teststr.split('Gap')
        combined=''.join(combined)
        CombinedMoneyTerms.append(combined)

        nlptoken=nlp(newitem)
        remark_gibberish=[]
        for items in nlptoken:
            if(items.pos_!='NUM' and items.pos_!='ADJ' and items.pos_!='ADP' and items.text!='rupees'and items.text!='I' and items.text!='Rupees' and items.text!='Rs' and items.text!='rs' and items.text!='bucks' and items.text!='dollars'):
                remark_gibberish.append(items.text)
            if(items.text=='to' or items.text=='in' or items.text=='of' or items.text=='for' or items.text=='as' or items.text=='from'):
                remark_gibberish.append(items.text)

        if(remark_gibberish[-1]=='for' or remark_gibberish[-1]=='of' or remark_gibberish[-1]=='as' or remark_gibberish[-1]=='from' or remark_gibberish[-1]=='in'):
            remark_gibberish.pop()
        remar=' '.join(remark_gibberish)
        remark_final.append(remar)

        loopchecker=0

        if(status!="Verb Not found"):

            IsWordPresent=False
            item=AllVerbs[0]
            itemstr=''.join(item[0])
            doc5=nlp(itemstr)
            for item in doc5:
                word=item.lemma_
            if((word in CashoutMainSet) or (word in CashInMainSet)):
                IsWordPresent=True
                if word in CashoutMainSet:
                    status="Cash-Out"
                else:
                    status="Cash-In"
            if(IsWordPresent==False):
                loopchecker=1
                status= Assign_New_Word_Status(word)

            for z,item in enumerate(AllVerbs):
                for j in item:
                    if(j=='me'):
                        if(status=="Cash-Out"):
                            status="Cash-In"
                        else:
                            status="Cash-Out"


        Confidence_score_Status="No"
        if(loopchecker==0 and status!="Verb Not found"):
            Confidence_score_Status="Yes"

        Confidence_score_Money="No"
        if(Gapcount==0):
            Confidence_score_Money="Yes"

        Dict = {'Status':status,'Confidence On Status':Confidence_score_Status, 'Date':Date,'Money Involved is': CombinedMoneyTerms,'Confidence on Money':Confidence_score_Money, 'Remark': remark_final}

        return Dict






