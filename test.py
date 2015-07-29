import gdata.photos.service
import gdata.media
import gdata.geo
from oauth2client.client import flow_from_clientsecrets

gd_client = gdata.photos.service.PhotosService()
gd_client.email = "focpibooth@gmail.com"
gd_client.password = "focraspberry"
gd_client.source = 'exampleCo-exampleApp-1'
gd_client.ProgrammaticLogin()
album = gd_client.InsertAlbum(title='New album', summary='This is an album')