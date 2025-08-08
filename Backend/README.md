# Using Backend
## Running on localhost:
1. Make sure you have all dependencies installed, mainly ASP.NET core.
2. While in TempAISpotter/Backend you may run "dotnet run". This should open the application on 
localhost:{port}, with port=5246.
3. To play with the api, go to "localhost:{port}/scalar". This should open up an easy-to-use GUI.

## Setup for VideosAPI:
There are 3 main scripts in 3 different folders making up the API we have so far. This is
**Controllers/VideoController.cs**, **Models/Video.cs**, and **Services/VideoService.cs**.

### Models/Video.cs
Video.cs contains the Video class. This acts as an interface for the potential future database
resource in the Video table. It currently contains an **id** as int, **path** as nullable
string, and **name** as nullable string.

### Services/VideoService.cs
the VideoService class works as a placeholder database. It has a list of videos as defined by the
Video class from Models/Video.cs, and methods to simulate the standard REST calls (Create, Get, Post,
Put, and Delete).

### Controllers/VideoController.cs
the VideoController is our API, at localhost:{port}/Video. We can Create, Get, Post, Put, and Delete. Using post 
we can indeed upload a video to Video/, but we can not currently change/remove it from the
folder, only the mock database at Services/VideoService.cs.

