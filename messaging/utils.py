from .models import Message, User
from django.shortcuts import get_object_or_404

## DEFINE THE SYSTEM ID FOR MESSAGING PURPOSES
def getSystemID():
    SYSTEM_ID = 42
    system_account = get_object_or_404(User,pk=SYSTEM_ID).id
    return system_account


def sendMessage(request,from_id,to_id,subject, message_body):
    
    from_user = User.objects.get(pk=from_id)
    to_user = User.objects.get(pk=to_id)
    message = Message()
    message.from_id = from_user
    message.to_id = to_user
    message.message_subject = str(subject)
    message.message_body = str(message_body)
    message.message_read = 0

    # Set deleted flag if it comes from the system account to remove it from systems mailbox
    if from_id == getSystemID():
        message.deleted_by =  User.objects.get(pk=getSystemID())
    message.save()

    return
    
def fileUploadMessage(request,uploaded_url):
    
    message = '''Dear {},

    You uploaded the file {}. The file is now ready for processing.\n\r\n\r
    To process the file, go to the sidebar and under the 'Files' sub-menu, click 'View File Details'. This will load all of your uploaded files that can be processed. If you have any further questions, please contact an administrator or raise a ticket from the 'Help' Menu.\n\r

    <pre>Please do not reply to this this message as it has been automatically generated.</pre>'''.format(request.user.first_name,uploaded_url[uploaded_url.rfind("/")+1:len(uploaded_url)] )

    return message


def fileProcessMessage(request,fileName):
    
    fileName = str(fileName)
    message = '''Dear {},

    The file {} has completed processing.\n\r\n\r
    The questions were successfully added to the subject specified. 

    <pre>Please do not reply to this this message as it has been automatically generated.</pre>'''.format(request.user.first_name,fileName[fileName.rfind("/")+1:len(fileName)])

    return message

def fileProcessError(request,fileName):
    
    fileName = str(fileName)
    message = '''Dear {},

    The processing for the file <strong>{}</strong> has failed.\n\r\n\r
    This is likely due to an invalid file format being uploaded, or corrupt data within the file.

    Valid file types are: 
    <ul><li>.csv</li><li>.txt</li><li>.xls</li><li>.xlsx</li><li>.xltx</li><li>.xltm</li></ul>

    If you have any questions, please contact a staff member or raise a ticket from the <a target='_blank' href='https://3.11.69.77/help/index.php?a=add'>Help Menu</a>.
    

    <pre>Please do not reply to this this message as it has been automatically generated.</pre>'''.format(request.user.first_name,fileName[fileName.rfind("/")+1:len(fileName)])

    return message


def fileDeleted(request,fileName):
    
    fileName = str(fileName)
    message = '''Dear {},

    The  file <strong>{}</strong> been deleted.\n\r\n\r
    Deleted files are removed from the database and filesystem and cannot be recovered.

    Any questions added from the file to the generator are still extant and have not been affected by this deletion

    If you have any questions, please contact a staff member or raise a ticket from the <a target='_blank' href='https://teachingperiodically.com/help/index.php?a=add&category=4&name={}'>Help Menu</a>.
    

    <pre>Please do not reply to this this message as it has been automatically generated.</pre>'''.format(request.user.first_name,fileName[fileName.rfind("/")+1:len(fileName)],request.user)

    return message