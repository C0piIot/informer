from informer_trendier import TrendierInboxEntryStorage
from uuid import uuid4
from datetime import datetime

print("hola")

class Stdclass:
	pass



'''
class InboxEntry(models.Model):
    key = models.UUIDField(_('key'), default=uuid4, primary_key=True, editable=False)
    site = models.ForeignKey(Site, verbose_name=_('site'), on_delete=models.CASCADE, related_name='+', editable=False)
    environment = models.ForeignKey('accounts.Environment', on_delete=models.CASCADE, verbose_name=_('environment'), related_name='+', editable=False)
    contact = models.ForeignKey('contacts.Contact', verbose_name=_('contact'), on_delete=models.CASCADE, related_name='+', editable=False)
    date = models.DateTimeField(_('date'), auto_now_add=True)
    title = models.CharField(_('title'), max_length=100)
    message = models.TextField(_('message'))
    url = models.URLField(_('url'), blank=True, default='')
    read = models.DateTimeField(_('read'), blank=True, null=True)
    entry_data
'''

thing = Stdclass()
thing.pk = 1
thing.key = 1

print(thing.__dict__)

entry = Stdclass()
entry.key = uuid4()
entry.site = thing
entry.environment = thing
entry.contact = thing
entry.date = datetime.now()
entry.title = 'hola'
entry.message = 'prueba texto'
entry.image = 'http://lalala'
entry.read = datetime.now()
entry.url = 'http://xxxx'
print(entry.__dict__)
TrendierInboxEntryStorage.save_entry(thing, entry)


