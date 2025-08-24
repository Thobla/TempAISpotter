namespace AI_spotter.Controllers;

using AI_spotter.Models;
using AI_spotter.Services;
using Microsoft.AspNetCore.Mvc;
using AI_spotter.PublicClasses;
using System.Net.Http;

public interface IAiClientConnect{
    HttpClient AiClient {get;}
    Task<HttpResponseMessage> Connect(string path);
}

public class AiClientConnect : IAiClientConnect{
    public HttpClient AiClient {get;}
    public AiClientConnect(HttpClient client){
        AiClient = client;
    }
//    public static async Task<VideoController> Create(){
//        var controller = new VideoController();
//        await controller.ConnectAiClient();
//        return controller;
//    }
    public async Task<HttpResponseMessage> Connect(string path){
        try{
            using HttpResponseMessage response = await AiClient.GetAsync($"http://localhost:8000/verdict?path={path}");
            response.EnsureSuccessStatusCode();
            string responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseBody);
            return response;
        }
        catch (HttpRequestException e){
            Console.WriteLine("\nException caught");
            Console.WriteLine("Exception message: {0}", e.Message);
            return new HttpResponseMessage(System.Net.HttpStatusCode.NoContent);
        }
    }
}

[ApiController]
[Route("[controller]")]
public class VideoController : ControllerBase{
    private readonly IAiClientConnect AiClient;
    UploadHandler handleHerVideo = new UploadHandler();

    public VideoController(IAiClientConnect aiClient){
        AiClient = aiClient;
    }


    [HttpGet]
    public ActionResult<List<Video>> GetAll() => VideoService.GetAll();


    [HttpGet("{id}")]
    public ActionResult<Video> Get(int id){
        var video = VideoService.Get(id);
        if (video == null){
            return NotFound();
        }
        return video;
    }

    [HttpGet("aiApi/{aiMethod}/{id}")]
    public async Task<IActionResult> GetAI(string aiMethod, int id){
        try{
            var path = VideoService.Get(id)?.Path;
            if (path == null){
                throw new NullReferenceException("id or path is null");
            }
            //HttpResponseMessage result = await AiClient.Connect(path);
            HttpResponseMessage result = await AiClient.AiClient.GetAsync($"http://localhost:8000/verdict?path={path}");
            if (result.IsSuccessStatusCode){
                Console.WriteLine("got results");
                return Ok(result.Content.ReadAsStringAsync().Result);
            }
            else{
                return StatusCode((int) result.StatusCode, result.ReasonPhrase);
            }
        }
        catch (HttpRequestException e){
            return (StatusCode(500, ("Internal Server Error {0}", e)));
        }
    }



    [HttpPost]
    public IActionResult Create(IFormFile video){
        (bool IsSuccess, string response) videoResponse = handleHerVideo.Upload(video);
        if (!videoResponse.IsSuccess){
            return BadRequest(videoResponse.response);
        }
        Video returnedVideo = new Video(){Id = -1, Name = videoResponse.response, 
                Path = Path.Combine(Path.Combine(Directory.GetCurrentDirectory(), "Videos"), videoResponse.response)};
        VideoService.Add(returnedVideo);
        return CreatedAtAction(nameof(Get), new { id = returnedVideo.Id }, returnedVideo);
    }

    [HttpPut("{id}")]
    public IActionResult Update(IFormFile newVideo, int id){
        Video? video = VideoService.Get(id);
        if (video == null){
            return NotFound();
        }
        (bool IsSuccess, string response) result = handleHerVideo.Upload(newVideo, video.Name);
        if (!result.IsSuccess){
            return BadRequest(result.response);
        }
        return CreatedAtAction(nameof(Get), new {id = id}, video);
    }
    
    [HttpDelete("{id}")]
    public IActionResult Delete(int id){
        Video? video = VideoService.Get(id);
        if (video is null){
            return NotFound();
        }
        if (System.IO.File.Exists(video.Path)){
            System.IO.File.Delete(video.Path);
            VideoService.Delete(id);
            return NoContent();
        }
        return StatusCode(500);
    }
}
