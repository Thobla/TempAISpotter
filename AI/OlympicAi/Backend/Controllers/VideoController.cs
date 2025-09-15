namespace AI_spotter.Controllers;

using AI_spotter.Models;
using AI_spotter.Services;
using Microsoft.AspNetCore.Mvc;
using AI_spotter.PublicClasses;
using System.Net.Http;
using System.Text.Json;

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

    [HttpDelete("path/{path}")]
    public IActionResult DeletePath(string path){
        path = System.IO.Directory.GetParent(System.IO.Directory.GetCurrentDirectory()) + "/" + path;
        if (System.IO.File.Exists(path)){
            System.IO.File.Delete(path);
            return NoContent();
        }
        return StatusCode(500);
    }

    [HttpPost("upload")]
    public async Task<IActionResult> UploadAndVerdict(IFormFile video){
        // 1. Upload the video
        var upload = this.Create(video) as ObjectResult;
        // Ensure the upload was a success
        if (upload?.StatusCode != 201){
            return StatusCode(upload?.StatusCode ?? 500);
        }
        Video? videoReference = (Video?)upload.Value;
        if (videoReference == null){
            return StatusCode(500);
        }
        // 2. Retrieve verdict
        var verdict = await this.GetAI("", videoReference.Id) as ObjectResult;
        if (verdict?.StatusCode != 200){
            return StatusCode(verdict?.StatusCode ?? 500);
        }
        // 3. Delete video
        if (verdict?.Value != null){
            JsonDocument doc = JsonDocument.Parse((String) verdict.Value);
            JsonElement root = doc.RootElement;
            string path = root.GetProperty("path").GetString() ?? ""; // Access the "path" property
            // Delete processed video
            var delete = this.DeletePath(path) as NoContentResult;
            if (delete == null){
                return StatusCode(500);
            }
            // Delete original video
            delete = this.Delete(videoReference.Id) as NoContentResult;
            if (delete == null){
                return StatusCode(500);
            }
        }
        return verdict?.Value != null ? Ok(verdict.Value) : StatusCode(500);
    }
}
