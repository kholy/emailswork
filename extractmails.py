import mailbox
import os


outputdir='C:/work/Mail/Takeout/Mail/out/'
mboxfile = 'C:/work/Mail/Takeout/Mail/software.mbox'
def uwritefile(*objects, sep=' ', end='\n', file):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


def getcharsets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    return charsets

def handleerror(errmsg, emailmsg,cs):
    print()
    print(errmsg)
    print("This error occurred while decoding with ",cs," charset.")
    print("These charsets were found in the one email.",getcharsets(emailmsg))
    print("This is the subject:",emailmsg['subject'])
    print("This is the sender:",emailmsg['From'])

def getbodyfromemail(msg):
    body = None
    #Walk through the parts of the email to find the text body.    
    if msg.is_multipart():    
        for part in msg.walk():

            # If part is multipart, walk through the subparts.            
            if part.is_multipart(): 

                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        # Get the subpart payload (i.e the message body)
                        body = subpart.get_payload(decode=True) 
                        #charset = subpart.get_charset()

            # Part isn't multipart so get the email body
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
                #charset = part.get_charset()

    # If this isn't a multi-part message then get the payload (i.e the message body)
    elif msg.get_content_type() == 'text/plain':
        body = msg.get_payload(decode=True) 

   # No checking done to match the charset with the correct part. 
    for charset in getcharsets(msg):
        print(charset)
        try:
            body = body.decode(charset)
        except UnicodeDecodeError:
            handleerror("UnicodeDecodeError: encountered.",msg,charset)
        except AttributeError:
             handleerror("AttributeError: encountered" ,msg,charset)
    return body    


def getcharsetfromemail(msg):
    return (getcharsets(msg))




# print(mboxfile)
# charsets=set()
# for thisemail in mailbox.mbox(mboxfile):
#     #print(++i)
#     for charset in getcharsetfromemail(thisemail):
#         charsets.add(charset)

#for charset in charsets:
#    print(charset)
def mygetbody(mail):
    body=""
#mail = email.message_from_string(email_body)
    for part in mail.walk():
        c_type = part.get_content_type()
        c_disp = part.get('Content-Disposition')

        if c_type == 'text/plain' and c_disp == None:
            body = body + '\n' + part.get_payload()
        else:
            continue
        return(body)

def mywrite(f,txt):
    if(isinstance(txt,str)):
        f.write(txt.encode('utf8'))
    if(isinstance(txt,bytes)):
        f.write(txt)


def extract_mails(mboxfile,outputdir):
    inbox=mailbox.mbox(mboxfile)
    ks=sorted(mailbox.mbox(mboxfile).keys())
    maxindex=(max(ks))
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    for i in ks:
        try:

            #print(i)
            #print(mygetbody(inbox[i]))
            file = open(outputdir+''+str(i), "wb")

            id=inbox[i]['Message-ID']
            if(not(id is None)):
                mywrite(file,'Message-ID :'+id+'\n')
                #file.write('Message-ID :'+id+'\n')


            d=inbox[i]['Date']
            if(not(d is None)):
                mywrite(file,'Date :'+d+'\n')
                #file.write('Date :'+d+'\n')

            if('To' in inbox[i].keys()):
                to=inbox[i]['To']
                if(not(to is None)):
                    mywrite(file,'To :'+to+'\n')
                    #file.write('To :'+to+'\n')



            if('Subject' in inbox[i].keys()):
                subject=inbox[i]['Subject']
                if(not(subject is None)):
                    mywrite(file,'Subject :'+subject+'\n')
                    #file.write('Subject :'+subject+'\n')

            body=mygetbody(inbox[i])
            if(not(body is None)):
                #file.write(body.encode(encoding='utf-8',errors='ignore'))
                mywrite(file,body.encode('utf8'))
                #file.write(body.encode('utf8'))
                #uwritefile(body,file=file)

            file.close()



        except Exception as e:
            print(e)
            #file.close()


extract_mails('C:/work/Mail/Takeout/Mail/red11.mbox','C:/work/Mail/Takeout/Mail/myout2/red11/')
extract_mails('C:/work/Mail/Takeout/Mail/semeval.mbox','C:/work/Mail/Takeout/Mail/myout2/semeval/')