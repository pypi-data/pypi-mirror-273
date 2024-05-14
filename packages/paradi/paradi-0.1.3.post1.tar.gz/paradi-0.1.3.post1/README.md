# Paradi
### Python Abstract Restful Api Dialoger Interface

This is an abstract class which purpose is to interface any Rest API using python's standard functionnalities. <br/>
It is meant to be very simple to allow a flexible implementation of the many ways to interact with any API, especially regarding the many different authentication methods. <br/>
You should also put in the child class any code that would parse the requests kwargs or read the output data format of the API and turn it into something more readable than a json (like a pandas dataframe). <br/>

# Example Implementation
The API is hosted at `https://exampleapiurl.com`. <br/>
To log in, you need to provide a username and a password in a **post** request at `https://exampleapiurl.com/login` which will return you a temporary connection token in the response. <br/>
To log out, you need to do a **get** request at `https://exampleapiurl.com/logout` with your credentials. <br/>
For any other request, to get your private data at `https://exampleapiurl.com/values` you need to provide your credentials in the header. <br/>

```py
class Dummy(Paradi):
    def __init__(self):
        super().__init__(entry=os.getenv('API_ENDPOINT')",
                         login_uri="login",
                         logout_uri="logout",
                         login_kwargs={"headers": {"Content-Type": r"application/x-www-form-urlencoded"},
                                       "data": {"username":os.getenv("API_USERNAME"),
                                                "password":os.getenv("API_PASSWORD")}})
        
        def _save_auth(self,
                       response: requests.Response
                       ):
            self.access_token = json.loads(response.text)['access_token']
            self.token_type = json.loads(response.text)['token_type']
            self.session.headers.update({'Authorization': f'{self.token_type} {self.access_token}'})

        def get_raw_data(self):
            response = self.get("values")
            return pd.json_normalize(json.loads(response.text), "data")
```

To use your newly made class you need to use the `with` syntax provided by python:

```py
with Dummy() as dummy:
    raw_data = dummy.get_raw_data()
```
This will ensure that the connection with your API is closed as soon as you are finished with the data recovery.

