# Cloudsaves

### Downloading Cloudsaves

The UUID must be put as a URL path e.g
    https://{serveraddr}:{serverport}/api/cloudsaves/{uuid}

The API will return 200 status code as well as the encrypted data when found
The API will return 404 status code when it is not found

### Uploading Cloudsaves

The UUID must be put as a URL path e.g
    https://{serveraddr}:{serverport}/api/cloudsaves/{uuid}

And the data must be put in the header with the field name called **data**
and the content being the **encrypted data**

A 201 Status code will be sent back when it is done